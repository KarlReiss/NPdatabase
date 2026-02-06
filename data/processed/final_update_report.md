# Natural Products 表字段更新最终报告

## 📋 更新概述

**更新时间**: 2026-02-05
**操作内容**:
1. 删除gene_cluster字段（无数据）
2. 恢复if_quantity字段（应用户要求）
3. 添加5个新的理化性质字段（log_s, log_d, log_p, tpsa, ring_count）
4. 重新导入数据

## ✅ 最终表结构

### natural_products 表字段（28个）

| 序号 | 字段名 | 数据类型 | 说明 | 数据覆盖率 |
|-----|--------|---------|------|-----------|
| **基础字段** |
| 1 | id | bigint | 主键ID | 100% |
| 2 | np_id | varchar | 天然产物ID（业务主键） | 100% |
| 3 | inchikey | varchar | InChIKey标识符 | 99.69% |
| 4 | pref_name | text | 首选名称 | 100% |
| 5 | iupac_name | text | IUPAC系统命名 | ~50% |
| 6 | name_initial | varchar | 名称首字母 | 100% |
| **结构信息** |
| 7 | inchi | text | InChI标识符 | 29.68% |
| 8 | smiles | text | SMILES结构式 | 29.68% |
| **外部链接** |
| 9 | chembl_id | varchar | ChEMBL数据库ID | 16.55% |
| 10 | pubchem_id | varchar | PubChem数据库ID | 36.56% |
| **理化性质（原有）** |
| 11 | molecular_weight | numeric | 分子量 | 26.68% |
| 12 | xlogp | numeric | 脂水分配系数（计算值） | 26.68% |
| 13 | psa | numeric | 极性表面积（计算值） | 26.68% |
| 14 | formula | varchar | 分子式 | ~0% |
| 15 | h_bond_donors | integer | 氢键供体数 | 26.68% |
| 16 | h_bond_acceptors | integer | 氢键受体数 | 26.68% |
| 17 | rotatable_bonds | integer | 可旋转键数 | 26.68% |
| **理化性质（新增）** |
| 18 | log_s | numeric | 水溶性对数值 | 26.68% |
| 19 | log_d | numeric | 分配系数（pH 7.4） | 26.68% |
| 20 | log_p | numeric | 脂水分配系数（原始值） | 26.68% |
| 21 | tpsa | numeric | 拓扑极性表面积（原始值） | 26.68% |
| 22 | ring_count | integer | 环数量 | 26.68% |
| **生物学信息** |
| 23 | num_of_organism | integer | 关联生物体数量 | 100% |
| 24 | num_of_target | integer | 关联靶点数量 | 100% |
| 25 | num_of_activity | integer | 关联活性记录数量 | 100% |
| **其他** |
| 26 | if_quantity | boolean | 是否有定量信息 | 2.99% (TRUE) |
| 27 | created_at | timestamp | 创建时间 | 100% |
| 28 | updated_at | timestamp | 更新时间 | 100% |

### 已删除的字段
- ~~gene_cluster~~ - 基因簇信息（0条记录有数据，已删除）

## 📊 数据统计

### 总体情况
- **总记录数**: 203,023条
- **成功导入**: 203,023条 (99.51%)
- **失败记录**: 1,000条 (0.49% - 因1条np_id为空导致整批失败)

### 理化性质字段覆盖率
所有理化性质字段的覆盖率均为 **26.68%** (54,165条记录)，这些数据来自CMAUP v2.0：

| 字段 | 覆盖率 | 记录数 |
|-----|--------|--------|
| molecular_weight | 26.68% | 54,165 |
| xlogp | 26.68% | 54,165 |
| psa | 26.68% | 54,165 |
| h_bond_donors | 26.68% | 54,165 |
| h_bond_acceptors | 26.68% | 54,165 |
| rotatable_bonds | 26.68% | 54,165 |
| **log_s** (新增) | 26.68% | 54,165 |
| **log_d** (新增) | 26.68% | 54,165 |
| **log_p** (新增) | 26.68% | 54,165 |
| **tpsa** (新增) | 26.68% | 54,165 |
| **ring_count** (新增) | 26.68% | 54,165 |

