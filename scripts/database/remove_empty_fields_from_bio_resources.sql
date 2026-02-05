-- ============================================
-- 删除 bio_resources 表中完全为空的字段
-- ============================================
-- 执行时间: 2026-02-05
-- 说明: 删除填充率为 0% 的字段

-- 首先删除依赖的视图
DROP VIEW IF EXISTS v_bio_resource_detail CASCADE;

-- 删除完全为空的字段 (32个)

-- 名称相关 (3个)
ALTER TABLE bio_resources DROP COLUMN IF EXISTS english_name;
ALTER TABLE bio_resources DROP COLUMN IF EXISTS pinyin_name;
ALTER TABLE bio_resources DROP COLUMN IF EXISTS alias;

-- 分类学相关 (3个)
ALTER TABLE bio_resources DROP COLUMN IF EXISTS taxonomy_phylum;
ALTER TABLE bio_resources DROP COLUMN IF EXISTS taxonomy_class;
ALTER TABLE bio_resources DROP COLUMN IF EXISTS taxonomy_order;

-- 药用部位 (2个)
ALTER TABLE bio_resources DROP COLUMN IF EXISTS medicinal_part;
ALTER TABLE bio_resources DROP COLUMN IF EXISTS medicinal_part_latin;

-- 产地与分布 (3个)
ALTER TABLE bio_resources DROP COLUMN IF EXISTS origin_region;
ALTER TABLE bio_resources DROP COLUMN IF EXISTS distribution;
ALTER TABLE bio_resources DROP COLUMN IF EXISTS habitat;

-- 中医属性 (4个)
ALTER TABLE bio_resources DROP COLUMN IF EXISTS tcm_property;
ALTER TABLE bio_resources DROP COLUMN IF EXISTS tcm_flavor;
ALTER TABLE bio_resources DROP COLUMN IF EXISTS tcm_meridian;
ALTER TABLE bio_resources DROP COLUMN IF EXISTS tcm_toxicity;

-- 功效与主治 (3个)
ALTER TABLE bio_resources DROP COLUMN IF EXISTS functions;
ALTER TABLE bio_resources DROP COLUMN IF EXISTS indications;
ALTER TABLE bio_resources DROP COLUMN IF EXISTS contraindications;

-- 矿物特有属性 (4个)
ALTER TABLE bio_resources DROP COLUMN IF EXISTS mineral_composition;
ALTER TABLE bio_resources DROP COLUMN IF EXISTS mineral_crystal_system;
ALTER TABLE bio_resources DROP COLUMN IF EXISTS mineral_hardness;
ALTER TABLE bio_resources DROP COLUMN IF EXISTS mineral_color;

-- 微生物特有属性 (3个)
ALTER TABLE bio_resources DROP COLUMN IF EXISTS microbe_strain;
ALTER TABLE bio_resources DROP COLUMN IF EXISTS microbe_culture_condition;
ALTER TABLE bio_resources DROP COLUMN IF EXISTS microbe_fermentation_product;

-- 动物特有属性 (2个)
ALTER TABLE bio_resources DROP COLUMN IF EXISTS animal_class;
ALTER TABLE bio_resources DROP COLUMN IF EXISTS animal_conservation_status;

-- 外部数据库链接 (2个)
ALTER TABLE bio_resources DROP COLUMN IF EXISTS tcmsp_id;
ALTER TABLE bio_resources DROP COLUMN IF EXISTS herb_id;

-- 参考文献 (2个)
ALTER TABLE bio_resources DROP COLUMN IF EXISTS pharmacopoeia_ref;
ALTER TABLE bio_resources DROP COLUMN IF EXISTS literature_ref;

-- 图片 (1个)
ALTER TABLE bio_resources DROP COLUMN IF EXISTS image_url;

-- 重建视图
CREATE OR REPLACE VIEW v_bio_resource_detail AS
SELECT
    br.id,
    br.resource_id,
    br.resource_type,
    br.chinese_name,
    br.latin_name,
    br.taxonomy_family,
    br.taxonomy_genus,
    br.taxonomy_species,
    br.taxonomy_kingdom,
    br.taxonomy_id,
    br.species_tax_id,
    br.genus_tax_id,
    br.family_tax_id,
    br.cmaup_id,
    br.tcmid_id,
    br.num_of_natural_products,
    br.num_of_prescriptions,
    br.created_at,
    br.updated_at
FROM bio_resources br;

COMMENT ON VIEW v_bio_resource_detail IS '生物资源详情视图 - 包含统计信息';

-- 显示剩余字段
\d bio_resources

-- 统计信息
SELECT
    '删除前字段数' as 说明,
    '51' as 数量
UNION ALL
SELECT
    '删除的字段数',
    '32'
UNION ALL
SELECT
    '剩余字段数',
    COUNT(column_name)::text
FROM information_schema.columns
WHERE table_name = 'bio_resources' AND table_schema = 'public';

-- 更新统计信息
ANALYZE bio_resources;

SELECT '✓ 空字段删除完成' as status;
