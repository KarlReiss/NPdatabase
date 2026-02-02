# 天然产物数据库 Schema 完整文档

> 版本: v2.0 (含数据补充)
> 更新时间: 2026-01-29
> 数据库: PostgreSQL 16

---

## 📊 数据库概览

### 表统计

| 表名 | 记录数 (预估) | 说明 |
|------|---------------|------|
| natural_products | ~500,000 | 天然产物核心表 |
| targets | ~12,368 | 靶点表 |
| bioactivity | ~1,000,000 | 生物活性记录 |
| toxicity | ~50,000 | 毒性数据 |
| bio_resources | ~27,000 | 生物资源/药材 |
| bio_resource_natural_products | ~1,500,000 | 生物资源-天然产物关联 |
| prescriptions | ~2,100 | 处方表 |
| prescription_resources | ~14,800 | 处方-药材关联 |
| prescription_natural_products | 0 | 处方-天然产物关联 |
| diseases | ~1,351 | 疾病表 |
| bio_resource_disease_associations | ~565,751 | 生物资源-疾病关联 |
| sys_dict | N/A | 系统字典 |
| sys_menu | N/A | 系统菜单 |

**总计**: 14 张数据表

---

## 🗂️ 表结构详解

### 1. natural_products (天然产物表)

存储天然产物基本信息与理化性质。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY | 内部主键 |
| np_id | VARCHAR(50) | NOT NULL, UNIQUE | 业务ID (如 NPC491451) |
| inchikey | VARCHAR(100) | | InChIKey |
| pref_name | TEXT | | 优选名称 |
| iupac_name | TEXT | | IUPAC名称 |
| name_initial | VARCHAR(10) | | 名称首字母 |
| inchi | TEXT | | InChI字符串 |
| smiles | TEXT | | SMILES字符串 |
| chembl_id | VARCHAR(50) | | ChEMBL ID |
| pubchem_id | VARCHAR(50) | | PubChem ID |
| molecular_weight | NUMERIC(10,2) | CHECK(>0) | 分子量 |
| xlogp | NUMERIC(10,2) | | XLogP (脂溶性) |
| psa | NUMERIC(10,2) | | 极性表面积 |
| formula | VARCHAR(200) | | 分子式 |
| h_bond_donors | INTEGER | | 氢键供体数 |
| h_bond_acceptors | INTEGER | | 氢键受体数 |
| rotatable_bonds | INTEGER | | 可旋转键数 |
| num_of_organism | INTEGER | DEFAULT 0 | 相关生物资源数 |
| num_of_target | INTEGER | DEFAULT 0 | 相关靶点数 |
| num_of_activity | INTEGER | DEFAULT 0 | 活性记录数 |
| gene_cluster | TEXT | | 基因簇 |
| if_quantity | BOOLEAN | DEFAULT FALSE | 是否量化 |
| created_at | TIMESTAMP | | 创建时间 |
| updated_at | TIMESTAMP | | 更新时间 |

**索引**:
- PRIMARY KEY: id
- UNIQUE: np_id
- idx_natural_products_np_id: np_id
- idx_natural_products_inchikey: inchikey
- idx_natural_products_pref_name: pref_name
- idx_natural_products_chembl_id: chembl_id
- idx_natural_products_pubchem_id: pubchem_id
- idx_natural_products_mw: molecular_weight
- idx_natural_products_xlogp: xlogp
- idx_natural_products_psa: psa
- idx_natural_products_num_activity: num_of_activity
- idx_natural_products_num_target: num_of_target
- idx_natural_products_pref_name_gin: GIN全文索引 (pref_name)
- idx_natural_products_iupac_name_gin: GIN全文索引 (iupac_name)

**外键引用**:
- bioactivity.natural_product_id
- bio_resource_natural_products.natural_product_id
- prescription_natural_products.natural_product_id
- toxicity.natural_product_id

---

### 2. targets (靶点表)

