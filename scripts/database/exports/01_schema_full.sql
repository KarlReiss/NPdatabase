--
-- PostgreSQL database dump
--

\restrict JBajSlJHh2giQYgBKmXf3ptqgY0wSYxeJ58On2axIUdLPueag6j7y980nqudnkn

-- Dumped from database version 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: update_updated_at_column(); Type: FUNCTION; Schema: public; Owner: yfguo
--

CREATE FUNCTION public.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_updated_at_column() OWNER TO yfguo;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: bio_resource_disease_associations; Type: TABLE; Schema: public; Owner: yfguo
--

CREATE TABLE public.bio_resource_disease_associations (
    id bigint NOT NULL,
    bio_resource_id bigint NOT NULL,
    disease_id bigint NOT NULL,
    evidence_therapeutic_target text,
    evidence_transcriptome boolean DEFAULT false,
    evidence_clinical_trial_plant text,
    evidence_clinical_trial_ingredient text,
    confidence_score numeric(3,2),
    source character varying(100) DEFAULT 'CMAUP'::character varying,
    source_version character varying(50),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.bio_resource_disease_associations OWNER TO yfguo;

--
-- Name: TABLE bio_resource_disease_associations; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON TABLE public.bio_resource_disease_associations IS '生物资源-疾病关联表 - 记录生物资源与疾病的治疗关联关系及证据来源';


--
-- Name: COLUMN bio_resource_disease_associations.id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_disease_associations.id IS '主键ID';


--
-- Name: COLUMN bio_resource_disease_associations.bio_resource_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_disease_associations.bio_resource_id IS '关联的生物资源ID';


--
-- Name: COLUMN bio_resource_disease_associations.disease_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_disease_associations.disease_id IS '关联的疾病ID';


--
-- Name: COLUMN bio_resource_disease_associations.evidence_therapeutic_target; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_disease_associations.evidence_therapeutic_target IS '治疗靶点证据 - 相关治疗靶点列表（分号分隔）';


--
-- Name: COLUMN bio_resource_disease_associations.evidence_transcriptome; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_disease_associations.evidence_transcriptome IS '转录组证据 - 是否有转录组学证据支持';


--
-- Name: COLUMN bio_resource_disease_associations.evidence_clinical_trial_plant; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_disease_associations.evidence_clinical_trial_plant IS '植物临床试验证据 - 相关临床试验ID';


--
-- Name: COLUMN bio_resource_disease_associations.evidence_clinical_trial_ingredient; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_disease_associations.evidence_clinical_trial_ingredient IS '成分临床试验证据 - 成分相关临床试验ID';


--
-- Name: COLUMN bio_resource_disease_associations.confidence_score; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_disease_associations.confidence_score IS '置信度评分（0-1之间，越高表示关联越可靠）';


--
-- Name: COLUMN bio_resource_disease_associations.source; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_disease_associations.source IS '数据来源';


--
-- Name: COLUMN bio_resource_disease_associations.source_version; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_disease_associations.source_version IS '数据来源版本';


--
-- Name: COLUMN bio_resource_disease_associations.created_at; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_disease_associations.created_at IS '记录创建时间';


--
-- Name: bio_resource_disease_associations_id_seq; Type: SEQUENCE; Schema: public; Owner: yfguo
--

CREATE SEQUENCE public.bio_resource_disease_associations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bio_resource_disease_associations_id_seq OWNER TO yfguo;

--
-- Name: bio_resource_disease_associations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yfguo
--

ALTER SEQUENCE public.bio_resource_disease_associations_id_seq OWNED BY public.bio_resource_disease_associations.id;


--
-- Name: bio_resource_natural_products; Type: TABLE; Schema: public; Owner: yfguo
--

CREATE TABLE public.bio_resource_natural_products (
    id bigint NOT NULL,
    org_id text,
    np_id text,
    src_org_record_id text,
    src_org_pair_id text,
    src_org_pair text,
    new_cp_found text,
    org_isolation_part text,
    org_collect_location text,
    org_collect_time text,
    ref_type text,
    ref_id text,
    ref_id_type text,
    ref_url text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.bio_resource_natural_products OWNER TO yfguo;

--
-- Name: TABLE bio_resource_natural_products; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON TABLE public.bio_resource_natural_products IS '生物资源-天然产物关联表 - 记录生物资源中包含的天然产物及其含量信息';


--
-- Name: COLUMN bio_resource_natural_products.id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_natural_products.id IS '主键ID';


--
-- Name: COLUMN bio_resource_natural_products.org_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_natural_products.org_id IS '生物来源编号';


--
-- Name: COLUMN bio_resource_natural_products.np_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_natural_products.np_id IS '天然产物编号';


--
-- Name: COLUMN bio_resource_natural_products.src_org_record_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_natural_products.src_org_record_id IS '来源生物记录ID';


--
-- Name: COLUMN bio_resource_natural_products.src_org_pair_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_natural_products.src_org_pair_id IS '来源生物-产物配对ID';


--
-- Name: COLUMN bio_resource_natural_products.src_org_pair; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_natural_products.src_org_pair IS '来源生物-产物配对信息';


--
-- Name: COLUMN bio_resource_natural_products.new_cp_found; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_natural_products.new_cp_found IS '是否发现新化合物';


--
-- Name: COLUMN bio_resource_natural_products.org_isolation_part; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_natural_products.org_isolation_part IS '分离部位 - 从生物体的哪个部位分离';


--
-- Name: COLUMN bio_resource_natural_products.org_collect_location; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_natural_products.org_collect_location IS '采集地点';


--
-- Name: COLUMN bio_resource_natural_products.org_collect_time; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_natural_products.org_collect_time IS '采集时间';


--
-- Name: COLUMN bio_resource_natural_products.ref_type; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_natural_products.ref_type IS '参考文献类型';


--
-- Name: COLUMN bio_resource_natural_products.ref_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_natural_products.ref_id IS '参考文献ID';


--
-- Name: COLUMN bio_resource_natural_products.ref_id_type; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_natural_products.ref_id_type IS '参考文献ID类型（PMID、DOI）';


--
-- Name: COLUMN bio_resource_natural_products.ref_url; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_natural_products.ref_url IS '参考文献URL链接';


--
-- Name: COLUMN bio_resource_natural_products.created_at; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_natural_products.created_at IS '记录创建时间';


--
-- Name: COLUMN bio_resource_natural_products.updated_at; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resource_natural_products.updated_at IS '记录更新时间';


--
-- Name: bio_resource_natural_products_new_id_seq; Type: SEQUENCE; Schema: public; Owner: yfguo
--

CREATE SEQUENCE public.bio_resource_natural_products_new_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bio_resource_natural_products_new_id_seq OWNER TO yfguo;

--
-- Name: bio_resource_natural_products_new_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yfguo
--

ALTER SEQUENCE public.bio_resource_natural_products_new_id_seq OWNED BY public.bio_resource_natural_products.id;


--
-- Name: bio_resources; Type: TABLE; Schema: public; Owner: yfguo
--

CREATE TABLE public.bio_resources (
    id bigint NOT NULL,
    resource_id character varying(50) NOT NULL,
    resource_type character varying(50) NOT NULL,
    chinese_name character varying(500),
    latin_name character varying(500),
    taxonomy_kingdom character varying(100),
    taxonomy_family character varying(200),
    taxonomy_genus character varying(200),
    taxonomy_species character varying(200),
    taxonomy_id character varying(50),
    tcmid_id character varying(500),
    num_of_natural_products integer DEFAULT 0,
    num_of_prescriptions integer DEFAULT 0,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    species_tax_id character varying(50),
    genus_tax_id character varying(50),
    family_tax_id character varying(50),
    cmaup_id character varying(50),
    translation_source character varying(200),
    family_chinese character varying(200),
    genus_chinese character varying(200)
);


ALTER TABLE public.bio_resources OWNER TO yfguo;

--
-- Name: TABLE bio_resources; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON TABLE public.bio_resources IS '生物资源表 - 存储植物、动物、微生物、矿物等天然产物来源，包含分类学信息和中医药用属性';


--
-- Name: COLUMN bio_resources.id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resources.id IS '主键ID';


--
-- Name: COLUMN bio_resources.resource_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resources.resource_id IS '资源唯一编号';


--
-- Name: COLUMN bio_resources.resource_type; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resources.resource_type IS '资源类型（Plant植物、Animal动物、Microorganism微生物、Mineral矿物、Fungus真菌）';


--
-- Name: COLUMN bio_resources.chinese_name; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resources.chinese_name IS '中文名称';


--
-- Name: COLUMN bio_resources.latin_name; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resources.latin_name IS '拉丁学名 - 国际通用的科学命名';


--
-- Name: COLUMN bio_resources.taxonomy_kingdom; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resources.taxonomy_kingdom IS '分类学-界';


--
-- Name: COLUMN bio_resources.taxonomy_family; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resources.taxonomy_family IS '分类学-科';


--
-- Name: COLUMN bio_resources.taxonomy_genus; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resources.taxonomy_genus IS '分类学-属';


--
-- Name: COLUMN bio_resources.taxonomy_species; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resources.taxonomy_species IS '分类学-种';


--
-- Name: COLUMN bio_resources.taxonomy_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resources.taxonomy_id IS 'NCBI分类学ID';


--
-- Name: COLUMN bio_resources.tcmid_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resources.tcmid_id IS 'TCMID中药分子数据库编号';


--
-- Name: COLUMN bio_resources.num_of_natural_products; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resources.num_of_natural_products IS '包含的天然产物数量';


--
-- Name: COLUMN bio_resources.num_of_prescriptions; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resources.num_of_prescriptions IS '相关处方数量';


--
-- Name: COLUMN bio_resources.created_at; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resources.created_at IS '记录创建时间';


--
-- Name: COLUMN bio_resources.updated_at; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resources.updated_at IS '记录更新时间';


--
-- Name: COLUMN bio_resources.species_tax_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resources.species_tax_id IS '种级分类学ID';


--
-- Name: COLUMN bio_resources.genus_tax_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resources.genus_tax_id IS '属级分类学ID';


--
-- Name: COLUMN bio_resources.family_tax_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resources.family_tax_id IS '科极分类学ID';


--
-- Name: COLUMN bio_resources.cmaup_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bio_resources.cmaup_id IS 'CMAUP中药材数据库编号';


--
-- Name: bio_resources_id_seq; Type: SEQUENCE; Schema: public; Owner: yfguo
--

CREATE SEQUENCE public.bio_resources_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bio_resources_id_seq OWNER TO yfguo;

--
-- Name: bio_resources_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yfguo
--

ALTER SEQUENCE public.bio_resources_id_seq OWNED BY public.bio_resources.id;


--
-- Name: bioactivity; Type: TABLE; Schema: public; Owner: yfguo
--

CREATE TABLE public.bioactivity (
    id bigint NOT NULL,
    natural_product_id bigint NOT NULL,
    target_id bigint NOT NULL,
    activity_type character varying(100),
    activity_type_grouped character varying(100),
    activity_relation character varying(10),
    activity_value numeric(30,6),
    activity_units character varying(100),
    activity_value_std numeric(30,6),
    activity_units_std character varying(20) DEFAULT 'nM'::character varying,
    assay_organism character varying(200),
    assay_tax_id character varying(100),
    assay_strain character varying(100),
    assay_tissue character varying(200),
    assay_cell_type character varying(100),
    ref_id character varying(300),
    ref_id_type character varying(20),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.bioactivity OWNER TO yfguo;

--
-- Name: TABLE bioactivity; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON TABLE public.bioactivity IS '生物活性表 - 存储天然产物对靶点的生物活性实验数据（IC50、EC50、Ki等）';


--
-- Name: COLUMN bioactivity.id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bioactivity.id IS '主键ID';


--
-- Name: COLUMN bioactivity.natural_product_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bioactivity.natural_product_id IS '关联的天然产物ID';


--
-- Name: COLUMN bioactivity.target_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bioactivity.target_id IS '关联的靶点ID';


--
-- Name: COLUMN bioactivity.activity_type; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bioactivity.activity_type IS '活性类型（IC50、EC50、Ki、Kd、GI50等）';


--
-- Name: COLUMN bioactivity.activity_type_grouped; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bioactivity.activity_type_grouped IS '活性类型分组（IC50/EC50/Ki/Kd等归为一组）';


--
-- Name: COLUMN bioactivity.activity_relation; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bioactivity.activity_relation IS '活性关系符号（= 等于、> 大于、< 小于、~ 约等于）';


--
-- Name: COLUMN bioactivity.activity_value; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bioactivity.activity_value IS '原始活性值';


--
-- Name: COLUMN bioactivity.activity_units; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bioactivity.activity_units IS '原始活性单位（nM、μM、mM、M等）';


--
-- Name: COLUMN bioactivity.activity_value_std; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bioactivity.activity_value_std IS '标准化活性值（统一转换为nM）';


--
-- Name: COLUMN bioactivity.activity_units_std; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bioactivity.activity_units_std IS '标准化活性单位（固定为nM）';


--
-- Name: COLUMN bioactivity.assay_organism; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bioactivity.assay_organism IS '实验物种 - 活性测定所用的生物体';


--
-- Name: COLUMN bioactivity.assay_tax_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bioactivity.assay_tax_id IS '实验物种分类学ID';


--
-- Name: COLUMN bioactivity.assay_strain; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bioactivity.assay_strain IS '实验菌株/品系';


--
-- Name: COLUMN bioactivity.assay_tissue; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bioactivity.assay_tissue IS '实验组织';


--
-- Name: COLUMN bioactivity.assay_cell_type; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bioactivity.assay_cell_type IS '实验细胞类型';


--
-- Name: COLUMN bioactivity.ref_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bioactivity.ref_id IS '参考文献ID（PMID、DOI等）';


--
-- Name: COLUMN bioactivity.ref_id_type; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bioactivity.ref_id_type IS '参考文献类型（PMID、DOI、Patent）';


--
-- Name: COLUMN bioactivity.created_at; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.bioactivity.created_at IS '记录创建时间';


--
-- Name: bioactivity_id_seq; Type: SEQUENCE; Schema: public; Owner: yfguo
--

CREATE SEQUENCE public.bioactivity_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bioactivity_id_seq OWNER TO yfguo;

--
-- Name: bioactivity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yfguo
--

ALTER SEQUENCE public.bioactivity_id_seq OWNED BY public.bioactivity.id;


--
-- Name: natural_products; Type: TABLE; Schema: public; Owner: yfguo
--

CREATE TABLE public.natural_products (
    id bigint NOT NULL,
    np_id character varying(50) NOT NULL,
    inchikey character varying(100),
    pref_name text,
    iupac_name text,
    name_initial character varying(10),
    inchi text,
    smiles text,
    chembl_id character varying(50),
    pubchem_id character varying(50),
    molecular_weight numeric(10,2),
    xlogp numeric(10,2),
    psa numeric(10,2),
    formula character varying(200),
    h_bond_donors integer,
    h_bond_acceptors integer,
    rotatable_bonds integer,
    num_of_organism integer DEFAULT 0,
    num_of_target integer DEFAULT 0,
    num_of_activity integer DEFAULT 0,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    if_quantity boolean DEFAULT false,
    log_s numeric(10,2),
    log_d numeric(10,2),
    log_p numeric(10,2),
    tpsa numeric(10,2),
    ring_count integer,
    CONSTRAINT chk_mw CHECK (((molecular_weight IS NULL) OR (molecular_weight > (0)::numeric)))
);


ALTER TABLE public.natural_products OWNER TO yfguo;

--
-- Name: TABLE natural_products; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON TABLE public.natural_products IS '天然产物表 - 存储天然产物的基本信息、化学结构和理化性质';


--
-- Name: COLUMN natural_products.id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.id IS '主键ID';


--
-- Name: COLUMN natural_products.np_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.np_id IS '天然产物编号（如NPC491451）';


--
-- Name: COLUMN natural_products.inchikey; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.inchikey IS 'InChIKey - 国际化合物标识符的哈希值';


--
-- Name: COLUMN natural_products.pref_name; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.pref_name IS '首选名称 - 化合物的常用名称';


--
-- Name: COLUMN natural_products.iupac_name; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.iupac_name IS 'IUPAC系统命名 - 国际纯粹与应用化学联合会标准命名';


--
-- Name: COLUMN natural_products.name_initial; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.name_initial IS '名称首字母 - 用于按字母排序';


--
-- Name: COLUMN natural_products.inchi; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.inchi IS 'InChI - 国际化合物标识符';


--
-- Name: COLUMN natural_products.smiles; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.smiles IS 'SMILES - 简化分子线性输入规范';


--
-- Name: COLUMN natural_products.chembl_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.chembl_id IS 'ChEMBL数据库编号';


--
-- Name: COLUMN natural_products.pubchem_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.pubchem_id IS 'PubChem化合物编号（CID）';


--
-- Name: COLUMN natural_products.molecular_weight; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.molecular_weight IS '分子量（单位：g/mol）';


--
-- Name: COLUMN natural_products.xlogp; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.xlogp IS '脂水分配系数XLogP - 衡量化合物的亲脂性';


--
-- Name: COLUMN natural_products.psa; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.psa IS '极性表面积PSA（单位：Å²）';


--
-- Name: COLUMN natural_products.formula; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.formula IS '分子式 - 化合物的元素组成';


--
-- Name: COLUMN natural_products.h_bond_donors; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.h_bond_donors IS '氢键供体数量';


--
-- Name: COLUMN natural_products.h_bond_acceptors; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.h_bond_acceptors IS '氢键受体数量';


--
-- Name: COLUMN natural_products.rotatable_bonds; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.rotatable_bonds IS '可旋转键数量';


--
-- Name: COLUMN natural_products.num_of_organism; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.num_of_organism IS '关联生物来源数量';


--
-- Name: COLUMN natural_products.num_of_target; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.num_of_target IS '关联靶点数量';


--
-- Name: COLUMN natural_products.num_of_activity; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.num_of_activity IS '生物活性记录数量';


--
-- Name: COLUMN natural_products.created_at; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.created_at IS '记录创建时间';


--
-- Name: COLUMN natural_products.updated_at; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.updated_at IS '记录更新时间';


--
-- Name: COLUMN natural_products.if_quantity; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.if_quantity IS '是否有定量数据';


--
-- Name: COLUMN natural_products.log_s; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.log_s IS 'LogS - 水溶解度对数值';


--
-- Name: COLUMN natural_products.log_d; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.log_d IS 'LogD - 分布系数对数值';


--
-- Name: COLUMN natural_products.log_p; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.log_p IS 'LogP - 辛醇-水分配系数对数值';


--
-- Name: COLUMN natural_products.tpsa; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.tpsa IS '拓扑极性表面积（TPSA）';


--
-- Name: COLUMN natural_products.ring_count; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.natural_products.ring_count IS '环数目 - 分子中环的数量';


--
-- Name: compounds_id_seq; Type: SEQUENCE; Schema: public; Owner: yfguo
--

CREATE SEQUENCE public.compounds_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.compounds_id_seq OWNER TO yfguo;

--
-- Name: compounds_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yfguo
--

ALTER SEQUENCE public.compounds_id_seq OWNED BY public.natural_products.id;


--
-- Name: diseases; Type: TABLE; Schema: public; Owner: yfguo
--

CREATE TABLE public.diseases (
    id bigint NOT NULL,
    icd11_code character varying(50) NOT NULL,
    disease_name character varying(500) NOT NULL,
    disease_name_zh character varying(500),
    disease_category character varying(200),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    disease_name_cmaup character varying(500)
);


ALTER TABLE public.diseases OWNER TO yfguo;

--
-- Name: TABLE diseases; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON TABLE public.diseases IS '疾病表 - 存储疾病信息，基于ICD-11国际疾病分类标准';


--
-- Name: COLUMN diseases.id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.diseases.id IS '主键ID';


--
-- Name: COLUMN diseases.icd11_code; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.diseases.icd11_code IS 'ICD-11国际疾病分类编码';


--
-- Name: COLUMN diseases.disease_name; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.diseases.disease_name IS '疾病英文名称';


--
-- Name: COLUMN diseases.disease_name_zh; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.diseases.disease_name_zh IS '疾病中文名称';


--
-- Name: COLUMN diseases.disease_category; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.diseases.disease_category IS '疾病分类';


--
-- Name: COLUMN diseases.created_at; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.diseases.created_at IS '记录创建时间';


--
-- Name: COLUMN diseases.updated_at; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.diseases.updated_at IS '记录更新时间';


--
-- Name: COLUMN diseases.disease_name_cmaup; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.diseases.disease_name_cmaup IS '参考数据库中的疾病名称';


--
-- Name: diseases_id_seq; Type: SEQUENCE; Schema: public; Owner: yfguo
--

CREATE SEQUENCE public.diseases_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.diseases_id_seq OWNER TO yfguo;

--
-- Name: diseases_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yfguo
--

ALTER SEQUENCE public.diseases_id_seq OWNED BY public.diseases.id;


--
-- Name: prescription_resources; Type: TABLE; Schema: public; Owner: yfguo
--

CREATE TABLE public.prescription_resources (
    id bigint NOT NULL,
    prescription_id bigint NOT NULL,
    bio_resource_id bigint NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    tcmid_component_id character varying(500)
);


ALTER TABLE public.prescription_resources OWNER TO yfguo;

--
-- Name: TABLE prescription_resources; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON TABLE public.prescription_resources IS '处方-生物资源关联表 - 记录处方的组成药材、用量及君臣佐使配伍关系';


--
-- Name: COLUMN prescription_resources.id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.prescription_resources.id IS '主键ID';


--
-- Name: COLUMN prescription_resources.prescription_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.prescription_resources.prescription_id IS '关联的处方ID';


--
-- Name: COLUMN prescription_resources.bio_resource_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.prescription_resources.bio_resource_id IS '关联的生物资源ID（药材）';


--
-- Name: COLUMN prescription_resources.created_at; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.prescription_resources.created_at IS '记录创建时间';


--
-- Name: COLUMN prescription_resources.tcmid_component_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.prescription_resources.tcmid_component_id IS '参考数据库药材组分ID（如TCMH1398）';


--
-- Name: prescription_resources_id_seq; Type: SEQUENCE; Schema: public; Owner: yfguo
--

CREATE SEQUENCE public.prescription_resources_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.prescription_resources_id_seq OWNER TO yfguo;

--
-- Name: prescription_resources_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yfguo
--

ALTER SEQUENCE public.prescription_resources_id_seq OWNED BY public.prescription_resources.id;


--
-- Name: prescriptions; Type: TABLE; Schema: public; Owner: yfguo
--

CREATE TABLE public.prescriptions (
    id bigint NOT NULL,
    prescription_id character varying(50) NOT NULL,
    chinese_name character varying(500),
    pinyin_name character varying(200),
    english_name character varying(500),
    functions text,
    indications text,
    tcmid_id character varying(50),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    disease_icd11_category text,
    reference text
);


ALTER TABLE public.prescriptions OWNER TO yfguo;

--
-- Name: TABLE prescriptions; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON TABLE public.prescriptions IS '处方表 - 存储中医方剂/处方信息，包括方剂组成、功效主治、用法用量等';


--
-- Name: COLUMN prescriptions.id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.prescriptions.id IS '主键ID';


--
-- Name: COLUMN prescriptions.prescription_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.prescriptions.prescription_id IS '处方编号';


--
-- Name: COLUMN prescriptions.chinese_name; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.prescriptions.chinese_name IS '处方中文名称';


--
-- Name: COLUMN prescriptions.pinyin_name; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.prescriptions.pinyin_name IS '处方拼音名称';


--
-- Name: COLUMN prescriptions.english_name; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.prescriptions.english_name IS '处方英文名称';


--
-- Name: COLUMN prescriptions.functions; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.prescriptions.functions IS '功能功效 - 方剂的功效描述';


--
-- Name: COLUMN prescriptions.indications; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.prescriptions.indications IS '主治 - 适应症和主治疾病';


--
-- Name: COLUMN prescriptions.tcmid_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.prescriptions.tcmid_id IS '参考数据库编号';


--
-- Name: COLUMN prescriptions.created_at; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.prescriptions.created_at IS '记录创建时间';


--
-- Name: COLUMN prescriptions.updated_at; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.prescriptions.updated_at IS '记录更新时间';


--
-- Name: COLUMN prescriptions.disease_icd11_category; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.prescriptions.disease_icd11_category IS 'ICD-11疾病分类编码（多个用分号分隔）';


--
-- Name: COLUMN prescriptions.reference; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.prescriptions.reference IS '参考文献';


--
-- Name: prescriptions_id_seq; Type: SEQUENCE; Schema: public; Owner: yfguo
--

CREATE SEQUENCE public.prescriptions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.prescriptions_id_seq OWNER TO yfguo;

--
-- Name: prescriptions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yfguo
--

ALTER SEQUENCE public.prescriptions_id_seq OWNED BY public.prescriptions.id;


--
-- Name: sys_dict; Type: TABLE; Schema: public; Owner: yfguo
--

CREATE TABLE public.sys_dict (
    dict_code bigint NOT NULL,
    dict_sort integer NOT NULL,
    dict_label character varying(100) NOT NULL,
    dict_value character varying(100) NOT NULL,
    dict_type character varying(100) NOT NULL,
    css_class character varying(100) DEFAULT ''::character varying NOT NULL,
    list_class character varying(100) DEFAULT ''::character varying NOT NULL,
    is_default character(1) DEFAULT 'N'::bpchar NOT NULL,
    status character(1) DEFAULT '0'::bpchar NOT NULL,
    create_by character varying(64) NOT NULL,
    create_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    update_by character varying(64) NOT NULL,
    update_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    remark character varying(500) DEFAULT ''::character varying NOT NULL
);


ALTER TABLE public.sys_dict OWNER TO yfguo;

--
-- Name: TABLE sys_dict; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON TABLE public.sys_dict IS '系统字典表 - 存储系统各类下拉选项的字典数据';


--
-- Name: COLUMN sys_dict.dict_code; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_dict.dict_code IS '字典编码 - 主键';


--
-- Name: COLUMN sys_dict.dict_sort; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_dict.dict_sort IS '字典排序序号';


--
-- Name: COLUMN sys_dict.dict_label; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_dict.dict_label IS '字典标签 - 显示给用户看的文字';


--
-- Name: COLUMN sys_dict.dict_value; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_dict.dict_value IS '字典键值 - 实际存储的值';


--
-- Name: COLUMN sys_dict.dict_type; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_dict.dict_type IS '字典类型 - 用于区分不同类型的字典';


--
-- Name: COLUMN sys_dict.css_class; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_dict.css_class IS 'CSS样式类名 - 前端显示样式';


--
-- Name: COLUMN sys_dict.list_class; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_dict.list_class IS '列表样式类名 - 表格中的显示样式';


--
-- Name: COLUMN sys_dict.is_default; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_dict.is_default IS '是否默认值（Y是、N否）';


--
-- Name: COLUMN sys_dict.status; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_dict.status IS '状态（0正常、1停用）';


--
-- Name: COLUMN sys_dict.create_by; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_dict.create_by IS '创建者';


--
-- Name: COLUMN sys_dict.create_time; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_dict.create_time IS '创建时间';


--
-- Name: COLUMN sys_dict.update_by; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_dict.update_by IS '更新者';


--
-- Name: COLUMN sys_dict.update_time; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_dict.update_time IS '更新时间';


--
-- Name: COLUMN sys_dict.remark; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_dict.remark IS '备注说明';


--
-- Name: sys_menu; Type: TABLE; Schema: public; Owner: yfguo
--

CREATE TABLE public.sys_menu (
    menu_id bigint NOT NULL,
    menu_name character varying(50) NOT NULL,
    parent_id bigint DEFAULT 0 NOT NULL,
    order_num integer DEFAULT 0 NOT NULL,
    path character varying(200) DEFAULT ''::character varying NOT NULL,
    component character varying(255),
    query_param character varying(255),
    is_frame integer DEFAULT 1 NOT NULL,
    is_cache integer DEFAULT 0 NOT NULL,
    menu_type character(1) NOT NULL,
    visible character(1) DEFAULT '0'::bpchar NOT NULL,
    status character(1) DEFAULT '0'::bpchar NOT NULL,
    perms character varying(100),
    icon character varying(100) DEFAULT ''::character varying,
    create_by character varying(64) NOT NULL,
    create_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    update_by character varying(64) NOT NULL,
    update_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    remark character varying(500) DEFAULT ''::character varying
);


ALTER TABLE public.sys_menu OWNER TO yfguo;

--
-- Name: TABLE sys_menu; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON TABLE public.sys_menu IS '系统菜单表 - 存储前端菜单导航和按钮权限配置';


--
-- Name: COLUMN sys_menu.menu_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_menu.menu_id IS '菜单ID - 主键';


--
-- Name: COLUMN sys_menu.menu_name; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_menu.menu_name IS '菜单名称';


--
-- Name: COLUMN sys_menu.parent_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_menu.parent_id IS '父菜单ID（0表示顶级菜单）';


--
-- Name: COLUMN sys_menu.order_num; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_menu.order_num IS '显示顺序';


--
-- Name: COLUMN sys_menu.path; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_menu.path IS '路由地址 - 前端路由路径';


--
-- Name: COLUMN sys_menu.component; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_menu.component IS '组件路径 - Vue组件路径';


--
-- Name: COLUMN sys_menu.query_param; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_menu.query_param IS '路由参数';


--
-- Name: COLUMN sys_menu.is_frame; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_menu.is_frame IS '是否为外链（0是、1否）';


--
-- Name: COLUMN sys_menu.is_cache; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_menu.is_cache IS '是否缓存（0缓存、1不缓存）';


--
-- Name: COLUMN sys_menu.menu_type; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_menu.menu_type IS '菜单类型（M目录、C菜单、F按钮）';


--
-- Name: COLUMN sys_menu.visible; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_menu.visible IS '显示状态（0显示、1隐藏）';


--
-- Name: COLUMN sys_menu.status; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_menu.status IS '菜单状态（0正常、1停用）';


--
-- Name: COLUMN sys_menu.perms; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_menu.perms IS '权限标识 - 用于权限控制';


--
-- Name: COLUMN sys_menu.icon; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_menu.icon IS '菜单图标';


--
-- Name: COLUMN sys_menu.create_by; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_menu.create_by IS '创建者';


--
-- Name: COLUMN sys_menu.create_time; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_menu.create_time IS '创建时间';


--
-- Name: COLUMN sys_menu.update_by; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_menu.update_by IS '更新者';


--
-- Name: COLUMN sys_menu.update_time; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_menu.update_time IS '更新时间';


--
-- Name: COLUMN sys_menu.remark; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.sys_menu.remark IS '备注说明';


--
-- Name: targets; Type: TABLE; Schema: public; Owner: yfguo
--

CREATE TABLE public.targets (
    id bigint NOT NULL,
    target_id character varying(50) NOT NULL,
    target_type character varying(200),
    target_name character varying(500),
    target_organism character varying(200),
    target_organism_tax_id character varying(100),
    uniprot_id character varying(300),
    num_of_compounds integer DEFAULT 0,
    num_of_activities integer DEFAULT 0,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    num_of_natural_products integer DEFAULT 0,
    gene_name character varying(100),
    synonyms text,
    function text,
    pdb_structure character varying(500),
    bioclass character varying(200),
    ec_number character varying(50),
    sequence text,
    ttd_id character varying(50)
);


ALTER TABLE public.targets OWNER TO yfguo;

--
-- Name: TABLE targets; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON TABLE public.targets IS '靶点表 - 存储生物靶点信息（蛋白质、细胞系、基因、酶等）';


--
-- Name: COLUMN targets.id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.targets.id IS '主键ID';


--
-- Name: COLUMN targets.target_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.targets.target_id IS '靶点编号（如NPT918）';


--
-- Name: COLUMN targets.target_type; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.targets.target_type IS '靶点类型（Protein蛋白质、Cell line细胞系、Gene基因、Enzyme酶）';


--
-- Name: COLUMN targets.target_name; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.targets.target_name IS '靶点名称';


--
-- Name: COLUMN targets.target_organism; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.targets.target_organism IS '靶点来源物种';


--
-- Name: COLUMN targets.target_organism_tax_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.targets.target_organism_tax_id IS '靶点来源物种的分类学ID';


--
-- Name: COLUMN targets.uniprot_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.targets.uniprot_id IS 'UniProt蛋白质数据库编号';


--
-- Name: COLUMN targets.num_of_compounds; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.targets.num_of_compounds IS '关联化合物数量（旧字段，保留兼容）';


--
-- Name: COLUMN targets.num_of_activities; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.targets.num_of_activities IS '生物活性记录数量';


--
-- Name: COLUMN targets.created_at; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.targets.created_at IS '记录创建时间';


--
-- Name: COLUMN targets.updated_at; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.targets.updated_at IS '记录更新时间';


--
-- Name: COLUMN targets.num_of_natural_products; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.targets.num_of_natural_products IS '关联天然产物数量';


--
-- Name: COLUMN targets.gene_name; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.targets.gene_name IS '基因名称 - 编码该蛋白的基因符号';


--
-- Name: COLUMN targets.synonyms; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.targets.synonyms IS '同义词 - 靶点的其他名称（分号分隔）';


--
-- Name: COLUMN targets.function; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.targets.function IS '功能描述 - 靶点的生物学功能';


--
-- Name: COLUMN targets.pdb_structure; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.targets.pdb_structure IS 'PDB结构编号 - 蛋白质三维结构数据';


--
-- Name: COLUMN targets.bioclass; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.targets.bioclass IS '生物分类 - 靶点的生物学类别';


--
-- Name: COLUMN targets.ec_number; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.targets.ec_number IS 'EC编号 - 酶的分类编号';


--
-- Name: COLUMN targets.sequence; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.targets.sequence IS '蛋白质氨基酸序列';


--
-- Name: COLUMN targets.ttd_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.targets.ttd_id IS 'TTD治疗靶点数据库编号';


--
-- Name: targets_id_seq; Type: SEQUENCE; Schema: public; Owner: yfguo
--

CREATE SEQUENCE public.targets_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.targets_id_seq OWNER TO yfguo;

--
-- Name: targets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yfguo
--

ALTER SEQUENCE public.targets_id_seq OWNED BY public.targets.id;


--
-- Name: v_target_detail; Type: VIEW; Schema: public; Owner: yfguo
--

CREATE VIEW public.v_target_detail AS
SELECT
    NULL::bigint AS id,
    NULL::character varying(50) AS target_id,
    NULL::character varying(200) AS target_type,
    NULL::character varying(500) AS target_name,
    NULL::character varying(200) AS target_organism,
    NULL::character varying(100) AS target_organism_tax_id,
    NULL::character varying(300) AS uniprot_id,
    NULL::integer AS num_of_compounds,
    NULL::integer AS num_of_activities,
    NULL::timestamp without time zone AS created_at,
    NULL::timestamp without time zone AS updated_at,
    NULL::bigint AS natural_product_count,
    NULL::bigint AS bioactivity_count,
    NULL::numeric AS best_activity_value;


ALTER VIEW public.v_target_detail OWNER TO yfguo;

--
-- Name: VIEW v_target_detail; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON VIEW public.v_target_detail IS '靶点详情视图 - 汇总关联天然产物数、生物活性数、最佳活性值等统计信息';


--
-- Name: COLUMN v_target_detail.id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.v_target_detail.id IS '主键ID';


--
-- Name: COLUMN v_target_detail.target_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.v_target_detail.target_id IS '靶点编号';


--
-- Name: COLUMN v_target_detail.target_type; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.v_target_detail.target_type IS '靶点类型（Protein、Cell line、Gene、Enzyme）';


--
-- Name: COLUMN v_target_detail.target_name; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.v_target_detail.target_name IS '靶点名称';


--
-- Name: COLUMN v_target_detail.target_organism; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.v_target_detail.target_organism IS '靶点来源物种';


--
-- Name: COLUMN v_target_detail.target_organism_tax_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.v_target_detail.target_organism_tax_id IS '靶点来源物种分类学ID';


--
-- Name: COLUMN v_target_detail.uniprot_id; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.v_target_detail.uniprot_id IS 'UniProt蛋白质数据库编号';


--
-- Name: COLUMN v_target_detail.num_of_compounds; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.v_target_detail.num_of_compounds IS '关联化合物数（旧字段）';


--
-- Name: COLUMN v_target_detail.num_of_activities; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.v_target_detail.num_of_activities IS '生物活性记录数';


--
-- Name: COLUMN v_target_detail.created_at; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.v_target_detail.created_at IS '创建时间';


--
-- Name: COLUMN v_target_detail.updated_at; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.v_target_detail.updated_at IS '更新时间';


--
-- Name: COLUMN v_target_detail.natural_product_count; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.v_target_detail.natural_product_count IS '关联天然产物总数';


--
-- Name: COLUMN v_target_detail.bioactivity_count; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.v_target_detail.bioactivity_count IS '生物活性记录总数';


--
-- Name: COLUMN v_target_detail.best_activity_value; Type: COMMENT; Schema: public; Owner: yfguo
--

COMMENT ON COLUMN public.v_target_detail.best_activity_value IS '最佳活性值（最小的标准化活性值）';


--
-- Name: bio_resource_disease_associations id; Type: DEFAULT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.bio_resource_disease_associations ALTER COLUMN id SET DEFAULT nextval('public.bio_resource_disease_associations_id_seq'::regclass);


--
-- Name: bio_resource_natural_products id; Type: DEFAULT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.bio_resource_natural_products ALTER COLUMN id SET DEFAULT nextval('public.bio_resource_natural_products_new_id_seq'::regclass);


--
-- Name: bio_resources id; Type: DEFAULT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.bio_resources ALTER COLUMN id SET DEFAULT nextval('public.bio_resources_id_seq'::regclass);


--
-- Name: bioactivity id; Type: DEFAULT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.bioactivity ALTER COLUMN id SET DEFAULT nextval('public.bioactivity_id_seq'::regclass);


--
-- Name: diseases id; Type: DEFAULT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.diseases ALTER COLUMN id SET DEFAULT nextval('public.diseases_id_seq'::regclass);


--
-- Name: natural_products id; Type: DEFAULT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.natural_products ALTER COLUMN id SET DEFAULT nextval('public.compounds_id_seq'::regclass);


--
-- Name: prescription_resources id; Type: DEFAULT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.prescription_resources ALTER COLUMN id SET DEFAULT nextval('public.prescription_resources_id_seq'::regclass);


--
-- Name: prescriptions id; Type: DEFAULT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.prescriptions ALTER COLUMN id SET DEFAULT nextval('public.prescriptions_id_seq'::regclass);


--
-- Name: targets id; Type: DEFAULT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.targets ALTER COLUMN id SET DEFAULT nextval('public.targets_id_seq'::regclass);


--
-- Name: bio_resource_disease_associations bio_resource_disease_associations_pkey; Type: CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.bio_resource_disease_associations
    ADD CONSTRAINT bio_resource_disease_associations_pkey PRIMARY KEY (id);


--
-- Name: bio_resource_natural_products bio_resource_natural_products_new_pkey; Type: CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.bio_resource_natural_products
    ADD CONSTRAINT bio_resource_natural_products_new_pkey PRIMARY KEY (id);


--
-- Name: bio_resources bio_resources_pkey; Type: CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.bio_resources
    ADD CONSTRAINT bio_resources_pkey PRIMARY KEY (id);


--
-- Name: bio_resources bio_resources_resource_id_key; Type: CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.bio_resources
    ADD CONSTRAINT bio_resources_resource_id_key UNIQUE (resource_id);


--
-- Name: bioactivity bioactivity_pkey; Type: CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.bioactivity
    ADD CONSTRAINT bioactivity_pkey PRIMARY KEY (id);


--
-- Name: natural_products compounds_np_id_key; Type: CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.natural_products
    ADD CONSTRAINT compounds_np_id_key UNIQUE (np_id);


--
-- Name: natural_products compounds_pkey; Type: CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.natural_products
    ADD CONSTRAINT compounds_pkey PRIMARY KEY (id);


--
-- Name: diseases diseases_pkey; Type: CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.diseases
    ADD CONSTRAINT diseases_pkey PRIMARY KEY (id);


--
-- Name: prescription_resources prescription_resources_pkey; Type: CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.prescription_resources
    ADD CONSTRAINT prescription_resources_pkey PRIMARY KEY (id);


--
-- Name: prescriptions prescriptions_pkey; Type: CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.prescriptions
    ADD CONSTRAINT prescriptions_pkey PRIMARY KEY (id);


--
-- Name: prescriptions prescriptions_prescription_id_key; Type: CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.prescriptions
    ADD CONSTRAINT prescriptions_prescription_id_key UNIQUE (prescription_id);


--
-- Name: sys_dict sys_dict_pkey; Type: CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.sys_dict
    ADD CONSTRAINT sys_dict_pkey PRIMARY KEY (dict_code);


--
-- Name: sys_menu sys_menu_pkey; Type: CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.sys_menu
    ADD CONSTRAINT sys_menu_pkey PRIMARY KEY (menu_id);


--
-- Name: targets targets_pkey; Type: CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.targets
    ADD CONSTRAINT targets_pkey PRIMARY KEY (id);


--
-- Name: targets targets_target_id_key; Type: CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.targets
    ADD CONSTRAINT targets_target_id_key UNIQUE (target_id);


--
-- Name: bio_resource_disease_associations uk_bio_resource_disease; Type: CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.bio_resource_disease_associations
    ADD CONSTRAINT uk_bio_resource_disease UNIQUE (bio_resource_id, disease_id);


--
-- Name: prescription_resources uk_prescription_resource; Type: CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.prescription_resources
    ADD CONSTRAINT uk_prescription_resource UNIQUE (prescription_id, bio_resource_id);


--
-- Name: idx_bio_resources_chinese_gin; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bio_resources_chinese_gin ON public.bio_resources USING gin (to_tsvector('simple'::regconfig, (COALESCE(chinese_name, ''::character varying))::text));


--
-- Name: idx_bio_resources_chinese_name; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bio_resources_chinese_name ON public.bio_resources USING btree (chinese_name);


--
-- Name: idx_bio_resources_cmaup_id; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bio_resources_cmaup_id ON public.bio_resources USING btree (cmaup_id);


--
-- Name: idx_bio_resources_family; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bio_resources_family ON public.bio_resources USING btree (taxonomy_family);


--
-- Name: idx_bio_resources_family_tax_id; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bio_resources_family_tax_id ON public.bio_resources USING btree (family_tax_id);


--
-- Name: idx_bio_resources_genus; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bio_resources_genus ON public.bio_resources USING btree (taxonomy_genus);


--
-- Name: idx_bio_resources_genus_tax_id; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bio_resources_genus_tax_id ON public.bio_resources USING btree (genus_tax_id);


--
-- Name: idx_bio_resources_id; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bio_resources_id ON public.bio_resources USING btree (resource_id);


--
-- Name: idx_bio_resources_latin_gin; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bio_resources_latin_gin ON public.bio_resources USING gin (to_tsvector('english'::regconfig, (COALESCE(latin_name, ''::character varying))::text));


--
-- Name: idx_bio_resources_latin_name; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bio_resources_latin_name ON public.bio_resources USING btree (latin_name);


--
-- Name: idx_bio_resources_species_tax_id; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bio_resources_species_tax_id ON public.bio_resources USING btree (species_tax_id);


--
-- Name: idx_bio_resources_tcmid_id; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bio_resources_tcmid_id ON public.bio_resources USING btree (tcmid_id);


--
-- Name: idx_bio_resources_type; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bio_resources_type ON public.bio_resources USING btree (resource_type);


--
-- Name: idx_bioactivity_activity_value; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bioactivity_activity_value ON public.bioactivity USING btree (activity_value);


--
-- Name: idx_bioactivity_natural_product; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bioactivity_natural_product ON public.bioactivity USING btree (natural_product_id);


--
-- Name: idx_bioactivity_natural_product_target; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bioactivity_natural_product_target ON public.bioactivity USING btree (natural_product_id, target_id);


--
-- Name: idx_bioactivity_natural_product_value_std; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bioactivity_natural_product_value_std ON public.bioactivity USING btree (natural_product_id, activity_value_std);


--
-- Name: idx_bioactivity_ref_id; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bioactivity_ref_id ON public.bioactivity USING btree (ref_id);


--
-- Name: idx_bioactivity_relation; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bioactivity_relation ON public.bioactivity USING btree (activity_relation);


--
-- Name: idx_bioactivity_target; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bioactivity_target ON public.bioactivity USING btree (target_id);


--
-- Name: idx_bioactivity_target_natural_product; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bioactivity_target_natural_product ON public.bioactivity USING btree (target_id, natural_product_id);


--
-- Name: idx_bioactivity_type; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bioactivity_type ON public.bioactivity USING btree (activity_type);


--
-- Name: idx_bioactivity_type_grouped; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bioactivity_type_grouped ON public.bioactivity USING btree (activity_type_grouped);


--
-- Name: idx_bioactivity_type_value_std; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bioactivity_type_value_std ON public.bioactivity USING btree (activity_type, activity_value_std);


--
-- Name: idx_bioactivity_value_std; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_bioactivity_value_std ON public.bioactivity USING btree (activity_value_std);


--
-- Name: idx_brda_bio_resource; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_brda_bio_resource ON public.bio_resource_disease_associations USING btree (bio_resource_id);


--
-- Name: idx_brda_confidence; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_brda_confidence ON public.bio_resource_disease_associations USING btree (confidence_score);


--
-- Name: idx_brda_disease; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_brda_disease ON public.bio_resource_disease_associations USING btree (disease_id);


--
-- Name: idx_brnp_np_id; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_brnp_np_id ON public.bio_resource_natural_products USING btree (np_id);


--
-- Name: idx_brnp_org_id; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_brnp_org_id ON public.bio_resource_natural_products USING btree (org_id);


--
-- Name: idx_brnp_org_np; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_brnp_org_np ON public.bio_resource_natural_products USING btree (org_id, np_id);


--
-- Name: idx_brnp_ref_id; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_brnp_ref_id ON public.bio_resource_natural_products USING btree (ref_id);


--
-- Name: idx_diseases_category; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_diseases_category ON public.diseases USING btree (disease_category);


--
-- Name: idx_diseases_icd11_code; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_diseases_icd11_code ON public.diseases USING btree (icd11_code);


--
-- Name: idx_diseases_name_gin; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_diseases_name_gin ON public.diseases USING gin (to_tsvector('english'::regconfig, (COALESCE(disease_name, ''::character varying))::text));


--
-- Name: idx_natural_products_chembl_id; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_natural_products_chembl_id ON public.natural_products USING btree (chembl_id);


--
-- Name: idx_natural_products_inchikey; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_natural_products_inchikey ON public.natural_products USING btree (inchikey);


--
-- Name: idx_natural_products_iupac_name_gin; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_natural_products_iupac_name_gin ON public.natural_products USING gin (to_tsvector('english'::regconfig, COALESCE(iupac_name, ''::text)));


--
-- Name: idx_natural_products_mw; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_natural_products_mw ON public.natural_products USING btree (molecular_weight);


--
-- Name: idx_natural_products_np_id; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_natural_products_np_id ON public.natural_products USING btree (np_id);


--
-- Name: idx_natural_products_num_activity; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_natural_products_num_activity ON public.natural_products USING btree (num_of_activity);


--
-- Name: idx_natural_products_num_target; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_natural_products_num_target ON public.natural_products USING btree (num_of_target);


--
-- Name: idx_natural_products_pref_name; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_natural_products_pref_name ON public.natural_products USING btree (pref_name);


--
-- Name: idx_natural_products_pref_name_gin; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_natural_products_pref_name_gin ON public.natural_products USING gin (to_tsvector('english'::regconfig, COALESCE(pref_name, (''::character varying)::text)));


--
-- Name: idx_natural_products_psa; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_natural_products_psa ON public.natural_products USING btree (psa);


--
-- Name: idx_natural_products_pubchem_id; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_natural_products_pubchem_id ON public.natural_products USING btree (pubchem_id);


--
-- Name: idx_natural_products_xlogp; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_natural_products_xlogp ON public.natural_products USING btree (xlogp);


--
-- Name: idx_pr_bio_resource; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_pr_bio_resource ON public.prescription_resources USING btree (bio_resource_id);


--
-- Name: idx_pr_prescription; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_pr_prescription ON public.prescription_resources USING btree (prescription_id);


--
-- Name: idx_pr_tcmid_component; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_pr_tcmid_component ON public.prescription_resources USING btree (tcmid_component_id);


--
-- Name: idx_prescriptions_chinese_gin; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_prescriptions_chinese_gin ON public.prescriptions USING gin (to_tsvector('simple'::regconfig, (COALESCE(chinese_name, ''::character varying))::text));


--
-- Name: idx_prescriptions_chinese_name; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_prescriptions_chinese_name ON public.prescriptions USING btree (chinese_name);


--
-- Name: idx_prescriptions_functions_gin; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_prescriptions_functions_gin ON public.prescriptions USING gin (to_tsvector('simple'::regconfig, COALESCE(functions, ''::text)));


--
-- Name: idx_prescriptions_icd11_gin; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_prescriptions_icd11_gin ON public.prescriptions USING gin (to_tsvector('english'::regconfig, COALESCE(disease_icd11_category, ''::text)));


--
-- Name: idx_prescriptions_id; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_prescriptions_id ON public.prescriptions USING btree (prescription_id);


--
-- Name: idx_prescriptions_indications_gin; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_prescriptions_indications_gin ON public.prescriptions USING gin (to_tsvector('simple'::regconfig, COALESCE(indications, ''::text)));


--
-- Name: idx_prescriptions_pinyin; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_prescriptions_pinyin ON public.prescriptions USING btree (pinyin_name);


--
-- Name: idx_targets_ec_number; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_targets_ec_number ON public.targets USING btree (ec_number);


--
-- Name: idx_targets_function_gin; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_targets_function_gin ON public.targets USING gin (to_tsvector('english'::regconfig, COALESCE(function, ''::text)));


--
-- Name: idx_targets_gene_name; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_targets_gene_name ON public.targets USING btree (gene_name);


--
-- Name: idx_targets_name; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_targets_name ON public.targets USING btree (target_name);


--
-- Name: idx_targets_name_gin; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_targets_name_gin ON public.targets USING gin (to_tsvector('english'::regconfig, (COALESCE(target_name, ''::character varying))::text));


--
-- Name: idx_targets_organism; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_targets_organism ON public.targets USING btree (target_organism);


--
-- Name: idx_targets_synonyms_gin; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_targets_synonyms_gin ON public.targets USING gin (to_tsvector('english'::regconfig, COALESCE(synonyms, ''::text)));


--
-- Name: idx_targets_target_id; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_targets_target_id ON public.targets USING btree (target_id);


--
-- Name: idx_targets_ttd_id; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_targets_ttd_id ON public.targets USING btree (ttd_id);


--
-- Name: idx_targets_type; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_targets_type ON public.targets USING btree (target_type);


--
-- Name: idx_targets_uniprot; Type: INDEX; Schema: public; Owner: yfguo
--

CREATE INDEX idx_targets_uniprot ON public.targets USING btree (uniprot_id);


--
-- Name: v_target_detail _RETURN; Type: RULE; Schema: public; Owner: yfguo
--

CREATE OR REPLACE VIEW public.v_target_detail AS
 SELECT t.id,
    t.target_id,
    t.target_type,
    t.target_name,
    t.target_organism,
    t.target_organism_tax_id,
    t.uniprot_id,
    t.num_of_compounds,
    t.num_of_activities,
    t.created_at,
    t.updated_at,
    count(DISTINCT b.natural_product_id) AS natural_product_count,
    count(DISTINCT b.id) AS bioactivity_count,
    min(b.activity_value_std) AS best_activity_value
   FROM (public.targets t
     LEFT JOIN public.bioactivity b ON ((t.id = b.target_id)))
  GROUP BY t.id;


--
-- Name: bio_resources update_bio_resources_updated_at; Type: TRIGGER; Schema: public; Owner: yfguo
--

CREATE TRIGGER update_bio_resources_updated_at BEFORE UPDATE ON public.bio_resources FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: bio_resource_natural_products update_brnp_updated_at; Type: TRIGGER; Schema: public; Owner: yfguo
--

CREATE TRIGGER update_brnp_updated_at BEFORE UPDATE ON public.bio_resource_natural_products FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: diseases update_diseases_updated_at; Type: TRIGGER; Schema: public; Owner: yfguo
--

CREATE TRIGGER update_diseases_updated_at BEFORE UPDATE ON public.diseases FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: natural_products update_natural_products_updated_at; Type: TRIGGER; Schema: public; Owner: yfguo
--

CREATE TRIGGER update_natural_products_updated_at BEFORE UPDATE ON public.natural_products FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: prescriptions update_prescriptions_updated_at; Type: TRIGGER; Schema: public; Owner: yfguo
--

CREATE TRIGGER update_prescriptions_updated_at BEFORE UPDATE ON public.prescriptions FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: targets update_targets_updated_at; Type: TRIGGER; Schema: public; Owner: yfguo
--

CREATE TRIGGER update_targets_updated_at BEFORE UPDATE ON public.targets FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: bioactivity fk_bioactivity_natural_product; Type: FK CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.bioactivity
    ADD CONSTRAINT fk_bioactivity_natural_product FOREIGN KEY (natural_product_id) REFERENCES public.natural_products(id) ON DELETE CASCADE;


--
-- Name: bioactivity fk_bioactivity_target; Type: FK CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.bioactivity
    ADD CONSTRAINT fk_bioactivity_target FOREIGN KEY (target_id) REFERENCES public.targets(id) ON DELETE CASCADE;


--
-- Name: bio_resource_disease_associations fk_brda_bio_resource; Type: FK CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.bio_resource_disease_associations
    ADD CONSTRAINT fk_brda_bio_resource FOREIGN KEY (bio_resource_id) REFERENCES public.bio_resources(id) ON DELETE CASCADE;


--
-- Name: bio_resource_disease_associations fk_brda_disease; Type: FK CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.bio_resource_disease_associations
    ADD CONSTRAINT fk_brda_disease FOREIGN KEY (disease_id) REFERENCES public.diseases(id) ON DELETE CASCADE;


--
-- Name: prescription_resources fk_pr_bio_resource; Type: FK CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.prescription_resources
    ADD CONSTRAINT fk_pr_bio_resource FOREIGN KEY (bio_resource_id) REFERENCES public.bio_resources(id) ON DELETE CASCADE;


--
-- Name: prescription_resources fk_pr_prescription; Type: FK CONSTRAINT; Schema: public; Owner: yfguo
--

ALTER TABLE ONLY public.prescription_resources
    ADD CONSTRAINT fk_pr_prescription FOREIGN KEY (prescription_id) REFERENCES public.prescriptions(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict JBajSlJHh2giQYgBKmXf3ptqgY0wSYxeJ58On2axIUdLPueag6j7y980nqudnkn

