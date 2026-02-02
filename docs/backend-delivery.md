# 后端交付说明（外包交付参考）

> 目标：保证你与外包团队对“交付物/可运行方式/验收入口”有统一认识。

---

## 一、交付物清单（必须提供）

- 后端代码：`backend/`
- 启动说明：包含 Java 17 / Maven / PostgreSQL 前置条件
- 环境变量说明：`DB_USER` / `DB_PASSWORD`
- Swagger 入口地址说明
- API 示例或 Postman Collection
- 验收记录模板：`docs/backend-acceptance.md`

---

## 二、启动方式（示例）

```bash
DB_USER=your_user DB_PASSWORD=your_password \
  mvn -f backend/pom.xml spring-boot:run -DskipTests
```

默认端口：`8080`

如部署在服务器上，可使用服务器 IP 访问，例如：`http://<server-ip>:8080/swagger-ui.html`。

---

## 三、Swagger 文档入口

- `http://localhost:8080/swagger-ui.html`
- 或 `http://localhost:8080/swagger-ui/index.html`

---

## 四、快速验证接口（示例）

```bash
# 健康检查
curl -s -i http://localhost:8080/api/health

# 数据统计
curl -s -i http://localhost:8080/api/stats

# 天然产物列表
curl -s -i "http://localhost:8080/api/natural-products?page=1&pageSize=5"

# 靶点列表
curl -s -i "http://localhost:8080/api/targets?page=1&pageSize=5"

# 搜索
curl -s -i "http://localhost:8080/api/search?q=IC50&type=all"
```

---

## 五、筛选字段（最小版）

- `mwMin/mwMax`
- `xlogpMin/xlogpMax`
- `psaMin/psaMax`
- `activityType`
- `activityMaxNm`
- `targetType`
- `hasToxicity`

---

## 六、验收入口

- 验收表格：`docs/backend-acceptance.md`
- 详细计划：`docs/backend-plan.md`
- 数据库结构：`docs/database.md`
