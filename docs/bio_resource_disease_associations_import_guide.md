# 植物-疾病关联数据导入指南

## 概述

本指南说明如何将 CMAUP v2.0 的植物-疾病关联数据导入到 `bio_resource_disease_associations` 表中。

## 数据源

- **文件**: `data/CMAUP/CMAUPv2.0_download_Plant_Human_Disease_Associations.txt`
- **记录数**: 765,267 条
- **关系类型**: 植物-疾病多对多关系

## 数据库表结构

### bio_resource_disease_associations 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGSERIAL | 主键 |
| bio_resource_id | BIGINT | 生物资源ID（外键 → bio_resources） |
| disease_id | BIGINT | 疾病ID（外键 → diseases） |
| evidence_therapeutic_target | TEXT | 治疗靶点证据（靶点列表） |
| evidence_transcriptome | BOOLEAN | 转录组证据 |
| evidence_clinical_trial_plant | TEXT | 植物临床试验证据 |
| evidence_clinical_trial_ingredient | TEXT | 成分临床试验证据 |
| confidence_score | DECIMAL(3,2) | 置信度评分（0-1） |
| source | VARCHAR(100) | 数据来源（CMAUP） |
| source_version | VARCHAR(50) | 数据版本（v2.0） |
| created_at | TIMESTAMP | 创建时间 |

## 字段映射

### 源文件 → 数据库表

| 源文件字段 | 数据库字段 | 处理方式 |
|-----------|-----------|---------|
| Plant_ID | bio_resource_id | 通过 bio_resources.resource_id 映射 |
| ICD-11 Code | disease_id | 通过 diseases.icd11_code 映射 |
| Association_by_Therapeutic_Target | evidence_therapeutic_target | 直接存储（文本） |
| Association_by_Disease_Transcriptiome_Reversion | evidence_transcriptome | 转换为布尔值 |
| Association_by_Clinical_Trials_of_Plant | evidence_clinical_trial_plant | 直接存储（文本） |
| Association_by_Clinical_Trials_of_Plant_Ingredients | evidence_clinical_trial_ingredient | 直接存储（文本） |

## 置信度计算规则

置信度评分基于证据类型计算（0-1之间）：

- **治疗靶点证据**: +0.3
- **转录组证据**: +0.2
- **植物临床试验**: +0.3
- **成分临床试验**: +0.2

**示例**:
- 仅有治疗靶点证据: 0.3
- 有治疗靶点 + 成分临床试验: 0.5
- 有全部4种证据: 1.0

## 使用步骤

### 1. 前置条件检查

确保以下表已创建并导入数据：

```bash
# 检查 bio_resources 表
psql -U postgres -d npdb -c "SELECT COUNT(*) FROM bio_resources;"

# 检查 diseases 表
psql -U postgres -d npdb -c "SELECT COUNT(*) FROM diseases;"

# 检查 diseases 表结构（注意：disease_id 字段已被删除）
psql -U postgres -d npdb -c "\d diseases"

# 检查 bio_resource_disease_associations 表是否存在
psql -U postgres -d npdb -c "\d bio_resource_disease_associations"
```

**注意**：diseases 表已经过优化，删除了 disease_id、description、symptoms 等字段，现在使用 icd11_code 作为唯一标识。

如果表不存在，先创建：

```bash
psql -U postgres -d npdb -f scripts/database/create_bio_resource_disease_associations_table.sql
```

### 2. 测试映射覆盖率（可选但推荐）

运行测试脚本检查数据映射情况：

```bash
python3 scripts/database/test_association_mapping.py
```

测试脚本会输出：
- 植物ID映射覆盖率
- 疾病编码映射覆盖率
- 预估导入成功率
- 证据类型分布统计

### 3. 执行导入

运行导入脚本：

```bash
python3 scripts/database/import_bio_resource_disease_associations.py
```

导入过程会：
1. 加载生物资源和疾病的ID映射
2. 读取CMAUP关联数据文件
3. 处理证据字段并计算置信度
4. 批量插入数据（BATCH_SIZE=1000）
5. 处理重复记录（ON CONFLICT DO UPDATE）
6. 生成导入报告

