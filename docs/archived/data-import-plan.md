# 天然产物数据库 - 数据导入规划

## 1. 数据源概览

### 1.1 NPASS 数据库 (Natural Products Activity & Species Source Database)
| 文件 | 记录数 | 大小 | 说明 |
|------|--------|------|------|
| NPASS3.0_naturalproducts_generalinfo.txt | 204,022 | 47MB | 天然产物基本信息 |
| NPASS3.0_naturalproducts_structure.txt | 203,390 | 62MB | 天然产物结构(InChI, SMILES) |
| NPASS3.0_species_info.txt | 48,939 | 7.2MB | 物种/生物资源信息 |
| NPASS3.0_naturalproducts_species_pair.txt | 1,117,269 | 112MB | 天然产物-物种关联 |
| NPASS3.0_target.txt | 8,763 | 648KB | 靶点信息 |
| NPASS3.0_activities.txt | 1,048,755 | 101MB | 活性数据 |
| NPASS3.0_toxicity.txt | 34,975 | 3.2MB | 毒性数据 |

### 1.2 CMAUP 数据库 (Collective Molecular Activities of Useful Plants)
| 文件 | 记录数 | 大小 | 说明 |
|------|--------|------|------|
| CMAUPv2.0_download_Ingredients_All.txt | 60,222 | 25MB | 天然产物/成分信息 |
| CMAUPv2.0_download_Plants.txt | 7,864 | 634KB | 植物信息 |
| CMAUPv2.0_download_Targets.txt | 758 | 116KB | 靶点信息 |
| CMAUPv2.0_download_Ingredient_Target_Associations.txt | 28,871 | 1.3MB | 活性数据 |
| CMAUPv2.0_download_Plant_Ingredient_Associations.txt | 412,760 | 7.7MB | 植物-成分关联 |
| CMAUPv2.0_download_Human_Oral_Bioavailability.txt | 60,222 | 9.6MB | 口服生物利用度 |

---

## 2. 数据库表与数据源映射

### 2.1 natural_products 表 (天然产物)

**主数据源**: NPASS (更全面，20万+记录)
**补充数据源**: CMAUP (6万记录，部分重叠)

| 数据库字段 | NPASS字段 | CMAUP字段 | 说明 |
|-----------|-----------|-----------|------|
| np_id | np_id | np_id | 主键，两库共用NPC前缀 |
| inchikey | InChIKey | InChIKey | 结构唯一标识 |
| pref_name | pref_name | pref_name | 常用名 |
| iupac_name | iupac_name | iupac_name | IUPAC名称 |
| inchi | InChI | InChI | InChI结构 |
| smiles | SMILES | SMILES | SMILES结构 |
| chembl_id | chembl_id | chembl_id | ChEMBL ID |
| pubchem_id | pubchem_id | pubchem_cid | PubChem ID |
| molecular_weight | - | MW | 分子量 |
| xlogp | - | LogP | 脂溶性 |
| psa | - | TPSA | 极性表面积 |
| h_bond_donors | - | nHD | 氢键供体数 |
| h_bond_acceptors | - | nHA | 氢键受体数 |
| rotatable_bonds | - | nRot | 可旋转键数 |
| name_initial | name_initial | - | 名称首字母 |
| num_of_organism | num_of_organism | - | 来源物种数 |
| num_of_target | num_of_target | - | 靶点数 |
| num_of_activity | num_of_activity | - | 活性记录数 |

**合并策略**:
1. 以NPASS为主，导入全部204,022条记录
2. 用CMAUP补充理化性质(MW, LogP, TPSA等)
3. 通过np_id或InChIKey匹配合并

---

### 2.2 targets 表 (靶点)

**主数据源**: NPASS (8,763条，包含细胞系)
**补充数据源**: CMAUP (758条，蛋白靶点更详细)

