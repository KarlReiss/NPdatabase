# 天然产物数据库需求文档（简化版）

**版本**: V1.1-Simplified
**日期**: 2026-01-29
**基于**: 现有界面原型 + NPASS 3.0 数据

---

## 0. 实现状态（快速说明）

- ✅ 后端核心 API 已完成并可运行
- ✅ Swagger 校验说明已提供（见 `docs/swagger-validation.md`）
- ✅ 开发日志与实现说明已归档（见 `docs/backend-dev-log.md` / `docs/backend-dev-doc.md`）

---

## 1. 项目概述

### 1.1 目标
构建一个天然产物数据库的展示与检索平台，基于 NPASS 3.0 数据，支持化合物、活性数据、靶点的浏览与关联查询。

### 1.2 一期范围
- ✅ 数据浏览与检索（化合物为核心）
- ✅ 基础筛选与排序
- ✅ 详情页展示与关联跳转
- ❌ 不做：AI 预测、导出功能、复杂分析

---

## 2. 核心数据实体

### 2.1 天然产物/化合物 (Natural Product)
**对应表**: `natural_products`（由 `compounds` 优化重命名）

**来源**: `NPASS3.0_naturalproducts_generalinfo.txt` + `NPASS3.0_naturalproducts_structure.txt`

**核心字段**:
- 业务ID: `np_id` (如 NPC491451)
- 名称: `pref_name`, `iupac_name`
- 结构: `inchikey`, SMILES (从 structure 文件获取)
- 外部 ID: `chembl_id`, `pubchem_id`
- 统计: `num_of_organism`, `num_of_target`, `num_of_activity`

**理化性质** (需计算或补充):
- 分子量 (Molecular Weight)
- XLogP (脂水分配系数)
- PSA (极性表面积)
- 分子式 (Formula)

### 2.2 活性记录 (Bioactivity)
**来源**: `NPASS3.0_activities.txt`

**核心字段**:
- 化合物: `np_id`
- 靶点: `target_id`
- 活性类型: `activity_type` (IC50, EC50, Ki, Kd 等)
- 活性值: `activity_value` + `activity_units`
- 关系: `activity_relation` (=, >, <)
- 实验条件: `assay_organism`, `assay_cell_type`, `assay_tissue`
- 参考文献: `ref_id` + `ref_id_type` (PMID)

**数据处理需求**:
- 单位标准化：统一转换为 nM (纳摩尔)
- 存储原始值和标准化值

### 2.3 靶点 (Target)
**来源**: `NPASS3.0_target.txt`

**核心字段**:
- ID: `target_id` (如 NPT918)
- 类型: `target_type` (Cell line, Protein, Gene 等)
- 名称: `target_name`
- 物种: `target_organism` + `target_organism_tax_id`
- UniProt ID: `uniprot_id`

### 2.4 生物资源/来源 (BioResource)
**对应表**: `bio_resources`（替代 `species`，来源/药材统一管理）

**来源**: `NPASS3.0_species_info.txt` + `NPASS3.0_naturalproducts_species_pair.txt`

**核心字段**:
- 分类学信息（taxonomy_*）
- 名称信息（中文/拉丁/拼音等，预留扩展字段）
- 天然产物关联：`bio_resource_natural_products`（原 `compound_species`）

### 2.5 处方/方剂 (Prescription，可选扩展)
**对应表**: `prescriptions` + `prescription_resources` + `prescription_natural_products`  
**说明**: 一期可不展示，但结构已预留用于后续扩展。

### 2.6 毒性 (Toxicity)
**来源**: `NPASS3.0_toxicity.txt`

**用途**: 标记有毒化合物，用于专题库筛选

---

## 3. 页面结构（基于现有原型）

### 3.1 首页 (Home)
**现有功能**:
- ✅ 搜索框（关键词搜索 / SMILES 搜索）
- ✅ 专题卡片（抗肿瘤、心脑血管、有毒药材）

**需要调整**:
- 搜索功能对接真实数据
- 专题卡片显示真实统计数量
- 添加数据库统计概览

### 3.2 列表页 (ListPage)
**现有功能**:
- ✅ 侧边栏筛选（理化属性、活性筛选、疾病）
- ✅ 数据表格（ID、结构、名称、属性、活性、靶点数）
- ✅ 分页与排序

**需要调整**:
- 对接 NPASS 数据
- 筛选器实现：
  - 分子量范围 (MW)
  - XLogP 范围
  - 活性阈值 (IC50 < 1μM)
  - 靶点类型
- 排序：按活性强度、分子量、靶点数

### 3.3 详情页 (DetailPage)
**现有功能**:
- ✅ 结构图展示
- ✅ 基本信息卡片
- ✅ 标签页（Bioactivity、Targets、In Herbs、Clinical Trials）

**需要调整**:
- **Bioactivity 标签页**:
  - 显示活性记录表格
  - 字段：Target、Assay Type、Raw Value、Std Value、Reference (PMID 链接)
  - 支持按活性类型筛选

