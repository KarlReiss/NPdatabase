-- ============================================
-- 新增表：生物资源表 + 处方表
-- 执行时间: 2026-01-28
-- ============================================

-- ============================================
-- 1. 生物资源表 (Bio-Resources)
-- 说明: 包含植物、动物、微生物、矿物等天然产物来源
-- 关系: 生物资源 → 包含多个天然产物 (compounds)
-- ============================================
CREATE TABLE bio_resources (
    id BIGSERIAL PRIMARY KEY,

    -- ========== 基本标识 ==========
    resource_id VARCHAR(50) UNIQUE NOT NULL,        -- 资源 ID (如 BR0001)
    resource_type VARCHAR(50) NOT NULL,             -- 资源类型: Plant, Animal, Microorganism, Mineral, Fungus

    -- ========== 名称信息 ==========
    chinese_name VARCHAR(500),                      -- 中文名 (如: 人参)
    latin_name VARCHAR(500),                        -- 拉丁名 (如: Panax ginseng)
    english_name VARCHAR(500),                      -- 英文名 (如: Ginseng)
    pinyin_name VARCHAR(200),                       -- 拼音名 (如: Ren Shen)
    alias TEXT,                                     -- 别名 (多个用逗号分隔)

    -- ========== 分类学信息 (主要用于植物/动物/微生物) ==========
    taxonomy_kingdom VARCHAR(100),                  -- 界 (Plantae, Animalia, Fungi, Bacteria)
    taxonomy_phylum VARCHAR(100),                   -- 门
    taxonomy_class VARCHAR(100),                    -- 纲
    taxonomy_order VARCHAR(100),                    -- 目
    taxonomy_family VARCHAR(200),                   -- 科
    taxonomy_genus VARCHAR(200),                    -- 属
    taxonomy_species VARCHAR(200),                  -- 种
    taxonomy_id VARCHAR(50),                        -- NCBI Taxonomy ID

    -- ========== 药用部位 (植物/动物) ==========
    medicinal_part VARCHAR(200),                    -- 药用部位 (根、茎、叶、花、果实、全草、骨、角等)
    medicinal_part_latin VARCHAR(200),              -- 药用部位拉丁名 (Radix, Herba, Flos, Fructus 等)

    -- ========== 产地与分布 ==========
    origin_region TEXT,                             -- 原产地
    distribution TEXT,                              -- 分布区域
    habitat TEXT,                                   -- 生境描述

    -- ========== 性味归经 (中医属性) ==========
    tcm_property VARCHAR(100),                      -- 性 (寒、热、温、凉、平)
    tcm_flavor VARCHAR(100),                        -- 味 (酸、苦、甘、辛、咸、淡、涩)
    tcm_meridian VARCHAR(200),                      -- 归经 (肝、心、脾、肺、肾等)
    tcm_toxicity VARCHAR(50),                       -- 毒性 (无毒、小毒、有毒、大毒)

    -- ========== 功效与主治 ==========
    functions TEXT,                                 -- 功效描述
    indications TEXT,                               -- 主治/适应症
    contraindications TEXT,                         -- 禁忌

    -- ========== 矿物特有属性 ==========
    mineral_composition VARCHAR(500),               -- 矿物成分 (如: CaCO3,ite calcium carbonate)
    mineral_crystal_system VARCHAR(100),            -- 晶系
    mineral_hardness VARCHAR(50),                   -- 硬度 (莫氏硬度)
    mineral_color VARCHAR(100),                     -- 颜色

    -- ========== 微生物特有属性 ==========
    microbe_strain VARCHAR(200),                    -- 菌株
    microbe_culture_condition TEXT,                 -- 培养条件
    microbe_fermentation_product TEXT,              -- 发酵产物

    -- ========== 动物特有属性 ==========
    animal_class VARCHAR(100),                      -- 动物类别 (哺乳类、爬行类、昆虫类等)
    animal_conservation_status VARCHAR(50),         -- 保护级别 (CITES, 国家保护等级)

    -- ========== 外部数据库链接 ==========
    tcmid_id VARCHAR(50),                           -- TCM-ID 数据库 ID
    tcmsp_id VARCHAR(50),                           -- TCMSP 数据库 ID
    herb_id VARCHAR(50),                            -- HERB 数据库 ID

    -- ========== 参考文献 ==========
    pharmacopoeia_ref VARCHAR(200),                 -- 药典收录 (如: 中国药典2020版)
    literature_ref TEXT,                            -- 文献参考

    -- ========== 图片与附件 ==========
    image_url TEXT,                                 -- 图片 URL

    -- ========== 统计信息 ==========
    num_of_compounds INT DEFAULT 0,                 -- 包含的化合物数量
    num_of_prescriptions INT DEFAULT 0,             -- 被处方引用次数

    -- ========== 时间戳 ==========
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 生物资源表索引
CREATE INDEX idx_bio_resources_id ON bio_resources(resource_id);
CREATE INDEX idx_bio_resources_type ON bio_resources(resource_type);
CREATE INDEX idx_bio_resources_chinese_name ON bio_resources(chinese_name);
CREATE INDEX idx_bio_resources_latin_name ON bio_resources(latin_name);
CREATE INDEX idx_bio_resources_pinyin ON bio_resources(pinyin_name);
CREATE INDEX idx_bio_resources_family ON bio_resources(taxonomy_family);
CREATE INDEX idx_bio_resources_genus ON bio_resources(taxonomy_genus);
CREATE INDEX idx_bio_resources_tcm_property ON bio_resources(tcm_property);
CREATE INDEX idx_bio_resources_tcm_meridian ON bio_resources(tcm_meridian);

-- 全文搜索索引
CREATE INDEX idx_bio_resources_chinese_gin ON bio_resources USING gin(to_tsvector('simple', COALESCE(chinese_name, '')));
CREATE INDEX idx_bio_resources_latin_gin ON bio_resources USING gin(to_tsvector('english', COALESCE(latin_name, '')));
CREATE INDEX idx_bio_resources_functions_gin ON bio_resources USING gin(to_tsvector('simple', COALESCE(functions, '')));

COMMENT ON TABLE bio_resources IS '生物资源表 - 存储植物、动物、微生物、矿物等天然产物来源';
COMMENT ON COLUMN bio_resources.resource_type IS '资源类型: Plant(植物), Animal(动物), Microorganism(微生物), Mineral(矿物), Fungus(真菌)';
COMMENT ON COLUMN bio_resources.tcm_property IS '中医药性: 寒、热、温、凉、平';
COMMENT ON COLUMN bio_resources.tcm_flavor IS '中医药味: 酸、苦、甘、辛、咸、淡、涩';


-- ============================================
-- 2. 生物资源-化合物关联表
-- 说明: 一个生物资源可以包含多个化合物
-- ============================================
CREATE TABLE bio_resource_compounds (
    id BIGSERIAL PRIMARY KEY,

    bio_resource_id BIGINT NOT NULL,                -- 关联生物资源
    compound_id BIGINT NOT NULL,                    -- 关联化合物

    -- ========== 含量信息 ==========
    content_value DECIMAL(20,6),                    -- 含量值
    content_unit VARCHAR(50),                       -- 含量单位 (mg/g, %, ppm)
    content_part VARCHAR(100),                      -- 含量测定部位

    -- ========== 来源信息 ==========
    isolation_method VARCHAR(200),                  -- 分离方法
    ref_id VARCHAR(50),                             -- 参考文献 ID
    ref_id_type VARCHAR(20),                        -- 参考文献类型 (PMID, DOI)

    -- ========== 时间戳 ==========
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 外键约束
    CONSTRAINT fk_brc_bio_resource FOREIGN KEY (bio_resource_id) REFERENCES bio_resources(id) ON DELETE CASCADE,
    CONSTRAINT fk_brc_compound FOREIGN KEY (compound_id) REFERENCES compounds(id) ON DELETE CASCADE,

    -- 唯一约束
    CONSTRAINT uk_bio_resource_compound UNIQUE (bio_resource_id, compound_id)
);

CREATE INDEX idx_brc_bio_resource ON bio_resource_compounds(bio_resource_id);
CREATE INDEX idx_brc_compound ON bio_resource_compounds(compound_id);

COMMENT ON TABLE bio_resource_compounds IS '生物资源-化合物关联表 - 记录生物资源包含的化合物';


-- ============================================
-- 3. 处方表 (Prescriptions / Formulas)
-- 说明: 中医方剂/处方信息
-- 关系: 处方 → 包含多个生物资源 (或直接包含化合物)
-- ============================================
CREATE TABLE prescriptions (
    id BIGSERIAL PRIMARY KEY,

    -- ========== 基本标识 ==========
    prescription_id VARCHAR(50) UNIQUE NOT NULL,    -- 处方 ID (如 RX0001, TCMF1122)

    -- ========== 名称信息 ==========
    chinese_name VARCHAR(500),                      -- 中文名 (如: 六味地黄丸)
    pinyin_name VARCHAR(200),                       -- 拼音名 (如: Liu Wei Di Huang Wan)
    english_name VARCHAR(500),                      -- 英文名 (如: Six-Ingredient Rehmannia Pill)
    alias TEXT,                                     -- 别名/异名

    -- ========== 来源与出处 ==========
    source_book VARCHAR(200),                       -- 出处/来源书籍 (如: 《小儿药证直诀》)
    source_dynasty VARCHAR(100),                    -- 朝代 (如: 宋代)
    source_author VARCHAR(100),                     -- 作者 (如: 钱乙)

    -- ========== 处方分类 ==========
    category VARCHAR(100),                          -- 方剂分类 (补益剂、解表剂、清热剂等)
    subcategory VARCHAR(100),                       -- 子分类 (补阴剂、补阳剂等)

    -- ========== 功效与主治 ==========
    functions TEXT,                                 -- 功效 (如: 滋阴补肾)
    indications TEXT,                               -- 主治/适应症
    indications_modern TEXT,                        -- 现代医学适应症
    syndrome VARCHAR(500),                          -- 证候 (如: 肾阴虚证)

    -- ========== 组成 (文本描述) ==========
    composition_text TEXT,                          -- 组成描述 (如: 熟地黄24g, 山茱萸12g...)

    -- ========== 用法用量 ==========
    dosage_form VARCHAR(100),                       -- 剂型 (丸、散、汤、膏、丹等)
    preparation_method TEXT,                        -- 制法
    usage_method TEXT,                              -- 用法 (口服、外用等)
    dosage TEXT,                                    -- 用量

    -- ========== 注意事项 ==========
    contraindications TEXT,                         -- 禁忌
    precautions TEXT,                               -- 注意事项
    adverse_reactions TEXT,                         -- 不良反应

    -- ========== 现代研究 ==========
    pharmacology TEXT,                              -- 药理作用
    clinical_application TEXT,                      -- 临床应用

    -- ========== 关联组织/疾病 ==========
    target_tissues TEXT,                            -- 靶向组织 (如: Lung, Kidney)
    related_diseases TEXT,                          -- 相关疾病

    -- ========== 外部数据库链接 ==========
    tcmid_id VARCHAR(50),                           -- TCM-ID 数据库 ID
    tcmsp_id VARCHAR(50),                           -- TCMSP 数据库 ID
    symmap_id VARCHAR(50),                          -- SymMap 数据库 ID

    -- ========== 参考文献 ==========
    pharmacopoeia_ref VARCHAR(200),                 -- 药典收录 (如: 中国药典2020版)
    literature_ref TEXT,                            -- 文献参考

    -- ========== 统计信息 ==========
    num_of_herbs INT DEFAULT 0,                     -- 包含的药材数量
    num_of_compounds INT DEFAULT 0,                 -- 包含的化合物数量 (间接)

    -- ========== 时间戳 ==========
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 处方表索引
CREATE INDEX idx_prescriptions_id ON prescriptions(prescription_id);
CREATE INDEX idx_prescriptions_chinese_name ON prescriptions(chinese_name);
CREATE INDEX idx_prescriptions_pinyin ON prescriptions(pinyin_name);
CREATE INDEX idx_prescriptions_category ON prescriptions(category);
CREATE INDEX idx_prescriptions_source_book ON prescriptions(source_book);
CREATE INDEX idx_prescriptions_dosage_form ON prescriptions(dosage_form);

-- 全文搜索索引
CREATE INDEX idx_prescriptions_chinese_gin ON prescriptions USING gin(to_tsvector('simple', COALESCE(chinese_name, '')));
CREATE INDEX idx_prescriptions_functions_gin ON prescriptions USING gin(to_tsvector('simple', COALESCE(functions, '')));
CREATE INDEX idx_prescriptions_indications_gin ON prescriptions USING gin(to_tsvector('simple', COALESCE(indications, '')));

COMMENT ON TABLE prescriptions IS '处方表 - 存储中医方剂/处方信息';
COMMENT ON COLUMN prescriptions.category IS '方剂分类: 补益剂、解表剂、清热剂、泻下剂、祛湿剂、理气剂、理血剂、治风剂等';
COMMENT ON COLUMN prescriptions.dosage_form IS '剂型: 丸、散、汤、膏、丹、酒、露、锭等';


-- ============================================
-- 4. 处方-生物资源关联表 (处方组成)
-- 说明: 一个处方包含多个生物资源 (药材)
-- ============================================
CREATE TABLE prescription_resources (
    id BIGSERIAL PRIMARY KEY,

    prescription_id BIGINT NOT NULL,                -- 关联处方
    bio_resource_id BIGINT NOT NULL,                -- 关联生物资源

    -- ========== 用量信息 ==========
    dosage_value DECIMAL(10,2),                     -- 用量值
    dosage_unit VARCHAR(20),                        -- 用量单位 (g, 两, 钱, 分)
    dosage_text VARCHAR(100),                       -- 用量描述 (如: 适量, 少许)

    -- ========== 角色信息 ==========
    role VARCHAR(50),                               -- 君臣佐使 (Monarch, Minister, Assistant, Guide)
    role_chinese VARCHAR(20),                       -- 君、臣、佐、使

    -- ========== 炮制信息 ==========
    processing_method VARCHAR(200),                 -- 炮制方法 (如: 酒炙, 蜜炙, 盐炙)
    processing_note TEXT,                           -- 炮制说明

    -- ========== 排序 ==========
    sort_order INT DEFAULT 0,                       -- 排序顺序

    -- ========== 时间戳 ==========
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 外键约束
    CONSTRAINT fk_pr_prescription FOREIGN KEY (prescription_id) REFERENCES prescriptions(id) ON DELETE CASCADE,
    CONSTRAINT fk_pr_bio_resource FOREIGN KEY (bio_resource_id) REFERENCES bio_resources(id) ON DELETE CASCADE,

    -- 唯一约束
    CONSTRAINT uk_prescription_resource UNIQUE (prescription_id, bio_resource_id)
);

CREATE INDEX idx_pr_prescription ON prescription_resources(prescription_id);
CREATE INDEX idx_pr_bio_resource ON prescription_resources(bio_resource_id);
CREATE INDEX idx_pr_role ON prescription_resources(role);

COMMENT ON TABLE prescription_resources IS '处方-生物资源关联表 - 记录处方的组成药材';
COMMENT ON COLUMN prescription_resources.role IS '君臣佐使: Monarch(君), Minister(臣), Assistant(佐), Guide(使)';


-- ============================================
-- 5. 处方-化合物关联表 (可选，用于直接关联)
-- 说明: 处方直接关联化合物 (跳过生物资源)
-- ============================================
CREATE TABLE prescription_compounds (
    id BIGSERIAL PRIMARY KEY,

    prescription_id BIGINT NOT NULL,                -- 关联处方
    compound_id BIGINT NOT NULL,                    -- 关联化合物

    -- ========== 来源信息 ==========
    source_resource_id BIGINT,                      -- 来源生物资源 (可选)

    -- ========== 时间戳 ==========
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 外键约束
    CONSTRAINT fk_pc_prescription FOREIGN KEY (prescription_id) REFERENCES prescriptions(id) ON DELETE CASCADE,
    CONSTRAINT fk_pc_compound FOREIGN KEY (compound_id) REFERENCES compounds(id) ON DELETE CASCADE,
    CONSTRAINT fk_pc_source_resource FOREIGN KEY (source_resource_id) REFERENCES bio_resources(id) ON DELETE SET NULL,

    -- 唯一约束
    CONSTRAINT uk_prescription_compound UNIQUE (prescription_id, compound_id)
);

CREATE INDEX idx_pc_prescription ON prescription_compounds(prescription_id);
CREATE INDEX idx_pc_compound ON prescription_compounds(compound_id);

COMMENT ON TABLE prescription_compounds IS '处方-化合物关联表 - 记录处方包含的化合物 (直接关联)';


-- ============================================
-- 6. 更新触发器
-- ============================================
CREATE TRIGGER update_bio_resources_updated_at BEFORE UPDATE ON bio_resources
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_prescriptions_updated_at BEFORE UPDATE ON prescriptions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


-- ============================================
-- 7. 视图：生物资源详情视图
-- ============================================
CREATE OR REPLACE VIEW v_bio_resource_detail AS
SELECT
    br.*,
    COUNT(DISTINCT brc.compound_id) as compound_count,
    COUNT(DISTINCT pr.prescription_id) as prescription_count
FROM bio_resources br
LEFT JOIN bio_resource_compounds brc ON br.id = brc.bio_resource_id
LEFT JOIN prescription_resources pr ON br.id = pr.bio_resource_id
GROUP BY br.id;

COMMENT ON VIEW v_bio_resource_detail IS '生物资源详情视图 - 包含统计信息';


-- ============================================
-- 8. 视图：处方详情视图
-- ============================================
CREATE OR REPLACE VIEW v_prescription_detail AS
SELECT
    p.*,
    COUNT(DISTINCT pr.bio_resource_id) as herb_count,
    COUNT(DISTINCT pc.compound_id) as direct_compound_count
FROM prescriptions p
LEFT JOIN prescription_resources pr ON p.id = pr.prescription_id
LEFT JOIN prescription_compounds pc ON p.id = pc.prescription_id
GROUP BY p.id;

COMMENT ON VIEW v_prescription_detail IS '处方详情视图 - 包含统计信息';


-- ============================================
-- 完成提示
-- ============================================
-- 新增表创建完成！
--
-- 新增的表:
-- 1. bio_resources - 生物资源表 (植物、动物、微生物、矿物)
-- 2. bio_resource_compounds - 生物资源-化合物关联表
-- 3. prescriptions - 处方表
-- 4. prescription_resources - 处方-生物资源关联表
-- 5. prescription_compounds - 处方-化合物关联表
--
-- 新增的视图:
-- 1. v_bio_resource_detail - 生物资源详情视图
-- 2. v_prescription_detail - 处方详情视图
-- ============================================