### 4. 验证导入结果

```bash
# 检查导入记录数
psql -U postgres -d npdb -c "SELECT COUNT(*) FROM bio_resource_disease_associations;"

# 查看置信度分布
psql -U postgres -d npdb -c "
SELECT
    confidence_score,
    COUNT(*) as count
FROM bio_resource_disease_associations
GROUP BY confidence_score
ORDER BY confidence_score DESC;
"

# 查看证据类型统计
psql -U postgres -d npdb -c "
SELECT
    COUNT(*) FILTER (WHERE evidence_therapeutic_target IS NOT NULL) as has_target,
    COUNT(*) FILTER (WHERE evidence_transcriptome = TRUE) as has_transcriptome,
    COUNT(*) FILTER (WHERE evidence_clinical_trial_plant IS NOT NULL) as has_trial_plant,
    COUNT(*) FILTER (WHERE evidence_clinical_trial_ingredient IS NOT NULL) as has_trial_ingredient
FROM bio_resource_disease_associations;
"

# 查看示例记录
psql -U postgres -d npdb -c "
SELECT
    br.resource_id,
    br.latin_name,
    d.icd11_code,
    d.disease_name,
    brda.confidence_score,
    brda.evidence_therapeutic_target
FROM bio_resource_disease_associations brda
JOIN bio_resources br ON brda.bio_resource_id = br.id
JOIN diseases d ON brda.disease_id = d.id
LIMIT 10;
"
```

## 导入报告

导入完成后会生成报告文件：

```
data/processed/bio_resource_disease_associations_import_report.txt
```

报告内容包括：
- 数据处理统计（总记录数、成功数、跳过数）
- 证据类型统计
- 数据库导入统计

## 常见问题

### Q1: 为什么有些记录被跳过？

**A**: 记录被跳过的原因：
1. **Plant_ID 无法映射**: 该植物ID在 bio_resources 表中不存在
2. **ICD-11 Code 无法映射**: 该疾病编码在 diseases 表中不存在

解决方法：
- 确保先导入 bio_resources 和 diseases 数据
- 检查数据源的一致性

### Q2: 如何处理重复记录？

**A**: 导入脚本使用 `ON CONFLICT DO UPDATE` 策略：
- 如果 (bio_resource_id, disease_id) 组合已存在，则更新证据字段
- 这样可以安全地重复运行导入脚本

### Q3: 置信度评分为0是否正常？

**A**: 不正常。如果置信度为0，说明该记录没有任何证据，这种情况不应该出现在CMAUP数据中。请检查数据处理逻辑。

### Q4: 如何重新导入数据？

**A**: 可以直接重新运行导入脚本，或者先清空表：

```bash
# 清空表（保留表结构）
psql -U postgres -d npdb -c "TRUNCATE TABLE bio_resource_disease_associations CASCADE;"

# 重新导入
python3 scripts/database/import_bio_resource_disease_associations.py
```

## 性能优化

### 索引

表已创建以下索引：
- `idx_brda_bio_resource`: bio_resource_id
- `idx_brda_disease`: disease_id
- `idx_brda_confidence`: confidence_score

### 批量插入

脚本使用批量插入（BATCH_SIZE=1000）来提高性能。如果遇到内存问题，可以减小批量大小。

## 相关文件

- **导入脚本**: `scripts/database/import_bio_resource_disease_associations.py`
- **测试脚本**: `scripts/database/test_association_mapping.py`
- **表创建脚本**: `scripts/database/create_bio_resource_disease_associations_table.sql`
- **数据源**: `data/CMAUP/CMAUPv2.0_download_Plant_Human_Disease_Associations.txt`

## 下一步

导入完成后，可以：

1. **更新统计信息**: 更新 bio_resources 和 diseases 表的关联计数
2. **创建视图**: 创建便于查询的视图
3. **后端API**: 在后端添加植物-疾病关联查询接口
4. **前端展示**: 在前端展示植物的疾病关联信息

## 联系方式

如有问题，请查看：
- 项目文档: `docs/database.md`
- 后端开发文档: `docs/backend-dev-doc.md`
