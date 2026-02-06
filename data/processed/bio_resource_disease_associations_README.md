# 植物-疾病关联数据导入 - README

## 📋 项目概述

本项目实现了 CMAUP v2.0 植物-疾病关联数据到 NPdatabase 的导入功能。数据存储在 `bio_resource_disease_associations` 关联表中，支持植物与疾病的多对多关系，包含4种证据类型和置信度评分。

## 🎯 方案决策

**✅ 采用方案**: 使用现有的 `bio_resource_disease_associations` 关联表

**理由**:
1. 符合数据库设计规范（多对多关系）
2. 表结构已存在且完美匹配
3. 避免数据冗余（76万+条记录）
4. 查询性能好，易于维护

## 📁 文件结构

```
NPdatabase/
├── scripts/database/
│   ├── import_bio_resource_disease_associations.py    # 主导入脚本
│   ├── test_association_mapping.py                    # 映射测试脚本
│   └── update_bio_resource_disease_stats.sql          # 统计更新脚本
├── docs/
│   └── bio_resource_disease_associations_import_guide.md  # 详细使用指南
└── data/
    ├── CMAUP/
    │   └── CMAUPv2.0_download_Plant_Human_Disease_Associations.txt  # 源数据
    └── processed/
        ├── bio_resource_disease_associations_implementation_summary.md  # 实施总结
        ├── bio_resource_disease_associations_quick_reference.md         # 快速参考
        └── bio_resource_disease_associations_import_report.txt          # 导入报告（运行后生成）
```

## 🚀 快速开始

### 前置条件

1. PostgreSQL 数据库已安装并运行
2. `npdb` 数据库已创建
3. 以下表已创建并导入数据：
   - `bio_resources` (生物资源表)
   - `diseases` (疾病表)
   - `bio_resource_disease_associations` (关联表)

### 步骤1: 测试映射（推荐）

```bash
cd /home/yfguo/NPdatabase
python3 scripts/database/test_association_mapping.py
```

**输出内容**:
- Plant_ID 映射覆盖率
- ICD-11 Code 映射覆盖率
- 预估导入成功率
- 证据类型分布

### 步骤2: 执行导入

```bash
python3 scripts/database/import_bio_resource_disease_associations.py
```

**预期时间**: 5-10 分钟

**输出内容**:
- 实时进度显示
- 数据处理统计
- 证据类型统计
- 导入报告路径

### 步骤3: 更新统计字段

```bash
psql -U postgres -d npdb -f scripts/database/update_bio_resource_disease_stats.sql
```

**功能**:
- 更新 `bio_resources.num_of_related_diseases`
- 更新 `diseases.num_of_related_plants`
- 显示统计摘要和Top 10排行

### 步骤4: 验证结果

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

# 查看示例数据
psql -U postgres -d npdb -c "
SELECT
    br.resource_id,
    br.latin_name,
    d.disease_name,
    brda.confidence_score
FROM bio_resource_disease_associations brda
JOIN bio_resources br ON brda.bio_resource_id = br.id
JOIN diseases d ON brda.disease_id = d.id
LIMIT 5;
"
```

## 📊 数据说明

### 源数据

- **文件**: `CMAUPv2.0_download_Plant_Human_Disease_Associations.txt`
- **记录数**: 765,267 条
- **字段数**: 8 个
- **编码**: UTF-8
- **分隔符**: Tab

### 字段映射

| 源字段 | 目标字段 | 类型 | 说明 |
|--------|---------|------|------|
| Plant_ID | bio_resource_id | BIGINT | 通过 bio_resources.resource_id 映射 |
| ICD-11 Code | disease_id | BIGINT | 通过 diseases.icd11_code 映射 |
| Association_by_Therapeutic_Target | evidence_therapeutic_target | TEXT | 治疗靶点列表 |
| Association_by_Disease_Transcriptiome_Reversion | evidence_transcriptome | BOOLEAN | 转录组证据 |
| Association_by_Clinical_Trials_of_Plant | evidence_clinical_trial_plant | TEXT | 植物临床试验ID |
| Association_by_Clinical_Trials_of_Plant_Ingredients | evidence_clinical_trial_ingredient | TEXT | 成分临床试验ID |

### 置信度计算

```
confidence_score =
    (有治疗靶点证据 ? 0.3 : 0) +
    (有转录组证据 ? 0.2 : 0) +
    (有植物临床试验 ? 0.3 : 0) +
    (有成分临床试验 ? 0.2 : 0)

