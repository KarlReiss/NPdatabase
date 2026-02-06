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
   bash scripts/backend-service.sh start
   ```

3. **等待启动完成**
   - 后端服务启动需要约 30-60 秒
   - 前端服务启动需要约 10-20 秒
   - 看到以下信息表示启动成功：
     ```
     npdb-backend 启动成功，PID: xxxxx
     访问地址：http://localhost:8080
     Swagger文档：http://localhost:8080/swagger-ui.html

     npdb-frontend 启动成功，PID: xxxxx
     访问地址：http://localhost:3001
     ```

4. **访问应用**
   - 前端页面：http://localhost:3001
   - 后端API文档：http://localhost:8080/swagger-ui.html

### 方法二：手动启动

如果启动脚本无法使用，可以手动启动：

#### 启动后端

```bash
# 在项目根目录执行
cd /home/yfguo/NPdatabase
DB_USER=yfguo DB_PASSWORD=npdb2024 mvn -f backend/pom.xml spring-boot:run -DskipTests
```

#### 启动前端（新开一个终端）

```bash
# 在项目根目录执行
cd /home/yfguo/NPdatabase/frontend/web
npm run dev -- --host 0.0.0.0 --port 3001
```

## 🛑 停止服务

### 使用脚本停止

```bash
bash scripts/backend-service.sh stop
```

### 手动停止

在运行服务的终端窗口按 `Ctrl + C`

## 🔄 重启服务

如果服务出现问题，可以重启：

```bash
bash scripts/backend-service.sh restart
```

## 📊 查看服务状态

检查服务是否正在运行：

```bash
bash scripts/backend-service.sh status
```

输出示例：
```
==========================================
服务状态
==========================================
✓ npdb-backend 运行中
  PID: 12345
  端口: 8080
  访问: http://localhost:8080

✓ npdb-frontend 运行中
  PID: 12346
  端口: 3001
  访问: http://localhost:3001
==========================================
```

## 📝 查看日志

### 查看后端日志

```bash
bash scripts/backend-service.sh logs
```

### 查看前端日志

```bash
bash scripts/backend-service.sh logs frontend
```

按 `Ctrl + C` 退出日志查看。

## ⚙️ 端口配置

默认端口配置：
- **后端端口**：8080
- **前端端口**：3001

如果需要修改端口（高级用户）：

```bash
# 自定义端口启动
SERVER_PORT=9090 FRONTEND_PORT=4000 bash scripts/backend-service.sh start
```

## ❓ 常见问题

### 1. 端口被占用

**问题**：启动时提示端口被占用

**解决方案**：
- 脚本会自动清理占用的端口
- 如果自动清理失败，手动停止服务后重新启动：
  ```bash
  bash scripts/backend-service.sh stop
  bash scripts/backend-service.sh start
  ```

### 2. 数据库连接失败

**问题**：后端日志显示数据库连接错误

**解决方案**：
1. 检查 PostgreSQL 是否正在运行：
   ```bash
   sudo systemctl status postgresql
   ```

2. 检查数据库用户名和密码是否正确
   - 默认用户名：`yfguo`
   - 默认密码：`npdb2024`

3. 如果需要修改数据库配置：
   ```bash
   DB_USER=your_user DB_PASSWORD=your_password bash scripts/backend-service.sh start
   ```

### 3. 前端无法访问后端

**问题**：前端页面打开但无法加载数据

**解决方案**：
1. 确认后端服务已启动：
   ```bash
   bash scripts/backend-service.sh status
   ```

2. 检查后端是否正常响应：
   ```bash
   curl http://localhost:8080/api/stats/overview
   ```

3. 查看后端日志排查错误：
   ```bash
   bash scripts/backend-service.sh logs
   ```

### 4. Maven 构建失败

**问题**：后端启动时 Maven 报错

**解决方案**：
1. 清理 Maven 缓存：
   ```bash
   mvn -f backend/pom.xml clean
   ```

2. 重新下载依赖：
   ```bash
   mvn -f backend/pom.xml dependency:resolve
   ```

3. 重新启动：
   ```bash
   bash scripts/backend-service.sh start
   ```

### 5. npm 依赖问题

**问题**：前端启动时 npm 报错

**解决方案**：
1. 重新安装依赖：
   ```bash
   cd frontend/web
   rm -rf node_modules package-lock.json
   npm install
   ```

2. 返回项目根目录重新启动：
   ```bash
   cd /home/yfguo/NPdatabase
   bash scripts/backend-service.sh start
   ```

## 🔧 高级配置

### 环境变量说明

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DB_USER` | 数据库用户名 | yfguo |
| `DB_PASSWORD` | 数据库密码 | npdb2024 |
| `SERVER_ADDRESS` | 后端绑定地址 | 0.0.0.0 |
| `SERVER_PORT` | 后端端口 | 8080 |
| `FRONTEND_HOST` | 前端绑定地址 | 0.0.0.0 |
| `FRONTEND_PORT` | 前端端口 | 3001 |

### 自定义配置示例

```bash
# 使用自定义数据库和端口
DB_USER=myuser \
DB_PASSWORD=mypassword \
SERVER_PORT=9090 \
FRONTEND_PORT=4000 \
bash scripts/backend-service.sh start
```

## 📞 获取帮助

查看脚本帮助信息：

```bash
bash scripts/backend-service.sh
```

或

```bash
bash scripts/backend-service.sh --help
```

## 📚 相关文档

- [数据库文档](database.md) - 数据库结构说明
- [后端开发文档](backend-dev-doc.md) - 后端 API 详细说明
- [项目说明](../CLAUDE.md) - 项目整体说明

---

**提示**：如果遇到问题，请先查看日志文件：
- 后端日志：`backend/logs/backend.log`
- 前端日志：`frontend/web/logs/frontend.log`
