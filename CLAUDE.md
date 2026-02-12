# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 重要

请使用中文交流

## Project Overview

Natural Product Database (天然产物数据库) is a full-stack web application for exploring natural products, their bioactivity data, targets, and biological resources based on NPASS 3.0 data. The application provides a scientific database interface with search, filtering, and detailed compound information views.

**Tech Stack:**
- **Backend**: Java + Spring Boot 3.2.5 + MyBatis-Plus 3.5.5
- **Database**: PostgreSQL 16
- **Frontend**: React prototypes available (framework TBD)
- **Cache**: Redis (optional, not yet implemented)
- **Authentication**: V1 has no login/authentication

## Project Structure

```
NPdatabase/
├── docs/                           # Project documentation
│   └── startup-guide.md            # 详细的服务启动指南
├── data/                           # 多源数据文件
│   ├── NPASS/                      # NPASS 3.0 数据
│   │   ├── NPASS3.0_naturalproducts_generalinfo.txt
│   │   ├── NPASS3.0_activities.txt
│   │   ├── NPASS3.0_target.txt
│   │   ├── NPASS3.0_species_info.txt
│   │   ├── NPASS3.0_naturalproducts_species_pair.txt
│   │   ├── NPASS3.0_naturalproducts_structure.txt
│   │   └── NPASS3.0_toxicity.txt
│   ├── TCMID/                      # TCMID 中药数据
│   │   ├── herbs.txt
│   │   ├── ingredients.txt
│   │   └── ...
│   ├── CMAUP/                      # CMAUP 中药材数据
│   │   └── ...
│   └── TTD/                        # TTD 靶点数据
│       └── ...
├── frontend/                       # 前端应用
│   └── web/                        # Vue 3 web 应用
│       ├── src/
│       │   ├── api/                # API 客户端
│       │   ├── components/         # 共享组件
│       │   ├── pages/              # 页面组件
│       │   ├── router/             # 路由配置
│       │   └── utils/              # 工具函数
│       └── run/                    # 运行时文件（PID等）
├── scripts/                        # 脚本集合
│   ├── backend-service.sh          # 服务管理脚本
│   └── data-import/                # 数据导入脚本
│       ├── README.md               # 导入说明
│       ├── import_npass_data.py    # NPASS 导入
│       ├── import_tcmid_data.py    # TCMID 导入
│       ├── import_cmaup_data.py    # CMAUP 导入
│       ├── import_bio_resource_disease_associations.py
│       └── output/                 # 导入报告和日志
└── backend/                        # Spring Boot 后端
    ├── pom.xml
    ├── run/                        # 运行时文件（PID等）
    └── src/main/java/cn/npdb/
        ├── controller/             # API 控制器
        ├── service/                # 服务接口
        ├── service/impl/           # 服务实现
        ├── mapper/                 # MyBatis-Plus 映射器
        ├── entity/                 # 数据库实体
        ├── dto/                    # 数据传输对象
        ├── common/                 # 通用工具（响应、异常）
        └── config/                 # 配置类
```

## Development Commands

### 快速启动（推荐）

使用启动脚本一键启动前后端服务：

```bash
# 启动服务
bash scripts/backend-service.sh start

# 停止服务
bash scripts/backend-service.sh stop

# 重启服务
bash scripts/backend-service.sh restart

# 查看状态
bash scripts/backend-service.sh status

# 查看日志
bash scripts/backend-service.sh logs          # 后端日志
bash scripts/backend-service.sh logs frontend # 前端日志
```

详细说明请参考 `docs/startup-guide.md`

### Backend

```bash
# Start backend (with environment variables)
DB_USER=yfguo DB_PASSWORD=npdb2024 \
  mvn -f backend/pom.xml spring-boot:run -DskipTests

# Build backend
mvn -f backend/pom.xml clean package -DskipTests

# Default port: 8080
# Swagger UI: http://localhost:8080/swagger-ui.html
# OpenAPI docs: http://localhost:8080/v3/api-docs
```

### Frontend

```bash
# Vue 3 web application
cd frontend/web
npm install
npm run dev  # Port 3001

# Build for production
npm run build

# Preview production build
npm run preview
```

### Database Setup

