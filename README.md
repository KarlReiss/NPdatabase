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
