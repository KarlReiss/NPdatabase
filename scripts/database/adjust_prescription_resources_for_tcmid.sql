-- ============================================================================
-- 调整 prescription_resources 表以匹配 TCMID 药材数据格式
-- ============================================================================
-- 文件: adjust_prescription_resources_for_tcmid.sql
-- 描述: 根据 TCMID prescription_herbs.csv 数据格式调整 prescription_resources 表结构
-- 日期: 2026-01-29
-- ============================================================================

-- TCMID prescription_herbs.csv 字段:
-- PrescriptionID, ComponentID, LatinName, ChineseName, ComponentQuantity, Barcode

-- 当前表已有字段映射:
-- prescription_id -> PrescriptionID (通过外键关联)
-- bio_resource_id -> ComponentID (通过外键关联到 bio_resources)
-- dosage_text -> ComponentQuantity (可以存储原始数量文本)

-- 需要新增的字段:
ALTER TABLE prescription_resources ADD COLUMN IF NOT EXISTS tcmid_component_id VARCHAR(50);
ALTER TABLE prescription_resources ADD COLUMN IF NOT EXISTS barcode VARCHAR(100);
ALTER TABLE prescription_resources ADD COLUMN IF NOT EXISTS latin_name VARCHAR(500);
ALTER TABLE prescription_resources ADD COLUMN IF NOT EXISTS chinese_name VARCHAR(500);

-- 添加索引
CREATE INDEX IF NOT EXISTS idx_pr_tcmid_component ON prescription_resources(tcmid_component_id);
CREATE INDEX IF NOT EXISTS idx_pr_barcode ON prescription_resources(barcode);

-- 添加注释
COMMENT ON COLUMN prescription_resources.tcmid_component_id IS 'TCMID药材组分ID（如 TCMH1398）';
COMMENT ON COLUMN prescription_resources.barcode IS 'TCMID药材条形码（如 ITSAM882-14）';
COMMENT ON COLUMN prescription_resources.latin_name IS '药材拉丁名（来自TCMID）';
COMMENT ON COLUMN prescription_resources.chinese_name IS '药材中文名（来自TCMID）';
COMMENT ON COLUMN prescription_resources.dosage_text IS '药材用量文本（来自TCMID的ComponentQuantity）';

-- 注意:
-- 1. latin_name 和 chinese_name 字段用于存储TCMID原始数据，便于匹配和验证
-- 2. bio_resource_id 是匹配后的生物资源ID
-- 3. 如果无法匹配到现有bio_resource，可能需要创建新的bio_resource记录