数据库已完成初始化和数据导入。当前数据库状态：

**数据库信息：**
- 数据库名：`npdb`
- 用户：`yfguo`
- 密码：`npdb2024`
- 主机：`localhost:5432`

**已导入的数据表：**
- `natural_products` - 天然产物（~500,000 条记录）
- `targets` - 靶点（~1,000 条记录）
- `bioactivity` - 生物活性（~1,000,000 条记录）
- `toxicity` - 毒性数据
- `bio_resources` - 生物资源（整合 NPASS、TCMID、CMAUP 数据）
- `bio_resource_natural_products` - 生物资源-天然产物关联
- `bio_resource_disease_associations` - 生物资源-疾病关联
- `prescriptions` - 方剂（预留，暂无数据）
- `prescription_resources` - 方剂-生物资源关联（预留）
- `prescription_natural_products` - 方剂-天然产物关联（预留）

**如需重新导入数据：**

```bash
# 数据导入脚本位于 scripts/data-import/
cd scripts/data-import

# 按顺序执行导入脚本
python import_npass_data.py
python import_tcmid_data.py
python import_cmaup_data.py
python import_bio_resource_disease_associations.py

# 详细导入报告位于 scripts/data-import/output/
```

## Database Schema

### Core Tables (10 tables)

- **natural_products**: Natural product core table (formerly `compounds`)
  - Chemical properties: MW, formula, CAS, PubChem ID, XLogP, PSA, H-bond donors/acceptors
  - Bioactivity metrics: best potency, related targets count
  - Structure data: SMILES, InChI, InChIKey

- **targets**: Protein targets with gene symbols, names, and inferred disease associations

- **bioactivity**: Assay evidence linking natural products to targets
  - IC50/EC50/Ki values
  - Literature references (PMID/DOI)

- **toxicity**: Toxicity data for natural products

- **bio_resources**: Biological resources (herbs, species, sources)
  - Replaces old `species` table
  - Key fields: `resource_id`, `resource_type`, `chinese_name`, `latin_name`, `official_chinese_name`
  - Taxonomy: `taxonomy_kingdom`, `taxonomy_family`, `taxonomy_genus`, `taxonomy_species`
  - External IDs: `tcmid_id`, `cmaup_id`, `species_tax_id`, `genus_tax_id`, `family_tax_id`
  - Statistics: `num_of_natural_products`, `num_of_prescriptions`

- **bio_resource_natural_products**: Many-to-many relationship between bio_resources and natural_products

- **bio_resource_disease_associations**: Disease associations for bio resources
  - Links bio resources to diseases with evidence from literature

- **prescriptions**: Traditional medicine prescriptions (reserved for future use)

- **prescription_resources**: Many-to-many between prescriptions and bio_resources

- **prescription_natural_products**: Many-to-many between prescriptions and natural_products

### Views (4 views)

- **v_natural_product_detail**: Comprehensive natural product view with aggregated stats
- **v_bio_resource_detail**: Bio resource view with related natural products count
- **v_target_detail**: Target view with bioactivity aggregations
- **v_prescription_detail**: Prescription view (reserved)

### Important Schema Changes

The database underwent optimization (see `scripts/database/optimize_table_structure.sql`):

1. **Renamed**: `compounds` → `natural_products`
2. **Deleted**: `species` and `compound_species` (merged into `bio_resources`)
3. **Renamed**: `bio_resource_compounds` → `bio_resource_natural_products`
4. **Renamed**: `prescription_compounds` → `prescription_natural_products`
5. **Field renames**: All `compound_id` → `natural_product_id`
6. **View renames**: `v_compound_detail` → `v_natural_product_detail`

**Always refer to `docs/database.md` for the authoritative schema documentation.**

## Backend Architecture

### API Response Format

All APIs return a unified response structure:

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

Paginated responses:

```json
{
  "records": [],
  "page": 1,
  "pageSize": 20,
  "total": 0
}
```

### Core API Endpoints

**Natural Products:**
- `GET /api/natural-products` - List with filters and pagination
- `GET /api/natural-products/{id}` - Detail view
- `GET /api/natural-products/search` - Keyword/SMILES search
- `GET /api/natural-products/stats` - Statistics

