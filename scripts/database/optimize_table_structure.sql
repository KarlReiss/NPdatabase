-- ============================================
-- 数据库表结构优化脚本
-- 执行时间: 2026-01-28
--
-- 优化内容:
-- 1. 删除 species 表，合并到 bio_resources
-- 2. 重命名 compounds 为 natural_products
-- 3. 重命名相关关联表和字段
-- ============================================

-- ============================================
-- Step 1: 删除依赖的视图
-- ============================================
DROP VIEW IF EXISTS v_compound_detail CASCADE;
DROP VIEW IF EXISTS v_bio_resource_detail CASCADE;
DROP VIEW IF EXISTS v_target_detail CASCADE;
DROP VIEW IF EXISTS v_prescription_detail CASCADE;


-- ============================================
-- Step 2: 删除旧的关联表和 species 表
-- ============================================
DROP TABLE IF EXISTS compound_species CASCADE;
DROP TABLE IF EXISTS species CASCADE;

-- 删除 species 相关的触发器（如果存在）
DROP TRIGGER IF EXISTS update_species_updated_at ON species;


-- ============================================
-- Step 3: 重命名 compounds 表为 natural_products
-- ============================================
ALTER TABLE compounds RENAME TO natural_products;

-- 重命名 compounds 表的索引
ALTER INDEX IF EXISTS idx_compounds_np_id RENAME TO idx_natural_products_np_id;
ALTER INDEX IF EXISTS idx_compounds_inchikey RENAME TO idx_natural_products_inchikey;
ALTER INDEX IF EXISTS idx_compounds_pref_name RENAME TO idx_natural_products_pref_name;
ALTER INDEX IF EXISTS idx_compounds_chembl_id RENAME TO idx_natural_products_chembl_id;
ALTER INDEX IF EXISTS idx_compounds_pubchem_id RENAME TO idx_natural_products_pubchem_id;
ALTER INDEX IF EXISTS idx_compounds_mw RENAME TO idx_natural_products_mw;
ALTER INDEX IF EXISTS idx_compounds_xlogp RENAME TO idx_natural_products_xlogp;
ALTER INDEX IF EXISTS idx_compounds_psa RENAME TO idx_natural_products_psa;
ALTER INDEX IF EXISTS idx_compounds_num_activity RENAME TO idx_natural_products_num_activity;
ALTER INDEX IF EXISTS idx_compounds_num_target RENAME TO idx_natural_products_num_target;
ALTER INDEX IF EXISTS idx_compounds_pref_name_gin RENAME TO idx_natural_products_pref_name_gin;
ALTER INDEX IF EXISTS idx_compounds_iupac_name_gin RENAME TO idx_natural_products_iupac_name_gin;

-- 重命名 compounds 表的触发器
DROP TRIGGER IF EXISTS update_compounds_updated_at ON natural_products;
CREATE TRIGGER update_natural_products_updated_at BEFORE UPDATE ON natural_products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


-- ============================================
-- Step 4: 重命名 bio_resource_compounds 表
-- ============================================
ALTER TABLE bio_resource_compounds RENAME TO bio_resource_natural_products;
ALTER TABLE bio_resource_natural_products RENAME COLUMN compound_id TO natural_product_id;

-- 重命名索引
ALTER INDEX IF EXISTS idx_brc_bio_resource RENAME TO idx_brnp_bio_resource;
ALTER INDEX IF EXISTS idx_brc_compound RENAME TO idx_brnp_natural_product;

-- 重命名约束
ALTER TABLE bio_resource_natural_products RENAME CONSTRAINT uk_bio_resource_compound TO uk_bio_resource_natural_product;
ALTER TABLE bio_resource_natural_products RENAME CONSTRAINT fk_brc_bio_resource TO fk_brnp_bio_resource;
ALTER TABLE bio_resource_natural_products RENAME CONSTRAINT fk_brc_compound TO fk_brnp_natural_product;


-- ============================================
-- Step 5: 重命名 prescription_compounds 表
-- ============================================
ALTER TABLE prescription_compounds RENAME TO prescription_natural_products;
ALTER TABLE prescription_natural_products RENAME COLUMN compound_id TO natural_product_id;

