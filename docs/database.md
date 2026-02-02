# 数据库结构说明（含数据补充更新）

> 版本: v2.0 (含数据补充)
> 更新时间: 2026-01-29
> 数据库: PostgreSQL 16
> 数据来源: NPASS 3.0 + TTD + TCMID + CMAUP

---

## 📊 数据库概览

- 数据库：PostgreSQL 16
- 核心表（11 张）：
  - `natural_products`（天然产物核心表）
  - `targets`（靶点表）
  - `bioactivity`（生物活性记录）
  - `toxicity`（毒性表）
  - `bio_resources`（生物资源/药材/来源）
  - `bio_resource_natural_products`（生物资源-天然产物关联）
  - `prescriptions`（处方/方剂表）
  - `prescription_resources`（处方-生物资源关联）
  - `prescription_natural_products`（处方-天然产物关联）
  - `diseases`（疾病表，新增）
  - `bio_resource_disease_associations`（生物资源-疾病关联表，新增）
- 系统表（2 张）：
  - `sys_dict`（系统字典）
  - `sys_menu`（系统菜单）
- 视图（4 个）：
  - `v_natural_product_detail`
  - `v_bio_resource_detail`
  - `v_target_detail`
  - `v_prescription_detail`
- 触发器：
  - `update_natural_products_updated_at`
  - `update_targets_updated_at`
  - `update_bio_resources_updated_at`
  - `update_prescriptions_updated_at`
  - `update_diseases_updated_at`

### 核心关系（简图）
```
natural_products 1---n bioactivity n---1 targets
natural_products 1---n bio_resource_natural_products n---1 bio_resources
natural_products 1---n toxicity
bio_resources 1---n bio_resource_disease_associations n---1 diseases
prescriptions 1---n prescription_resources n---1 bio_resources
prescriptions 1---n prescription_natural_products n---1 natural_products
```

---

## 📋 数据统计（2026-01-29）

| 表名 | 记录数 | 数据来源 |
|------|---------|----------|
| natural_products | ~500,000 | NPASS 3.0 |
| targets | 12,368 | NPASS 3.0 + TTD 补充 |
| bioactivity | ~1,000,000 | NPASS 3.0 |
| toxicity | ~50,000 | NPASS 3.0 |
| bio_resources | 26,789 (植物) | NPASS 3.0 + CMAUP 补充 |
| bio_resource_natural_products | ~1,500,000 | NPASS 3.0 |
| prescriptions | 2,093 | TCMID |
| prescription_resources | 14,785 | TCMID |
| prescription_natural_products | 0 | 保留字段 |
| diseases | 1,351 | CMAUP |
| bio_resource_disease_associations | 565,751 | CMAUP |

---

## 📝 数据补充说明

### 阶段 4: 数据补充

#### Step 4.1: TTD 靶点数据补充

**补充内容**:
- 新增字段：`gene_name`, `synonyms`, `function`, `pdb_structure`, `bioclass`, `ec_number`, `sequence`, `ttd_id`
- 更新记录数：4,297 个靶点
- 匹配率：34.74%
- 数据来源：TTD (Therapeutic Target Database)

**补充效果**:
- 基因名覆盖率：29.7%
- 同义词覆盖率：30.6%
- 功能描述覆盖率：29.9%
- PDB结构覆盖率：18.5%

#### Step 4.2: TCMID 处方数据导入

**补充内容**:
- 新增表：`prescriptions`, `prescription_resources`
- 新增字段：`tcmid_id`, `component_id`, `barcode`, `disease_icd11_category`, `human_tissues`, `reference`, `reference_book`
- 处方记录数：2,093
- 药材关联数：14,785
- 药材匹配率：5.55%
- 数据来源：TCMID (Traditional Chinese Medicine Information Database)

**补充效果**:
- 新增处方数据：2,093 个
- 涵盖中医处方组成和功能主治
- 支持 ICD-11 疾病分类

#### Step 4.3: CMAUP 植物数据补充