存储蛋白/细胞系/基因等靶点信息。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY | 内部主键 |
| target_id | VARCHAR(50) | NOT NULL, UNIQUE | 业务ID (如 NPT918) |
| target_type | VARCHAR(200) | | 靶点类型 (Cell line, Protein, Gene, Enzyme) |
| target_name | VARCHAR(500) | | 靶点名称 |
| target_organism | VARCHAR(200) | | 生物物种 |
| target_organism_tax_id | VARCHAR(100) | | 物种Taxonomy ID |
| uniprot_id | VARCHAR(300) | | UniProt ID |
| gene_name | VARCHAR(100) | | 基因名 (TTD补充) |
| synonyms | TEXT | | 同义词 (TTD补充) |
| function | TEXT | | 功能描述 (TTD补充) |
| pdb_structure | VARCHAR(500) | | PDB结构ID (TTD补充) |
| bioclass | VARCHAR(200) | | 生物分类 (TTD补充) |
| ec_number | VARCHAR(50) | | EC编号 (TTD补充) |
| sequence | TEXT | | 蛋白序列 (TTD补充) |
| ttd_id | VARCHAR(50) | | TTD ID (TTD补充) |
| num_of_compounds | INTEGER | DEFAULT 0 | 相关化合物数 (旧字段) |
| num_of_activities | INTEGER | DEFAULT 0 | 相关活性数 |
| num_of_natural_products | INTEGER | DEFAULT 0 | 相关天然产物数 (新字段) |
| created_at | TIMESTAMP | | 创建时间 |
| updated_at | TIMESTAMP | | 更新时间 |

**索引**:
- PRIMARY KEY: id
- UNIQUE: target_id
- idx_targets_target_id: target_id
- idx_targets_target_name: target_name
- idx_targets_type: target_type
- idx_targets_organism: target_organism
- idx_targets_uniprot: uniprot_id
- idx_targets_gene_name: gene_name (TTD补充)
- idx_targets_ttd_id: ttd_id (TTD补充)
- idx_targets_ec_number: ec_number (TTD补充)
- idx_targets_name_gin: GIN全文索引 (target_name)
- idx_targets_function_gin: GIN全文索引 (function)
- idx_targets_synonyms_gin: GIN全文索引 (synonyms)

**外键引用**:
- bioactivity.target_id

---

### 3. bioactivity (活性记录表)

存储天然产物-靶点活性记录。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY | 内部主键 |
| natural_product_id | BIGINT | NOT NULL, FK | 天然产物ID |
| target_id | BIGINT | NOT NULL, FK | 靶点ID |
| activity_type | VARCHAR(100) | | 活性类型 (IC50, EC50, Ki) |
| activity_type_grouped | VARCHAR(50) | | 分组活性类型 |
| activity_relation | VARCHAR(50) | | 活性关系 (>, <, =, ≈) |
| activity_value | NUMERIC(15,3) | | 活性值 (原始单位) |
| activity_units | VARCHAR(50) | | 活性单位 (M, mM, μM, nM, pM) |
| activity_value_std | NUMERIC(15,3) | | 活性值 (标准化为nM) |
| activity_units_std | VARCHAR(50) | DEFAULT 'nM' | 活性单位 (标准为nM) |
| assay_organism | VARCHAR(200) | | 实验生物 |
| assay_tax_id | VARCHAR(100) | | 实验物种Taxonomy ID |
| assay_strain | VARCHAR(200) | | 实验菌株 |
| assay_tissue | VARCHAR(200) | | 实验组织 |
| assay_cell_type | VARCHAR(200) | | 实验细胞类型 |
| ref_id | VARCHAR(200) | | 文献ID |
| ref_id_type | VARCHAR(50) | | 文献类型 (PMID, DOI, Patent) |
| created_at | TIMESTAMP | | 创建时间 |

**索引**:
- PRIMARY KEY: id
- idx_bioactivity_natural_product_id: natural_product_id
- idx_bioactivity_target_id: target_id
- idx_bioactivity_activity_type: activity_type
- idx_bioactivity_activity_type_grouped: activity_type_grouped
- idx_bioactivity_activity_value_std: activity_value_std
- idx_bioactivity_activity_relation: activity_relation
- idx_bioactivity_ref_id: ref_id

**外键**:
- fk_bioactivity_natural_product: natural_product_id → natural_products(id)
- fk_bioactivity_target: target_id → targets(id)

---

### 4. toxicity (毒性表)

存储天然产物毒性数据。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY | 内部主键 |
| natural_product_id | BIGINT | NOT NULL, FK | 天然产物ID |
| toxicity_type | VARCHAR(100) | | 毒性类型 |
| toxicity_value | NUMERIC(15,3) | | 毒性值 |
| toxicity_units | VARCHAR(50) | | 毒性单位 |
| dose | VARCHAR(200) | | 剂量 |
| symptoms | TEXT | | 症状 |
| assay_organism | VARCHAR(200) | | 实验生物 |
| assay_method | VARCHAR(200) | | 实验方法 |
| ref_id | VARCHAR(200) | | 文献ID |
| ref_id_type | VARCHAR(50) | | 文献类型 |
| created_at | TIMESTAMP | | 创建时间 |

