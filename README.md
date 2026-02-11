# Natural Product Database

天然产物数据库 - 基于 NPASS 3.0 数据的化合物、活性、靶点展示与检索平台

## 项目架构

- **前端**: Vue 3 + TypeScript (`frontend/web/`)
- **后端**: Java + Spring Boot + MyBatis-Plus
- **数据库**: PostgreSQL
- **缓存**: Redis (可选)
- **鉴权**: V1 不做登录

数据库类型: PostgreSQL
主机地址: 127.0.0.1
端口: 5432
数据库名: npdb
用户名: yfguo
密码: npdb2024

## 目录结构

```
NPdatabase/
├── docs/                    # 项目文档
│   ├── database.md           # 数据库结构说明（最终结构）
│   ├── requirements-simplified.md   # 简化版需求文档（推荐先读）
│   ├── backend-dev-doc.md    # 后端开发文档（实现说明）
│   ├── backend-dev-log.md    # 后端开发日志（关键节点）
│   ├── archived/                    # 历史/归档文档
│   │   └── requirements-full.md     # 完整版需求文档
│   └── README.md
├── data/                    # NPASS 3.0 原始数据与数据库备份
│   ├── NPASS3.0_naturalproducts_generalinfo.txt
│   ├── NPASS3.0_activities.txt
│   ├── NPASS3.0_target.txt
│   ├── npdb_full_dump.sql.gz  # 完整数据库备份（压缩）
│   └── ...
├── backend/                 # Spring Boot 后端项目（已完成）
├── frontend/                # 前端应用
│   └── web/                 # Vue 3 Web 应用
├── scripts/                 # 数据处理脚本与服务管理
│   ├── backend-service.sh   # 服务启动/停止/重启脚本
│   └── database/            # 数据库脚本
└── CLAUDE.md               # Claude Code 开发指南
```

## 当前状态

### ✅ 已完成
- [x] 需求文档整理（简化版 + 完整版）
- [x] 数据文件准备（NPASS 3.0）
- [x] 项目结构规划
- [x] Vue 3 前端应用结构
- [x] 数据库表结构与数据处理完成
- [x] 后端项目初始化（Spring Boot + MyBatis-Plus）
- [x] 核心 API 实现（天然产物/靶点/搜索/统计）
- [x] Swagger 文档与校验说明
- [x] **CMAUP 与 NPASS 物种数据整合** (2026-02-05)
  - 整合了 CMAUP Plants (7,865条) 和 NPASS species (48,940条)
  - 匹配率: 100% (7,865/7,865)
  - 整合后总记录数: 49,054条
  - 匹配方法: 99.53% ID精确匹配, 0.47% 属科组合匹配
  - 输出文件: `data/processed/bio_resources_integrated.txt`
- [x] **完整数据库备份** (2026-02-06)
  - 导出完整的 npdb 数据库为 SQL 文件
  - 文件: `data/npdb_full_dump.sql.gz` (33MB 压缩，原始 164MB)
  - 包含所有表结构、数据、视图、索引和约束

### 🚧 进行中
- [ ] 前端联调与页面完善
- [ ] 将整合后的生物资源数据导入数据库

## 快速开始

### 📋 前置要求

在启动服务之前，请确保已安装：
- ✅ **Java 17 或更高版本**
- ✅ **Maven 3.6 或更高版本**
- ✅ **Node.js 16 或更高版本**
- ✅ **PostgreSQL 16 数据库**

**新成员请先阅读 [SETUP.md](SETUP.md) 获取完整的环境设置指南！**

### 1. 克隆项目

```bash
git clone <repository-url>
cd NPdatabase
```

### 2. 设置数据库

**方式一：使用完整数据库备份（推荐）**

```bash
# 解压并导入完整数据库（包含所有数据）
gunzip -c data/npdb_full_dump.sql.gz | psql -h localhost -U yfguo

# 或者分步操作
gunzip data/npdb_full_dump.sql.gz
psql -h localhost -U yfguo -f data/npdb_full_dump.sql
```

**方式二：从头构建数据库**

```bash
# 创建数据库
createdb -U postgres npdb

# 导入结构
psql -U postgres -d npdb -f scripts/database/exports/01_schema_full.sql

# 导入示例数据（快速开始）
cd scripts/database/exports/
psql -U postgres -d npdb -f 02_import_sample_data.sql
```

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

- **[docs/startup-guide.md](docs/startup-guide.md)** ⭐ - 服务启动指南（推荐）
- **[SETUP.md](SETUP.md)** - 环境设置指南（新成员必读）
- **[CLAUDE.md](CLAUDE.md)** - AI 辅助开发指南
- **[docs/database.md](docs/database.md)** - 数据库结构说明
- **[docs/backend-dev-doc.md](docs/backend-dev-doc.md)** - 后端 API 文档
- **[docs/requirements-simplified.md](docs/requirements-simplified.md)** - 项目需求
- **[data/README.md](data/README.md)** - 数据文件获取说明

## 数据库备份与恢复

项目提供完整的数据库备份文件 `data/npdb_full_dump.sql.gz`（33MB），包含：
- 所有表结构（natural_products、targets、bioactivity、toxicity、bio_resources等）
- 完整数据（约50万天然产物、100万生物活性记录）
- 所有视图、索引和约束

**恢复数据库：**
```bash
# 直接从压缩文件恢复
gunzip -c data/npdb_full_dump.sql.gz | psql -h localhost -U yfguo

# 或者先解压再导入
gunzip data/npdb_full_dump.sql.gz
psql -h localhost -U yfguo -f data/npdb_full_dump.sql
```

**创建新备份：**
```bash
# 导出并压缩
pg_dump -h localhost -U yfguo -d npdb --clean --if-exists --create | gzip -9 > data/npdb_backup_$(date +%Y%m%d).sql.gz
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

详见 `CLAUDE.md` 文件

## 联系方式

项目负责人: 郭洋帆