-- 重命名索引
ALTER INDEX IF EXISTS idx_pc_prescription RENAME TO idx_pnp_prescription;
ALTER INDEX IF EXISTS idx_pc_compound RENAME TO idx_pnp_natural_product;

-- 重命名约束
ALTER TABLE prescription_natural_products RENAME CONSTRAINT uk_prescription_compound TO uk_prescription_natural_product;
ALTER TABLE prescription_natural_products RENAME CONSTRAINT fk_pc_prescription TO fk_pnp_prescription;
ALTER TABLE prescription_natural_products RENAME CONSTRAINT fk_pc_compound TO fk_pnp_natural_product;
ALTER TABLE prescription_natural_products RENAME CONSTRAINT fk_pc_source_resource TO fk_pnp_source_resource;


-- ============================================
-- Step 6: 修改 bioactivity 表的外键字段
-- ============================================
ALTER TABLE bioactivity RENAME COLUMN compound_id TO natural_product_id;

-- 重命名索引
ALTER INDEX IF EXISTS idx_bioactivity_compound RENAME TO idx_bioactivity_natural_product;
ALTER INDEX IF EXISTS idx_bioactivity_compound_target RENAME TO idx_bioactivity_natural_product_target;

-- 重命名约束
ALTER TABLE bioactivity RENAME CONSTRAINT fk_bioactivity_compound TO fk_bioactivity_natural_product;


-- ============================================
-- Step 7: 修改 toxicity 表的外键字段
-- ============================================
ALTER TABLE toxicity RENAME COLUMN compound_id TO natural_product_id;

-- 重命名索引
ALTER INDEX IF EXISTS idx_toxicity_compound RENAME TO idx_toxicity_natural_product;

-- 重命名约束
ALTER TABLE toxicity RENAME CONSTRAINT fk_toxicity_compound TO fk_toxicity_natural_product;


-- ============================================
-- Step 8: 重建视图
-- ============================================

-- 天然产物详情视图
CREATE OR REPLACE VIEW v_natural_product_detail AS
SELECT
    np.id,
    np.np_id,
    np.pref_name,
    np.molecular_weight,
    np.xlogp,
    np.psa,
    np.num_of_activity,
    np.num_of_target,
    np.num_of_organism,
    (SELECT COUNT(*) FROM bioactivity b WHERE b.natural_product_id = np.id) as bioactivity_count,
    (SELECT COUNT(DISTINCT b.target_id) FROM bioactivity b WHERE b.natural_product_id = np.id) as target_count,
    (SELECT COUNT(*) FROM bio_resource_natural_products brnp WHERE brnp.natural_product_id = np.id) as bio_resource_count,
    (SELECT MIN(b.activity_value_std) FROM bioactivity b WHERE b.natural_product_id = np.id AND b.activity_value_std > 0) as best_activity_value,
    (SELECT COUNT(*) > 0 FROM toxicity t WHERE t.natural_product_id = np.id) as has_toxicity
FROM natural_products np;

COMMENT ON VIEW v_natural_product_detail IS '天然产物详情视图 - 包含统计信息';


-- 生物资源详情视图
CREATE OR REPLACE VIEW v_bio_resource_detail AS
SELECT
    br.id,
    br.resource_id,
    br.resource_type,
    br.chinese_name,
    br.latin_name,
    br.taxonomy_family,
    br.taxonomy_genus,
    br.num_of_natural_products,
    br.num_of_prescriptions
FROM bio_resources br;

COMMENT ON VIEW v_bio_resource_detail IS '生物资源详情视图 - 包含统计信息';


-- 靶点详情视图
CREATE OR REPLACE VIEW v_target_detail AS
SELECT
    t.id,
    t.target_id,
    t.target_type,
    t.target_name,
    t.gene_name,
    t.num_of_natural_products,
    t.num_of_activities,
    (SELECT COUNT(DISTINCT b.natural_product_id) FROM bioactivity b WHERE b.target_id = t.id) as natural_product_count,
    (SELECT COUNT(*) FROM bioactivity b WHERE b.target_id = t.id) as bioactivity_count,
    (SELECT MIN(b.activity_value_std) FROM bioactivity b WHERE b.target_id = t.id AND b.activity_value_std > 0) as best_activity_value