**索引**:
- PRIMARY KEY: id
- idx_toxicity_natural_product_id: natural_product_id
- idx_toxicity_toxicity_type: toxicity_type
- idx_toxicity_ref_id: ref_id

**外键**:
- fk_toxicity_natural_product: natural_product_id → natural_products(id)

---

### 5. bio_resources (生物资源表)

存储植物/动物/微生物/矿物等来源信息。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY | 内部主键 |
| resource_id | VARCHAR(50) | NOT NULL, UNIQUE | 业务ID |
| resource_type | VARCHAR(50) | NOT NULL | 资源类型 (Plant, Animal, Microbe, Mineral) |
| chinese_name | VARCHAR(500) | | 中文名 |
| latin_name | VARCHAR(500) | | 拉丁名 |
| english_name | VARCHAR(500) | | 英文名 |
| pinyin_name | VARCHAR(200) | | 拼音名 |
| alias | TEXT | | 别名 |
| taxonomy_kingdom | VARCHAR(100) | | 界 |
| taxonomy_phylum | VARCHAR(100) | | 门 |
| taxonomy_class | VARCHAR(100) | | 纲 |
| taxonomy_order | VARCHAR(100) | | 目 |
| taxonomy_family | VARCHAR(200) | | 科 |
| taxonomy_genus | VARCHAR(200) | | 属 |
| taxonomy_species | VARCHAR(200) | | 种 |
| taxonomy_id | VARCHAR(50) | | Taxonomy ID |
| species_tax_id | VARCHAR(50) | | 种Taxonomy ID (CMAUP补充) |
| genus_tax_id | VARCHAR(50) | | 属Taxonomy ID (CMAUP补充) |
| family_tax_id | VARCHAR(50) | | 科Taxonomy ID (CMAUP补充) |
| cmaup_id | VARCHAR(50) | | CMAUP ID (CMAUP补充) |
| medicinal_part | VARCHAR(200) | | 药用部位 |
| medicinal_part_latin | VARCHAR(200) | | 药用部位拉丁名 |
| origin_region | TEXT | | 产地 |
| distribution | TEXT | | 分布 |
| habitat | TEXT | | 生境 |
| tcm_property | VARCHAR(100) | | 中药性味 |
| tcm_flavor | VARCHAR(100) | | 中药性味 |
| tcm_meridian | VARCHAR(200) | | 中药归经 |
| tcm_toxicity | VARCHAR(50) | | 中药毒性 |
| functions | TEXT | | 功效 |
| indications | TEXT | | 主治 |
| contraindications | TEXT | | 禁忌 |
| mineral_composition | VARCHAR(500) | | 矿物成分 |
| mineral_crystal_system | VARCHAR(100) | | 矿物晶系 |
| mineral_hardness | VARCHAR(50) | | 矿物硬度 |
| mineral_color | VARCHAR(100) | | 矿物颜色 |
| microbe_strain | VARCHAR(200) | | 微生物菌株 |
| microbe_culture_condition | TEXT | | 微生物培养条件 |
| microbe_fermentation_product | TEXT | | 微生物发酵产物 |
| animal_class | VARCHAR(100) | | 动物分类 |
| animal_conservation_status | VARCHAR(50) | | 动物保护状态 |
| tcmid_id | VARCHAR(50) | | TCMID ID (TCMID补充) |
| tcmsp_id | VARCHAR(50) | | TCMSP ID |
| herb_id | VARCHAR(50) | | 草药ID |
| pharmacopoeia_ref | VARCHAR(200) | | 药典参考 |
| literature_ref | TEXT | | 文献参考 |
| image_url | TEXT | | 图片URL |
| num_of_natural_products | INTEGER | DEFAULT 0 | 天然产物数 |
| num_of_prescriptions | INTEGER | DEFAULT 0 | 相关处方数 |
| created_at | TIMESTAMP | | 创建时间 |
| updated_at | TIMESTAMP | | 更新时间 |