**补充内容**:
- 新增字段：`species_tax_id`, `genus_tax_id`, `family_tax_id`, `cmaup_id`
- 更新记录数：5,635 个生物资源
- 匹配率：21.03%
- 数据来源：CMAUP v2.0 (Chinese Medicine and Alzheimer's Disease Prediction)

**补充效果**:
- Taxonomy ID 填充率：21.0%
- 种分类信息：5,422 条
- 属分类信息：5,634 条
- 科分类信息：5,635 条
- 涵盖 364 科、2,187 属、5,422 种

#### Step 4.4: CMAUP 疾病数据导入

**补充内容**:
- 新增表：`diseases`, `bio_resource_disease_associations`
- 疾病记录数：1,351
- 疾病关联数：565,751
- 疾病覆盖范围：ICD-11 主要分类
- 数据来源：CMAUP v2.0

**补充效果**:
- 疾病分类：涵盖 ICD-11 所有主要分类
- 关联植物：4,741 种生物资源
- 证据类型：治疗靶点、转录组、临床试验
- 置信度评分：每个关联都有置信度 (0-1)
- 97.93% 的疾病有植物关联

---

## 📋 表结构详解（最终结构）

### 1. natural_products（天然产物表）

**用途**：存储天然产物基本信息与理化性质。

**核心字段**：
- 标识：`np_id`（唯一业务 ID，如 NPC491451）、`inchikey`
- 名称：`pref_name`, `iupac_name`, `name_initial`
- 结构：`inchi`, `smiles`
- 外部ID：`chembl_id`, `pubchem_id`
- 理化：`molecular_weight`, `xlogp`, `psa`, `formula`, `h_bond_donors`, `h_bond_acceptors`, `rotatable_bonds`
- 统计：`num_of_organism`, `num_of_target`, `num_of_activity`
- 其他：`gene_cluster`, `if_quantity`

**约束**：
- `np_id` 唯一
- `molecular_weight` > 0（若不为空）

**索引**：
- `np_id`, `inchikey`, `pref_name`, `chembl_id`, `pubchem_id`
- `molecular_weight`, `xlogp`, `psa`
- `num_of_activity`, `num_of_target`
- 全文索引（GIN）：`pref_name`, `iupac_name`

---

### 2. targets（靶点表）

**用途**：存储靶点信息（蛋白、细胞系、基因等），包含 TTD 补充数据。

**核心字段**：
- 标识：`target_id`（唯一业务 ID，如 NPT918）
- 基本信息：`target_type`, `target_name`, `target_organism`, `target_organism_tax_id`
- 外部ID：`uniprot_id`
- **TTD 补充字段**：
  - `gene_name` - 基因名
  - `synonyms` - 同义词
  - `function` - 功能描述
  - `pdb_structure` - PDB结构ID
  - `bioclass` - 生物分类
  - `ec_number` - EC编号
  - `sequence` - 蛋白序列
  - `ttd_id` - TTD ID
- 统计：`num_of_natural_products`, `num_of_activities`

**索引**：
- `target_id`, `target_type`, `target_name`, `target_organism`, `uniprot_id`
- `gene_name`, `ttd_id`, `ec_number` (TTD 补充)
- 全文索引（GIN）：`target_name`, `function`, `synonyms`

---

### 3. bioactivity（活性记录表）

**用途**：存储天然产物-靶点活性记录。

**核心字段**：
- 关联：`natural_product_id`, `target_id`
- 活性类型：`activity_type`, `activity_type_grouped`, `activity_relation`
- 数值：`activity_value`, `activity_units`
- 标准化：`activity_value_std`, `activity_units_std`（默认 nM）
- 实验条件：`assay_organism`, `assay_tax_id`, `assay_strain`, `assay_tissue`, `assay_cell_type`
- 文献：`ref_id`, `ref_id_type`（PMID/DOI/Patent）

**约束**：
- `activity_value` / `activity_value_std` >= 0（若不为空）
- 外键：`natural_product_id` → `natural_products(id)`，`target_id` → `targets(id)`

**索引**：
- `natural_product_id`, `target_id`, `activity_type`, `activity_type_grouped`
- `activity_value_std`, `activity_relation`, `ref_id`
- 复合索引：`(natural_product_id, target_id)`

**单位标准化规则**：
```
M  → nM: × 1,000,000,000
mM → nM: × 1,000,000
μM → nM: × 1,000
nM → nM: × 1
pM → nM: × 0.001
```

---

### 4. toxicity（毒性表）

**用途**：存储天然产物毒性数据。

**核心字段**：
- `natural_product_id`
- `toxicity_type`, `toxicity_value`, `toxicity_units`, `dose`
- `symptoms`, `assay_organism`, `assay_method`
- `ref_id`, `ref_id_type`

**索引**：
- `natural_product_id`, `toxicity_type`, `ref_id`

---

### 5. bio_resources（生物资源表）

**用途**：存储植物/动物/微生物/矿物等来源信息，包含 CMAUP 分类学补充。

**核心字段**（节选）：
- 标识：`resource_id`, `resource_type`
- 名称：`chinese_name`, `latin_name`, `english_name`, `pinyin_name`, `alias`
- 分类：`taxonomy_kingdom`/`phylum`/`class`/`order`/`family`/`genus`/`species`, `taxonomy_id`
- **CMAUP 补充字段**：
  - `species_tax_id` - 种的 Taxonomy ID
  - `genus_tax_id` - 属的 Taxonomy ID
  - `family_tax_id` - 科的 Taxonomy ID
  - `cmaup_id` - CMAUP 植物 ID
- 中医属性：`tcm_property`, `tcm_flavor`, `tcm_meridian`, `tcm_toxicity`
- 功效与主治：`functions`, `indications`, `contraindications`
- 统计：`num_of_natural_products`, `num_of_prescriptions`

**索引**：
- `resource_id`, `resource_type`, `chinese_name`, `latin_name`, `pinyin_name`
- `taxonomy_family`, `taxonomy_genus`, `tcm_property`, `tcm_meridian`
- `species_tax_id`, `genus_tax_id`, `family_tax_id`, `cmaup_id` (CMAUP 补充)
- 全文索引（GIN）：`chinese_name`, `latin_name`, `functions`

---

### 6. bio_resource_natural_products（生物资源-天然产物关联表）

**用途**：记录某个生物资源包含的天然产物。

**核心字段**：
- `bio_resource_id`, `natural_product_id`
- 含量：`content_value`, `content_unit`, `content_part`
- 来源：`isolation_method`, `ref_id`, `ref_id_type`

**约束**：
- 唯一约束：`(bio_resource_id, natural_product_id)`

---

### 7. prescriptions（处方/方剂表）

**用途**：存储中医方剂/处方信息，包含 TCMID 补充数据。

**核心字段**（节选）：
- 标识：`prescription_id`
- 名称：`chinese_name`, `pinyin_name`, `english_name`, `alias`
- 分类：`category`, `subcategory`
- 功效/主治：`functions`, `indications`, `indications_modern`, `syndrome`
- **TCMID 补充字段**：
  - `tcmid_id` - TCMID 处方 ID
  - `disease_icd11_category` - ICD-11 疾病分类
  - `human_tissues` - 人体组织
  - `reference` - 参考文献
  - `reference_book` - 参考书籍
- 组成/用法：`composition_text`, `dosage_form`, `usage_method`, `dosage`
- 统计：`num_of_herbs`, `num_of_natural_products`

---

### 8. prescription_resources（处方-生物资源关联表）

**用途**：处方组成药材关系。

**核心字段**：
- `prescription_id`, `bio_resource_id`
- 用量：`dosage_value`, `dosage_unit`, `dosage_text`
- 角色：`role`, `role_chinese`
- 炮制：`processing_method`, `processing_note`
- **TCMID 补充字段**：
  - `component_id` - 成分 ID
  - `barcode` - 条码
- `sort_order`

---

### 9. prescription_natural_products（处方-天然产物关联表）

**用途**：处方直接关联天然产物（可选路径）。

**核心字段**：
- `prescription_id`, `natural_product_id`
- `source_resource_id`（可选）

---

### 10. diseases（疾病表，新增）

**用途**：存储 ICD-11 疾病分类信息（CMAUP 数据）。

**核心字段**：
- 标识：`disease_id`（如 DIS0001）
- ICD-11 分类：`icd11_code`, `disease_category`
- 名称：`disease_name`, `disease_name_zh`
- 描述：`description`, `symptoms`
- 统计：`num_of_related_plants`, `num_of_related_targets`

**索引**：
- `disease_id`, `icd11_code`, `disease_category`
- 全文索引（GIN）：`disease_name`

**数据统计**：
- 总记录数：1,351
- 有植物关联：1,323 (97.93%)
- 有靶点关联：472 (34.9%)

---

### 11. bio_resource_disease_associations（生物资源-疾病关联表，新增）

**用途**：记录生物资源与疾病的关联及证据（CMAUP 数据）。

**核心字段**：
- 关联：`bio_resource_id`, `disease_id`
- 证据类型：
  - `evidence_therapeutic_target` - 治疗靶点证据
  - `evidence_transcriptome` - 转录组证据
  - `evidence_clinical_trial_plant` - 植物临床试验
  - `evidence_clinical_trial_ingredient` - 成分临床试验
- 置信度：`confidence_score` (0-1)
- 来源：`source` (CMAUP), `source_version`

**约束**：
- 唯一约束：`(bio_resource_id, disease_id)`

**数据统计**：
- 总记录数：565,751
- 涉及生物资源：4,741
- 涉及疾病：1,323

**证据类型分布**：
- 治疗靶点：318,705 (56.3%)
- 转录组：155,615 (27.5%)
- 成分临床试验：121,906 (21.5%)
- 植物临床试验：640 (0.1%)

**置信度分布**：
- 1.0: 5 (<0.01%)
- 0.8: 585 (0.1%)
- 0.6: 24,935 (4.4%)
- 0.5: 4,993 (0.9%)
- 0.3: 385,008 (68.1%)
- 0.2: 150,224 (26.5%)

---

## 🔍 视图说明

### v_natural_product_detail
基于 `natural_products` 聚合统计字段：
- `bioactivity_count`, `target_count`, `bio_resource_count`, `best_activity_value`, `has_toxicity`

### v_bio_resource_detail
基于 `bio_resources` 聚合统计字段：
- `natural_product_count`, `prescription_count`

### v_target_detail
基于 `targets` 聚合统计字段：
- `natural_product_count`, `bioactivity_count`, `best_activity_value`

### v_prescription_detail
基于 `prescriptions` 聚合统计字段：
- `herb_count`, `direct_natural_product_count`

---

## 🧩 触发器与时间戳

- `update_natural_products_updated_at`：更新 `natural_products.updated_at`
- `update_targets_updated_at`：更新 `targets.updated_at`
- `update_bio_resources_updated_at`：更新 `bio_resources.updated_at`
- `update_prescriptions_updated_at`：更新 `prescriptions.updated_at`
- `update_diseases_updated_at`：更新 `diseases.updated_at`

---

## 🎯 常用查询示例

### 1) 天然产物列表（筛选 + 排序）
```sql
SELECT
  np.id, np.np_id, np.pref_name, np.molecular_weight, np.xlogp, np.psa,
  np.num_of_activity, np.num_of_target
FROM natural_products np
WHERE np.molecular_weight BETWEEN 200 AND 500
  AND np.xlogp BETWEEN -2 AND 5
  AND np.num_of_activity > 0
ORDER BY np.num_of_activity DESC
LIMIT 20 OFFSET 0;
```

### 2) 天然产物详情（含活性/来源/毒性）
```sql
-- 基本信息
SELECT * FROM natural_products WHERE np_id = 'NPC491451';

-- 活性记录
SELECT b.activity_type, b.activity_value, b.activity_units,
       b.activity_value_std, t.target_name, t.target_type, b.ref_id
FROM bioactivity b
JOIN targets t ON b.target_id = t.id
WHERE b.natural_product_id = (SELECT id FROM natural_products WHERE np_id = 'NPC491451')
ORDER BY b.activity_value_std;

-- 来源生物资源
SELECT br.chinese_name, br.latin_name, br.taxonomy_family
FROM bio_resource_natural_products brnp
JOIN bio_resources br ON brnp.bio_resource_id = br.id
WHERE brnp.natural_product_id = (SELECT id FROM natural_products WHERE np_id = 'NPC491451');

-- 毒性信息
SELECT * FROM toxicity
WHERE natural_product_id = (SELECT id FROM natural_products WHERE np_id = 'NPC491451');
```

### 3) 全文搜索（PostgreSQL）
```sql
SELECT * FROM natural_products
WHERE to_tsvector('english', COALESCE(pref_name, '') || ' ' || COALESCE(iupac_name, ''))
      @@ to_tsquery('english', 'curcumin');
```

### 4) 疾病-植物关联查询
```sql
SELECT
  d.disease_name, d.icd11_code,
  br.chinese_name, br.latin_name,
  brda.evidence_therapeutic_target,
  brda.confidence_score
FROM bio_resource_disease_associations brda
JOIN diseases d ON brda.disease_id = d.id
JOIN bio_resources br ON brda.bio_resource_id = br.id
WHERE d.disease_name = 'Type 2 Diabetes'
ORDER BY brda.confidence_score DESC
LIMIT 20;
```

### 5) 处方药材组成查询
```sql
SELECT
  p.chinese_name as prescription_name,
  pr.dosage_value, pr.dosage_unit,
  br.chinese_name as herb_name,
  br.latin_name as herb_latin_name
FROM prescription_resources pr
JOIN prescriptions p ON pr.prescription_id = p.id
JOIN bio_resources br ON pr.bio_resource_id = br.id
WHERE p.prescription_id = 'TCMPRE0001'
ORDER BY pr.sort_order;
```

---

## 🔧 维护任务

### 1) 更新统计字段（示例）
```sql
-- 更新天然产物统计
UPDATE natural_products np SET
  num_of_activity = (SELECT COUNT(*) FROM bioactivity WHERE natural_product_id = np.id),
  num_of_target = (SELECT COUNT(DISTINCT target_id) FROM bioactivity WHERE natural_product_id = np.id),
  num_of_organism = (SELECT COUNT(*) FROM bio_resource_natural_products WHERE natural_product_id = np.id);

-- 更新靶点统计
UPDATE targets t SET
  num_of_natural_products = (SELECT COUNT(DISTINCT natural_product_id) FROM bioactivity WHERE target_id = t.id),
  num_of_activities = (SELECT COUNT(*) FROM bioactivity WHERE target_id = t.id);

-- 更新生物资源统计
UPDATE bio_resources br SET
  num_of_natural_products = (SELECT COUNT(*) FROM bio_resource_natural_products WHERE bio_resource_id = br.id),
  num_of_prescriptions = (SELECT COUNT(*) FROM prescription_resources WHERE bio_resource_id = br.id);

-- 更新处方统计
UPDATE prescriptions p SET
  num_of_herbs = (SELECT COUNT(*) FROM prescription_resources WHERE prescription_id = p.id),
  num_of_natural_products = (SELECT COUNT(*) FROM prescription_natural_products WHERE prescription_id = p.id);

-- 更新疾病统计
UPDATE diseases d SET
  num_of_related_plants = (SELECT COUNT(DISTINCT bio_resource_id) FROM bio_resource_disease_associations WHERE disease_id = d.id);
```

---

## 📝 数据质量验证

### 验证结果（2026-01-29）

**数据完整性评分**: 96/100

**外键完整性**:
- ✅ 所有外键引用都有效，没有发现孤立记录

**匹配率统计**:
- TTD 靶点匹配: 34.74% (一般)
- TCMID 药材匹配: 5.55% (一般)
- CMAUP 植物匹配: 21.03% (一般)
- 疾病关联匹配: 97.93% (优秀)

**数据质量**:
- ⚠️ 发现 1 条记录缺失 target_name
- ⚠️ 发现 5 条记录的 UniProt ID 格式可能异常
- ✅ 其他检查全部通过

### 改进建议

1. 优化匹配算法以提高匹配率
2. 修复发现的数据质量问题
3. 分析未匹配数据原因
4. 建立数据质量监控系统

---

## 📝 版本历史

### v2.0 (2026-01-29)

- 新增 `diseases` 表
- 新增 `bio_resource_disease_associations` 表
- 新增 TTD 靶点补充字段
- 新增 TCMID 处方补充字段
- 新增 CMAUP 植物补充字段
- 新增疾病关联功能
- 数据完整性验证
- 更新文档

### v1.0 (2025-01-XX)

- 初始版本
- 基础表结构
- 优化脚本执行（compounds → natural_products）

---

## 📋 备注

- **业务 ID**：`np_id` / `target_id` / `resource_id` / `prescription_id` / `disease_id` 用于对外展示；`id` 为内部主键。
- **数据补充**：包含 TTD、TCMID、CMAUP 三个数据源的补充数据。
- **命名规范**：使用 `natural_products` 而非 `compounds`，`bio_resource_natural_products` 而非 `bio_resource_compounds`。
- **外键约束**：所有关联表都有外键约束，确保数据完整性。
- **全文搜索**：使用 PostgreSQL GIN 索引支持中文、英文全文搜索。
- **触发器**：自动更新时间戳字段。

---

**文档版本**: v2.0  
**最后更新**: 2026-01-29  
**数据库版本**: PostgreSQL 16  
**数据来源**: NPASS 3.0 + TTD + TCMID + CMAUP  
**维护者**: NPdatabase Team
