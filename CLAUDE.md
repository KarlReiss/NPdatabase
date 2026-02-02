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
│   ├── database.md                 # Database schema (final structure)
│   ├── requirements-simplified.md  # Simplified requirements (recommended)
│   ├── backend-dev-doc.md          # Backend development documentation
│   ├── backend-dev-log.md          # Backend development log
│   ├── swagger-validation.md       # Swagger validation guide
│   ├── next-steps.md               # Next steps after backend completion
│   └── archived/                   # Historical documents
│       └── requirements-full.md    # Full requirements document
├── data/                           # NPASS 3.0 raw data files
│   ├── NPASS3.0_naturalproducts_generalinfo.txt
│   ├── NPASS3.0_activities.txt
│   ├── NPASS3.0_target.txt
│   ├── NPASS3.0_species_info.txt
│   ├── NPASS3.0_naturalproducts_species_pair.txt
│   ├── NPASS3.0_naturalproducts_structure.txt
│   └── NPASS3.0_toxicity.txt
├── frontend/                       # Frontend application
│   └── web/                        # Vue 3 web application
├── scripts/                        # Data processing scripts
│   └── database/
│       ├── schema.sql              # Base schema
│       ├── add_prescription_bioresource.sql  # Extended tables
│       ├── optimize_table_structure.sql      # Structure optimization
│       ├── import_natural_products.py
│       ├── import_targets.py
│       ├── import_bioactivity.py
│       ├── import_toxicity.py
│       ├── import_bio_resources.py
│       └── import_bio_resource_natural_products.py
└── backend/                        # Spring Boot backend (completed)
    ├── pom.xml
    └── src/main/java/cn/npdb/
        ├── controller/             # API controllers
        ├── service/                # Service interfaces
        ├── service/impl/           # Service implementations
        ├── mapper/                 # MyBatis-Plus mappers
        ├── entity/                 # Database entities
        ├── dto/                    # Data transfer objects
        ├── common/                 # Common utilities (response, exceptions)
        └── config/                 # Configuration classes
```

## Development Commands

### Backend

```bash
# Start backend (with environment variables)
DB_USER=your_user DB_PASSWORD=your_password \
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

```bash
# Execute in order:
psql -U postgres -d npdb -f scripts/database/schema.sql
psql -U postgres -d npdb -f scripts/database/add_prescription_bioresource.sql
psql -U postgres -d npdb -f scripts/database/optimize_table_structure.sql

# Import data
python scripts/database/import_natural_products.py
python scripts/database/import_targets.py
python scripts/database/import_bioactivity.py
python scripts/database/import_toxicity.py
python scripts/database/import_bio_resources.py
python scripts/database/import_bio_resource_natural_products.py
```

## Database Schema

### Core Tables (9 tables)

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
  - Includes Latin names, Chinese names, categories

- **bio_resource_natural_products**: Many-to-many relationship between bio_resources and natural_products

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

NPASS 3.0 data files in `data/` directory:
- ~500,000 natural products
- ~1,000,000 bioactivity records
- ~1,000 targets
- Species/source information
- Toxicity data

## Current Status

### ✅ Completed

- [x] Requirements documentation (simplified + full versions)
- [x] Data files prepared (NPASS 3.0)
- [x] Project structure planning
- [x] Vue 3 frontend application structure
- [x] Database schema and data processing complete
- [x] Backend project initialization (Spring Boot + MyBatis-Plus)
- [x] Core API implementation (natural products/targets/search/stats)
- [x] Swagger documentation and validation guide

### 🚧 In Progress

- [ ] Frontend integration with backend APIs
- [ ] Data quality improvements (physicochemical properties, null handling)
- [ ] Performance optimization (caching, indexing)

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

Priority reading order:

1. **`docs/database.md`** ⭐⭐⭐⭐⭐ - Database schema (must read)
2. **`docs/requirements-simplified.md`** ⭐⭐⭐⭐⭐ - Project requirements
3. **`docs/backend-dev-doc.md`** ⭐⭐⭐⭐⭐ - Backend implementation guide
4. **`docs/backend-dev-log.md`** ⭐⭐⭐⭐ - Development history
5. **`docs/backend-delivery.md`** ⭐⭐⭐⭐ - Delivery checklist
6. **`docs/next-steps.md`** ⭐⭐⭐ - Future roadmap

## Contact

Project owner: [To be added]
