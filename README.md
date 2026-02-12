# Natural Product Database

天然产物数据库 - 基于 NPASS 3.0 数据的天然产物、活性、靶点、生物资源展示与检索平台

## 项目架构

- **前端**: Vue 3 + TypeScript (`frontend/web/`)
- **后端**: Java + Spring Boot 3.2.5 + MyBatis-Plus 3.5.5
- **数据库**: PostgreSQL 16
- **缓存**: Redis (可选，尚未启用)
- **鉴权**: V1 不做登录

数据库连接（默认）:
- 主机: 127.0.0.1
- 端口: 5432
- 数据库: npdb
- 用户名: yfguo
- 密码: npdb2024

## 目录结构

```
NPdatabase/
├── docs/                           # 项目文档
│   ├── startup-guide.md            # 详细服务启动指南（推荐）
│   └── archived/                   # 历史/归档文档
├── data/                           # 多源数据文件
│   ├── NPASS/                      # NPASS 3.0 数据
│   ├── TCMID/                      # TCMID 中药数据
│   ├── CMAUP/                      # CMAUP 中药材数据
│   └── TTD/                        # TTD 靶点数据
├── backend/                        # Spring Boot 后端
├── frontend/                       # 前端应用
│   └── web/                        # Vue 3 Web 应用
├── scripts/                        # 脚本集合
│   ├── backend-service.sh          # 服务管理脚本
│   └── data-import/                # 数据导入脚本
└── CLAUDE.md                       # Claude Code 开发指南
```

## 当前状态

### ✅ 已完成
- [x] 需求文档整理（简化版 + 完整版）
- [x] 数据文件准备（NPASS 3.0）
- [x] 项目结构规划
- [x] Vue 3 前端应用结构
- [x] 数据库表结构优化与数据处理完成
- [x] 后端项目初始化（Spring Boot + MyBatis-Plus）
- [x] 核心 API 实现（天然产物/靶点/生物资源/搜索/统计）
- [x] Swagger 文档与校验说明
- [x] 多源数据整合（NPASS + TCMID + CMAUP + TTD）
- [x] 数据导入脚本与验证报告
- [x] 服务管理脚本（backend-service.sh）
- [x] 启动指南文档（docs/startup-guide.md）

### 🚧 进行中
- [ ] 前端联调与页面完善
- [ ] 生物资源详情页完善
- [ ] 疾病关联展示
- [ ] 高级搜索（结构/相似性）功能

## 快速开始

### 📋 前置要求

在启动服务之前，请确保已安装：
- ✅ **Java 17 或更高版本**
- ✅ **Maven 3.6 或更高版本**
- ✅ **Node.js 16 或更高版本**
- ✅ **PostgreSQL 16 数据库**

### 1. 克隆项目

```bash
git clone <repository-url>
cd NPdatabase
```

### 2. 设置数据库

**方式一：从头构建数据库**

```bash
# 创建数据库
createdb -U postgres npdb

# 导入结构
psql -U postgres -d npdb -f scripts/database/exports/01_schema_full.sql
```

**方式二：使用已有数据库（已完成初始化与导入）**

数据库默认配置见“项目架构”部分。

### 3. 启动服务

**方式一：使用启动脚本（推荐）**

```bash
# 一键启动后端和前端服务
bash scripts/backend-service.sh start

# 查看服务状态
bash scripts/backend-service.sh status

# 停止服务
bash scripts/backend-service.sh stop

# 重启服务
bash scripts/backend-service.sh restart

# 查看日志
bash scripts/backend-service.sh logs
```

启动成功后访问：
- 前端页面：http://localhost:3001
- 后端API文档：http://localhost:8080/swagger-ui.html

**方式二：手动启动**

启动后端：
```bash
# 在项目根目录执行
DB_USER=yfguo DB_PASSWORD=npdb2024 mvn -f backend/pom.xml spring-boot:run -DskipTests
```

启动前端（新开终端）：
```bash
# 在项目根目录执行
cd frontend/web
npm install  # 首次运行需要安装依赖
npm run dev -- --host 0.0.0.0 --port 3001
```

### 4. 访问应用

- **前端页面**：http://localhost:3001
- **后端API文档**：http://localhost:8080/swagger-ui.html
- **API接口**：http://localhost:8080/api/

## 📚 文档导航

- **[README.md](README.md)** ⭐ - 项目介绍与快速开始
- **[quick-start.md](quick-start.md)** ⭐ - 快速启动指南
- **[docs/startup-guide.md](docs/startup-guide.md)** ⭐ - 详细服务启动指南
- **[CLAUDE.md](CLAUDE.md)** - 开发指南与最新项目信息
- **[docs/requirements-simplified.md](docs/requirements-simplified.md)** - 需求文档
- **[data/README.md](data/README.md)** - 数据文件说明

## 数据库备份与恢复

如需备份或迁移，请使用 `pg_dump`/`psql`：

```bash
# 导出并压缩
pg_dump -h localhost -U yfguo -d npdb --clean --if-exists --create | gzip -9 > data/npdb_backup_$(date +%Y%m%d).sql.gz

# 从压缩文件恢复
gunzip -c data/npdb_backup_YYYYMMDD.sql.gz | psql -h localhost -U yfguo
```

## ❓ 常见问题

### 1. 端口被占用

**问题**：启动时提示端口 8080 或 3001 被占用

**解决方案**：
```bash
# 使用脚本自动清理并重启
bash scripts/backend-service.sh restart

# 或手动查找并终止占用端口的进程
lsof -ti:8080 | xargs kill -9  # 清理后端端口
lsof -ti:3001 | xargs kill -9  # 清理前端端口
```

### 2. 数据库连接失败

**问题**：后端日志显示数据库连接错误

**解决方案**：
1. 检查 PostgreSQL 是否正在运行：
   ```bash
   sudo systemctl status postgresql
   ```

2. 确认数据库配置正确（默认：用户名 `yfguo`，密码 `npdb2024`）

3. 使用自定义配置启动：
   ```bash
   DB_USER=your_user DB_PASSWORD=your_password bash scripts/backend-service.sh start
   ```

### 3. 前端无法加载数据

**问题**：前端页面打开但无法显示数据

**解决方案**：
1. 确认后端服务已启动：
   ```bash
   bash scripts/backend-service.sh status
   ```

2. 测试后端API是否响应：
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
```bash
# 清理并重新构建
mvn -f backend/pom.xml clean
mvn -f backend/pom.xml dependency:resolve
bash scripts/backend-service.sh start
```

### 5. npm 依赖问题

**问题**：前端启动时 npm 报错

**解决方案**：
```bash
# 重新安装依赖
cd frontend/web
rm -rf node_modules package-lock.json
npm install
cd ../..
bash scripts/backend-service.sh start
```

**更多问题请参考 [docs/startup-guide.md](docs/startup-guide.md)**

## 参考文档

前端应用文档位于 `frontend/web/README.md`：
- Vue 3 + TypeScript 架构
- 页面组件说明
- API 集成指南
- 路由配置

**注意**: 前端使用 Vue 3 框架，已完成基础结构搭建

## 开发指南

以 `CLAUDE.md` 为准（包含最新的架构、数据源、数据库与开发约定）。

## 联系方式

项目负责人: 郭洋帆
