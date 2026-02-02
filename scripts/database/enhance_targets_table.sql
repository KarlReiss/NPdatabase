-- ============================================================================
-- 增强 targets 表 - 添加 TTD 靶点数据字段
-- ============================================================================
-- 文件: enhance_targets_table.sql
-- 描述: 为 targets 表添加新字段以支持 TTD 靶点数据导入
-- 日期: 2026-01-29
-- ============================================================================

-- 新增字段
ALTER TABLE targets ADD COLUMN IF NOT EXISTS gene_name VARCHAR(100);
ALTER TABLE targets ADD COLUMN IF NOT EXISTS synonyms TEXT;
ALTER TABLE targets ADD COLUMN IF NOT EXISTS function TEXT;
ALTER TABLE targets ADD COLUMN IF NOT EXISTS pdb_structure VARCHAR(500);
ALTER TABLE targets ADD COLUMN IF NOT EXISTS bioclass VARCHAR(200);
ALTER TABLE targets ADD COLUMN IF NOT EXISTS ec_number VARCHAR(50);
ALTER TABLE targets ADD COLUMN IF NOT EXISTS sequence TEXT;
ALTER TABLE targets ADD COLUMN IF NOT EXISTS ttd_id VARCHAR(50);

-- 添加索引
CREATE INDEX IF NOT EXISTS idx_targets_gene_name ON targets(gene_name);
CREATE INDEX IF NOT EXISTS idx_targets_ttd_id ON targets(ttd_id);
CREATE INDEX IF NOT EXISTS idx_targets_ec_number ON targets(ec_number);

-- 全文搜索索引
CREATE INDEX IF NOT EXISTS idx_targets_function_gin
ON targets USING gin(to_tsvector('english', COALESCE(function, '')));
CREATE INDEX IF NOT EXISTS idx_targets_synonyms_gin
ON targets USING gin(to_tsvector('english', COALESCE(synonyms, '')));

-- 添加注释
COMMENT ON COLUMN targets.gene_name IS '基因名称';
COMMENT ON COLUMN targets.synonyms IS '同义词（多个用分号分隔）';
COMMENT ON COLUMN targets.function IS '功能描述';
COMMENT ON COLUMN targets.pdb_structure IS 'PDB结构ID（多个用分号分隔）';
COMMENT ON COLUMN targets.bioclass IS '生物分类';
COMMENT ON COLUMN targets.ec_number IS 'EC编号';
COMMENT ON COLUMN targets.sequence IS '蛋白质序列';
COMMENT ON COLUMN targets.ttd_id IS 'TTD数据库ID';
