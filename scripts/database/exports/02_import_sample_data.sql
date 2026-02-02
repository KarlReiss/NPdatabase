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
