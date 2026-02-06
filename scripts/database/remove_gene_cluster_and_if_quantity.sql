-- ============================================
-- 删除 gene_cluster 和 if_quantity 字段
-- 原因：
--   - gene_cluster: 0条记录有数据（0%）
--   - if_quantity: 仅6,072条记录为TRUE（2.99%），使用率很低
-- 日期：2026-02-05
-- ============================================

-- 1. 先删除依赖该字段的视图
DROP VIEW IF EXISTS v_natural_product_detail;

-- 2. 删除字段
ALTER TABLE natural_products DROP COLUMN IF EXISTS gene_cluster;
ALTER TABLE natural_products DROP COLUMN IF EXISTS if_quantity;

-- 3. 重新创建视图（不包含已删除的字段）
CREATE OR REPLACE VIEW v_natural_product_detail AS
SELECT
    np.id,
    np.np_id,
    np.inchikey,
    np.pref_name,
    np.iupac_name,
    np.name_initial,
    np.inchi,
    np.smiles,
    np.chembl_id,
    np.pubchem_id,
    np.molecular_weight,
    np.xlogp,
    np.psa,
    np.formula,
    np.h_bond_donors,
    np.h_bond_acceptors,
    np.rotatable_bonds,
    np.num_of_organism,
    np.num_of_target,
    np.num_of_activity,
    np.created_at,
    np.updated_at,
    -- 聚合统计
    COUNT(DISTINCT b.id) AS bioactivity_count,
    COUNT(DISTINCT b.target_id) AS target_count,
    COUNT(DISTINCT brnp.bio_resource_id) AS bio_resource_count,
    MIN(b.activity_value_std) AS best_activity_value,
    EXISTS(SELECT 1 FROM toxicity t WHERE t.natural_product_id = np.id) AS has_toxicity
FROM natural_products np
LEFT JOIN bioactivity b ON np.id = b.natural_product_id
LEFT JOIN bio_resource_natural_products brnp ON np.id = brnp.natural_product_id
GROUP BY np.id;

-- 4. 添加视图注释
COMMENT ON VIEW v_natural_product_detail IS '天然产物详情视图 - 包含聚合统计信息（已移除gene_cluster和if_quantity字段）';

-- 5. 验证
SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'natural_products'
AND column_name IN ('gene_cluster', 'if_quantity');

-- 如果上面的查询返回空结果，说明字段已成功删除