| 数据库字段 | NPASS字段 | CMAUP字段 | 说明 |
|-----------|-----------|-----------|------|
| target_id | target_id | Target_ID | 主键 |
| target_type | target_type | Target_type | 靶点类型 |
| target_name | target_name | Protein_Name | 靶点名称 |
| target_organism | target_organism | - | 物种 |
| target_organism_tax_id | target_organism_tax_id | - | 物种分类ID |
| uniprot_id | uniprot_id | Uniprot_ID | UniProt ID |

**CMAUP额外字段** (可扩展):
- Gene_Symbol: 基因符号
- ChEMBL_ID: ChEMBL靶点ID
- TTD_ID: TTD靶点ID
- Target_Class_Level1/2/3: 靶点分类

**合并策略**:
1. 导入NPASS全部靶点
2. 用CMAUP补充UniProt ID和分类信息
3. 通过target_id匹配

---

### 2.3 bio_resources 表 (生物资源)

**主数据源**: NPASS species_info (48,939条，多物种类型)
**补充数据源**: CMAUP Plants (7,864条，仅植物)

| 数据库字段 | NPASS字段 | CMAUP字段 | 说明 |
|-----------|-----------|-----------|------|
| resource_id | org_id | Plant_ID | 主键 |
| resource_type | - | - | 需根据kingdom推断 |
| latin_name | org_name | Plant_Name | 拉丁名 |
| taxonomy_kingdom | kingdom_name | - | 界 |
| taxonomy_family | family_name | Family_Name | 科 |
| taxonomy_genus | genus_name | Genus_Name | 属 |
| taxonomy_species | species_name | Species_Name | 种 |
| taxonomy_id | species_tax_id | Species_Tax_ID | NCBI分类ID |

**NPASS额外分类字段**:
- superkingdom_name/tax_id
- genus_tax_id, family_tax_id
- org_tax_level

**合并策略**:
1. 导入NPASS全部物种(包含植物、动物、微生物等)
2. resource_type根据kingdom_name推断:
   - Viridiplantae → Plant (植物)
   - Fungi → Microbe (真菌)
   - Bacteria → Microbe (细菌)
   - Metazoa → Animal (动物)
3. CMAUP植物数据用于补充

---

### 2.4 bioactivity 表 (活性数据)

**主数据源**: NPASS activities (1,048,755条)
**补充数据源**: CMAUP Ingredient_Target_Associations (28,871条)

| 数据库字段 | NPASS字段 | CMAUP字段 | 说明 |
|-----------|-----------|-----------|------|
| natural_product_id | np_id → FK | Ingredient_ID → FK | 天然产物外键 |
| target_id | target_id → FK | Target_ID → FK | 靶点外键 |
| activity_type | activity_type | Activity_Type | 活性类型 |
| activity_type_grouped | activity_type_grouped | - | 活性类型分组 |
| activity_relation | activity_relation | Activity_Relationship | 关系符号 |
| activity_value | activity_value | Activity_Value | 活性值 |
| activity_units | activity_units | Activity_Unit | 单位 |
| assay_organism | assay_organism | - | 测试物种 |
| assay_tax_id | assay_tax_id | - | 测试物种ID |
| assay_strain | assay_strain | - | 菌株 |
| assay_tissue | assay_tissue | - | 组织 |
| assay_cell_type | assay_cell_type | - | 细胞类型 |
| ref_id | ref_id | Reference_ID | 文献ID |
| ref_id_type | ref_id_type | Reference_ID_Type | 文献类型 |

**合并策略**:
1. 导入NPASS全部活性数据
2. CMAUP数据作为补充（去重）
3. 需要先导入natural_products和targets表

---

### 2.5 toxicity 表 (毒性数据)

**数据源**: NPASS toxicity (34,975条)
**CMAUP无对应数据**

| 数据库字段 | NPASS字段 | 说明 |
|-----------|-----------|------|
| natural_product_id | np_id → FK | 天然产物外键 |
| toxicity_type | activity_type | 毒性类型(LD50, LD90等) |
| toxicity_value | activity_value | 毒性值 |
| toxicity_units | activity_units | 单位 |
| assay_organism | assay_organism | 测试物种 |
| ref_id | ref_id | 文献ID |
| ref_id_type | ref_id_type | 文献类型 |