**Targets:**
- `GET /api/targets` - List with filters
- `GET /api/targets/{id}` - Detail view
- `GET /api/targets/search` - Search targets

**Bioactivity:**
- `GET /api/bioactivity` - Query by natural product or target

**Statistics:**
- `GET /api/stats/overview` - Database overview statistics

See `docs/backend-dev-doc.md` for complete API documentation.

### Configuration

Backend configuration is in `backend/src/main/resources/application.yml`:

- Database connection uses environment variables: `DB_USER`, `DB_PASSWORD`
- Default database: `npdb` on `localhost:5432`
- MyBatis-Plus pagination configured
- Swagger/OpenAPI enabled

## Frontend Application

### Vue 3 Web Application (`frontend/web/`)

**Tech Stack:**
- Vue 3 + TypeScript
- Vue Router (Hash mode)
- Vite build tool
- Tailwind CSS (inline classes)
- Axios for API calls

**Project Structure:**
```
src/
├── api/                    # API client modules
│   ├── naturalProducts.ts  # Natural products API
│   ├── targets.ts          # Targets API
│   ├── search.ts           # Search API
│   └── types.ts            # API type definitions
├── components/             # Shared components
│   ├── AppHeader.vue       # Navigation header
│   └── SortIcon.vue        # Sort icon component
├── pages/                  # Page components
│   ├── Home.vue                    # Landing page
│   ├── NaturalProductList.vue      # Natural products list
│   ├── NaturalProductDetail.vue    # Natural product detail
│   ├── TargetList.vue              # Targets list
│   ├── TargetDetail.vue            # Target detail
│   ├── BioResourceList.vue         # Bio resources list
│   ├── BioResourceDetail.vue       # Bio resource detail
│   └── ...                         # Other pages
├── router/                 # Router configuration
└── utils/                  # Utility functions
```

**Key Routes:**
- `/` - Home page with search
- `/natural-products` - Natural products list with filters
- `/natural-products/:id` - Natural product detail
- `/targets` - Targets list
- `/targets/:id` - Target detail
- `/bio-resources` - Bio resources list
- `/bio-resources/:id` - Bio resource detail

**Legacy Route Redirects:**
- `/compounds` → `/natural-products`
- `/resources` → `/bio-resources`

**API Configuration:**
- Base URL: `http://localhost:8080/api` (configurable via `VITE_API_BASE_URL`)
- Uses Axios with unified response handling
- Mock data available in `src/mockData.ts` for development

## Data Sources

### NPASS 3.0 (主要数据源)
NPASS 3.0 data files in `data/NPASS/` directory:
- ~500,000 natural products
- ~1,000,000 bioactivity records
- ~1,000 targets
- Species/source information
- Toxicity data

### TCMID (中药分子数据库)
TCMID data in `data/TCMID/` directory:
- 中药材信息（herbs）
- 中药成分信息（ingredients）
- 中药-成分关联关系
- 疾病关联信息

### CMAUP (中药材数据库)
CMAUP data in `data/CMAUP/` directory:
- 植物药材信息
- 标准中文名称
- 分类学信息
- 疾病治疗关联

### TTD (治疗靶点数据库)
TTD data in `data/TTD/` directory:
- 靶点信息
- 靶点-疾病关联
- 药物-靶点关联

数据整合说明：
- bio_resources 表整合了 NPASS、TCMID、CMAUP 的生物资源数据
- 通过 `tcmid_id`、`cmaup_id` 等字段关联外部数据库
- `official_chinese_name` 字段存储 CMAUP 的标准中文名称
- 详细的数据导入报告见 `scripts/data-import/output/`

## Current Status

### ✅ Completed

- [x] Requirements documentation (simplified + full versions)
- [x] Data files prepared (NPASS 3.0, TCMID, CMAUP, TTD)
- [x] Project structure planning
- [x] Vue 3 frontend application structure
- [x] Database schema design and optimization
- [x] Multi-source data integration (NPASS + TCMID + CMAUP + TTD)
- [x] Data import scripts and validation
- [x] Backend project initialization (Spring Boot + MyBatis-Plus)
- [x] Core API implementation (natural products/targets/bio-resources/search/stats)
- [x] Swagger documentation and validation guide
- [x] Service management scripts (backend-service.sh)
- [x] Startup guide documentation

