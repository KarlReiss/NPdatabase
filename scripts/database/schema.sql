-- ============================================
-- Natural Product Database Schema
-- 基于 NPASS 3.0 数据结构设计
-- 数据库: PostgreSQL (推荐) 或 MySQL
-- ============================================

-- 删除已存在的表（开发环境使用，生产环境请注释）
DROP TABLE IF EXISTS compound_species CASCADE;
DROP TABLE IF EXISTS toxicity CASCADE;
DROP TABLE IF EXISTS bioactivity CASCADE;
DROP TABLE IF EXISTS targets CASCADE;
DROP TABLE IF EXISTS species CASCADE;
DROP TABLE IF EXISTS compounds CASCADE;

-- ============================================
-- 1. 化合物表 (Compounds)
-- 来源: NPASS3.0_naturalproducts_generalinfo.txt + structure.txt
-- ============================================
CREATE TABLE compounds (
    id BIGSERIAL PRIMARY KEY,

    -- 基本标识
    np_id VARCHAR(50) UNIQUE NOT NULL,              -- NPC491451
    inchikey VARCHAR(100),                          -- InChIKey

    -- 名称
    pref_name VARCHAR(500),                         -- 首选名称
    iupac_name TEXT,                                -- IUPAC 名称
    name_initial VARCHAR(10),                       -- 名称首字母

    -- 结构信息
    inchi TEXT,                                     -- InChI
    smiles TEXT,                                    -- SMILES

    -- 外部数据库 ID
    chembl_id VARCHAR(50),                          -- ChEMBL ID
    pubchem_id VARCHAR(50),                         -- PubChem CID

    -- 理化性质（需要计算或补充）
    molecular_weight DECIMAL(10,2),                 -- 分子量
    xlogp DECIMAL(10,2),                           -- 脂水分配系数
    psa DECIMAL(10,2),                             -- 极性表面积
    formula VARCHAR(200),                           -- 分子式
    h_bond_donors INT,                              -- 氢键供体数
    h_bond_acceptors INT,                           -- 氢键受体数
    rotatable_bonds INT,                            -- 可旋转键数

    -- 统计信息（来自原始数据）
    num_of_organism INT DEFAULT 0,                  -- 关联物种数
    num_of_target INT DEFAULT 0,                    -- 关联靶点数
    num_of_activity INT DEFAULT 0,                  -- 活性记录数

    -- 其他信息
    gene_cluster TEXT,                              -- 基因簇信息
    if_quantity BOOLEAN DEFAULT FALSE,              -- 是否有定量数据

    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 索引
    CONSTRAINT chk_mw CHECK (molecular_weight IS NULL OR molecular_weight > 0)
);

-- 化合物表索引
CREATE INDEX idx_compounds_np_id ON compounds(np_id);
CREATE INDEX idx_compounds_inchikey ON compounds(inchikey);
CREATE INDEX idx_compounds_pref_name ON compounds(pref_name);
CREATE INDEX idx_compounds_chembl_id ON compounds(chembl_id);
CREATE INDEX idx_compounds_pubchem_id ON compounds(pubchem_id);
CREATE INDEX idx_compounds_mw ON compounds(molecular_weight);
CREATE INDEX idx_compounds_xlogp ON compounds(xlogp);
CREATE INDEX idx_compounds_psa ON compounds(psa);
CREATE INDEX idx_compounds_num_activity ON compounds(num_of_activity);
CREATE INDEX idx_compounds_num_target ON compounds(num_of_target);

-- 全文搜索索引（PostgreSQL）
CREATE INDEX idx_compounds_pref_name_gin ON compounds USING gin(to_tsvector('english', COALESCE(pref_name, '')));
CREATE INDEX idx_compounds_iupac_name_gin ON compounds USING gin(to_tsvector('english', COALESCE(iupac_name, '')));

COMMENT ON TABLE compounds IS '化合物表 - 存储天然产物的基本信息和理化性质';
COMMENT ON COLUMN compounds.np_id IS 'NPASS 化合物 ID (如 NPC491451)';
COMMENT ON COLUMN compounds.molecular_weight IS '分子量 (g/mol)';
COMMENT ON COLUMN compounds.xlogp IS '脂水分配系数 (计算值)';
COMMENT ON COLUMN compounds.psa IS '极性表面积 (Å²)';


