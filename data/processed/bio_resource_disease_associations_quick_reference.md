# 植物-疾病关联数据导入 - 快速参考

## 🎯 方案决策

**✅ 使用现有的 `bio_resource_disease_associations` 关联表**

**❌ 不将字段补充到 diseases 表**

## 📊 数据概览

- **数据源**: CMAUP v2.0 Plant-Human Disease Associations
- **记录数**: 765,267 条
- **关系**: 植物-疾病多对多关系
- **证据类型**: 4种（治疗靶点、转录组、植物临床试验、成分临床试验）

## 🚀 快速开始

### 1. 测试映射（可选）

```bash
python3 scripts/database/test_association_mapping.py
```

### 2. 执行导入

```bash
python3 scripts/database/import_bio_resource_disease_associations.py
```

### 3. 验证结果

```bash
psql -U postgres -d npdb -c "SELECT COUNT(*) FROM bio_resource_disease_associations;"
```

## 📁 关键文件

| 文件 | 说明 |
|------|------|
| `scripts/database/import_bio_resource_disease_associations.py` | 导入脚本 |
| `scripts/database/test_association_mapping.py` | 测试脚本 |
| `docs/bio_resource_disease_associations_import_guide.md` | 详细指南 |
| `data/processed/bio_resource_disease_associations_implementation_summary.md` | 实施总结 |

## 🔑 置信度计算

```
治疗靶点证据:    +0.3
转录组证据:      +0.2
植物临床试验:    +0.3
成分临床试验:    +0.2
-------------------
总分范围:        0.2 - 1.0
```

## 📋 字段映射

```
Plant_ID                                    → bio_resource_id (映射)
ICD-11 Code                                 → disease_id (映射)
Association_by_Therapeutic_Target           → evidence_therapeutic_target
Association_by_Disease_Transcriptiome_...   → evidence_transcriptome (布尔)
Association_by_Clinical_Trials_of_Plant     → evidence_clinical_trial_plant
Association_by_Clinical_Trials_of_Plant_... → evidence_clinical_trial_ingredient
```

## ✅ 验收标准

- [x] 导入记录数 > 700,000
- [x] 所有置信度 > 0
- [x] 外键约束满足
- [x] 生成导入报告

## 📞 获取帮助

详细文档: `docs/bio_resource_disease_associations_import_guide.md`
