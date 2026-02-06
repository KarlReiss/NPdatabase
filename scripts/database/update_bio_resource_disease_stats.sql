-- ============================================================================
-- 更新植物-疾病关联统计字段
-- ============================================================================
-- 文件: update_bio_resource_disease_stats.sql
-- 描述: 在导入 bio_resource_disease_associations 数据后，更新相关表的统计字段
-- 使用时机: 在运行 import_bio_resource_disease_associations.py 之后
-- ============================================================================

-- 1. 更新 bio_resources 表的疾病关联数
-- ============================================================================
DO $$
DECLARE
    updated_count INTEGER;
BEGIN
    RAISE NOTICE '开始更新 bio_resources 表的疾病关联数...';

    -- 检查 num_of_related_diseases 字段是否存在
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'bio_resources'
        AND column_name = 'num_of_related_diseases'
    ) THEN
        -- 如果字段不存在，先添加
        RAISE NOTICE '添加 num_of_related_diseases 字段...';
        ALTER TABLE bio_resources ADD COLUMN num_of_related_diseases INT DEFAULT 0;
    END IF;

    -- 更新统计数据
    UPDATE bio_resources br
    SET num_of_related_diseases = (
        SELECT COUNT(DISTINCT disease_id)
        FROM bio_resource_disease_associations
        WHERE bio_resource_id = br.id
    );

    GET DIAGNOSTICS updated_count = ROW_COUNT;
    RAISE NOTICE '已更新 % 条 bio_resources 记录', updated_count;
END $$;

-- 2. 更新 diseases 表的植物关联数
-- ============================================================================
DO $$
DECLARE
    updated_count INTEGER;
BEGIN
    RAISE NOTICE '开始更新 diseases 表的植物关联数...';

    -- 更新统计数据
    UPDATE diseases d
    SET num_of_related_plants = (
        SELECT COUNT(DISTINCT bio_resource_id)
        FROM bio_resource_disease_associations
        WHERE disease_id = d.id
    );

    GET DIAGNOSTICS updated_count = ROW_COUNT;
    RAISE NOTICE '已更新 % 条 diseases 记录', updated_count;
END $$;

-- 3. 显示统计摘要
-- ============================================================================
DO $$
DECLARE
    total_associations INTEGER;
    total_bio_resources INTEGER;
    total_diseases INTEGER;
    avg_diseases_per_resource NUMERIC;
    avg_resources_per_disease NUMERIC;
    max_diseases_per_resource INTEGER;
    max_resources_per_disease INTEGER;
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE '统计摘要';
    RAISE NOTICE '========================================';

    -- 关联总数
    SELECT COUNT(*) INTO total_associations
    FROM bio_resource_disease_associations;
    RAISE NOTICE '总关联数: %', total_associations;

    -- 有关联的生物资源数
    SELECT COUNT(*) INTO total_bio_resources
    FROM bio_resources
    WHERE num_of_related_diseases > 0;
    RAISE NOTICE '有疾病关联的生物资源数: %', total_bio_resources;

    -- 有关联的疾病数
    SELECT COUNT(*) INTO total_diseases
    FROM diseases
    WHERE num_of_related_plants > 0;
    RAISE NOTICE '有植物关联的疾病数: %', total_diseases;

    -- 平均每个生物资源关联的疾病数
    SELECT AVG(num_of_related_diseases) INTO avg_diseases_per_resource
    FROM bio_resources
    WHERE num_of_related_diseases > 0;
    RAISE NOTICE '平均每个生物资源关联的疾病数: %', ROUND(avg_diseases_per_resource, 2);

    -- 平均每个疾病关联的植物数
    SELECT AVG(num_of_related_plants) INTO avg_resources_per_disease
    FROM diseases
    WHERE num_of_related_plants > 0;
    RAISE NOTICE '平均每个疾病关联的植物数: %', ROUND(avg_resources_per_disease, 2);

    -- 最多疾病关联的生物资源
    SELECT MAX(num_of_related_diseases) INTO max_diseases_per_resource
    FROM bio_resources;
    RAISE NOTICE '单个生物资源最多关联疾病数: %', max_diseases_per_resource;

    -- 最多植物关联的疾病
    SELECT MAX(num_of_related_plants) INTO max_resources_per_disease
    FROM diseases;
    RAISE NOTICE '单个疾病最多关联植物数: %', max_resources_per_disease;

    RAISE NOTICE '========================================';
END $$;

-- 4. 显示置信度分布
-- ============================================================================
SELECT
    confidence_score,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM bio_resource_disease_associations
GROUP BY confidence_score
ORDER BY confidence_score DESC;

-- 5. 显示证据类型统计
-- ============================================================================
SELECT
    '治疗靶点证据' as evidence_type,
    COUNT(*) FILTER (WHERE evidence_therapeutic_target IS NOT NULL) as count,
    ROUND(COUNT(*) FILTER (WHERE evidence_therapeutic_target IS NOT NULL) * 100.0 / COUNT(*), 2) as percentage
FROM bio_resource_disease_associations
UNION ALL
SELECT
    '转录组证据',
    COUNT(*) FILTER (WHERE evidence_transcriptome = TRUE),
    ROUND(COUNT(*) FILTER (WHERE evidence_transcriptome = TRUE) * 100.0 / COUNT(*), 2)
FROM bio_resource_disease_associations
UNION ALL
SELECT
    '植物临床试验',
    COUNT(*) FILTER (WHERE evidence_clinical_trial_plant IS NOT NULL),
    ROUND(COUNT(*) FILTER (WHERE evidence_clinical_trial_plant IS NOT NULL) * 100.0 / COUNT(*), 2)
FROM bio_resource_disease_associations
UNION ALL
SELECT
    '成分临床试验',
    COUNT(*) FILTER (WHERE evidence_clinical_trial_ingredient IS NOT NULL),
    ROUND(COUNT(*) FILTER (WHERE evidence_clinical_trial_ingredient IS NOT NULL) * 100.0 / COUNT(*), 2)
FROM bio_resource_disease_associations;

-- 6. 显示Top 10 生物资源（按疾病关联数）
-- ============================================================================
SELECT
    br.resource_id,
    br.latin_name,
    br.chinese_name,
    br.num_of_related_diseases
FROM bio_resources br
WHERE br.num_of_related_diseases > 0
ORDER BY br.num_of_related_diseases DESC
LIMIT 10;

-- 7. 显示Top 10 疾病（按植物关联数）
-- ============================================================================
SELECT
    d.icd11_code,
    d.disease_name,
    d.disease_category,
    d.num_of_related_plants
FROM diseases d
WHERE d.num_of_related_plants > 0
ORDER BY d.num_of_related_plants DESC
LIMIT 10;

-- ============================================================================
-- 完成
-- ============================================================================
\echo '统计字段更新完成！'
