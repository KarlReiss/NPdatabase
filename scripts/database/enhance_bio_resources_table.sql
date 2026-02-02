-- ============================================================================
-- 增强 bio_resources 表 - 添加 CMAUP 植物分类学数据字段
-- ============================================================================
-- 文件: enhance_bio_resources_table.sql
-- 描述: 为 bio_resources 表添加新字段以支持 CMAUP 植物分类学数据导入
-- 日期: 2026-01-29
-- ============================================================================

-- 新增字段
ALTER TABLE bio_resources ADD COLUMN IF NOT EXISTS species_tax_id VARCHAR(50);
ALTER TABLE bio_resources ADD COLUMN IF NOT EXISTS genus_tax_id VARCHAR(50);
ALTER TABLE bio_resources ADD COLUMN IF NOT EXISTS family_tax_id VARCHAR(50);
ALTER TABLE bio_resources ADD COLUMN IF NOT EXISTS cmaup_id VARCHAR(50);

-- 添加索引
CREATE INDEX IF NOT EXISTS idx_bio_resources_species_tax_id ON bio_resources(species_tax_id);
CREATE INDEX IF NOT EXISTS idx_bio_resources_genus_tax_id ON bio_resources(genus_tax_id);
CREATE INDEX IF NOT EXISTS idx_bio_resources_family_tax_id ON bio_resources(family_tax_id);
CREATE INDEX IF NOT EXISTS idx_bio_resources_cmaup_id ON bio_resources(cmaup_id);

-- 添加注释
COMMENT ON COLUMN bio_resources.species_tax_id IS '种的Taxonomy ID';
COMMENT ON COLUMN bio_resources.genus_tax_id IS '属的Taxonomy ID';
COMMENT ON COLUMN bio_resources.family_tax_id IS '科的Taxonomy ID';
COMMENT ON COLUMN bio_resources.cmaup_id IS 'CMAUP数据库ID';