**索引**:
- PRIMARY KEY: id
- UNIQUE: resource_id
- idx_bio_resources_resource_id: resource_id
- idx_bio_resources_type: resource_type
- idx_bio_resources_chinese_name: chinese_name
- idx_bio_resources_latin_name: latin_name
- idx_bio_resources_pinyin: pinyin_name
- idx_bio_resources_family: taxonomy_family
- idx_bio_resources_genus: taxonomy_genus
- idx_bio_resources_tcm_property: tcm_property
- idx_bio_resources_tcm_meridian: tcm_meridian
- idx_bio_resources_species_tax_id: species_tax_id (CMAUP补充)
- idx_bio_resources_genus_tax_id: genus_tax_id (CMAUP补充)
- idx_bio_resources_family_tax_id: family_tax_id (CMAUP补充)
- idx_bio_resources_cmaup_id: cmaup_id (CMAUP补充)
- idx_bio_resources_chinese_gin: GIN全文索引 (chinese_name)
- idx_bio_resources_latin_gin: GIN全文索引 (latin_name)
- idx_bio_resources_functions_gin: GIN全文索引 (functions)

**外键引用**:
- bio_resource_natural_products.bio_resource_id
- bio_resource_disease_associations.bio_resource_id
- prescription_resources.bio_resource_id
- prescription_natural_products.source_resource_id

---

### 6. bio_resource_natural_products (生物资源-天然产物关联表)

记录生物资源包含的天然产物。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY | 内部主键 |
| bio_resource_id | BIGINT | NOT NULL, FK | 生物资源ID |
| natural_product_id | BIGINT | NOT NULL, FK | 天然产物ID |
| content_value | NUMERIC(15,3) | | 含量值 |
| content_unit | VARCHAR(50) | | 含量单位 |
| content_part | VARCHAR(200) | | 含量部位 |
| isolation_method | TEXT | | 分离方法 |
| ref_id | VARCHAR(200) | | 文献ID |
| ref_id_type | VARCHAR(50) | | 文献类型 |
| created_at | TIMESTAMP | | 创建时间 |

**约束**:
- UNIQUE: (bio_resource_id, natural_product_id)

**索引**:
- PRIMARY KEY: id
- UNIQUE: uk_bio_resource_natural_product
- idx_brnp_bio_resource_id: bio_resource_id
- idx_brnp_natural_product_id: natural_product_id

**外键**:
- fk_brnp_bio_resource: bio_resource_id → bio_resources(id)
- fk_brnp_natural_product: natural_product_id → natural_products(id)

---

### 7. prescriptions (处方/方剂表)

存储中医方剂/处方信息。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY | 内部主键 |
| prescription_id | VARCHAR(50) | NOT NULL, UNIQUE | 业务ID |
| chinese_name | VARCHAR(500) | | 中文名 |
| pinyin_name | VARCHAR(200) | | 拼音名 |
| english_name | VARCHAR(500) | | 英文名 |
| alias | TEXT | | 别名 |
| source_book | VARCHAR(200) | | 来源书籍 |
| source_dynasty | VARCHAR(100) | | 来源朝代 |
| source_author | VARCHAR(100) | | 作者 |
| category | VARCHAR(100) | | 分类 |
| subcategory | VARCHAR(100) | | 子分类 |
| functions | TEXT | | 功效 |
| indications | TEXT | | 主治 |
| indications_modern | TEXT | | 现代主治 |
| syndrome | VARCHAR(500) | | 证型 |
| composition_text | TEXT | | 组成文本 |
| dosage_form | VARCHAR(100) | | 剂型 |
| preparation_method | TEXT | | 制备方法 |
| usage_method | TEXT | | 用法 |
| dosage | TEXT | | 用量 |
| contraindications | TEXT | | 禁忌 |
| precautions | TEXT | | 注意事项 |
| adverse_reactions | TEXT | | 不良反应 |
| pharmacology | TEXT | | 药理 |
| clinical_application | TEXT | | 临床应用 |
| target_tissues | TEXT | | 靶向组织 |
| related_diseases | TEXT | | 相关疾病 |
| tcmid_id | VARCHAR(50) | | TCMID ID (TCMID补充) |
| tcmsp_id | VARCHAR(50) | | TCMSP ID |
| symmap_id | VARCHAR(50) | | SymMap ID |
| disease_icd11_category | TEXT | | ICD-11疾病分类 (TCMID补充) |
| human_tissues | TEXT | | 人体组织 (TCMID补充) |
| reference | TEXT | | 参考文献 (TCMID补充) |
| reference_book | TEXT | | 参考书籍 (TCMID补充) |
| pharmacopoeia_ref | VARCHAR(200) | | 药典参考 |
| literature_ref | TEXT | | 文献参考 |
| num_of_herbs | INTEGER | DEFAULT 0 | 药材数 |
| num_of_natural_products | INTEGER | DEFAULT 0 | 天然产物数 |
| created_at | TIMESTAMP | | 创建时间 |
| updated_at | TIMESTAMP | | 更新时间 |

