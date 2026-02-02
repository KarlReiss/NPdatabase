# 下一步开发计划

## 📋 项目概览

**当前状态**: 数据库表结构与数据已完成，文档已同步更新（见 `docs/database.md`）

**技术栈**:
- 前端: 现有原型在 `frontend/prototype-react/`，具体框架待定
- 后端: Java + Spring Boot + MyBatis-Plus
- 数据库: PostgreSQL
- 缓存: Redis (可选)
- 鉴权: V1 不做登录

---

## 🎯 Phase 1: 数据库与数据（已完成，可重复执行）

### 1.1 建表脚本执行顺序
**推荐顺序**（与最终表结构一致）：
```bash
psql npdb < scripts/database/schema.sql
psql npdb < scripts/database/add_prescription_bioresource.sql
psql npdb < scripts/database/optimize_table_structure.sql
```

**最终核心表（9 张）**:
- `natural_products`（原 `compounds`）
- `targets`
- `bioactivity`
- `toxicity`
- `bio_resources`
- `bio_resource_natural_products`
- `prescriptions`
- `prescription_resources`
- `prescription_natural_products`

**视图（4 个）**:
- `v_natural_product_detail`
- `v_bio_resource_detail`
- `v_target_detail`
- `v_prescription_detail`

> 详细字段、索引、视图说明请参考 `docs/database.md`。

### 1.2 数据导入脚本
当前已有数据导入脚本位于 `scripts/database/`（按需执行）：
- `import_natural_products.py`
- `import_targets.py`
- `import_bioactivity.py`
- `import_toxicity.py`
- `import_bio_resources.py`
- `import_bio_resource_natural_products.py`

---

## 🎯 Phase 2: 后端项目初始化（第 1 周）

### 2.1 Spring Boot 初始化
**依赖建议**:
- spring-boot-starter-web
- mybatis-plus-boot-starter
- postgresql
- spring-boot-starter-validation
- lombok
- springdoc-openapi-starter-webmvc-ui

**基础配置要点**:
- `map-underscore-to-camel-case: true`
- MyBatis-Plus 分页插件
- 统一响应体与全局异常处理

### 2.2 项目结构（建议）
```
backend/
├── src/main/java/com/npdb/
│   ├── controller/
│   ├── service/
│   ├── mapper/
│   ├── entity/
│   ├── dto/
│   ├── vo/
│   └── common/
└── src/main/resources/
    ├── application.yml
    └── mapper/
```

---

## 🎯 Phase 3: 核心 API 开发（第 2-3 周）

### 3.1 天然产物（natural_products）
- `GET /api/natural-products`（分页 + 筛选 + 排序）
- `GET /api/natural-products/{npId}`
- `GET /api/natural-products/{npId}/bioactivity`
- `GET /api/natural-products/{npId}/targets`
- `GET /api/natural-products/{npId}/bio-resources`
- `GET /api/natural-products/{npId}/toxicity`

### 3.2 靶点（targets）
- `GET /api/targets`
- `GET /api/targets/{targetId}`
- `GET /api/targets/{targetId}/natural-products`

### 3.3 全局搜索 & 统计
- `GET /api/search?q=...&type=natural_product|target|all`
- `GET /api/stats`（首页统计概览）

---

## 🎯 Phase 4: 联调与优化（第 4 周）

- 与前端原型对齐字段输出（VO/DTO）
- 查询性能优化（索引、视图、分页）
- Swagger/OpenAPI 文档完善
- 测试（Service 单测 + MockMvc 集成测试）

---

## 🧾 参考文档

- 数据库结构说明：`docs/database.md`
- 简化版需求文档：`docs/requirements-simplified.md`
- 完整需求文档：`docs/requirements-full.md`
