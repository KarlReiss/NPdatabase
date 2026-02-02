# 后端开发步骤（检查清单版，面向非程序员）

> 读者：你（数据分析研究人员）+ 外包开发团队
>
> 目标：把后端开发拆成“可验收的步骤”，你只需逐条检查结果。
>
> 适用范围：
> - 数据库：PostgreSQL
> - ORM：MyBatis-Plus
> - V1 不做登录
> - 数据结构以 `docs/database.md` 为准（已包含优化脚本变更）
>
> **执行状态**：本计划已完成并验收通过，过程记录见 `docs/backend-dev-log.md`。

---

## 一、关键约定（先读 2 分钟）

- **最终表名**：`natural_products`（原 `compounds` 已改名）
- **来源表**：`bio_resources`（替代原 `species`）
- **关联表**：`bio_resource_natural_products`
- **对外业务 ID**：`np_id` / `target_id` / `resource_id` / `prescription_id`
- **内部主键**：`id` 仅用于数据库关联

> 详细字段、索引、视图请查 `docs/database.md`

---

## 二、逐步检查清单（按顺序验收）

### 步骤 1：环境与软件可用

**外包执行**：检查 Java/Maven/PostgreSQL 是否可用。

**验收要点**：
- [ ] `java -version` 显示 Java 17
- [ ] `mvn -v` 正常输出
- [ ] `psql -V` 正常输出

**你需要看到的结果**：有截图或终端日志即可。

---

### 步骤 2：数据库结构核对（非常关键）

**外包执行**：按顺序执行建表脚本，并确认表/视图存在。

执行顺序：
```bash
psql npdb < scripts/database/schema.sql
psql npdb < scripts/database/add_prescription_bioresource.sql
psql npdb < scripts/database/optimize_table_structure.sql
```

验证命令：
```bash
psql npdb -c "\dt"
psql npdb -c "\dv"
```

**验收要点**：
- [ ] 最终表（9 张）全部出现：
  - `natural_products`, `targets`, `bioactivity`, `toxicity`
  - `bio_resources`, `bio_resource_natural_products`
  - `prescriptions`, `prescription_resources`, `prescription_natural_products`
- [ ] 视图（4 个）全部出现：
  - `v_natural_product_detail`, `v_bio_resource_detail`
  - `v_target_detail`, `v_prescription_detail`

**你需要看到的结果**：
- `\dt` 与 `\dv` 的输出截图或粘贴文本

---

### 步骤 3：后端项目创建（Spring Boot）

**外包执行**：创建 `backend/` 项目并可运行。

**必选依赖**：
- Spring Web
- MyBatis-Plus
- PostgreSQL Driver
- Validation
- Lombok
- springdoc-openapi

**验收要点**：
- [ ] 项目位于 `backend/`
- [ ] 能启动：`mvn spring-boot:run`

**你需要看到的结果**：
- 启动成功日志截图（无报错）

---

### 步骤 4：数据库连接配置

**外包执行**：配置 `application.yml` 并连通数据库。

关键配置：
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/npdb
    username: postgres
    password: your_password
    driver-class-name: org.postgresql.Driver