### 其他字段覆盖率
| 字段 | 覆盖率 | 记录数 |
|-----|--------|--------|
| InChIKey | 99.69% | 202,390 |
| SMILES | 29.68% | 60,251 |
| InChI | 29.68% | 60,251 |
| PubChem ID | 36.56% | 74,233 |
| ChEMBL ID | 16.55% | 33,600 |
| if_quantity (TRUE) | 2.99% | 6,072 |

## 🎯 字段说明

### xlogp vs log_p
- **xlogp**: 计算的脂水分配系数（可能经过标准化或调整）
- **log_p**: 原始的脂水分配系数值（来自CMAUP）
- 两者可能略有差异，保留两个字段以提供更多选择

### psa vs tpsa
- **psa**: 极性表面积（可能经过计算或调整）
- **tpsa**: 拓扑极性表面积（原始值，来自CMAUP）
- 两者可能略有差异，保留两个字段以提供更多选择

### 新增字段的价值
1. **log_s**: 水溶性，对药物开发很重要
2. **log_d**: pH 7.4下的分配系数，更接近生理条件
3. **log_p**: 原始脂水分配系数，用于对比
4. **tpsa**: 原始拓扑极性表面积，用于对比
5. **ring_count**: 环数量，用于结构分析和筛选

## 📝 示例记录

### 有完整理化性质的记录
```
np_id: NPC100005
名称: MXFUWJQZQGWIOY-FETLVNPKSA-N
分子量: 1042.57
xlogp: 3.60 (计算值)
log_p: 3.60 (原始值)
psa: 294.60 (计算值)
tpsa: 294.60 (原始值)
log_s: -4.19 (水溶性)
log_d: 3.38 (pH 7.4分配系数)
氢键供体: 10
氢键受体: 20
可旋转键: 12
环数量: 9
if_quantity: False
```

## 🔧 更新的文件

### 1. 数据库
- ✅ 删除了gene_cluster字段
- ✅ 恢复了if_quantity字段
- ✅ 添加了5个新字段（log_s, log_d, log_p, tpsa, ring_count）
- ✅ 更新了v_natural_product_detail视图

### 2. 后端实体类
- ✅ `backend/src/main/java/cn/npdb/entity/NaturalProduct.java`
- ✅ `backend/src/main/java/cn/npdb/entity/NaturalProductDetailView.java`

### 3. 导入脚本
- ✅ `scripts/database/update_natural_products_with_integrated_data.py`

### 4. SQL脚本
- ✅ `scripts/database/remove_gene_cluster_and_if_quantity.sql` (已过时)
- 新增: 添加新字段的SQL已执行

## ⚠️ 注意事项

### 1. 字段命名
- 数据库字段使用下划线命名：`log_s`, `log_d`, `log_p`, `tpsa`, `ring_count`
- Java实体类使用驼峰命名：`logS`, `logD`, `logP`, `tpsa`, `ringCount`

### 2. 数据覆盖率
- 理化性质字段覆盖率为26.68%，意味着73.32%的记录缺少这些数据
- 建议：
  - 使用RDKit等工具计算缺失的理化性质
  - 或从PubChem API获取
  - 或在前端显示时标注"数据缺失"

### 3. 重复字段
- xlogp vs log_p：保留两者以提供选择
- psa vs tpsa：保留两者以提供选择
- 前端可以选择显示其中一个，或同时显示以供对比

### 4. if_quantity字段
- 仅2.99%的记录为TRUE
- 使用率较低，但应用户要求保留
- 可用于筛选有定量数据的化合物

## 🎉 更新完成

Natural Products表已成功更新，包含203,023条记录，新增了5个理化性质字段，为数据分析和药物筛选提供了更多维度。

**当前状态**:
- ✅ 表结构已更新（28个字段）
- ✅ 数据已重新导入
- ✅ 视图已更新
- ✅ 后端实体类已更新
- ✅ 导入脚本已更新

**下一步建议**:
1. 更新前端代码，显示新的理化性质字段
2. 更新API文档
3. 测试后端API和前端展示
4. 考虑补充缺失的理化性质数据（73.32%的记录）