- **Targets 标签页**:
  - 显示关联靶点列表
  - 显示每个靶点的最佳活性值
  - 靶点类型分类（Protein、Cell line 等）

- **In Herbs 标签页** (改为 "来源生物资源/药材"):
  - 显示天然产物来源的生物资源
  - 来自 `bio_resource_natural_products`（由 species_pair 导入）

- **Clinical Trials 标签页** (一期暂不实现):
  - 显示占位符

---

## 4. 核心功能需求

### 4.1 全局搜索
**支持搜索**:
- 化合物名称 (`pref_name`, `iupac_name`)
- 化合物 ID (`np_id`)
- 外部 ID (`chembl_id`, `pubchem_id`)
- SMILES / InChIKey (结构搜索)

**搜索结果**:
- 按实体类型分组（化合物、靶点）
- 显示匹配度排序

### 4.2 筛选功能
**化合物列表筛选**:
1. **理化属性**:
   - 分子量范围 (0-1000)
   - XLogP 范围 (-5 to 10)
   - PSA 范围

2. **活性筛选**:
   - 活性类型 (IC50, EC50, Ki, Kd)
   - 活性阈值 (如 < 1μM, < 100nM)
   - 是否有活性记录

3. **靶点筛选**:
   - 靶点类型 (Protein, Cell line, Gene)
   - 靶点名称关键词

4. **来源筛选**:
   - 生物资源分类/来源
   - 是否有毒性记录

### 4.3 排序功能
- 按名称 (A-Z)
- 按分子量
- 按活性强度 (最强活性值)
- 按靶点数量
- 按更新时间

### 4.4 详情页关联
**化合物详情页可跳转到**:
- 靶点详情页
- 生物资源详情页
- 外部链接 (PubChem, ChEMBL)
- 文献链接 (PMID → PubMed)

---

## 5. 数据处理需求

### 5.1 数据导入
**步骤**:
1. 解析 NPASS 3.0 数据文件 (TSV 格式)
2. 数据清洗与验证
3. 计算理化性质 (使用 RDKit 或类似工具)
4. 单位标准化 (活性值统一为 nM)
5. 导入数据库

### 5.2 理化性质计算
**需要计算的属性**:
- 分子量 (MW)
- XLogP (脂水分配系数)
- PSA (极性表面积)
- 氢键供体数 (H-Bond Donors)
- 氢键受体数 (H-Bond Acceptors)
- 可旋转键数 (Rotatable Bonds)

**工具**: RDKit (Python) 或 ChemAxon

### 5.3 单位标准化规则
**活性值单位转换**:
- M → nM: × 1,000,000,000
- mM → nM: × 1,000,000
- μM → nM: × 1,000
- nM → nM: × 1
- pM → nM: × 0.001

**存储格式**:
```json
{
  "value_raw": "1.5",
  "unit_raw": "μM",
  "value_std": 1500,
  "unit_std": "nM"
}
```

---

## 6. 专题库定义

### 6.1 抗肿瘤 (Anti-tumor)
**筛选条件**:
- 靶点类型包含癌细胞系 (Cell line)
- 或靶点名称包含肿瘤相关基因 (EGFR, VEGFR, HER2 等)
- 活性值 < 10μM

### 6.2 心脑血管 (Cardiovascular)
**筛选条件**:
- 靶点名称包含心血管相关 (COX-2, ACE, AT1 等)
- 或疾病标签包含心血管疾病

### 6.3 有毒药材 (Toxic Herbs)
**筛选条件**:
- 存在毒性记录 (`NPASS3.0_toxicity.txt`)
- 显示毒性类型、剂量、症状

### 6.4 抗炎免疫 (Anti-inflammatory)
**筛选条件**:
- 靶点包含炎症相关 (TNF-α, IL-6, NF-κB 等)

---

## 7. UI/UX 规范

### 7.1 设计风格
**现有风格** (保持):
- 主色: `#10B981` (翠绿色)
- 背景: `#F8FAFC` (浅灰)
- 边框: `#E2E8F0`
- 字体: Arial, 中文用常规的无衬线字体

### 7.2 组件规范
**表格**:
- 固定表头（表头可排序）
- 斑马纹行 (交替背景色)
- Hover 高亮
- 行高: 48px

**筛选器**:
- 可折叠侧边栏
- 范围滑块 (Range Slider)
- 多选复选框
- "清空筛选" 按钮

**标签页**:
- 底部边框高亮当前标签
- 显示数据计数 (如 "Bioactivity (34)")

---

## 8. 技术实现建议

### 8.1 后端
**技术栈**:
- Java + Spring Boot
- MyBatis-Plus
- PostgreSQL (关系型数据库)
- Redis (缓存，可选)

**API 设计**:
```
GET /api/natural-products?page=1&pageSize=20&mw_min=0&mw_max=500
GET /api/natural-products/:npId
GET /api/natural-products/:npId/bioactivity
GET /api/natural-products/:npId/targets
GET /api/search?q=curcumin&type=natural_product
```

