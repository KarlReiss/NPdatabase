# 处理后的靶点数据

## 文件说明

### 1. merged_targets.tsv
完整的天然产物靶点表，合并了 CMAUP 和 NPASS 数据。

- **总靶点数**: 8,764
- **数据来源**:
  - NPASS 3.0: 提供基础靶点列表（8,764个）
  - CMAUP v2.0: 提供详细注释信息（758个靶点的补充信息）

### 2. merged_targets_proteins_only.tsv
仅包含蛋白质类靶点的子集，排除了细胞系、组织、生物体等非蛋白质靶点。

- **蛋白质靶点数**: 4,893
- **包含类型**: Individual protein, Single protein, Protein complex, Protein family

## 字段说明

| 字段名 | 说明 | 数据来源 |
|--------|------|----------|
| Target_ID | 靶点唯一标识符（NPT开头） | NPASS |
| Gene_Symbol | 基因符号 | CMAUP |
| Target_Name | 靶点名称 | CMAUP优先，否则NPASS |
| Uniprot_ID | UniProt数据库ID | CMAUP优先，否则NPASS |
| NPASS_Target_Type | NPASS靶点类型分类 | NPASS |
| CMAUP_Target_Type | CMAUP靶点类型分类 | CMAUP |
| Organism_Tax_ID | 物种分类ID | NPASS |
| Organism | 物种名称 | NPASS |
| ChEMBL_ID | ChEMBL数据库ID | CMAUP |
| TTD_ID | TTD数据库ID | CMAUP |
| if_DTP | 是否为药物转运蛋白 (0/1) | CMAUP |
| if_CYP | 是否为细胞色素P450 (0/1) | CMAUP |
| if_therapeutic_target | 是否为治疗靶点 (0/1) | CMAUP |
| Target_Class_Level1 | 靶点分类一级 | CMAUP |
| Target_Class_Level2 | 靶点分类二级 | CMAUP |
| Target_Class_Level3 | 靶点分类三级 | CMAUP |
| Target_Class_level_displayed | 靶点分类显示名称 | CMAUP |
| TTD_Former_ID | TTD历史ID | TTD |
| TTD_Uniprot_Name | TTD的Uniprot Entry Name | TTD |
| TTD_Target_Name | TTD靶点名称 | TTD |
| TTD_Gene_Name | TTD基因名称 | TTD |
| TTD_Target_Type | TTD靶点类型 | TTD |
| TTD_Synonyms | TTD同义词 | TTD |
| TTD_Function | TTD功能描述 | TTD |
| TTD_PDB_Structures | TTD的PDB结构ID列表 | TTD |
| TTD_Bio_Class | TTD生物学分类 | TTD |
| TTD_EC_Number | TTD的EC编号 | TTD |
| TTD_Sequence | TTD蛋白质序列 | TTD |

## 数据统计

### 完整靶点表 (merged_targets.tsv)
- 总靶点数: 8,764
- 总字段数: 28
- 有CMAUP详细注释: 758 (8.6%)
- 仅NPASS基础信息: 8,006 (91.4%)
- 有效Uniprot ID: 5,056 (57.7%)
- 有ChEMBL ID: 758
- 有TTD ID: 552
- 有TTD详细信息: 552 (包含11个TTD字段)
- 治疗靶点: 709

### 蛋白质靶点表 (merged_targets_proteins_only.tsv)
- Individual protein: 2,927
- Single protein: 1,377
- Protein complex: 343
- Protein family: 246

## 合并策略

1. **基础数据**: 以NPASS为基础，包含所有8,764个靶点
2. **注释补充**: 通过Target_ID匹配，用CMAUP的详细信息补充758个靶点
3. **TTD数据补充**: 通过TTD_ID匹配，从TTD数据库补充552个靶点的详细信息
4. **字段优先级**:
   - Uniprot_ID: CMAUP优先（更可靠）
   - Target_Name: CMAUP的蛋白名称优先
   - 其他注释字段: 来自CMAUP（Gene_Symbol, ChEMBL_ID, TTD_ID, 分类信息等）
   - TTD字段: 来自TTD数据库（功能、结构、序列等详细信息）

## 使用建议

- 如果需要完整的靶点列表（包括细胞系、组织等），使用 `merged_targets.tsv`
- 如果只关注蛋白质靶点，使用 `merged_targets_proteins_only.tsv`
- 有Gene_Symbol的记录包含更丰富的注释信息，适合深入分析
- Uniprot_ID为"n.a."的记录可能是非蛋白质靶点或缺少注释

## 生成脚本

数据由以下脚本生成：
- `/home/yfguo/NPdatabase/scripts/merge_target_data.py` - 合并NPASS和CMAUP数据
- `/home/yfguo/NPdatabase/scripts/enrich_targets_with_ttd.py` - 补充TTD详细信息
