-- ============================================================================
-- 创建 bio_resource_disease_associations 表 - 生物资源-疾病关联表
-- ============================================================================
-- 文件: create_bio_resource_disease_associations_table.sql
-- 描述: 创建生物资源-疾病关联表以支持 CMAUP 疾病关联数据导入
-- 日期: 2026-01-29
-- ============================================================================

CREATE TABLE IF NOT EXISTS bio_resource_disease_associations (
    id BIGSERIAL PRIMARY KEY,

    -- 关联关系
    bio_resource_id BIGINT NOT NULL,            -- 关联生物资源
    disease_id BIGINT NOT NULL,                 -- 关联疾病

    -- 证据类型 (可以有多种证据)
    evidence_therapeutic_target TEXT,           -- 治疗靶点证据 (靶点列表)
    evidence_transcriptome BOOLEAN DEFAULT FALSE,  -- 转录组证据
    evidence_clinical_trial_plant TEXT,         -- 植物临床试验 (试验ID)
    evidence_clinical_trial_ingredient TEXT,    -- 成分临床试验 (试验ID)

    -- 置信度
    confidence_score DECIMAL(3,2),              -- 置信度评分 (0-1)

    -- 来源信息
    source VARCHAR(100) DEFAULT 'CMAUP',        -- 数据来源
    source_version VARCHAR(50),                 -- 数据版本

    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 外键约束
    CONSTRAINT fk_brda_bio_resource FOREIGN KEY (bio_resource_id)
        REFERENCES bio_resources(id) ON DELETE CASCADE,
    CONSTRAINT fk_brda_disease FOREIGN KEY (disease_id)
        REFERENCES diseases(id) ON DELETE CASCADE,

    -- 唯一约束
    CONSTRAINT uk_bio_resource_disease UNIQUE (bio_resource_id, disease_id)
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_brda_bio_resource ON bio_resource_disease_associations(bio_resource_id);
CREATE INDEX IF NOT EXISTS idx_brda_disease ON bio_resource_disease_associations(disease_id);
CREATE INDEX IF NOT EXISTS idx_brda_confidence ON bio_resource_disease_associations(confidence_score);

-- 添加注释
COMMENT ON TABLE bio_resource_disease_associations IS '生物资源-疾病关联表 - 记录植物与疾病的关联及证据';
COMMENT ON COLUMN bio_resource_disease_associations.bio_resource_id IS '关联的生物资源ID';
COMMENT ON COLUMN bio_resource_disease_associations.disease_id IS '关联的疾病ID';
COMMENT ON COLUMN bio_resource_disease_associations.evidence_therapeutic_target IS '治疗靶点证据（靶点列表，分号分隔）';
COMMENT ON COLUMN bio_resource_disease_associations.evidence_transcriptome IS '转录组证据（布尔值）';
COMMENT ON COLUMN bio_resource_disease_associations.evidence_clinical_trial_plant IS '植物临床试验证据（试验ID，分号分隔）';
COMMENT ON COLUMN bio_resource_disease_associations.evidence_clinical_trial_ingredient IS '成分临床试验证据（试验ID，分号分隔）';
COMMENT ON COLUMN bio_resource_disease_associations.confidence_score IS '置信度评分（0-1之间的小数）';
COMMENT ON COLUMN bio_resource_disease_associations.source IS '数据来源';
COMMENT ON COLUMN bio_resource_disease_associations.source_version IS '数据版本';