---

### 2.6 bio_resource_natural_products 表 (生物资源-天然产物关联)

**主数据源**: NPASS naturalproducts_species_pair (1,117,269条)
**补充数据源**: CMAUP Plant_Ingredient_Associations (412,760条)

| 数据库字段 | NPASS字段 | CMAUP字段 | 说明 |
|-----------|-----------|-----------|------|
| bio_resource_id | org_id → FK | Plant_ID → FK | 生物资源外键 |
| natural_product_id | np_id → FK | Ingredient_ID → FK | 天然产物外键 |
| isolation_method | - | - | 分离方法 |
| ref_id | ref_id | - | 文献ID |
| ref_id_type | ref_id_type | - | 文献类型 |

**NPASS额外字段**:
- org_isolation_part: 分离部位
- org_collect_location: 采集地点
- org_collect_time: 采集时间
- new_cp_found: 是否新发现

---

## 3. 缺失数据分析

### 3.1 当前数据源缺失的内容

| 数据库表 | 缺失内容 | 建议 |
|---------|---------|------|
| bio_resources | 中文名、拼音、中药属性(性味归经) | 需从TCMSP/TCMID等中药数据库补充 |
| bio_resources | 药用部位、功效、主治 | 需从中国药典或中药数据库补充 |
| prescriptions | 处方/方剂数据 | 完全缺失，需从方剂数据库获取 |
| prescription_resources | 处方-药材关联 | 完全缺失 |
| prescription_natural_products | 处方-成分关联 | 完全缺失 |

### 3.2 建议补充的数据源

1. **TCMSP** (中药系统药理学数据库)
   - 中药材中文名、拼音
   - 性味归经、功效主治
   - 方剂数据

2. **TCMID** (中医药整合数据库)
   - 中药材详细信息
   - 处方组成

3. **中国药典数据**
   - 标准中药材信息
   - 药用部位、用法用量

---

## 4. 数据导入顺序

由于外键约束，必须按以下顺序导入：

```
Step 1: 基础表（无外键依赖）
├── natural_products  ← NPASS generalinfo + structure + CMAUP Ingredients
├── targets           ← NPASS target + CMAUP Targets
└── bio_resources     ← NPASS species_info + CMAUP Plants

Step 2: 关联表（依赖基础表）
├── bioactivity                    ← NPASS activities + CMAUP associations
├── toxicity                       ← NPASS toxicity
└── bio_resource_natural_products  ← NPASS species_pair + CMAUP associations

Step 3: 处方相关（需额外数据源）
├── prescriptions                  ← 待补充
├── prescription_resources         ← 待补充
└── prescription_natural_products  ← 待补充

Step 4: 统计字段更新
└── 更新各表的计数字段 (num_of_*)
```

---

## 5. 详细导入步骤

### Step 1.1: 导入 natural_products

```sql
-- 1. 从NPASS导入基本信息
-- 源文件: NPASS3.0_naturalproducts_generalinfo.txt + NPASS3.0_naturalproducts_structure.txt

-- 2. 用CMAUP补充理化性质
-- 源文件: CMAUPv2.0_download_Ingredients_All.txt
-- 匹配字段: np_id 或 InChIKey
```

**Python脚本任务**:
1. 读取NPASS generalinfo和structure，合并
2. 读取CMAUP Ingredients
3. 通过np_id匹配，补充MW, LogP, TPSA等
4. 批量插入数据库

### Step 1.2: 导入 targets

```sql
-- 1. 从NPASS导入靶点
-- 源文件: NPASS3.0_target.txt

-- 2. 用CMAUP补充详细信息
-- 源文件: CMAUPv2.0_download_Targets.txt
```

### Step 1.3: 导入 bio_resources

```sql
-- 1. 从NPASS导入物种信息
-- 源文件: NPASS3.0_species_info.txt

-- 2. 根据kingdom推断resource_type
-- 3. 用CMAUP补充植物信息
```

