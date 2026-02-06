# 植物-疾病关联数据导入实施总结

## 📋 实施概述

根据用户需求和数据分析，我们选择使用**现有的 `bio_resource_disease_associations` 关联表**来存储植物-疾病关联数据，而不是将字段补充到 diseases 表中。

## ✅ 已完成的工作

### 1. 数据导入脚本

**文件**: `scripts/database/import_bio_resource_disease_associations.py`

**功能**:
- 读取 CMAUP v2.0 植物-疾病关联数据（765,267条记录）
- 映射 Plant_ID → bio_resource_id
- 映射 ICD-11 Code → disease_id
- 处理4种证据类型字段
- 计算置信度评分（0-1）
- 批量插入数据（BATCH_SIZE=1000）
- 处理重复记录（ON CONFLICT DO UPDATE）
- 生成详细的导入报告

**关键特性**:
- ✅ 完整的错误处理和事务管理
- ✅ 批量插入优化性能
- ✅ 详细的进度输出
- ✅ 统计信息收集

### 2. 测试脚本

**文件**: `scripts/database/test_association_mapping.py`

**功能**:
- 检查 Plant_ID 映射覆盖率
- 检查 ICD-11 Code 映射覆盖率
- 预估导入成功率
- 分析证据类型分布
- 识别无法映射的记录

**用途**: 在正式导入前验证数据质量和映射情况

### 3. 使用文档

**文件**: `docs/bio_resource_disease_associations_import_guide.md`

**内容**:
- 数据源说明
- 表结构说明
- 字段映射规则
- 置信度计算规则
- 详细的使用步骤
- 验证方法
- 常见问题解答
- 性能优化建议

## 📊 数据映射方案

### 字段映射表

| 源文件字段 | 数据库字段 | 处理方式 |
|-----------|-----------|---------|
| Plant_ID | bio_resource_id | 通过 bio_resources.resource_id 查找 id |
| ICD-11 Code | disease_id | 通过 diseases.icd11_code 查找 id |
| Association_by_Therapeutic_Target | evidence_therapeutic_target | 直接存储（TEXT） |
| Association_by_Disease_Transcriptiome_Reversion | evidence_transcriptome | 转换为 BOOLEAN |
| Association_by_Clinical_Trials_of_Plant | evidence_clinical_trial_plant | 直接存储（TEXT） |
| Association_by_Clinical_Trials_of_Plant_Ingredients | evidence_clinical_trial_ingredient | 直接存储（TEXT） |

### 置信度计算规则

```python
confidence_score = 0.0
if has_therapeutic_target:    confidence_score += 0.3
if has_transcriptome:         confidence_score += 0.2
if has_clinical_trial_plant:  confidence_score += 0.3
if has_clinical_trial_ingredient: confidence_score += 0.2
```

**可能的置信度值**: 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0

## 🎯 方案优势

### 为什么选择关联表而不是补充到 diseases 表？

1. **符合数据库设计规范**
   - 植物-疾病是典型的多对多关系
   - 一个植物可关联多个疾病（最多557个）
   - 一个疾病可关联多个植物（最多33个）

2. **表结构完美匹配**
   - `bio_resource_disease_associations` 表已存在
   - 字段设计与源数据完美对应
   - 无需修改表结构

3. **数据量巨大**
   - 76万+条关联记录
   - 如果放到 diseases 表会导致严重的数据冗余

4. **查询性能好**
   - 已创建必要的索引
   - 支持高效的双向查询
   - 便于统计和聚合

5. **易于维护和扩展**
   - 可以独立更新关联数据
   - 便于添加新的证据类型
   - 不影响其他表结构

## 📁 文件清单

### 脚本文件

```
scripts/database/
├── import_bio_resource_disease_associations.py  # 导入脚本（320行）
└── test_association_mapping.py                  # 测试脚本（140行）
```

### 文档文件

```
docs/
└── bio_resource_disease_associations_import_guide.md  # 使用指南
```

### 数据文件

```
data/CMAUP/
└── CMAUPv2.0_download_Plant_Human_Disease_Associations.txt  # 源数据（765,267条）
```

## 🚀 使用流程

### 1. 前置条件检查

```bash
# 确保 bio_resources 和 diseases 表已有数据
psql -U postgres -d npdb -c "SELECT COUNT(*) FROM bio_resources;"
psql -U postgres -d npdb -c "SELECT COUNT(*) FROM diseases;"
```

### 2. 测试映射（可选）

```bash
python3 scripts/database/test_association_mapping.py
```

### 3. 执行导入

```bash
python3 scripts/database/import_bio_resource_disease_associations.py
```

### 4. 验证结果

