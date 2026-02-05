-- ============================================
-- 为 bio_resources 表添加 TCMID 相关字段
-- ============================================

-- 添加 tcmid_id 字段（用于存储 TCMID Component ID）
ALTER TABLE bio_resources ADD COLUMN IF NOT EXISTS tcmid_id VARCHAR(500);

-- 添加 tcmid_chinese_name 字段（用于存储 TCMID 中文名）
-- 注意：这个字段可能与 chinese_name 重复，但保留以便区分来源
-- ALTER TABLE bio_resources ADD COLUMN IF NOT EXISTS tcmid_chinese_name TEXT;

-- 添加索引
CREATE INDEX IF NOT EXISTS idx_bio_resources_tcmid_id ON bio_resources(tcmid_id);

-- 添加注释
COMMENT ON COLUMN bio_resources.tcmid_id IS 'TCMID Component ID (多个用逗号分隔)';

-- 验证字段是否添加成功
\d bio_resources

-- 显示当前记录数
SELECT COUNT(*) as total_records FROM bio_resources;

-- 完成提示
SELECT '✓ TCMID 字段添加完成' as status;