FROM targets t;

COMMENT ON VIEW v_target_detail IS '靶点详情视图 - 包含统计信息';


-- 处方详情视图
CREATE OR REPLACE VIEW v_prescription_detail AS
SELECT
    p.id,
    p.prescription_id,
    p.chinese_name,
    p.category,
    p.num_of_herbs,
    p.num_of_natural_products,
    (SELECT COUNT(*) FROM prescription_resources pr WHERE pr.prescription_id = p.id) as herb_count,
    (SELECT COUNT(*) FROM prescription_natural_products pnp WHERE pnp.prescription_id = p.id) as direct_natural_product_count
FROM prescriptions p;

COMMENT ON VIEW v_prescription_detail IS '处方详情视图 - 包含统计信息';


-- ============================================
-- Step 9: 更新表注释
-- ============================================
COMMENT ON TABLE natural_products IS '天然产物表 - 存储天然产物的基本信息、结构和理化性质';
COMMENT ON COLUMN natural_products.np_id IS 'NPASS 天然产物 ID (如 NPC491451)';
COMMENT ON COLUMN natural_products.molecular_weight IS '分子量 (g/mol)';
COMMENT ON COLUMN natural_products.xlogp IS '脂水分配系数 (计算值)';
COMMENT ON COLUMN natural_products.psa IS '极性表面积 (Å²)';

COMMENT ON TABLE bio_resources IS '生物资源表 - 存储植物、动物、微生物、矿物等天然产物来源，包含分类学信息和药用属性';

COMMENT ON TABLE bio_resource_natural_products IS '生物资源-天然产物关联表 - 记录生物资源包含的天然产物';

COMMENT ON TABLE prescription_natural_products IS '处方-天然产物关联表 - 记录处方包含的天然产物（直接关联）';

COMMENT ON TABLE bioactivity IS '活性记录表 - 存储天然产物对靶点的生物活性数据';
COMMENT ON COLUMN bioactivity.natural_product_id IS '关联的天然产物 ID';

COMMENT ON TABLE toxicity IS '毒性表 - 存储天然产物的毒性数据';


-- ============================================
-- Step 10: 更新 bio_resources 表的统计字段名称
-- ============================================
-- 将 num_of_compounds 重命名为 num_of_natural_products
ALTER TABLE bio_resources RENAME COLUMN num_of_compounds TO num_of_natural_products;
COMMENT ON COLUMN bio_resources.num_of_natural_products IS '包含的天然产物数量';

-- 将 prescriptions 表的 num_of_compounds 重命名为 num_of_natural_products
ALTER TABLE prescriptions RENAME COLUMN num_of_compounds TO num_of_natural_products;
COMMENT ON COLUMN prescriptions.num_of_natural_products IS '包含的天然产物数量 (间接)';


-- ============================================
-- 完成提示
-- ============================================
-- 数据库表结构优化完成！
--
-- 最终表结构 (9张表):
-- 1. natural_products - 天然产物表（核心表）
-- 2. targets - 靶点表
-- 3. bioactivity - 活性记录表
-- 4. toxicity - 毒性记录表
-- 5. bio_resources - 生物资源表（植物/动物/微生物/矿物）
-- 6. bio_resource_natural_products - 生物资源-天然产物关联表
-- 7. prescriptions - 处方/方剂表
-- 8. prescription_resources - 处方-生物资源关联表
-- 9. prescription_natural_products - 处方-天然产物关联表
--
-- 视图 (4个):
-- 1. v_natural_product_detail - 天然产物详情视图
-- 2. v_bio_resource_detail - 生物资源详情视图
-- 3. v_target_detail - 靶点详情视图
-- 4. v_prescription_detail - 处方详情视图
--
-- 验证方法:
-- psql npdb -c "\dt"  -- 检查表列表
-- psql npdb -c "\dv"  -- 检查视图列表
-- psql npdb -c "\d natural_products"  -- 验证表结构
-- ============================================
