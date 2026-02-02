-- ============================================================================
-- 创建 diseases 表 - 存储疾病信息（基于ICD-11分类）
-- ============================================================================
-- 文件: create_diseases_table.sql
-- 描述: 创建疾病表以支持 CMAUP 疾病关联数据导入
-- 日期: 2026-01-29
-- ============================================================================

CREATE TABLE IF NOT EXISTS diseases (
    id BIGSERIAL PRIMARY KEY,

    -- 基本标识
    disease_id VARCHAR(50) UNIQUE NOT NULL,     -- 自动生成 (如 DIS0001)
    icd11_code VARCHAR(50) NOT NULL,            -- ICD-11编码

    -- 名称信息
    disease_name VARCHAR(500) NOT NULL,         -- 疾病名称
    disease_name_zh VARCHAR(500),               -- 中文名称
    disease_category VARCHAR(200),              -- 疾病分类

    -- 描述信息
    description TEXT,                           -- 疾病描述
    symptoms TEXT,                              -- 症状

    -- 统计信息
    num_of_related_plants INT DEFAULT 0,       -- 关联植物数
    num_of_related_targets INT DEFAULT 0,      -- 关联靶点数

    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_diseases_disease_id ON diseases(disease_id);
CREATE INDEX IF NOT EXISTS idx_diseases_icd11_code ON diseases(icd11_code);
CREATE INDEX IF NOT EXISTS idx_diseases_category ON diseases(disease_category);
CREATE INDEX IF NOT EXISTS idx_diseases_name_gin ON diseases
    USING gin(to_tsvector('english', COALESCE(disease_name, '')));

-- 添加注释
COMMENT ON TABLE diseases IS '疾病表 - 存储疾病信息（基于ICD-11分类）';
COMMENT ON COLUMN diseases.disease_id IS '疾病唯一标识符（自动生成，如 DIS0001）';
COMMENT ON COLUMN diseases.icd11_code IS 'ICD-11疾病分类编码';
COMMENT ON COLUMN diseases.disease_name IS '疾病英文名称';
COMMENT ON COLUMN diseases.disease_name_zh IS '疾病中文名称';
COMMENT ON COLUMN diseases.disease_category IS '疾病分类';
COMMENT ON COLUMN diseases.description IS '疾病描述';
COMMENT ON COLUMN diseases.symptoms IS '疾病症状';
COMMENT ON COLUMN diseases.num_of_related_plants IS '关联植物数量';
COMMENT ON COLUMN diseases.num_of_related_targets IS '关联靶点数量';

-- 创建更新时间戳触发器
CREATE TRIGGER update_diseases_updated_at
    BEFORE UPDATE ON diseases
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
