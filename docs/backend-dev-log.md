# 后端开发日志（对外合作记录）

**项目**: Natural Product Database (NPdatabase)

**更新日期**: 2026-01-29

---

## 一、开发概览

- **技术栈**: Spring Boot 3.2.5 + MyBatis-Plus 3.5.5 + PostgreSQL 16
- **V1 范围**: 无登录，开放查询
- **数据结构基线**: `docs/database.md`（已包含 `optimize_table_structure.sql` 的变更）

---

## 二、时间线（关键节点）

| 日期 | 事项 | 结果 |
|---|---|---|
| 2026-01-29 | 数据库脚本与表结构核对 | 按 `schema.sql` → `add_prescription_bioresource.sql` → `optimize_table_structure.sql` 执行完成 |
| 2026-01-29 | 后端项目创建与依赖配置 | `backend/` 项目可启动 |
| 2026-01-29 | 实体/Mapper/Service 骨架 | 完成核心实体映射 |
| 2026-01-29 | 核心 API 实现 | 完成天然产物、靶点、搜索、统计接口 |
| 2026-01-29 | 性能优化 | 新增索引 `idx_bioactivity_type_value_std` |
| 2026-01-29 | Swagger 验证 | 可访问并可验证接口 |

---

## 三、关键实现与决策

- **视图实体**: 详情类使用视图 `v_natural_product_detail` / `v_target_detail` 以减少多表复杂 JOIN。
- **分页稳定性**: 列表接口统一加 `ORDER BY id DESC`，避免分页抖动。
- **活性筛选**: `activity_value_std` 统一以 nM 进行筛选。
- **索引优化**: `bioactivity(activity_type, activity_value_std)` 用于常见活性筛选。

---

## 四、问题与修复记录

1. **MyBatis 报错 `factoryBeanObjectType`**
   - 处理：补充依赖 `mybatis-spring 3.0.3`。
2. **8080 端口占用**
   - 处理：释放占用进程后重启。
3. **Swagger 调用 500**
   - 处理：重启服务后恢复，已增加全局异常日志输出。
4. **targetType=Protein 返回空**
   - 说明：库内实际为 `Individual protein` / `Single protein` / `Protein complex` 等枚举值。

---

## 五、验证记录（已通过）

- `GET /api/health` → 200
- `GET /api/stats` → 200
- `GET /api/natural-products?page=1&pageSize=3` → 200
- `GET /api/natural-products/{npId}` → 200
- `GET /api/targets?page=1&pageSize=3` → 200
- `GET /api/search?q=IC50&type=all` → 200

**接口示例**:
```bash
curl -s -i http://localhost:8080/api/health
curl -s -i http://localhost:8080/api/stats
curl -s -i "http://localhost:8080/api/natural-products?page=1&pageSize=3"
curl -s -i "http://localhost:8080/api/targets?page=1&pageSize=3"
curl -s -i "http://localhost:8080/api/search?q=IC50&type=all"
```

---

## 六、运行环境

- Java: OpenJDK 17
- Maven: 3.8.7
- PostgreSQL: 16
- 启动命令：
```bash
DB_USER=your_user DB_PASSWORD=your_password \
  mvn -f backend/pom.xml spring-boot:run -DskipTests
```

---

## 七、交付文档列表

- 开发计划（检查清单）：`docs/backend-plan.md`
- 验收表格：`docs/backend-acceptance.md`
- 交付说明：`docs/backend-delivery.md`
- Swagger 校验：`docs/swagger-validation.md`
- 数据库结构：`docs/database.md`

---

## 八、待办与建议

- 前端联调与真实数据展示
- 数据质量与字段补齐（理化属性）
- 可选：统计缓存 / 物化视图 / 运维脚本