**索引**:
- PRIMARY KEY: id
- UNIQUE: prescription_id
- idx_prescriptions_prescription_id: prescription_id
- idx_prescriptions_chinese_name: chinese_name
- idx_prescriptions_pinyin: pinyin_name
- idx_prescriptions_category: category
- idx_prescriptions_dosage_form: dosage_form
- idx_prescriptions_source_book: source_book
- idx_prescriptions_chinese_gin: GIN全文索引 (chinese_name)
- idx_prescriptions_functions_gin: GIN全文索引 (functions)
- idx_prescriptions_indications_gin: GIN全文索引 (indications)
- idx_prescriptions_icd11_gin: GIN全文索引 (disease_icd11_category)

**外键引用**:
- prescription_resources.prescription_id
- prescription_natural_products.prescription_id

---

### 8. prescription_resources (处方-生物资源关联表)

处方组成药材关系。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY | 内部主键 |
| prescription_id | BIGINT | NOT NULL, FK | 处方ID |
| bio_resource_id | BIGINT | NOT NULL, FK | 生物资源ID |
| dosage_value | NUMERIC(15,3) | | 用量值 |
| dosage_unit | VARCHAR(50) | | 用量单位 |
| dosage_text | TEXT | | 用量文本 |
| role | VARCHAR(200) | | 角色 (君、臣、佐、使) |
| role_chinese | VARCHAR(50) | | 角色中文 |
| processing_method | TEXT | | 炮制方法 |
| processing_note | TEXT | | 炮制说明 |
| component_id | VARCHAR(50) | | 成分ID (TCMID补充) |
| barcode | VARCHAR(50) | | 条码 (TCMID补充) |
| sort_order | INTEGER | | 排序 |
| created_at | TIMESTAMP | | 创建时间 |

**索引**:
- PRIMARY KEY: id
- idx_pr_prescription_id: prescription_id
- idx_pr_bio_resource_id: bio_resource_id

**外键**:
- fk_pr_prescription: prescription_id → prescriptions(id)
- fk_pr_bio_resource: bio_resource_id → bio_resources(id)

---

### 9. prescription_natural_products (处方-天然产物关联表)

处方直接关联天然产物（可选路径）。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY | 内部主键 |
| prescription_id | BIGINT | NOT NULL, FK | 处方ID |
| natural_product_id | BIGINT | NOT NULL, FK | 天然产物ID |
| source_resource_id | BIGINT | FK | 来源生物资源ID (可选) |
| created_at | TIMESTAMP | | 创建时间 |

**索引**:
- PRIMARY KEY: id
- idx_pnp_prescription_id: prescription_id
- idx_pnp_natural_product_id: natural_product_id
- idx_pnp_source_resource_id: source_resource_id

**外键**:
- fk_pnp_prescription: prescription_id → prescriptions(id)
- fk_pnp_natural_product: natural_product_id → natural_products(id)
- fk_pnp_source_resource: source_resource_id → bio_resources(id) ON DELETE SET NULL

---

### 10. diseases (疾病表)

存储ICD-11疾病分类信息（CMAUP补充）。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY | 内部主键 |
| disease_id | VARCHAR(50) | NOT NULL, UNIQUE | 业务ID (如 DIS0001) |
| icd11_code | VARCHAR(50) | NOT NULL | ICD-11编码 |
| disease_name | VARCHAR(500) | NOT NULL | 疾病名称 (英文) |
| disease_name_zh | VARCHAR(500) | | 疾病名称 (中文) |
| disease_category | VARCHAR(200) | | 疾病分类 |
| description | TEXT | | 疾病描述 |
| symptoms | TEXT | | 症状 |
| num_of_related_plants | INTEGER | DEFAULT 0 | 关联植物数 |
| num_of_related_targets | INTEGER | DEFAULT 0 | 关联靶点数 |
| created_at | TIMESTAMP | | 创建时间 |
| updated_at | TIMESTAMP | | 更新时间 |

**索引**:
- PRIMARY KEY: id
- UNIQUE: disease_id
- idx_diseases_disease_id: disease_id
- idx_diseases_icd11_code: icd11_code
- idx_diseases_category: disease_category
- idx_diseases_name_gin: GIN全文索引 (disease_name)

**外键引用**:
- bio_resource_disease_associations.disease_id

---

