# NPdatabase 项目设置指南

本指南帮助团队成员快速设置开发环境。

## 📋 前置要求

- **Java**: JDK 17+
- **Node.js**: 18+
- **PostgreSQL**: 16+
- **Maven**: 3.8+
- **Python**: 3.8+ (用于数据导入脚本)

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd NPdatabase
```

### 2. 设置数据库

#### 2.1 创建数据库

```bash
createdb -U postgres npdb
```

#### 2.2 导入数据库结构

```bash
psql -U postgres -d npdb -f scripts/database/exports/01_schema_full.sql
```

#### 2.3 导入数据

**选项 A: 使用示例数据（快速开始）**

```bash
cd scripts/database/exports/
psql -U postgres -d npdb -f 02_import_sample_data.sql
```

**选项 B: 导入完整数据**

1. 获取数据文件（见 `data/README.md`）
2. 运行导入脚本：

```bash
python scripts/database/import_natural_products.py
python scripts/database/import_targets.py
python scripts/database/import_bioactivity.py
python scripts/database/import_toxicity.py
python scripts/database/import_bio_resources.py
python scripts/database/import_bio_resource_natural_products.py
```

### 3. 启动后端

```bash
cd backend

# 设置数据库连接（根据实际情况修改）
export DB_USER=postgres
export DB_PASSWORD=your_password

# 启动服务
mvn spring-boot:run -DskipTests
```

后端将在 http://localhost:8080 启动

- Swagger UI: http://localhost:8080/swagger-ui.html
- API Docs: http://localhost:8080/v3/api-docs

### 4. 启动前端

```bash
cd frontend/web

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将在 http://localhost:3001 启动

## 🔧 配置说明

### 后端配置

配置文件: `backend/src/main/resources/application.yml`

主要配置项：
- 数据库连接（使用环境变量 `DB_USER` 和 `DB_PASSWORD`）
- 服务器端口（默认 8080）
- MyBatis-Plus 配置

### 前端配置

环境变量文件: `frontend/web/.env`

```env
VITE_API_BASE_URL=http://localhost:8080/api
```

## 📚 开发文档

- [数据库结构](docs/database.md) - 数据库表结构和关系
- [后端开发文档](docs/backend-dev-doc.md) - API 接口文档
- [项目需求](docs/requirements-simplified.md) - 功能需求说明
- [CLAUDE.md](CLAUDE.md) - AI 辅助开发指南

## 🧪 测试

### 后端测试

```bash
cd backend
mvn test
```

### 前端测试

```bash
cd frontend/web
npm run test
```

## 🐛 常见问题

### 数据库连接失败

检查：
1. PostgreSQL 服务是否启动
2. 数据库 `npdb` 是否已创建
3. 用户名和密码是否正确
4. 环境变量 `DB_USER` 和 `DB_PASSWORD` 是否设置

### 后端启动失败

检查：
1. JDK 版本是否为 17+
2. Maven 依赖是否下载完成
3. 8080 端口是否被占用

### 前端启动失败

检查：
1. Node.js 版本是否为 18+
2. 依赖是否安装完成 (`npm install`)
3. 3001 端口是否被占用

## 📞 获取帮助

遇到问题？
1. 查看 [项目文档](docs/)
2. 提交 GitHub Issue
3. 联系项目负责人

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

[待添加]