### 🚧 In Progress

- [ ] Frontend integration with backend APIs
- [ ] Bio resources detail page implementation
- [ ] Disease associations display
- [ ] Advanced search features (structure search, similarity search)

### 📋 Future Enhancements

- [ ] Performance optimization (caching, indexing)
- [ ] Data quality improvements (physicochemical properties validation)
- [ ] User authentication and authorization
- [ ] Data export functionality
- [ ] API rate limiting
- [ ] Advanced analytics and visualization

## Important Notes

### For Backend Development

- **Read-only V1**: No authentication, no write operations
- **Environment variables**: Always use `DB_USER` and `DB_PASSWORD` for database connection
- **Unified responses**: All APIs must use the common response wrapper
- **Swagger**: Keep API documentation up to date
- **Error handling**: Use global exception handler in `common/` package

### For Frontend Development

- **Framework**: Vue 3 with TypeScript and Composition API
- **API integration**: Replace mock data with actual backend API calls
- **Naming convention**: Use `NaturalProduct` (not `Compound`), `BioResource` (not `Resource` or `Species`)
- **Routes**: Use kebab-case URLs (`/natural-products`, `/bio-resources`)
- **Bilingual UI**: Interface uses both English and Chinese labels (e.g., "理化属性 (Properties)")
- **Scientific accuracy**: Maintain correct terminology (IC50, XLogP, PSA, etc.)
- **HashRouter**: Use hash-based routing for static hosting compatibility
- **Error handling**: All API calls must handle errors gracefully

### For Database Work

- **Schema changes**: Always update `docs/database.md` when modifying schema
- **Naming convention**: Use `natural_products` (not `compounds`), `natural_product_id` (not `compound_id`)
- **Views**: Prefer using detail views (`v_natural_product_detail`, etc.) for complex queries
- **Indexes**: Check existing indexes before adding new ones

### Scientific Context

This is a research tool for natural products and drug discovery. Key concepts:

- **Natural Products**: Compounds derived from natural sources (plants, microorganisms, etc.)
- **Bioactivity**: Biological activity measured by IC50/EC50/Ki values (lower = more potent)
- **Targets**: Proteins that compounds interact with (genes, receptors, enzymes)
- **SMILES**: Simplified molecular-input line-entry system for chemical structures
- **XLogP**: Partition coefficient (lipophilicity)
- **PSA**: Polar surface area (drug-likeness indicator)

## Key Documentation

### 核心文档（推荐阅读顺序）

1. **`README.md`** ⭐⭐⭐⭐⭐ - 项目介绍和快速开始
2. **`quick-start.md`** ⭐⭐⭐⭐⭐ - 快速启动指南
3. **`docs/startup-guide.md`** ⭐⭐⭐⭐⭐ - 详细的服务启动指南（推荐）

### 数据导入文档

- **`scripts/data-import/README.md`** - 数据导入总览
- **`scripts/data-import/output/`** - 数据导入报告和日志
  - `import_report_*.txt` - 各数据源导入报告
  - `validation_report_*.txt` - 数据验证报告
  - `bio_resource_disease_associations_import_report.txt` - 疾病关联导入报告

### 脚本文档

- **`scripts/backend-service.sh`** - 服务管理脚本（启动/停止/重启/状态/日志）
- **`scripts/data-import/`** - 数据导入脚本集合
  - `import_npass_data.py` - NPASS 数据导入
  - `import_tcmid_data.py` - TCMID 数据导入
  - `import_cmaup_data.py` - CMAUP 数据导入
  - `import_bio_resource_disease_associations.py` - 疾病关联导入

### 已归档文档（历史参考）

以下文档已删除，内容已整合到上述核心文档中：
- `docs/database.md` - 数据库结构（已整合到 CLAUDE.md）
- `docs/backend-dev-doc.md` - 后端开发文档
- `docs/backend-dev-log.md` - 开发日志
- `docs/backend-delivery.md` - 交付清单
- `docs/requirements-simplified.md` - 需求文档

## Contact

Project owner: [To be added]