### Step 2.1: 导入 bioactivity

```sql
-- 1. 从NPASS导入活性数据
-- 源文件: NPASS3.0_activities.txt
-- 需要: np_id → natural_product_id (FK)
--       target_id → target_id (FK)

-- 2. 用CMAUP补充
-- 源文件: CMAUPv2.0_download_Ingredient_Target_Associations.txt
```

### Step 2.2: 导入 toxicity

```sql
-- 从NPASS导入毒性数据
-- 源文件: NPASS3.0_toxicity.txt
```

### Step 2.3: 导入 bio_resource_natural_products

```sql
-- 1. 从NPASS导入关联
-- 源文件: NPASS3.0_naturalproducts_species_pair.txt

-- 2. 用CMAUP补充
-- 源文件: CMAUPv2.0_download_Plant_Ingredient_Associations.txt
```

---

## 6. 数据质量处理

### 6.1 数据清洗规则

1. **空值处理**
   - `n.a.` → NULL
   - 空字符串 → NULL

2. **ID标准化**
   - np_id: 保持NPC前缀格式
   - target_id: 保持NPT前缀格式
   - org_id/resource_id: 保持NPO前缀格式

3. **数值转换**
   - 活性值: 转为numeric类型
   - 分子量: 转为numeric(10,2)

4. **去重策略**
   - natural_products: 按np_id去重
   - bioactivity: 按(np_id, target_id, activity_type, activity_value, ref_id)去重

### 6.2 数据验证

```sql
-- 导入后验证
SELECT COUNT(*) FROM natural_products;  -- 预期: ~204,000
SELECT COUNT(*) FROM targets;           -- 预期: ~8,700
SELECT COUNT(*) FROM bio_resources;     -- 预期: ~49,000
SELECT COUNT(*) FROM bioactivity;       -- 预期: ~1,000,000
SELECT COUNT(*) FROM toxicity;          -- 预期: ~35,000
SELECT COUNT(*) FROM bio_resource_natural_products; -- 预期: ~1,100,000
```

---

## 7. 预估数据量

| 表名 | 预估记录数 | 说明 |
|------|-----------|------|
| natural_products | ~210,000 | NPASS + CMAUP去重 |
| targets | ~9,000 | NPASS + CMAUP去重 |
| bio_resources | ~50,000 | NPASS物种 |
| bioactivity | ~1,070,000 | NPASS + CMAUP |
| toxicity | ~35,000 | NPASS |
| bio_resource_natural_products | ~1,500,000 | NPASS + CMAUP |
| prescriptions | 0 | 待补充 |
| prescription_resources | 0 | 待补充 |
| prescription_natural_products | 0 | 待补充 |

---

## 8. 下一步行动

### 8.1 立即可执行
1. 编写Python导入脚本
2. 按顺序导入NPASS和CMAUP数据
3. 验证数据完整性

### 8.2 需要补充数据
1. 获取TCMSP数据库（中药材中文信息）
2. 获取方剂数据库（处方信息）
3. 补充中药属性（性味归经）

### 8.3 脚本文件规划
```
scripts/database/
├── import_natural_products.py    # 导入天然产物
├── import_targets.py             # 导入靶点
├── import_bio_resources.py       # 导入生物资源
├── import_bioactivity.py         # 导入活性数据
├── import_toxicity.py            # 导入毒性数据
├── import_associations.py        # 导入关联数据
├── update_statistics.py          # 更新统计字段
└── validate_import.py            # 验证导入结果
```

---

## 9. 附录：字段对照表

### NPASS 文件分隔符
- 所有.txt文件: Tab分隔 (`\t`)
- 所有.tsv文件: Tab分隔 (`\t`)

### CMAUP 文件分隔符
- 所有.txt文件: Tab分隔 (`\t`)

### 编码
- 所有文件: UTF-8

---

**文档创建时间**: 2026-01-29
**数据库版本**: PostgreSQL 16.3
**目标表数量**: 9张表 + 4个视图