### 11. bio_resource_disease_associations (生物资源-疾病关联表)

记录生物资源与疾病的关联及证据（CMAUP补充）。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY | 内部主键 |
| bio_resource_id | BIGINT | NOT NULL, FK | 生物资源ID |
| disease_id | BIGINT | NOT NULL, FK | 疾病ID |
| evidence_therapeutic_target | TEXT | | 治疗靶点证据 |
| evidence_transcriptome | BOOLEAN | DEFAULT FALSE | 转录组证据 |
| evidence_clinical_trial_plant | TEXT | | 植物临床试验 |
| evidence_clinical_trial_ingredient | TEXT | | 成分临床试验 |
| confidence_score | NUMERIC(3,2) | | 置信度评分 (0-1) |
| source | VARCHAR(100) | DEFAULT 'CMAUP' | 数据来源 |
| source_version | VARCHAR(50) | | 数据版本 |
| created_at | TIMESTAMP | | 创建时间 |

**约束**:
- UNIQUE: (bio_resource_id, disease_id)

**索引**:
- PRIMARY KEY: id
- UNIQUE: uk_bio_resource_disease
- idx_brda_bio_resource: bio_resource_id
- idx_brda_disease: disease_id
- idx_brda_confidence: confidence_score

**外键**:
- fk_brda_bio_resource: bio_resource_id → bio_resources(id)
- fk_brda_disease: disease_id → diseases(id)

---

### 12. sys_dict (系统字典表)

系统字典配置。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY | 内部主键 |
| dict_code | VARCHAR(100) | NOT NULL | 字典编码 |
| dict_name | VARCHAR(200) | | 字典名称 |
| dict_value | TEXT | | 字典值 |
| dict_type | VARCHAR(50) | | 字典类型 |
| sort_order | INTEGER | | 排序 |
| status | VARCHAR(20) | | 状态 |
| created_at | TIMESTAMP | | 创建时间 |

---

### 13. sys_menu (系统菜单表)

系统菜单配置。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY | 内部主键 |
| menu_name | VARCHAR(100) | NOT NULL | 菜单名称 |
| menu_code | VARCHAR(100) | NOT NULL | 菜单编码 |
| parent_id | BIGINT | | 父菜单ID |
| menu_url | VARCHAR(200) | | 菜单URL |
| menu_icon | VARCHAR(100) | | 菜单图标 |
| sort_order | INTEGER | | 排序 |
| status | VARCHAR(20) | | 状态 |
| created_at | TIMESTAMP | | 创建时间 |

---

## 🔗 实体关系图 (ERD)

```
┌─────────────────┐
│ natural_products│
└───────┬─────────┘
        │
        ├───────────┬──────────────────┐
        │           │                  │
        ▼           ▼                  ▼
┌─────────────┐ ┌───────────┐   ┌──────────────┐
│ bioactivity │ │ toxicity  │   │ bio_resource_│
└───────┬─────┘ └───────────┘   │_natural_products│
        │                         └───────┬───────┘
        ▼                                 │
┌───────────┐                             │
│ targets   │                             │
└───────────┘                             │
                                         │
┌─────────────┐                            │
│bio_resources│◄───────────────────────────┘
└──────┬──────┘
       │
       ├──────────┬─────────────┐
       │          │             │
       ▼          ▼             ▼
┌──────────────┐ ┌─────────────┐ ┌──────────────────────────┐
│prescription_│ │ bio_resource│ │prescription_natural_   │
│_resources   │ │_disease_   │ │products               │
└──────┬───────┘ │associations │ └───────────┬──────────┘
       │         └──────┬─────┘             │
       │                │                    │
       ▼                ▼                    │
┌───────────┐    ┌──────────┐              │
│prescriptions│    │ diseases │              │
└───────────┘    └──────────┘              │
                                             │
                                             │
                                        ┌────┴────┐
                                        │natural_ │
                                        │products │
                                        └─────────┘
```

---

## 🔍 视图说明

### v_natural_product_detail

天然产物详情视图，包含统计信息。