```

**验收要点**：
- [ ] 应用启动后无数据库连接错误

**你需要看到的结果**：
- 启动日志中显示连接成功

---

### 步骤 5：接口规范与统一返回格式

**外包执行**：统一 JSON 返回格式与分页格式。

**验收要点**：
- [ ] 返回格式：`{ code, message, data }`
- [ ] 分页格式含 `records/page/pageSize/total`

**你需要看到的结果**：
- 任意接口示例响应（截图或文本）

---

### 步骤 6：核心实体映射（数据库表 → 代码）

**外包执行**：完成 Entity/Mapper/Service 基础结构。

**最小实体**：
- `NaturalProduct`（`natural_products`）
- `Target`（`targets`）
- `Bioactivity`（`bioactivity`）
- `Toxicity`（`toxicity`）
- `BioResource`（`bio_resources`）
- `BioResourceNaturalProduct`（`bio_resource_natural_products`）

**验收要点**：
- [ ] 对应类与表名一致
- [ ] 基础 CRUD 可用

**你需要看到的结果**：
- 类文件列表截图或目录结构说明

---

### 步骤 7：核心 API 实现（按模块）

#### 7.1 天然产物
- `GET /api/natural-products`
- `GET /api/natural-products/{npId}`
- `GET /api/natural-products/{npId}/bioactivity`
- `GET /api/natural-products/{npId}/targets`
- `GET /api/natural-products/{npId}/bio-resources`
- `GET /api/natural-products/{npId}/toxicity`

#### 7.2 靶点
- `GET /api/targets`
- `GET /api/targets/{targetId}`
- `GET /api/targets/{targetId}/natural-products`

#### 7.3 搜索与统计
- `GET /api/search?q=...&type=natural_product|target|all`
- `GET /api/stats`

**验收要点**：
- [ ] 接口可通过浏览器 / Postman 打开
- [ ] 返回 JSON 正常
- [ ] `np_id` / `target_id` 可正确查询

**你需要看到的结果**：
- 每个接口至少 1 个成功示例

---

### 步骤 8：筛选规则（最小版）

**建议最小筛选字段**：
- `mwMin/mwMax`
- `xlogpMin/xlogpMax`
- `psaMin/psaMax`
- `activityType`
- `activityMaxNm`
- `targetType`
- `hasToxicity`

**验收要点**：
- [ ] 活性阈值使用 `activity_value_std`（nM）
- [ ] 列表页能按筛选条件变化

---

### 步骤 9：性能与可读性保障

**外包执行**：确认视图与索引被正确使用。

**验收要点**：
- [ ] 列表查询 < 2s（常用筛选）
- [ ] 详情查询 < 2s
- [ ] 使用 `v_natural_product_detail` 进行统计字段读取
- [ ] 已创建组合索引 `idx_bioactivity_type_value_std`（`bioactivity(activity_type, activity_value_std)`）

---

### 步骤 10：交付与验收材料

**外包需要交付**：
- [ ] 后端代码（`backend/`）
- [ ] 可运行的启动说明（包含环境变量 `DB_USER` / `DB_PASSWORD`）
- [ ] Swagger 文档可访问（路径说明）
- [ ] API 示例或 Postman Collection
- [ ] 验收记录模板（`docs/backend-acceptance.md`）
- [ ] 交付说明文档（`docs/backend-delivery.md`）

**你需要看到的结果**：
- Swagger 地址可打开（`/swagger-ui.html` 或 `/swagger-ui/index.html`）
- 示例请求可复现
- 验收表格可直接填写（`docs/backend-acceptance.md`）

---

## 三、统一验收清单（总览版）

- [ ] 数据库结构与 `docs/database.md` 一致
- [ ] 后端项目可启动、无数据库错误
- [ ] `/api/natural-products` 可分页查询
- [ ] `/api/natural-products/{npId}` 可返回详情
- [ ] 关联接口（bioactivity/targets/bio-resources/toxicity）可用
- [ ] `/api/targets` 与 `/api/targets/{targetId}` 可用
- [ ] `/api/search` 可正常检索
- [ ] Swagger 文档可打开
- [ ] 索引优化完成（`idx_bioactivity_type_value_std`）

---

## 四、验收表格模板（可复制到 Excel/在线表格）

| 序号 | 步骤 | 交付物/结果 | 验收方式 | 验收人 | 状态 | 备注 |
|---|---|---|---|---|---|---|
| 1 | 环境可用 | Java/Maven/PostgreSQL 可用截图 | 查看日志/截图 | 你 | ☐ 通过 ☐ 不通过 | |
| 2 | 数据库结构 | 9 张表 + 4 视图截图 | `\dt`/`\dv` | 你 | ☐ 通过 ☐ 不通过 | |
| 3 | 后端可启动 | 启动日志截图 | 运行 `mvn spring-boot:run` | 你 | ☐ 通过 ☐ 不通过 | |
| 4 | DB 连接成功 | 无连接错误日志 | 启动日志 | 你 | ☐ 通过 ☐ 不通过 | |
| 5 | 基础接口 | API 返回 JSON | Postman/浏览器 | 你 | ☐ 通过 ☐ 不通过 | |
| 6 | 关联接口 | Bioactivity/Targets/Bio-resources | Postman/浏览器 | 你 | ☐ 通过 ☐ 不通过 | |
| 7 | 搜索接口 | `/api/search` 返回结果 | Postman/浏览器 | 你 | ☐ 通过 ☐ 不通过 | |
| 8 | Swagger 文档 | 可打开访问 | 浏览器 | 你 | ☐ 通过 ☐ 不通过 | |
| 9 | 性能指标 | 列表 < 2s | 实测/日志 | 你 | ☐ 通过 ☐ 不通过 | |
| 10 | 交付材料 | 代码 + 使用说明 + 示例 | 文件清单 | 你 | ☐ 通过 ☐ 不通过 | |

---

## 五、常见问题（非技术人员友好）

**Q1: 接口报 500 错误**
- 多数是数据库连接或 SQL 拼接问题，需要开发者排查日志

**Q2: 查询很慢**
- 检查是否使用视图（`v_natural_product_detail`）
- 检查索引是否存在

**Q3: 查不到数据**
- 检查是否导入数据
- 检查 `np_id` 拼写是否正确

---

## 参考文档

- `docs/database.md`（最终表结构）
- `docs/requirements-simplified.md`（一期需求）
- `docs/next-steps.md`（执行步骤）
