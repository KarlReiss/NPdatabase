-- ============================================================================
-- 调整 prescriptions 表以匹配 TCMID 数据格式
-- ============================================================================
-- 文件: adjust_prescriptions_for_tcmid.sql
-- 描述: 根据 TCMID 数据格式调整 prescriptions 表结构
-- 日期: 2026-01-29
-- ============================================================================

-- TCMID prescription_basic_info.csv 字段:
-- PrescriptionID, PinyinName, ChineseName, EnglishName, FunctionDescription,
-- Indications, DiseaseICD11Category, HumanTissues, Reference, ReferenceBook

-- 当前表已有字段映射:
-- prescription_id -> PrescriptionID (TCMID格式: TCMF1, TCMF2, etc.)
-- pinyin_name -> PinyinName
-- chinese_name -> ChineseName
-- english_name -> EnglishName
-- functions -> FunctionDescription
-- indications -> Indications

-- 需要新增的字段:
ALTER TABLE prescriptions ADD COLUMN IF NOT EXISTS disease_icd11_category TEXT;
ALTER TABLE prescriptions ADD COLUMN IF NOT EXISTS human_tissues TEXT;
ALTER TABLE prescriptions ADD COLUMN IF NOT EXISTS reference TEXT;
ALTER TABLE prescriptions ADD COLUMN IF NOT EXISTS reference_book TEXT;

-- 添加索引
CREATE INDEX IF NOT EXISTS idx_prescriptions_icd11_gin
ON prescriptions USING gin(to_tsvector('english', COALESCE(disease_icd11_category, '')));

-- 添加注释
COMMENT ON COLUMN prescriptions.disease_icd11_category IS 'ICD-11疾病分类编码（多个用分号分隔）';
COMMENT ON COLUMN prescriptions.human_tissues IS '相关人体组织';
COMMENT ON COLUMN prescriptions.reference IS '参考文献';
COMMENT ON COLUMN prescriptions.reference_book IS '参考书籍';

-- 更新现有字段注释以匹配TCMID数据
COMMENT ON COLUMN prescriptions.prescription_id IS '处方唯一标识符（TCMID格式: TCMF1, TCMF2等）';
COMMENT ON COLUMN prescriptions.pinyin_name IS '处方拼音名称';
COMMENT ON COLUMN prescriptions.chinese_name IS '处方中文名称';
COMMENT ON COLUMN prescriptions.english_name IS '处方英文名称';
COMMENT ON COLUMN prescriptions.functions IS '功能描述（功效）';
COMMENT ON COLUMN prescriptions.indications IS '适应症';

-- 注意: TCMID prescription_herbs.csv 字段:
-- PrescriptionID, ComponentID, LatinName, ChineseName, ComponentQuantity, Barcode
-- 这些数据将通过 prescription_resources 关联表导入
-- ComponentID 对应 bio_resources 表中的药材
