# 后端改动计划（对齐 schema_v2）

版本：v0.1（草案）

## 目标
- 后端 API 返回字段与 `docs/schema_v2.md` 保持一致，支撑已更新的前端展示。
- 统一表、视图、实体、查询与统计字段口径，避免前后端字段不一致。
- 覆盖列表、详情与关联查询（天然产物、靶点、生物资源、处方、疾病）。

## 范围
- 数据库：表结构、视图（`v_*`）与统计字段。
- 后端：实体类/Mapper/Service/Controller/DTO。
- 不包含：前端改动（已完成）、数据导入脚本的全量重写（仅必要字段补充）。

## 现状差距（简要）
- 后端仅覆盖天然产物与靶点的列表/详情接口；缺少生物资源、处方、疾病的 API。
- `Target`/`TargetDetailView` 未包含 v2 新字段（gene_name、synonyms、function、pdb_structure、bioclass、ec_number、sequence、ttd_id、num_of_natural_products）。
- 视图 `v_*` 已在 `scripts/database/optimize_table_structure.sql` 存在，但可能与 v2 字段不完全一致，需要核对与更新。
- 统计返回 `StatsResponse` 未包含疾病数量。

## 执行阶段与任务拆分

### Phase 0：对齐 schema 与数据库视图（1 次性确认）
**目标**：确认数据库实际结构与 `schema_v2.md` 一致，确保视图与统计字段可用。
- 0.1 核对 `natural_products/targets/bio_resources/prescriptions/diseases` 字段是否与 `schema_v2.md` 一致。
- 0.2 更新视图定义：
  - `v_natural_product_detail`（确认包含统计字段与 has_toxicity）
  - `v_target_detail`（增加 TTD 补充字段与 num_of_natural_products 统计）
  - `v_bio_resource_detail`（确认统计字段名称）
  - `v_prescription_detail`（确认 herb_count 与 direct_natural_product_count）
- 0.3 更新或新增数据库脚本：
  - 推荐新建 `scripts/database/upgrade_to_v2.sql`（保留历史脚本）
  - 或补充 `scripts/database/optimize_table_structure.sql` 中的字段/视图

**产出**：SQL 变更脚本 + 数据库结构确认记录。

### Phase 1：实体层对齐（Entity/Mapper）
**目标**：实体字段与 v2 schema 对齐，确保查询与序列化正确。
- 1.1 更新 `Target` 实体字段：
  - 新增：`geneName/synonyms/function/pdbStructure/bioclass/ecNumber/sequence/ttdId/numOfNaturalProducts`
  - 保留：`numOfCompounds/numOfActivities`
- 1.2 更新 `TargetDetailView` 实体字段（同上，并包含统计字段）。
- 1.3 若后端需要列表/详情视图：新增实体
  - `BioResourceDetailView`（表名 `v_bio_resource_detail`）
  - `PrescriptionDetailView`（表名 `v_prescription_detail`）
  - `Disease`（表名 `diseases`）
- 1.4 对应 Mapper：新增 `BioResourceDetailMapper` / `PrescriptionDetailMapper` / `DiseaseMapper`。

**产出**：`entity/*` 与 `mapper/*` 完整对齐 v2。

### Phase 2：服务与控制层接口补齐
**目标**：提供前端所需的列表/详情/关联接口。
- 2.1 现有接口调整：
  - `NaturalProductController.list`：返回字段补齐（formula/psa/num_of_* 等），若可行改为直接查询 `v_natural_product_detail`。
  - `TargetController.list`：支持 `gene_name` 展示与 `num_of_natural_products` 字段。
  - `SearchController`：补充对 target gene_name 的搜索（可选）。
- 2.2 新增控制器：
  - `BioResourceController`：list/detail/`/natural-products`/`/prescriptions` 等关联接口
  - `PrescriptionController`：list/detail/`/bio-resources`/`/natural-products` 等关联接口
  - `DiseaseController`：list/detail/`/bio-resources`/`/natural-products`（若有需求）
- 2.3 Service 层补齐（若目前仅有基础 Service）：
  - 新增 DiseaseService
  - 适配 BioResource/Prescription 的关联查询

**产出**：与前端页面对应的 API 路由与返回字段。

### Phase 3：DTO 与统计接口
**目标**：统计与通用返回体字段补齐。
- 3.1 更新 `StatsResponse`：新增 `diseases` 字段。
- 3.2 `StatsController` 添加疾病统计。

**产出**：统计接口与前端一致。

### Phase 4：验证与回归
**目标**：确保接口返回字段与前端/Schema 一致。
- 4.1 启动后端并跑接口冒烟测试（Postman/HTTPie/脚本）。
- 4.2 验证以下页面的字段一致性：
  - 天然产物列表/详情
  - 靶点列表/详情
  - 生物资源列表/详情
  - 处方列表/详情
  - 疾病列表/详情
- 4.3 记录异常字段与修复清单。

**产出**：字段一致性确认与修复记录。

## 文件改动建议清单（按优先级）
1. `backend/src/main/java/cn/npdb/entity/Target.java`
2. `backend/src/main/java/cn/npdb/entity/TargetDetailView.java`
3. `backend/src/main/java/cn/npdb/entity/BioResourceDetailView.java`（新增）
4. `backend/src/main/java/cn/npdb/entity/PrescriptionDetailView.java`（新增）
5. `backend/src/main/java/cn/npdb/entity/Disease.java`（新增）
6. `backend/src/main/java/cn/npdb/mapper/*`（新增/调整）
7. `backend/src/main/java/cn/npdb/controller/*`（新增/调整）
8. `backend/src/main/java/cn/npdb/dto/StatsResponse.java`
9. `backend/src/main/java/cn/npdb/controller/StatsController.java`
10. `scripts/database/*`（视图与字段升级脚本）

## 需要你确认的信息
- 后端当前数据库是否已执行 `scripts/database/optimize_table_structure.sql` 或其他 v2 升级脚本？
- 你希望 API 保持当前路径不变，还是新增 `/api/bio-resources`、`/api/prescriptions`、`/api/diseases` 等 REST 路由？
- 疾病相关接口的字段与关联范围（仅生物资源关联，还是也要天然产物/靶点？）

## 下一步执行方式
- 如果你确认该计划可行，我将按 Phase 0 → Phase 4 依次实施并在每个阶段输出变更摘要。