```sql
CREATE VIEW v_natural_product_detail AS
SELECT 
    np.id,
    np.np_id,
    np.pref_name,
    np.molecular_weight,
    np.xlogp,
    np.psa,
    np.num_of_activity,
    np.num_of_target,
    np.num_of_organism,
    (SELECT COUNT(*) FROM bioactivity b WHERE b.natural_product_id = np.id) as bioactivity_count,
    (SELECT COUNT(DISTINCT b.target_id) FROM bioactivity b WHERE b.natural_product_id = np.id) as target_count,
    (SELECT COUNT(*) FROM bio_resource_natural_products brnp WHERE brnp.natural_product_id = np.id) as bio_resource_count,
    (SELECT MIN(b.activity_value_std) FROM bioactivity b WHERE b.natural_product_id = np.id AND b.activity_value_std > 0) as best_activity_value,
    (SELECT COUNT(*) > 0 FROM toxicity t WHERE t.natural_product_id = np.id) as has_toxicity
FROM natural_products np;
```

### v_bio_resource_detail

生物资源详情视图，包含统计信息。

```sql
CREATE VIEW v_bio_resource_detail AS
SELECT 
    br.id,
    br.resource_id,
    br.resource_type,
    br.chinese_name,
    br.latin_name,
    br.taxonomy_family,
    br.taxonomy_genus,
    br.num_of_natural_products,
    br.num_of_prescriptions
FROM bio_resources br;
```

### v_target_detail

靶点详情视图，包含统计信息。

```sql
CREATE VIEW v_target_detail AS
SELECT 
    t.id,
    t.target_id,
    t.target_type,
    t.target_name,
    t.gene_name,
    t.num_of_natural_products,
    t.num_of_activities,
    (SELECT COUNT(DISTINCT b.natural_product_id) FROM bioactivity b WHERE b.target_id = t.id) as natural_product_count,
    (SELECT COUNT(*) FROM bioactivity b WHERE b.target_id = t.id) as bioactivity_count,
    (SELECT MIN(b.activity_value_std) FROM bioactivity b WHERE b.target_id = t.id AND b.activity_value_std > 0) as best_activity_value
FROM targets t;
```

### v_prescription_detail

处方详情视图，包含统计信息。

```sql
CREATE VIEW v_prescription_detail AS
SELECT 
    p.id,
    p.prescription_id,
    p.chinese_name,
    p.category,
    p.num_of_herbs,
    p.num_of_natural_products,
    (SELECT COUNT(*) FROM prescription_resources pr WHERE pr.prescription_id = p.id) as herb_count,
    (SELECT COUNT(*) FROM prescription_natural_products pnp WHERE pnp.prescription_id = p.id) as direct_natural_product_count
FROM prescriptions p;
```

---

## 🧩 触发器

### update_updated_at_column

通用触发器函数，自动更新 `updated_at` 字段。

```sql
CREATE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';
```

**触发器列表**:
- `update_natural_products_updated_at`: natural_products
- `update_targets_updated_at`: targets
- `update_bio_resources_updated_at`: bio_resources
- `update_prescriptions_updated_at`: prescriptions
- `update_diseases_updated_at`: diseases

---

## 📝 单位标准化规则

活性值单位转换规则：

| 原单位 | 转换系数 | 标准单位 |
|--------|----------|----------|
| M | ×1,000,000,000 | nM |
| mM | ×1,000,000 | nM |
| μM | ×1,000 | nM |
| nM | ×1 | nM |
| pM | ×0.001 | nM |

---

## 🎯 索引策略

### B-tree 索引

用于等值查询、范围查询、排序：
- 主键、外键、业务ID
- 分子量、XLogP、PSA等数值字段
- 创建时间、更新时间

### GIN 全文索引

用于中文、英文全文搜索：
- `natural_products.pref_name`
- `natural_products.iupac_name`
- `targets.target_name`
- `targets.function`
- `targets.synonyms`
- `bio_resources.chinese_name`
- `bio_resources.latin_name`
- `bio_resources.functions`
- `prescriptions.chinese_name`
- `prescriptions.functions`
- `prescriptions.indications`
- `prescriptions.disease_icd11_category`
- `diseases.disease_name`

---

## 📊 数据补充标记

### TTD 靶点补充 (Step 4.1)

新增字段:
- `gene_name` - 基因名
- `synonyms` - 同义词
- `function` - 功能描述
- `pdb_structure` - PDB结构ID
- `bioclass` - 生物分类
- `ec_number` - EC编号
- `sequence` - 蛋白序列
- `ttd_id` - TTD ID

### TCMID 处方补充 (Step 4.2)

新增字段:
- `tcmid_id` - TCMID ID (prescriptions)
- `component_id` - 成分ID (prescription_resources)
- `barcode` - 条码 (prescription_resources)
- `disease_icd11_category` - ICD-11疾病分类 (prescriptions)
- `human_tissues` - 人体组织 (prescriptions)
- `reference` - 参考文献 (prescriptions)
- `reference_book` - 参考书籍 (prescriptions)