范围: 0.2 - 1.0
```

## 📖 文档说明

### 1. 详细使用指南
**文件**: `docs/bio_resource_disease_associations_import_guide.md`

**内容**:
- 完整的使用步骤
- 表结构说明
- 字段映射规则
- 常见问题解答
- 性能优化建议

### 2. 实施总结
**文件**: `data/processed/bio_resource_disease_associations_implementation_summary.md`

**内容**:
- 方案决策说明
- 已完成工作清单
- 技术要点
- 后续工作建议

### 3. 快速参考
**文件**: `data/processed/bio_resource_disease_associations_quick_reference.md`

**内容**:
- 一页纸快速参考
- 关键命令
- 文件清单

## 🔧 脚本说明

### 1. 导入脚本
**文件**: `scripts/database/import_bio_resource_disease_associations.py`

**功能**:
- 读取 CMAUP 关联数据
- 映射 Plant_ID 和 ICD-11 Code
- 处理证据字段
- 计算置信度
- 批量插入数据
- 生成导入报告

**参数**: 无（配置在脚本内部）

**输出**: `data/processed/bio_resource_disease_associations_import_report.txt`

### 2. 测试脚本
**文件**: `scripts/database/test_association_mapping.py`

**功能**:
- 检查映射覆盖率
- 识别无法映射的记录
- 预估导入成功率
- 分析证据分布

**参数**: 无

**输出**: 控制台输出

### 3. 统计更新脚本
**文件**: `scripts/database/update_bio_resource_disease_stats.sql`

**功能**:
- 更新统计字段
- 显示统计摘要
- 显示Top 10排行

**参数**: 无

**输出**: 控制台输出 + 数据库更新

## ⚠️ 注意事项

### 1. 数据库连接

脚本中的数据库配置：
```python
DB_CONFIG = {
    'dbname': 'npdb',
    'user': 'yfguo',
    'host': 'localhost',
    'port': 5432
}
```

如需修改，请编辑脚本中的 `DB_CONFIG` 字典。

### 2. 重复运行

导入脚本使用 `ON CONFLICT DO UPDATE` 策略，可以安全地重复运行。重复运行会更新已存在的记录。

### 3. 性能优化

- 批量大小: BATCH_SIZE = 1000
- 如遇内存问题，可减小批量大小
- 建议在数据库空闲时运行

### 4. 错误处理

如果导入失败：
1. 检查数据库连接
2. 确认前置表已有数据
3. 查看错误日志
4. 检查磁盘空间

## 📈 预期结果

### 导入统计

- **总记录数**: 765,267
- **预期成功率**: 95%+ （取决于映射覆盖率）
- **处理时间**: 5-10 分钟

### 证据分布

- **治疗靶点**: ~48%
- **转录组**: ~17%
- **植物临床试验**: ~2%
- **成分临床试验**: ~47%

### 置信度分布

大部分记录的置信度在 0.3-0.5 之间。

## 🐛 故障排除

### 问题1: 数据库连接失败

**错误**: `psycopg2.OperationalError: could not connect to server`

**解决**:
1. 检查 PostgreSQL 是否运行: `sudo systemctl status postgresql`
2. 检查数据库配置
3. 检查用户权限

### 问题2: 映射失败率高

**现象**: 大量记录被跳过

**解决**:
1. 运行测试脚本查看详情
2. 确认 bio_resources 和 diseases 表已导入数据
3. 检查数据源的一致性

### 问题3: 内存不足

**错误**: `MemoryError`

**解决**:
1. 减小 BATCH_SIZE（如改为500）
2. 关闭其他应用程序
3. 增加系统内存

## 📞 获取帮助

- **详细文档**: `docs/bio_resource_disease_associations_import_guide.md`
- **数据库文档**: `docs/database.md`
- **后端文档**: `docs/backend-dev-doc.md`

## ✅ 验收清单

导入完成后，请检查：

- [ ] 导入脚本运行无错误
- [ ] 记录数 > 700,000
- [ ] 所有置信度 > 0
- [ ] 统计字段已更新
- [ ] 导入报告已生成
- [ ] 示例查询返回正确结果

## 🎉 完成

恭喜！您已成功完成植物-疾病关联数据的导入。

下一步可以：
1. 开发后端API接口
2. 在前端展示关联数据
3. 进行数据分析和可视化

---

**最后更新**: 2026-02-05
**版本**: 1.0
**作者**: Claude Code
