# 前端页面与字段展示规划（基于数据库结构）

**更新日期**: 2026-01-29  
**依据文档**: `docs/database.md`  
**说明**: 规划以可用字段为准，疾病页为占位，后期补充数据后再完善。

---

## 1. 页面数量与结构

**必选页面（10 个）**
- 首页（全局搜索 + 统计概览 + 专题入口）
- 天然产物：列表 / 详情
- 靶点：列表 / 详情
- 生物资源：列表 / 详情
- 处方：列表 / 详情
- 疾病：列表 / 详情（占位）
- 专题库索引页（抗肿瘤 / 心脑血管 / 有毒药材 / 抗炎免疫）

**可选页面（2 个）**
- 活性数据列表页（全库 bioactivity）
- 毒性数据列表页（全库 toxicity）

---

## 2. 列表页字段规划

### 2.1 天然产物列表（`natural_products` + `v_natural_product_detail`）
**主字段**:
- 编号：`np_id`
- 名称：`pref_name`（次级展示 `iupac_name`）
- 结构：`smiles`（渲染结构缩略图）
- 理化属性：`molecular_weight` / `xlogp` / `psa`
- 统计：`num_of_activity` / `num_of_target` / `num_of_organism`
- 最佳活性：`best_activity_value`（来自视图）
- 毒性标记：`has_toxicity`（来自视图）

**排序**:
- 最佳活性 / 活性记录数 / 靶点数 / 分子量 / 编号

**筛选**:
- 分子量、XLogP、PSA
- 活性类型与阈值（关联 `bioactivity`）
- 是否有毒性
- 靶点类型 / 关键词

---

### 2.2 靶点列表（`targets` + `v_target_detail`）
**主字段**:
- 编号：`target_id`
- 名称：`target_name`
- 类型：`target_type`
- 物种：`target_organism`
- UniProt：`uniprot_id`
- 统计：`num_of_compounds` / `num_of_activities` / `best_activity_value`

**排序**:
- 关联化合物数 / 活性记录数 / 最佳活性

**筛选**:
- 类型（Protein / Cell line / Gene）
- 物种关键词

---

### 2.3 生物资源列表（`bio_resources` + `v_bio_resource_detail`）
**主字段**:
- 编号：`resource_id`
- 中文名 / 拉丁名
- 类型：`resource_type`
- 分类：`taxonomy_family` / `taxonomy_genus`
- 中医属性：`tcm_property` / `tcm_flavor` / `tcm_meridian`
- 统计：`num_of_natural_products` / `num_of_prescriptions`

**排序**:
- 天然产物数量 / 处方数量

**筛选**:
- 类型（植物/动物/微生物/矿物）
- 中医属性 / 经络

---

### 2.4 处方列表（`prescriptions` + `v_prescription_detail`）
**主字段**:
- 编号：`prescription_id`
- 中文名 / 拼音
- 分类：`category` / `subcategory`
- 功效/主治（简版）
- 统计：`num_of_herbs` / `num_of_natural_products`

**排序**:
- 药材数 / 关联天然产物数

**筛选**:
- 分类 / 功效关键词

---

### 2.5 疾病列表（占位）
**主字段（预留）**:
- 疾病名称
- 别名
- 关联靶点数（预留）
- 关联化合物数（预留）

**排序/筛选（预留）**:
- 关联靶点数 / 关联化合物数
- 疾病关键词 / 系统分类

---

## 3. 详情页分区规划

### 3.1 天然产物详情
**顶部信息区**:
- `pref_name` / `np_id`
- `iupac_name`
- 外部 ID：`chembl_id` / `pubchem_id`
- 结构图（SMILES）
- 理化属性卡片：
  - 分子量（MW）
  - XLogP
  - PSA
  - 分子式（Formula）
  - 氢键供体/受体
  - 可旋转键

**标签页**:
- 活性数据（bioactivity）
  - 靶点、类型、关系符号、原始值、标准化值、实验条件、参考文献
- 相关靶点（targets）
  - 靶点名称、类型、最佳活性
- 来源生物资源（bio_resources）
  - 中文名 / 拉丁名 / 分类 / 中医属性
- 毒性信息（toxicity）
  - 类型、剂量、症状、参考文献

---

### 3.2 靶点详情
**顶部信息区**:
- `target_name` / `target_id`
- `target_type`
- `target_organism`
- `uniprot_id`

**标签页**:
- 相关天然产物列表
- 活性记录列表（bioactivity）

---

### 3.3 生物资源详情
**顶部信息区**:
- 中文名 / 拉丁名 / 类型 / 分类

**中医属性**:
- `tcm_property` / `tcm_flavor` / `tcm_meridian` / `tcm_toxicity`

**标签页**:
- 相关天然产物
- 相关处方

---

### 3.4 处方详情
**顶部信息区**:
- 中文名 / 拼音 / 类别

**功效与组成**:
- 功效 / 主治
- 组成与用法（`composition_text` / `dosage_form` / `usage_method`）

**标签页**:
- 处方药材（prescription_resources）
- 关联天然产物（prescription_natural_products）

---

### 3.5 疾病详情（占位）
**顶部信息区（预留）**:
- 疾病名称 / 别名 / 分类 / 简介

**标签页（预留）**:
- 关联靶点
- 关联天然产物

---

## 4. 字段展示规范

- **中文为主，缩写保留**:  
  分子量（MW）、脂水分配系数（XLogP）、极性表面积（PSA）
- **数值显示**: 原始值 + 标准化值并列（默认 nM）
- **业务 ID 优先展示**: `np_id` / `target_id` / `resource_id` / `prescription_id`
- **空值展示**: 用 “—” 替代，避免破碎感
- **长文本**: 默认 2 行折叠，点击展开
- **表格**: 表头支持排序、固定表头、行 hover
- **统计字段**: 优先使用 `v_*_detail` 视图，保证一致

