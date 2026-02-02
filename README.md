# Natural Product Database

天然产物数据库 - 基于 NPASS 3.0 数据的化合物、活性、靶点展示与检索平台

## 项目架构

- **前端**: Vue 3 + TypeScript (`frontend/web/`)
- **后端**: Java + Spring Boot + MyBatis-Plus
- **数据库**: PostgreSQL
- **缓存**: Redis (可选)
- **鉴权**: V1 不做登录

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
├── data/                    # NPASS 3.0 原始数据
│   ├── NPASS3.0_naturalproducts_generalinfo.txt
│   ├── NPASS3.0_activities.txt
│   ├── NPASS3.0_target.txt
│   └── ...
├── backend/                 # Spring Boot 后端项目（已完成）
├── frontend/                # 前端应用
│   └── web/                 # Vue 3 Web 应用
├── scripts/                 # 数据处理脚本
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

### 🚧 进行中
- [ ] 前端联调与页面完善

## 快速开始

**新成员请先阅读 [SETUP.md](SETUP.md) 获取完整的环境设置指南！**

### 1. 克隆项目

```bash
git clone <repository-url>
cd NPdatabase
```

### 2. 设置数据库

```bash
# 创建数据库
createdb -U postgres npdb

# 导入结构
psql -U postgres -d npdb -f scripts/database/exports/01_schema_full.sql

# 导入示例数据（快速开始）
cd scripts/database/exports/
psql -U postgres -d npdb -f 02_import_sample_data.sql
```

### 3. 启动后端

```bash
cd backend
export DB_USER=postgres
export DB_PASSWORD=your_password
mvn spring-boot:run -DskipTests
```

访问 http://localhost:8080/swagger-ui.html 查看 API 文档

### 4. 启动前端

```bash
cd frontend/web
npm install
npm run dev
```

访问 http://localhost:3001

## 📚 文档导航

- **[SETUP.md](SETUP.md)** - 环境设置指南（新成员必读）
- **[CLAUDE.md](CLAUDE.md)** - AI 辅助开发指南
- **[docs/database.md](docs/database.md)** - 数据库结构说明
- **[docs/backend-dev-doc.md](docs/backend-dev-doc.md)** - 后端 API 文档
- **[docs/requirements-simplified.md](docs/requirements-simplified.md)** - 项目需求
- **[data/README.md](data/README.md)** - 数据文件获取说明

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

项目负责人: [待补充]