### 8.2 前端
**现有技术栈** (保持):
- React 19 + TypeScript
- React Router DOM
- Vite
- Tailwind CSS (内联样式)

**需要添加**:
- 状态管理: React Query 或 SWR (数据获取)
- 图表库: Recharts 或 Chart.js (可选)
- 结构渲染: Ketcher 或 RDKit.js (SMILES → 结构图)

### 8.3 数据库设计
**核心表**:
```sql
-- 天然产物表（原 compounds）
natural_products (
  id, np_id, pref_name, iupac_name, inchikey, smiles,
  chembl_id, pubchem_id, molecular_weight, xlogp, psa, formula,
  num_of_organism, num_of_target, num_of_activity
)

-- 活性记录表
bioactivity (
  id, natural_product_id, target_id, activity_type,
  activity_value, activity_units,
  activity_value_std, activity_units_std,
  activity_relation, assay_organism, assay_cell_type,
  ref_id, ref_id_type
)

-- 靶点表
targets (
  id, target_id, target_type, target_name,
  target_organism, target_organism_tax_id, uniprot_id
)

-- 生物资源表（替代 species）
bio_resources (
  id, resource_id, resource_type, chinese_name, latin_name,
  taxonomy_kingdom, taxonomy_family, taxonomy_genus, taxonomy_species
)

-- 生物资源-天然产物关联表
bio_resource_natural_products (
  bio_resource_id, natural_product_id
)

-- 毒性表
toxicity (
  id, natural_product_id, toxicity_type, dose, symptoms, ref_id
)
```

**说明**:
- 最终表结构以 `scripts/database/schema.sql` → `add_prescription_bioresource.sql` → `optimize_table_structure.sql` 为准。

---

## 9. 开发优先级

### Phase 1: 核心功能 (2-3 周)
- [ ] 数据导入脚本 (NPASS → 数据库)
- [ ] 理化性质计算
- [ ] 化合物列表页 (基础筛选 + 排序)
- [ ] 化合物详情页 (基本信息 + Bioactivity 标签)
- [ ] 全局搜索 (关键词)

### Phase 2: 增强功能 (2 周)
- [ ] 高级筛选 (活性阈值、靶点类型)
- [ ] 靶点详情页
- [ ] 生物资源详情页
- [ ] 专题库页面 (3 个专题)

### Phase 3: 优化 (1 周)
- [ ] 性能优化 (分页、索引)
- [ ] 结构图渲染优化
- [ ] 响应式适配
- [ ] 用户反馈收集

---

## 10. 非功能性需求

### 10.1 性能
- 列表查询 < 2s
- 详情页加载 < 1s
- 支持 10 万+ 化合物记录

### 10.2 安全
- 一期暂不需要登录 (公开访问)
- 二期考虑登录门槛

### 10.3 兼容性
- 支持 Chrome、Firefox、Safari、Edge 最新版本
- 桌面优先 (>= 1280px)

---

## 11. 数据来源说明

**NPASS 3.0 数据集**:
- 化合物数: ~50 万条
- 活性记录: ~100 万条
- 靶点数: ~1000 个
- 生物资源数: ~7000 个（由 NPASS 物种数据导入）

**数据文件**:
- `NPASS3.0_naturalproducts_generalinfo.txt` - 化合物基本信息
- `NPASS3.0_naturalproducts_structure.txt` - 化合物结构
- `NPASS3.0_activities.txt` - 活性记录
- `NPASS3.0_target.txt` - 靶点信息
- `NPASS3.0_species_info.txt` - 物种信息（导入到 bio_resources）
- `NPASS3.0_naturalproducts_species_pair.txt` - 天然产物-来源关联（导入到 bio_resource_natural_products）
- `NPASS3.0_toxicity.txt` - 毒性记录

---

## 12. 参考资源

**参考网站**:
- TCM-ID: 中药数据库参考 (见 `reference/` 目录)
- NPASS: https://bidd.group/NPASS/
- PubChem: https://pubchem.ncbi.nlm.nih.gov/
- ChEMBL: https://www.ebi.ac.uk/chembl/

**技术文档**:
- RDKit: https://www.rdkit.org/docs/
- React Query: https://tanstack.com/query/latest
- PostgreSQL: https://www.postgresql.org/docs/

---

## 附录: 与完整需求文档的差异

**简化内容**:
- ❌ 移除：方剂、证候、通路、疾病映射
- ❌ 移除：LC-MS/组学数据
- ❌ 移除：管理后台、数据审核流程
- ❌ 移除：权限管理、导出功能
- ❌ 移除：复杂的疾病反查逻辑

**保留内容**:
- ✅ 化合物、活性、靶点核心实体
- ✅ 基础浏览与检索
- ✅ 筛选与排序
- ✅ 详情页与关联跳转
- ✅ 专题库（简化版）

**原因**:
- 聚焦核心功能，快速交付可用版本
- 基于现有界面原型，减少设计变更
- 基于 NPASS 数据，避免数据缺失问题