```bash
# 检查记录数
psql -U postgres -d npdb -c "SELECT COUNT(*) FROM bio_resource_disease_associations;"

# 查看置信度分布
psql -U postgres -d npdb -c "
SELECT confidence_score, COUNT(*)
FROM bio_resource_disease_associations
GROUP BY confidence_score
ORDER BY confidence_score DESC;
"
```

## 📈 预期结果

### 导入统计

- **总记录数**: 765,267 条
- **预期成功率**: 取决于 Plant_ID 和 ICD-11 Code 的映射覆盖率
- **处理时间**: 约 5-10 分钟（取决于硬件性能）

### 证据类型分布（基于源数据分析）

- **治疗靶点证据**: ~48%
- **转录组证据**: ~17%
- **植物临床试验**: ~2%
- **成分临床试验**: ~47%

### 置信度分布

预期大部分记录的置信度在 0.3-0.5 之间（有1-2种证据）。

## 🔍 质量保证

### 数据验证

1. **映射验证**: 测试脚本会检查所有 Plant_ID 和 ICD-11 Code 的映射情况
2. **重复处理**: 使用 UNIQUE 约束和 ON CONFLICT 策略防止重复
3. **空值处理**: 正确处理 "n.a." 和空字符串
4. **类型转换**: 转录组证据正确转换为布尔值

### 错误处理

1. **事务管理**: 出错时自动回滚
2. **详细日志**: 记录所有跳过的记录和原因
3. **统计报告**: 生成完整的导入报告

## 📝 后续工作建议

### 1. 更新统计字段

导入完成后，更新相关表的统计字段：

```sql
-- 更新 bio_resources 表的疾病关联数
UPDATE bio_resources br
SET num_of_related_diseases = (
    SELECT COUNT(DISTINCT disease_id)
    FROM bio_resource_disease_associations
    WHERE bio_resource_id = br.id
);

-- 更新 diseases 表的植物关联数
UPDATE diseases d
SET num_of_related_plants = (
    SELECT COUNT(DISTINCT bio_resource_id)
    FROM bio_resource_disease_associations
    WHERE disease_id = d.id
);
```

### 2. 创建查询视图

创建便于查询的视图：

```sql
CREATE VIEW v_bio_resource_disease_detail AS
SELECT
    br.resource_id,
    br.latin_name,
    br.chinese_name,
    d.icd11_code,
    d.disease_name,
    d.disease_category,
    brda.evidence_therapeutic_target,
    brda.evidence_transcriptome,
    brda.evidence_clinical_trial_plant,
    brda.evidence_clinical_trial_ingredient,
    brda.confidence_score
FROM bio_resource_disease_associations brda
JOIN bio_resources br ON brda.bio_resource_id = br.id
JOIN diseases d ON brda.disease_id = d.id;
```

### 3. 后端API开发

在后端添加以下接口：

- `GET /api/bio-resources/{id}/diseases` - 查询植物的疾病关联
- `GET /api/diseases/{id}/bio-resources` - 查询疾病的植物关联
- `GET /api/bio-resource-disease-associations` - 查询关联列表（支持过滤）

### 4. 前端展示

在前端页面添加：

- 生物资源详情页：展示关联的疾病列表
- 疾病详情页：展示关联的植物列表
- 证据类型标签和置信度评分展示

## 🎓 技术要点

### 1. 批量插入优化

使用 `psycopg2.extras.execute_values` 进行批量插入，比逐条插入快10-100倍。

### 2. 冲突处理

使用 `ON CONFLICT DO UPDATE` 策略，允许安全地重复运行导入脚本。

### 3. 内存管理

使用批量处理（BATCH_SIZE=1000）避免一次性加载所有数据到内存。

### 4. 进度监控

每处理10000条记录输出一次进度，便于监控长时间运行的导入任务。

## ✅ 验收标准

导入成功的标准：

1. ✅ 脚本运行无错误
2. ✅ 导入记录数 > 700,000（考虑到部分记录可能无法映射）
3. ✅ 所有记录的置信度 > 0
4. ✅ 外键约束满足（所有 bio_resource_id 和 disease_id 都有效）
5. ✅ 生成完整的导入报告

## 📞 支持

如有问题，请参考：

- **使用指南**: `docs/bio_resource_disease_associations_import_guide.md`
- **数据库文档**: `docs/database.md`
- **后端开发文档**: `docs/backend-dev-doc.md`

## 🎉 总结

本次实施完成了植物-疾病关联数据的导入方案设计和脚本开发。选择使用现有的关联表是正确的数据库设计决策，符合规范化原则，性能优良，易于维护。所有必要的脚本和文档已准备就绪，可以立即执行导入操作。