### CMAUP 植物补充 (Step 4.3)

新增字段:
- `species_tax_id` - 种Taxonomy ID
- `genus_tax_id` - 属Taxonomy ID
- `family_tax_id` - 科Taxonomy ID
- `cmaup_id` - CMAUP ID

### CMAUP 疾病补充 (Step 4.4)

新增表:
- `diseases` - 疾病表
- `bio_resource_disease_associations` - 生物资源-疾病关联表

---

## 🔧 维护任务

### 更新统计字段

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

## 📋 字典表说明

### sys_dict

系统配置字典，用于存储：
- 资源类型 (Plant, Animal, Microbe, Mineral)
- 靶点类型 (Cell line, Protein, Gene, Enzyme)
- 活性类型 (IC50, EC50, Ki, Kd, etc.)
- 文献类型 (PMID, DOI, Patent)
- 中药性味、归经
- 疾病分类
- 其他系统配置

### sys_menu

系统菜单结构，用于前端导航。

---

## 🏷️ 业务ID说明

| 表 | 业务ID字段 | 说明 | 示例 |
|---|-----------|------|------|
| natural_products | np_id | 天然产物ID | NPC491451 |
| targets | target_id | 靶点ID | NPT918 |
| bio_resources | resource_id | 生物资源ID | NPO1 |
| prescriptions | prescription_id | 处方ID | PRE001 |
| diseases | disease_id | 疾病ID | DIS0001 |

**注意**: 业务ID用于对外展示，`id` 为内部主键。

---

## 🔒 数据完整性约束

### 主键约束

所有表都有自增 `id` 字段作为主键。

### 唯一约束

- `natural_products.np_id`
- `targets.target_id`
- `bio_resources.resource_id`
- `prescriptions.prescription_id`
- `diseases.disease_id`
- `bio_resource_natural_products(bio_resource_id, natural_product_id)`
- `bio_resource_disease_associations(bio_resource_id, disease_id)`

### 外键约束

所有关联表都有外键约束，确保数据完整性。

### 检查约束

- `natural_products.molecular_weight > 0` (若不为空)

---

## 📈 性能优化建议

1. **查询优化**
   - 合理使用索引
   - 避免全表扫描
   - 使用分页查询

2. **连接优化**
   - 在关联字段上建立索引
   - 使用 EXISTS 替代 JOIN (适用场景)
   - 避免多表大连接

3. **全文搜索**
   - 使用 GIN 索引
   - 使用 `@@` 操作符
   - 使用 `ts_headline` 高亮结果

4. **缓存策略**
   - 对频繁查询的数据使用 Redis 缓存
   - 设置合理的过期时间
   - 缓存穿透保护

---

## 📞 常见问题

### Q1: 为什么 natural_products 的主键序列名是 `compounds_id_seq`?

A: 这是历史遗留问题。在优化脚本中，`compounds` 表重命名为 `natural_products`，但序列名没有同步更新。不影响功能，仅序列命名不一致。

### Q2: 如何处理单位转换?

A: 活性值已统一转换为 nM 单位存储在 `activity_value_std` 字段，原始值保存在 `activity_value` 字段。建议查询时使用标准化字段。

### Q3: 全文搜索如何使用?

A: 使用 PostgreSQL 的全文搜索功能：
```sql
SELECT * FROM natural_products
WHERE to_tsvector('english', COALESCE(pref_name, '') || ' ' || COALESCE(iupac_name, ''))
      @@ to_tsquery('english', 'curcumin');
```

---

## 📝 变更历史

### v2.0 (2026-01-29)

- 新增 `diseases` 表
- 新增 `bio_resource_disease_associations` 表
- 新增 TTD 靶点补充字段 (gene_name, synonyms, function, pdb_structure, bioclass, ec_number, sequence, ttd_id)
- 新增 TCMID 处方补充字段
- 新增 CMAUP 植物补充字段 (species_tax_id, genus_tax_id, family_tax_id, cmaup_id)
- 新增疾病关联视图
- 新增全文搜索索引

### v1.0 (2025-01-XX)

- 初始版本
- 基础表结构 (natural_products, targets, bioactivity, toxicity, bio_resources, bio_resource_natural_products, prescriptions, prescription_resources, prescription_natural_products)
- 优化脚本执行 (compounds → natural_products)

---

**文档版本**: v2.0  
**最后更新**: 2026-01-29  
**维护者**: NPdatabase Team