-- ============================================
-- 2. 靶点表 (Targets)
-- 来源: NPASS3.0_target.txt
-- ============================================
CREATE TABLE targets (
    id BIGSERIAL PRIMARY KEY,

    -- 基本标识
    target_id VARCHAR(50) UNIQUE NOT NULL,          -- NPT918
    target_type VARCHAR(50),                        -- Cell line, Protein, Gene, Enzyme
    target_name VARCHAR(500),                       -- 靶点名称

    -- 物种信息
    target_organism VARCHAR(200),                   -- 物种名称
    target_organism_tax_id VARCHAR(50),             -- 物种分类 ID

    -- 外部数据库 ID
    uniprot_id VARCHAR(50),                         -- UniProt ID

    -- 统计信息
    num_of_compounds INT DEFAULT 0,                 -- 关联化合物数
    num_of_activities INT DEFAULT 0,                -- 活性记录数

    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 靶点表索引
CREATE INDEX idx_targets_target_id ON targets(target_id);
CREATE INDEX idx_targets_type ON targets(target_type);
CREATE INDEX idx_targets_name ON targets(target_name);
CREATE INDEX idx_targets_organism ON targets(target_organism);
CREATE INDEX idx_targets_uniprot ON targets(uniprot_id);

-- 全文搜索索引
CREATE INDEX idx_targets_name_gin ON targets USING gin(to_tsvector('english', COALESCE(target_name, '')));

COMMENT ON TABLE targets IS '靶点表 - 存储生物靶点信息（蛋白、细胞系、基因等）';
COMMENT ON COLUMN targets.target_type IS '靶点类型: Cell line, Protein, Gene, Enzyme';


-- ============================================
-- 3. 活性记录表 (Bioactivity)
-- 来源: NPASS3.0_activities.txt
-- ============================================
CREATE TABLE bioactivity (
    id BIGSERIAL PRIMARY KEY,

    -- 关联关系
    compound_id BIGINT NOT NULL,                    -- 关联化合物
    target_id BIGINT NOT NULL,                      -- 关联靶点

    -- 活性类型
    activity_type VARCHAR(50),                      -- IC50, EC50, Ki, Kd, GI50, etc.
    activity_type_grouped VARCHAR(50),              -- 分组类型
    activity_relation VARCHAR(10),                  -- =, >, <, >=, <=, ~

    -- 活性值（原始）
    activity_value DECIMAL(20,6),                   -- 原始活性值
    activity_units VARCHAR(20),                     -- 原始单位 (nM, μM, mM, M)

    -- 活性值（标准化为 nM）
    activity_value_std DECIMAL(20,6),               -- 标准化活性值
    activity_units_std VARCHAR(20) DEFAULT 'nM',    -- 标准化单位

    -- 实验条件
    assay_organism VARCHAR(200),                    -- 实验物种
    assay_tax_id VARCHAR(50),                       -- 实验物种分类 ID
    assay_strain VARCHAR(200),                      -- 菌株/品系
    assay_tissue VARCHAR(200),                      -- 组织
    assay_cell_type VARCHAR(200),                   -- 细胞类型

    -- 参考文献
    ref_id VARCHAR(50),                             -- 文献 ID
    ref_id_type VARCHAR(20),                        -- PMID, DOI, Patent

    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 外键约束
    CONSTRAINT fk_bioactivity_compound FOREIGN KEY (compound_id) REFERENCES compounds(id) ON DELETE CASCADE,
    CONSTRAINT fk_bioactivity_target FOREIGN KEY (target_id) REFERENCES targets(id) ON DELETE CASCADE,

    -- 检查约束
    CONSTRAINT chk_activity_value CHECK (activity_value IS NULL OR activity_value >= 0),
    CONSTRAINT chk_activity_value_std CHECK (activity_value_std IS NULL OR activity_value_std >= 0)
);

-- 活性记录表索引
CREATE INDEX idx_bioactivity_compound ON bioactivity(compound_id);
CREATE INDEX idx_bioactivity_target ON bioactivity(target_id);
CREATE INDEX idx_bioactivity_type ON bioactivity(activity_type);
CREATE INDEX idx_bioactivity_type_grouped ON bioactivity(activity_type_grouped);
CREATE INDEX idx_bioactivity_value_std ON bioactivity(activity_value_std);
CREATE INDEX idx_bioactivity_relation ON bioactivity(activity_relation);
CREATE INDEX idx_bioactivity_ref_id ON bioactivity(ref_id);
CREATE INDEX idx_bioactivity_compound_target ON bioactivity(compound_id, target_id);

COMMENT ON TABLE bioactivity IS '活性记录表 - 存储化合物对靶点的生物活性数据';
COMMENT ON COLUMN bioactivity.activity_value_std IS '标准化活性值 (统一转换为 nM)';
COMMENT ON COLUMN bioactivity.activity_relation IS '活性关系: = (等于), > (大于), < (小于)';


-- ============================================
-- 4. 物种表 (Species)
-- 来源: NPASS3.0_species_info.txt
-- ============================================
CREATE TABLE species (
    id BIGSERIAL PRIMARY KEY,

    -- 基本标识
    org_id VARCHAR(50) UNIQUE NOT NULL,             -- NPO1
    org_name VARCHAR(500),                          -- 物种名称
    org_name_initial VARCHAR(10),                   -- 名称首字母
    org_tax_level VARCHAR(50),                      -- 分类级别
    org_tax_id VARCHAR(50),                         -- 分类 ID

    -- 亚种信息
    subspecies_tax_id VARCHAR(50),
    subspecies_name VARCHAR(500),

    -- 分类学层级
    species_tax_id VARCHAR(50),
    species_name VARCHAR(500),
    genus_tax_id VARCHAR(50),
    genus_name VARCHAR(200),
    family_tax_id VARCHAR(50),
    family_name VARCHAR(200),
    kingdom_tax_id VARCHAR(50),
    kingdom_name VARCHAR(100),
    superkingdom_tax_id VARCHAR(50),
    superkingdom_name VARCHAR(100),

    -- 统计信息
    num_of_np_act INT DEFAULT 0,                    -- 有活性的化合物数
    num_of_np_no_act INT DEFAULT 0,                 -- 无活性的化合物数
    num_of_np_quantity INT DEFAULT 0,               -- 有定量数据的化合物数

    -- 特殊标记
    if_org_coculture BOOLEAN DEFAULT FALSE,         -- 是否共培养
    if_org_engineered BOOLEAN DEFAULT FALSE,        -- 是否工程菌
    if_org_symbiont BOOLEAN DEFAULT FALSE,          -- 是否共生菌

    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 物种表索引
CREATE INDEX idx_species_org_id ON species(org_id);
CREATE INDEX idx_species_org_name ON species(org_name);
CREATE INDEX idx_species_tax_id ON species(org_tax_id);
CREATE INDEX idx_species_kingdom ON species(kingdom_name);
CREATE INDEX idx_species_family ON species(family_name);
CREATE INDEX idx_species_genus ON species(genus_name);
CREATE INDEX idx_species_name_initial ON species(org_name_initial);

-- 全文搜索索引
CREATE INDEX idx_species_org_name_gin ON species USING gin(to_tsvector('english', COALESCE(org_name, '')));

COMMENT ON TABLE species IS '物种表 - 存储天然产物来源生物的分类学信息';
COMMENT ON COLUMN species.org_tax_level IS '分类级别: Species, Genus, Family, etc.';


-- ============================================
-- 5. 化合物-物种关联表 (Compound-Species)
-- 来源: NPASS3.0_naturalproducts_species_pair.txt
-- ============================================
CREATE TABLE compound_species (
    id BIGSERIAL PRIMARY KEY,

    -- 关联关系
    compound_id BIGINT NOT NULL,                    -- 关联化合物
    species_id BIGINT NOT NULL,                     -- 关联物种

    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 外键约束
    CONSTRAINT fk_compound_species_compound FOREIGN KEY (compound_id) REFERENCES compounds(id) ON DELETE CASCADE,
    CONSTRAINT fk_compound_species_species FOREIGN KEY (species_id) REFERENCES species(id) ON DELETE CASCADE,

    -- 唯一约束
    CONSTRAINT uk_compound_species UNIQUE (compound_id, species_id)
);

-- 化合物-物种关联表索引
CREATE INDEX idx_compound_species_compound ON compound_species(compound_id);
CREATE INDEX idx_compound_species_species ON compound_species(species_id);

COMMENT ON TABLE compound_species IS '化合物-物种关联表 - 记录化合物的生物来源';


-- ============================================
-- 6. 毒性表 (Toxicity)
-- 来源: NPASS3.0_toxicity.txt
-- ============================================
CREATE TABLE toxicity (
    id BIGSERIAL PRIMARY KEY,

    -- 关联关系
    compound_id BIGINT NOT NULL,                    -- 关联化合物

    -- 毒性信息
    toxicity_type VARCHAR(100),                     -- 毒性类型
    toxicity_value DECIMAL(20,6),                   -- 毒性值
    toxicity_units VARCHAR(50),                     -- 毒性单位
    dose VARCHAR(100),                              -- 剂量
    symptoms TEXT,                                  -- 症状描述

    -- 实验信息
    assay_organism VARCHAR(200),                    -- 实验物种
    assay_method VARCHAR(200),                      -- 实验方法

    -- 参考文献
    ref_id VARCHAR(50),                             -- 文献 ID
    ref_id_type VARCHAR(20),                        -- PMID, DOI

    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 外键约束
    CONSTRAINT fk_toxicity_compound FOREIGN KEY (compound_id) REFERENCES compounds(id) ON DELETE CASCADE
);

-- 毒性表索引
CREATE INDEX idx_toxicity_compound ON toxicity(compound_id);
CREATE INDEX idx_toxicity_type ON toxicity(toxicity_type);
CREATE INDEX idx_toxicity_ref_id ON toxicity(ref_id);

COMMENT ON TABLE toxicity IS '毒性表 - 存储化合物的毒性数据';


-- ============================================
-- 7. 视图：化合物详情视图
-- ============================================
CREATE OR REPLACE VIEW v_compound_detail AS
SELECT
    c.*,
    COUNT(DISTINCT b.id) as bioactivity_count,
    COUNT(DISTINCT b.target_id) as target_count,
    COUNT(DISTINCT cs.species_id) as species_count,
    MIN(b.activity_value_std) as best_activity_value,
    EXISTS(SELECT 1 FROM toxicity t WHERE t.compound_id = c.id) as has_toxicity
FROM compounds c
LEFT JOIN bioactivity b ON c.id = b.compound_id
LEFT JOIN compound_species cs ON c.id = cs.compound_id
GROUP BY c.id;

COMMENT ON VIEW v_compound_detail IS '化合物详情视图 - 包含统计信息';


-- ============================================
-- 8. 视图：靶点详情视图
-- ============================================
CREATE OR REPLACE VIEW v_target_detail AS
SELECT
    t.*,
    COUNT(DISTINCT b.compound_id) as compound_count,
    COUNT(DISTINCT b.id) as bioactivity_count,
    MIN(b.activity_value_std) as best_activity_value
FROM targets t
LEFT JOIN bioactivity b ON t.id = b.target_id
GROUP BY t.id;

COMMENT ON VIEW v_target_detail IS '靶点详情视图 - 包含统计信息';


-- ============================================
-- 9. 触发器：更新时间戳
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_compounds_updated_at BEFORE UPDATE ON compounds
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_targets_updated_at BEFORE UPDATE ON targets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_species_updated_at BEFORE UPDATE ON species
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


-- ============================================
-- 10. 初始化统计信息
-- ============================================
-- 这些统计信息将在数据导入后更新
-- 可以通过触发器或定期任务维护


-- ============================================
-- 完成提示
-- ============================================
-- 数据库表结构创建完成！
--
-- 下一步:
-- 1. 运行数据导入脚本 (scripts/data-import/)
-- 2. 验证数据完整性
-- 3. 更新统计信息
-- 4. 创建额外的索引（根据查询性能需求）
-- ============================================
