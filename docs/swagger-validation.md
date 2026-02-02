# Swagger 校验操作说明

> 目的：让你在本机快速验证 Swagger 是否可用、接口是否正常展示，并能通过“Try it out”执行。

---

## 一、前置条件

- Java 17
- Maven
- PostgreSQL 正常运行
- 数据库已导入数据

---

## 二、启动后端服务

```bash
DB_USER=your_user DB_PASSWORD=your_password \
  mvn -f /home/yfguo/NPdatabase/backend/pom.xml spring-boot:run -DskipTests
```

**看到以下日志说明启动成功**：
- `Tomcat started on port 8080`

---

## 三、打开 Swagger 页面

在浏览器中打开任一地址：
- `http://localhost:8080/swagger-ui.html`
- `http://localhost:8080/swagger-ui/index.html`

**验收点**：页面能打开并显示接口列表。

---

## 四、Swagger 页面必看内容

页面中应该看到这些接口分组（或对应 Controller 名称）：
- `/api/natural-products`
- `/api/targets`
- `/api/search`
- `/api/stats`
- `/api/health`

---

## 五、在 Swagger 里执行 3 个基础测试

### 1) 健康检查
- 接口：`GET /api/health`
- 操作：点击 **Try it out** → **Execute**
- 期望返回：
```json
{"code":0,"message":"success","data":"ok"}
```

### 2) 统计接口
- 接口：`GET /api/stats`
- 操作：**Try it out** → **Execute**
- 期望返回：包含各表的统计数字

### 3) 列表接口
- 接口：`GET /api/natural-products`
- 参数：`page=1`、`pageSize=3`
- 操作：**Try it out** → **Execute**
- 期望返回：`records` 数组 + `page/pageSize/total`

---

## 六、常见问题排查

### 1) Swagger 页面打不开
- 检查服务是否启动：
```bash
curl -i http://localhost:8080/api/health
```

### 2) 端口被占用
- 检查端口占用：
```bash
ss -ltnp | rg ":8080"
```

### 3) 访问路径错误
- 只需尝试下面两个地址：
  - `/swagger-ui.html`
  - `/swagger-ui/index.html`

---

## 七、验收记录建议

建议把下面内容截图或记录到 `docs/backend-acceptance.md`：
- Swagger 页面能打开
- Try it out 执行成功（至少 3 个接口）
- 返回 JSON 正常

---

如果你需要，我可以补充“Swagger 验收记录模板（可直接填写）”。

