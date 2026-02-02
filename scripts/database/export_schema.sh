#!/bin/bash
# ===========================
# 导出数据库结构和示例数据
# 用于 GitHub 团队协作
# ===========================

set -e

# 配置
DB_NAME="npdb"
DB_USER="${DB_USER:-postgres}"
EXPORT_DIR="/home/yfguo/NPdatabase/scripts/database/exports"

# 创建导出目录
mkdir -p "$EXPORT_DIR"

echo "开始导出数据库..."

# 1. 导出完整结构（包含表、视图、索引、约束）
echo "1. 导出数据库结构..."
pg_dump -U "$DB_USER" -d "$DB_NAME" \
  --schema-only \
  --no-owner \
  --no-privileges \
  -f "$EXPORT_DIR/01_schema_full.sql"

# 2. 导出示例数据（每个表前100条）
echo "2. 导出示例数据..."

# Natural Products (前100条)
psql -U "$DB_USER" -d "$DB_NAME" -c "\COPY (SELECT * FROM natural_products LIMIT 100) TO '$EXPORT_DIR/sample_natural_products.csv' WITH CSV HEADER"

# Targets (前100条)
psql -U "$DB_USER" -d "$DB_NAME" -c "\COPY (SELECT * FROM targets LIMIT 100) TO '$EXPORT_DIR/sample_targets.csv' WITH CSV HEADER"

# Bioactivity (前100条)
psql -U "$DB_USER" -d "$DB_NAME" -c "\COPY (SELECT * FROM bioactivity LIMIT 100) TO '$EXPORT_DIR/sample_bioactivity.csv' WITH CSV HEADER"

# Bio Resources (前100条)
psql -U "$DB_USER" -d "$DB_NAME" -c "\COPY (SELECT * FROM bio_resources LIMIT 100) TO '$EXPORT_DIR/sample_bio_resources.csv' WITH CSV HEADER"

# 3. 创建示例数据导入脚本
cat > "$EXPORT_DIR/02_import_sample_data.sql" << 'EOF'
-- ===========================
-- 导入示例数据
-- ===========================

-- 注意：先执行 01_schema_full.sql 创建表结构

-- 导入 Natural Products 示例数据
\COPY natural_products FROM 'sample_natural_products.csv' WITH CSV HEADER;

-- 导入 Targets 示例数据
\COPY targets FROM 'sample_targets.csv' WITH CSV HEADER;

-- 导入 Bioactivity 示例数据
\COPY bioactivity FROM 'sample_bioactivity.csv' WITH CSV HEADER;

-- 导入 Bio Resources 示例数据
\COPY bio_resources FROM 'sample_bio_resources.csv' WITH CSV HEADER;

-- 更新序列
SELECT setval('natural_products_id_seq', (SELECT MAX(id) FROM natural_products));
SELECT setval('targets_id_seq', (SELECT MAX(id) FROM targets));
SELECT setval('bioactivity_id_seq', (SELECT MAX(id) FROM bioactivity));
SELECT setval('bio_resources_id_seq', (SELECT MAX(id) FROM bio_resources));
EOF

# 4. 创建 README
cat > "$EXPORT_DIR/README.md" << 'EOF'
# 数据库导出文件

## 文件说明

- `01_schema_full.sql` - 完整数据库结构（表、视图、索引、约束）
- `02_import_sample_data.sql` - 示例数据导入脚本
- `sample_*.csv` - 示例数据文件（每个表100条记录）

## 使用方法

### 1. 创建数据库并导入结构

```bash
# 创建数据库
createdb -U postgres npdb

# 导入结构
psql -U postgres -d npdb -f 01_schema_full.sql
```

### 2. 导入示例数据（可选）

```bash
cd exports/
psql -U postgres -d npdb -f 02_import_sample_data.sql
```

### 3. 导入完整数据

完整数据文件较大，不包含在 GitHub 仓库中。
请联系项目负责人获取完整数据文件，或使用 `/scripts/database/import_*.py` 脚本从原始数据导入。

## 注意事项

- 示例数据仅用于开发测试
- 生产环境需要导入完整数据
- 数据库用户和权限需要根据实际情况调整
EOF

echo "✅ 导出完成！"
echo "导出文件位置: $EXPORT_DIR"
echo ""
echo "文件列表:"
ls -lh "$EXPORT_DIR"
