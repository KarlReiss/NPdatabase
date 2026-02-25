# Natural Product Database - 数据字典

## 文档信息

| 项目 | 内容 |
|------|------|
| 数据库名称 | npdb |
| 数据库类型 | PostgreSQL 16 |
| 生成时间 | 2026-02-22 |
| 表数量 | 11 |
| 总记录数 | ~3,270,000 |

---

## 目录

1. [表清单](#表清单)
2. [表结构详细说明](#表结构详细说明)
   - [natural_products 天然产物表](#natural_products-天然产物表)
   - [targets 靶点表](#targets-靶点表)
   - [bio_resources 生物资源表](#bio_resources-生物资源表)
   - [bioactivity 生物活性表](#bioactivity-生物活性表)
   - [bio_resource_natural_products 生物资源-天然产物关联表](#bio_resource_natural_products-生物资源-天然产物关联表)
   - [bio_resource_disease_associations 生物资源-疾病关联表](#bio_resource_disease_associations-生物资源-疾病关联表)
   - [diseases 疾病表](#diseases-疾病表)
   - [prescriptions 处方表](#prescriptions-处方表)
   - [prescription_resources 处方-生物资源关联表](#prescription_resources-处方-生物资源关联表)
   - [sys_dict 系统字典表](#sys_dict-系统字典表)
   - [sys_menu 系统菜单表](#sys_menu-系统菜单表)
3. [实体关系图](#实体关系图)

---

## 表清单

| 序号 | 表名 | 中文名 | 说明 | 记录数 |
|------|------|--------|------|--------|
| 1 | natural_products | 天然产物表 | 存储天然产物的化学信息和理化性质 | ~203,000 |
| 2 | targets | 靶点表 | 存储蛋白质、基因、酶等生物靶点信息 | ~8,700 |
| 3 | bio_resources | 生物资源表 | 存储植物、动物、微生物等天然产物来源 | ~49,000 |
| 4 | bioactivity | 生物活性表 | 存储天然产物对靶点的活性实验数据 | ~1,050,000 |
| 5 | bio_resource_natural_products | 生物资源-天然产物关联表 | 记录生物资源包含的天然产物 | ~1,117,000 |
| 6 | bio_resource_disease_associations | 生物资源-疾病关联表 | 记录生物资源与疾病的治疗关联 | ~802,000 |
| 7 | diseases | 疾病表 | 存储ICD-11疾病信息 | ~1,500 |
| 8 | prescriptions | 处方表 | 存储中医方剂信息 | ~7,400 |
| 9 | prescription_resources | 处方-生物资源关联表 | 记录处方的组成药材 | ~80,000 |
| 10 | sys_dict | 系统字典表 | 存储系统字典数据 | - |
| 11 | sys_menu | 系统菜单表 | 存储前端菜单权限配置 | - |

---

## 表结构详细说明

### natural_products 天然产物表

**表说明**：存储天然产物的化学信息和理化性质，主要来源于 NPASS 3.0 数据库。

**记录数**：约 203,000 条

| 序号 | 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|------|--------|----------|------|--------|------|
| 1 | id | bigint | NO | 自增序列 | 主键ID |
| 2 | np_id | varchar(50) | NO | - | 天然产物编号（如NPC491451） |
| 3 | inchikey | varchar(100) | YES | - | InChIKey - 国际化合物标识符的哈希值 |
| 4 | pref_name | text | YES | - | 首选名称 - 化合物的常用名称 |
| 5 | iupac_name | text | YES | - | IUPAC系统命名 - 国际纯粹与应用化学联合会标准命名 |
| 6 | name_initial | varchar(10) | YES | - | 名称首字母 - 用于按字母排序 |
| 7 | inchi | text | YES | - | InChI - 国际化合物标识符 |
| 8 | smiles | text | YES | - | SMILES - 简化分子线性输入规范 |
| 9 | chembl_id | varchar(50) | YES | - | ChEMBL数据库编号 |
| 10 | pubchem_id | varchar(50) | YES | - | PubChem化合物编号（CID） |
| 11 | molecular_weight | numeric(10,2) | YES | - | 分子量（单位：g/mol） |
| 12 | xlogp | numeric(10,2) | YES | - | 脂水分配系数XLogP - 衡量化合物的亲脂性 |
| 13 | psa | numeric(10,2) | YES | - | 极性表面积PSA（单位：Å²） |
| 14 | formula | varchar(200) | YES | - | 分子式 - 化合物的元素组成 |
| 15 | h_bond_donors | integer | YES | - | 氢键供体数量 |
| 16 | h_bond_acceptors | integer | YES | - | 氢键受体数量 |
| 17 | rotatable_bonds | integer | YES | - | 可旋转键数量 |
| 18 | num_of_organism | integer | YES | 0 | 关联生物来源数量 |
| 19 | num_of_target | integer | YES | 0 | 关联靶点数量 |
| 20 | num_of_activity | integer | YES | 0 | 生物活性记录数量 |
| 21 | created_at | timestamp | YES | CURRENT_TIMESTAMP | 记录创建时间 |
| 22 | updated_at | timestamp | YES | CURRENT_TIMESTAMP | 记录更新时间 |
| 23 | if_quantity | boolean | YES | false | 是否有定量数据 |
| 24 | log_s | numeric(10,2) | YES | - | LogS - 水溶解度对数值 |
| 25 | log_d | numeric(10,2) | YES | - | LogD - 分布系数对数值 |
| 26 | log_p | numeric(10,2) | YES | - | LogP - 辛醇-水分配系数对数值 |
| 27 | tpsa | numeric(10,2) | YES | - | 拓扑极性表面积（TPSA） |
| 28 | ring_count | integer | YES | - | 环数目 - 分子中环的数量 |

**索引**：
- `idx_natural_products_np_id` ON (np_id)
- `idx_natural_products_inchikey` ON (inchikey)
- `idx_natural_products_pref_name` ON (pref_name)
- `idx_natural_products_mw` ON (molecular_weight)
- `idx_natural_products_num_activity` ON (num_of_activity)

---

### targets 靶点表

**表说明**：存储生物靶点信息，包括蛋白质、细胞系、基因、酶等，数据来源于 NPASS 和 TTD 数据库。

**记录数**：约 8,700 条

| 序号 | 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|------|--------|----------|------|--------|------|
| 1 | id | bigint | NO | 自增序列 | 主键ID |
| 2 | target_id | varchar(50) | NO | - | 靶点编号（如NPT918） |
| 3 | target_type | varchar(200) | YES | - | 靶点类型（Protein蛋白质、Cell line细胞系、Gene基因、Enzyme酶） |
| 4 | target_name | varchar(500) | YES | - | 靶点名称 |
| 5 | target_organism | varchar(200) | YES | - | 靶点来源物种 |
| 6 | target_organism_tax_id | varchar(100) | YES | - | 靶点来源物种的分类学ID |
| 7 | uniprot_id | varchar(300) | YES | - | UniProt蛋白质数据库编号 |
| 8 | num_of_compounds | integer | YES | 0 | 关联化合物数量（旧字段，保留兼容） |
| 9 | num_of_activities | integer | YES | 0 | 生物活性记录数量 |
| 10 | created_at | timestamp | YES | CURRENT_TIMESTAMP | 记录创建时间 |
| 11 | updated_at | timestamp | YES | CURRENT_TIMESTAMP | 记录更新时间 |
| 12 | num_of_natural_products | integer | YES | 0 | 关联天然产物数量 |
| 13 | gene_name | varchar(100) | YES | - | 基因名称 - 编码该蛋白的基因符号 |
| 14 | synonyms | text | YES | - | 同义词 - 靶点的其他名称（分号分隔） |
| 15 | function | text | YES | - | 功能描述 - 靶点的生物学功能 |
| 16 | pdb_structure | varchar(500) | YES | - | PDB结构编号 - 蛋白质三维结构数据 |
| 17 | bioclass | varchar(200) | YES | - | 生物分类 - 靶点的生物学类别 |
| 18 | ec_number | varchar(50) | YES | - | EC编号 - 酶的分类编号 |
| 19 | sequence | text | YES | - | 蛋白质氨基酸序列 |
| 20 | ttd_id | varchar(50) | YES | - | TTD治疗靶点数据库编号 |

**索引**：
- `idx_targets_target_id` ON (target_id)
- `idx_targets_type` ON (target_type)
- `idx_targets_name` ON (target_name)
- `idx_targets_gene_name` ON (gene_name)
- `idx_targets_uniprot` ON (uniprot_id)

---

### bio_resources 生物资源表

**表说明**：存储天然产物的生物来源信息，包括植物、动物、微生物、矿物等，整合了 NPASS、TCMID、CMAUP 数据。

**记录数**：约 49,000 条

| 序号 | 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|------|--------|----------|------|--------|------|
| 1 | id | bigint | NO | 自增序列 | 主键ID |
| 2 | resource_id | varchar(50) | NO | - | 资源唯一编号 |
| 3 | resource_type | varchar(50) | NO | - | 资源类型（Plant植物、Animal动物、Microorganism微生物、Mineral矿物、Fungus真菌） |
| 4 | chinese_name | varchar(500) | YES | - | 中文名称 |
| 5 | latin_name | varchar(500) | YES | - | 拉丁学名 - 国际通用的科学命名 |
| 6 | taxonomy_kingdom | varchar(100) | YES | - | 分类学-界 |
| 7 | taxonomy_family | varchar(200) | YES | - | 分类学-科 |
| 8 | taxonomy_genus | varchar(200) | YES | - | 分类学-属 |
| 9 | taxonomy_species | varchar(200) | YES | - | 分类学-种 |
| 10 | taxonomy_id | varchar(50) | YES | - | NCBI分类学ID |
| 11 | tcmid_id | varchar(500) | YES | - | TCMID中药分子数据库编号 |
| 12 | num_of_natural_products | integer | YES | 0 | 包含的天然产物数量 |
| 13 | num_of_prescriptions | integer | YES | 0 | 相关处方数量 |
| 14 | created_at | timestamp | YES | CURRENT_TIMESTAMP | 记录创建时间 |
| 15 | updated_at | timestamp | YES | CURRENT_TIMESTAMP | 记录更新时间 |
| 16 | species_tax_id | varchar(50) | YES | - | 种级分类学ID |
| 17 | genus_tax_id | varchar(50) | YES | - | 属级分类学ID |
| 18 | family_tax_id | varchar(50) | YES | - | 科级分类学ID |
| 19 | cmaup_id | varchar(50) | YES | - | CMAUP中药材数据库编号 |
| 20 | official_chinese_name | varchar(255) | YES | - | 官方中文名称 |
| 21 | standard_chinese_name | varchar(500) | YES | - | 标准中文名称 |

**索引**：
- `idx_bio_resources_id` ON (resource_id)
- `idx_bio_resources_type` ON (resource_type)
- `idx_bio_resources_chinese_name` ON (chinese_name)
- `idx_bio_resources_latin_name` ON (latin_name)
- `idx_bio_resources_tcmid_id` ON (tcmid_id)
- `idx_bio_resources_cmaup_id` ON (cmaup_id)

---

### bioactivity 生物活性表

**表说明**：存储天然产物对靶点的生物活性实验数据，包括 IC50、EC50、Ki 等活性值。

**记录数**：约 1,050,000 条

| 序号 | 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|------|--------|----------|------|--------|------|
| 1 | id | bigint | NO | 自增序列 | 主键ID |
| 2 | natural_product_id | bigint | NO | - | 关联的天然产物ID |
| 3 | target_id | bigint | NO | - | 关联的靶点ID |
| 4 | activity_type | varchar(100) | YES | - | 活性类型（IC50、EC50、Ki、Kd、GI50等） |
| 5 | activity_type_grouped | varchar(100) | YES | - | 活性类型分组（IC50/EC50/Ki/Kd等归为一组） |
| 6 | activity_relation | varchar(10) | YES | - | 活性关系符号（= 等于、> 大于、< 小于、~ 约等于） |
| 7 | activity_value | numeric(30,6) | YES | - | 原始活性值 |
| 8 | activity_units | varchar(100) | YES | - | 原始活性单位（nM、μM、mM、M等） |
| 9 | activity_value_std | numeric(30,6) | YES | - | 标准化活性值（统一转换为nM） |
| 10 | activity_units_std | varchar(20) | YES | 'nM' | 标准化活性单位（固定为nM） |
| 11 | assay_organism | varchar(200) | YES | - | 实验物种 - 活性测定所用的生物体 |
| 12 | assay_tax_id | varchar(100) | YES | - | 实验物种分类学ID |
| 13 | assay_strain | varchar(100) | YES | - | 实验菌株/品系 |
| 14 | assay_tissue | varchar(200) | YES | - | 实验组织 |
| 15 | assay_cell_type | varchar(100) | YES | - | 实验细胞类型 |
| 16 | ref_id | varchar(300) | YES | - | 参考文献ID（PMID、DOI等） |
| 17 | ref_id_type | varchar(20) | YES | - | 参考文献类型（PMID、DOI、Patent） |
| 18 | created_at | timestamp | YES | CURRENT_TIMESTAMP | 记录创建时间 |

**索引**：
- `idx_bioactivity_natural_product` ON (natural_product_id)
- `idx_bioactivity_target` ON (target_id)
- `idx_bioactivity_type` ON (activity_type)
- `idx_bioactivity_value_std` ON (activity_value_std)
- `idx_bioactivity_natural_product_target` ON (natural_product_id, target_id)

---

### bio_resource_natural_products 生物资源-天然产物关联表

**表说明**：记录生物资源中包含的天然产物及其分离信息。

**记录数**：约 1,117,000 条

| 序号 | 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|------|--------|----------|------|--------|------|
| 1 | id | bigint | NO | 自增序列 | 主键ID |
| 2 | org_id | text | YES | - | 生物来源编号 |
| 3 | np_id | text | YES | - | 天然产物编号 |
| 4 | src_org_record_id | text | YES | - | 来源生物记录ID |
| 5 | src_org_pair_id | text | YES | - | 来源生物-产物配对ID |
| 6 | src_org_pair | text | YES | - | 来源生物-产物配对信息 |
| 7 | new_cp_found | text | YES | - | 是否发现新化合物 |
| 8 | org_isolation_part | text | YES | - | 分离部位 - 从生物体的哪个部位分离 |
| 9 | org_collect_location | text | YES | - | 采集地点 |
| 10 | org_collect_time | text | YES | - | 采集时间 |
| 11 | ref_type | text | YES | - | 参考文献类型 |
| 12 | ref_id | text | YES | - | 参考文献ID |
| 13 | ref_id_type | text | YES | - | 参考文献ID类型（PMID、DOI） |
| 14 | ref_url | text | YES | - | 参考文献URL链接 |
| 15 | created_at | timestamp | YES | CURRENT_TIMESTAMP | 记录创建时间 |
| 16 | updated_at | timestamp | YES | CURRENT_TIMESTAMP | 记录更新时间 |

---

### bio_resource_disease_associations 生物资源-疾病关联表

**表说明**：记录生物资源与疾病的治疗关联关系及证据来源，数据来源于 CMAUP。

**记录数**：约 802,000 条

| 序号 | 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|------|--------|----------|------|--------|------|
| 1 | id | bigint | NO | 自增序列 | 主键ID |
| 2 | bio_resource_id | bigint | NO | - | 关联的生物资源ID |
| 3 | disease_id | bigint | NO | - | 关联的疾病ID |
| 4 | evidence_therapeutic_target | text | YES | - | 治疗靶点证据 - 相关治疗靶点列表（分号分隔） |
| 5 | evidence_transcriptome | boolean | YES | false | 转录组证据 - 是否有转录组学证据支持 |
| 6 | evidence_clinical_trial_plant | text | YES | - | 植物临床试验证据 - 相关临床试验ID |
| 7 | evidence_clinical_trial_ingredient | text | YES | - | 成分临床试验证据 - 成分相关临床试验ID |
| 8 | confidence_score | numeric(3,2) | YES | - | 置信度评分（0-1之间，越高表示关联越可靠） |
| 9 | source | varchar(100) | YES | 'CMAUP' | 数据来源 |
| 10 | source_version | varchar(50) | YES | - | 数据来源版本 |
| 11 | created_at | timestamp | YES | CURRENT_TIMESTAMP | 记录创建时间 |

---

### diseases 疾病表

**表说明**：存储疾病信息，基于 ICD-11 国际疾病分类标准。

**记录数**：约 1,500 条

| 序号 | 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|------|--------|----------|------|--------|------|
| 1 | id | bigint | NO | 自增序列 | 主键ID |
| 2 | icd11_code | varchar(50) | NO | - | ICD-11国际疾病分类编码 |
| 3 | disease_name | varchar(500) | NO | - | 疾病英文名称 |
| 4 | disease_name_zh | varchar(500) | YES | - | 疾病中文名称 |
| 5 | disease_category | varchar(200) | YES | - | 疾病分类 |
| 6 | created_at | timestamp | YES | CURRENT_TIMESTAMP | 记录创建时间 |
| 7 | updated_at | timestamp | YES | CURRENT_TIMESTAMP | 记录更新时间 |
| 8 | disease_name_cmaup | varchar(500) | YES | - | CMAUP数据库中的疾病名称 |

**索引**：
- `idx_diseases_icd11_code` ON (icd11_code)
- `idx_diseases_category` ON (disease_category)

---

### prescriptions 处方表

**表说明**：存储中医方剂/处方信息，包括方剂组成、功效主治、用法用量等。

**记录数**：约 7,400 条

| 序号 | 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|------|--------|----------|------|--------|------|
| 1 | id | bigint | NO | 自增序列 | 主键ID |
| 2 | prescription_id | varchar(50) | NO | - | 处方编号 |
| 3 | chinese_name | varchar(500) | YES | - | 处方中文名称 |
| 4 | pinyin_name | varchar(200) | YES | - | 处方拼音名称 |
| 5 | english_name | varchar(500) | YES | - | 处方英文名称 |
| 6 | functions | text | YES | - | 功能功效 - 方剂的功效描述 |
| 7 | indications | text | YES | - | 主治 - 适应症和主治疾病 |
| 8 | tcmid_id | varchar(50) | YES | - | TCMID数据库编号 |
| 9 | created_at | timestamp | YES | CURRENT_TIMESTAMP | 记录创建时间 |
| 10 | updated_at | timestamp | YES | CURRENT_TIMESTAMP | 记录更新时间 |
| 11 | disease_icd11_category | text | YES | - | ICD-11疾病分类编码（多个用分号分隔） |
| 12 | reference | text | YES | - | 参考文献 |

**索引**：
- `idx_prescriptions_id` ON (prescription_id)
- `idx_prescriptions_chinese_name` ON (chinese_name)
- `idx_prescriptions_tcmid_id` ON (tcmid_id)

---

### prescription_resources 处方-生物资源关联表

**表说明**：记录处方的组成药材。

**记录数**：约 80,000 条

| 序号 | 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|------|--------|----------|------|--------|------|
| 1 | id | bigint | NO | 自增序列 | 主键ID |
| 2 | prescription_id | bigint | NO | - | 关联的处方ID |
| 3 | bio_resource_id | bigint | NO | - | 关联的生物资源ID（药材） |
| 4 | created_at | timestamp | YES | CURRENT_TIMESTAMP | 记录创建时间 |
| 5 | tcmid_component_id | varchar(500) | YES | - | TCMID药材组分ID（如TCMH1398） |

---

### sys_dict 系统字典表

**表说明**：存储系统各类下拉选项的字典数据。

| 序号 | 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|------|--------|----------|------|--------|------|
| 1 | dict_code | bigint | NO | - | 字典编码 - 主键 |
| 2 | dict_sort | integer | NO | - | 字典排序序号 |
| 3 | dict_label | varchar(100) | NO | - | 字典标签 - 显示给用户看的文字 |
| 4 | dict_value | varchar(100) | NO | - | 字典键值 - 实际存储的值 |
| 5 | dict_type | varchar(100) | NO | - | 字典类型 - 用于区分不同类型的字典 |
| 6 | css_class | varchar(100) | NO | '' | CSS样式类名 - 前端显示样式 |
| 7 | list_class | varchar(100) | NO | '' | 列表样式类名 - 表格中的显示样式 |
| 8 | is_default | char(1) | NO | 'N' | 是否默认值（Y是、N否） |
| 9 | status | char(1) | NO | '0' | 状态（0正常、1停用） |
| 10 | create_by | varchar(64) | NO | - | 创建者 |
| 11 | create_time | timestamp | NO | CURRENT_TIMESTAMP | 创建时间 |
| 12 | update_by | varchar(64) | NO | - | 更新者 |
| 13 | update_time | timestamp | NO | CURRENT_TIMESTAMP | 更新时间 |
| 14 | remark | varchar(500) | NO | '' | 备注说明 |

---

### sys_menu 系统菜单表

**表说明**：存储前端菜单导航和按钮权限配置。

| 序号 | 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|------|--------|----------|------|--------|------|
| 1 | menu_id | bigint | NO | - | 菜单ID - 主键 |
| 2 | menu_name | varchar(50) | NO | - | 菜单名称 |
| 3 | parent_id | bigint | NO | 0 | 父菜单ID（0表示顶级菜单） |
| 4 | order_num | integer | NO | 0 | 显示顺序 |
| 5 | path | varchar(200) | NO | '' | 路由地址 - 前端路由路径 |
| 6 | component | varchar(255) | YES | - | 组件路径 - Vue组件路径 |
| 7 | query_param | varchar(255) | YES | - | 路由参数 |
| 8 | is_frame | integer | NO | 1 | 是否为外链（0是、1否） |
| 9 | is_cache | integer | NO | 0 | 是否缓存（0缓存、1不缓存） |
| 10 | menu_type | char(1) | NO | - | 菜单类型（M目录、C菜单、F按钮） |
| 11 | visible | char(1) | NO | '0' | 显示状态（0显示、1隐藏） |
| 12 | status | char(1) | NO | '0' | 菜单状态（0正常、1停用） |
| 13 | perms | varchar(100) | YES | - | 权限标识 - 用于权限控制 |
| 14 | icon | varchar(100) | YES | '' | 菜单图标 |
| 15 | create_by | varchar(64) | NO | - | 创建者 |
| 16 | create_time | timestamp | NO | CURRENT_TIMESTAMP | 创建时间 |
| 17 | update_by | varchar(64) | NO | - | 更新者 |
| 18 | update_time | timestamp | NO | CURRENT_TIMESTAMP | 更新时间 |
| 19 | remark | varchar(500) | YES | '' | 备注说明 |

---

## 实体关系图

详细 ER 图请参考 [database-er-diagram.md](database-er-diagram.md)

```
┌─────────────────┐     ┌─────────────────┐
│ natural_products│     │    targets      │
│   (天然产物)     │     │     (靶点)       │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
             ┌──────────────┐
             │ bioactivity  │
             │  (生物活性)   │
             └──────────────┘

┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ bio_resources   │     │    diseases     │     │  prescriptions  │
│  (生物资源)      │     │     (疾病)       │     │     (处方)       │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         ├───────────────────────┤                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌──────────────────────┐  ┌──────────────────────────────────┐
│ bio_resource_        │  │ prescription_resources           │
│ disease_associations │  │     (处方-生物资源关联)           │
└──────────────────────┘  └──────────────────────────────────┘
```

---

## 数据来源

| 数据源 | 说明 | 相关表 |
|--------|------|--------|
| NPASS 3.0 | 天然产物及活性数据库 | natural_products, targets, bioactivity, bio_resource_natural_products |
| TCMID | 中药分子数据库 | prescriptions, bio_resources, prescription_resources |
| CMAUP | 中药材数据库 | bio_resources, diseases, bio_resource_disease_associations |
| TTD | 治疗靶点数据库 | targets |

---

*文档生成时间: 2026-02-22*
