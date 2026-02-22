# NPdatabase 服务启动指南

> 本指南面向不熟悉编程的用户，提供简单易懂的服务启动步骤。

## 📋 前置要求

在启动服务之前，请确保已安装以下软件：

- ✅ **Java 17 或更高版本**
- ✅ **Maven 3.6 或更高版本**
- ✅ **Node.js 16 或更高版本**
- ✅ **PostgreSQL 16 数据库**
- ✅ **数据库已创建并导入数据**

## 🚀 快速启动（推荐）

### 方法一：使用启动脚本（最简单）

1. **打开终端**
   - 在项目根目录 `/home/yfguo/NPdatabase` 下打开终端

2. **启动服务**
   ```bash
   bash npdb.sh start
   ```

3. **等待启动完成**
   - 后端服务启动需要约 30-60 秒
   - 前端服务启动需要约 10-20 秒
   - 看到以下信息表示启动成功：
     ```
     ✓ 后端启动成功
       API: http://localhost:8080
       Swagger: http://localhost:8080/swagger-ui.html

     ✓ 前端启动成功
       访问: http://localhost:3001
     ```

4. **访问应用**
   - 前端页面：http://localhost:3001
   - 后端API文档：http://localhost:8080/swagger-ui.html

### 方法二：手动启动

如果启动脚本无法使用，可以手动启动：

#### 启动后端

```bash
cd /home/yfguo/NPdatabase
DB_USER=yfguo DB_PASSWORD=npdb2024 mvn -f backend/pom.xml spring-boot:run -DskipTests
```

#### 启动前端（新开一个终端）

```bash
cd /home/yfguo/NPdatabase/frontend/web
npm run dev -- --host 0.0.0.0 --port 3001
```

## 🛑 停止服务

```bash
bash npdb.sh stop
```

手动停止：在运行服务的终端窗口按 `Ctrl + C`

## 🔄 重启服务

```bash
bash npdb.sh restart
```

## 📊 查看服务状态

```bash
bash npdb.sh status
```

## 📝 查看日志

```bash
bash npdb.sh logs            # 后端日志
bash npdb.sh logs frontend   # 前端日志
```

按 `Ctrl + C` 退出日志查看。

## ⚙️ 默认配置

- **后端端口**：8080
- **前端端口**：3001
- **数据库用户**：yfguo
- **数据库密码**：npdb2024

如需修改配置，直接编辑 `npdb.sh` 文件开头的配置部分。

## ❓ 常见问题

### 1. 端口被占用

**解决方案**：先停止服务再启动
```bash
bash npdb.sh stop
bash npdb.sh start
```

### 2. 数据库连接失败

**解决方案**：
1. 检查 PostgreSQL 是否正在运行：
   ```bash
   sudo systemctl status postgresql
   ```
2. 确认数据库配置正确（默认用户名 `yfguo`，密码 `npdb2024`）

### 3. 前端无法访问后端

**解决方案**：
1. 确认后端服务已启动：`bash npdb.sh status`
2. 测试后端响应：`curl http://localhost:8080/api/stats/overview`
3. 查看后端日志：`bash npdb.sh logs`

### 4. Maven 构建失败

**解决方案**：
```bash
mvn -f backend/pom.xml clean
mvn -f backend/pom.xml dependency:resolve
bash npdb.sh start
```

### 5. npm 依赖问题

**解决方案**：
```bash
cd frontend/web
rm -rf node_modules package-lock.json
npm install
cd ../..
bash npdb.sh start
```

## 📞 获取帮助

```bash
bash npdb.sh
```

## 📚 相关文档

- [快速启动卡片](../quick-start.md) - 常用命令速查
- [项目说明](../CLAUDE.md) - 项目整体说明

---

**提示**：如果遇到问题，请先查看日志文件：
- 后端日志：`backend/logs/backend.log`
- 前端日志：`frontend/web/logs/frontend.log`
