# 后端开发文档（实现说明）

**适用读者**: 外包开发团队、后续接手维护人员

**更新日期**: 2026-01-29

---

## 1. 项目概述

- **后端框架**: Spring Boot 3.2.5
- **ORM**: MyBatis-Plus 3.5.5
- **数据库**: PostgreSQL 16
- **V1 策略**: 无登录、只读查询

---

## 2. 代码结构（实际目录）

```
backend/
└── src/main/java/cn/npdb/
    ├── controller/   # 接口层
    ├── service/      # 业务接口
    ├── service/impl/ # 业务实现
    ├── mapper/       # MyBatis-Plus Mapper
    ├── entity/       # 表/视图实体
    ├── dto/          # 请求参数对象
    ├── common/       # 统一响应/异常处理
    └── config/       # MyBatis-Plus 与分页配置
```

资源文件：`backend/src/main/resources/application.yml`

---

## 3. 配置说明

### 3.1 数据库连接（环境变量优先）

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/npdb
    username: ${DB_USER:postgres}
    password: ${DB_PASSWORD:}
```

启动示例：
```bash
DB_USER=your_user DB_PASSWORD=your_password \
  mvn -f backend/pom.xml spring-boot:run -DskipTests
```

### 3.2 Swagger

- 入口：`/swagger-ui.html`
- OpenAPI：`/v3/api-docs`

---

## 4. 统一返回格式

所有接口返回统一结构：
```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

分页结构：
```json
{
  "records": [],
  "page": 1,
  "pageSize": 20,
  "total": 0
}
```

---

## 5. 核心实体与视图

- **天然产物**: `natural_products`
- **靶点**: `targets`
- **活性**: `bioactivity`
- **毒性**: `toxicity`
- **来源**: `bio_resources` / `bio_resource_natural_products`
- **处方**: `prescriptions` / `prescription_resources` / `prescription_natural_products`（预留）

**详情视图**:
- `v_natural_product_detail`
- `v_target_detail`

详见：`docs/database.md`

---

## 6. 已实现 API（V1）

### 6.1 基础
- `GET /api/health`
- `GET /api/stats`

### 6.2 天然产物
- `GET /api/natural-products`
- `GET /api/natural-products/{npId}`
- `GET /api/natural-products/{npId}/bioactivity`
- `GET /api/natural-products/{npId}/targets`
- `GET /api/natural-products/{npId}/bio-resources`
- `GET /api/natural-products/{npId}/toxicity`

### 6.3 靶点
- `GET /api/targets`
- `GET /api/targets/{targetId}`
- `GET /api/targets/{targetId}/natural-products`

### 6.4 搜索
- `GET /api/search?q=...&type=natural_product|target|all`

---

## 7. 列表筛选参数（天然产物）

| 参数 | 说明 | 备注 |
|---|---|---|
| page | 页码 | 默认 1 |
| pageSize | 每页数量 | 默认 20 |
| mwMin / mwMax | 分子量范围 | double |
| xlogpMin / xlogpMax | XLogP 范围 | double |
| psaMin / psaMax | PSA 范围 | double |
| activityType | 活性类型 | IC50/EC50/Ki/Kd |
| activityMaxNm | 活性阈值（nM） | 走 `activity_value_std` |
| targetType | 靶点类型 | 取值来自 `targets.target_type` |
| hasToxicity | 是否有毒性 | true/false |

**稳定排序**: 列表统一 `ORDER BY id DESC`。

---

## 8. 性能优化点

- **索引**: `bioactivity(activity_type, activity_value_std)`
- **视图**: 详情接口使用聚合视图，减少多表 JOIN

如需进一步优化：可考虑统计缓存或物化视图。

---

## 9. 错误处理与日志

- 全局异常处理类：`cn/npdb/common/GlobalExceptionHandler`
- 统一返回错误码：`ApiCode`
- 建议在生产环境追加日志输出与告警

---

## 10. 维护与扩展建议

- **字段扩展**: 新字段优先加在表中，并同步实体/VO
- **过滤扩展**: 新筛选条件需在 DTO + Mapper QueryWrapper 中同时维护
- **新模块**: 新增实体建议按 `entity → mapper → service → controller` 结构添加

---

## 11. 常见问题

- **targetType=Protein 返回空**：数据库中实际值为 `Individual protein` / `Single protein` / `Protein complex`。
- **8080 端口占用**：使用 `ss -ltnp | rg ":8080"` 排查占用后重启。

---

## 参考文档

- 后端开发日志：`docs/backend-dev-log.md`
- 后端交付说明：`docs/backend-delivery.md`
- Swagger 校验：`docs/swagger-validation.md`
- 数据库结构：`docs/database.md`
