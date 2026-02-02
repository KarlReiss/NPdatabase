--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.3

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
-- Name: update_updated_at_column(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: bio_resource_natural_products; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bio_resource_natural_products (
    id bigint NOT NULL,
    bio_resource_id bigint NOT NULL,
    natural_product_id bigint NOT NULL,
    content_value numeric(20,6),
    content_unit character varying(50),
    content_part character varying(200),
    isolation_method character varying(200),
    ref_id character varying(100),
    ref_id_type character varying(20),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: TABLE bio_resource_natural_products; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.bio_resource_natural_products IS '生物资源-天然产物关联表 - 记录生物资源包含的天然产物';


--
-- Name: bio_resource_compounds_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bio_resource_compounds_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bio_resource_compounds_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bio_resource_compounds_id_seq OWNED BY public.bio_resource_natural_products.id;


--
-- Name: bio_resource_disease_associations; Type: TABLE; Schema: public; Owner: -
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


--
-- Name: TABLE bio_resource_disease_associations; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.bio_resource_disease_associations IS '生物资源-疾病关联表 - 记录植物与疾病的关联及证据';


--
-- Name: COLUMN bio_resource_disease_associations.bio_resource_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.bio_resource_disease_associations.bio_resource_id IS '关联的生物资源ID';


--
-- Name: COLUMN bio_resource_disease_associations.disease_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.bio_resource_disease_associations.disease_id IS '关联的疾病ID';


--
-- Name: COLUMN bio_resource_disease_associations.evidence_therapeutic_target; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.bio_resource_disease_associations.evidence_therapeutic_target IS '治疗靶点证据（靶点列表，分号分隔）';


--
-- Name: COLUMN bio_resource_disease_associations.evidence_transcriptome; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.bio_resource_disease_associations.evidence_transcriptome IS '转录组证据（布尔值）';


--
-- Name: COLUMN bio_resource_disease_associations.evidence_clinical_trial_plant; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.bio_resource_disease_associations.evidence_clinical_trial_plant IS '植物临床试验证据（试验ID，分号分隔）';


--
-- Name: COLUMN bio_resource_disease_associations.evidence_clinical_trial_ingredient; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.bio_resource_disease_associations.evidence_clinical_trial_ingredient IS '成分临床试验证据（试验ID，分号分隔）';


--
-- Name: COLUMN bio_resource_disease_associations.confidence_score; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.bio_resource_disease_associations.confidence_score IS '置信度评分（0-1之间的小数）';


--
-- Name: COLUMN bio_resource_disease_associations.source; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.bio_resource_disease_associations.source IS '数据来源';


--
-- Name: COLUMN bio_resource_disease_associations.source_version; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.bio_resource_disease_associations.source_version IS '数据版本';


--
-- Name: bio_resource_disease_associations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bio_resource_disease_associations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bio_resource_disease_associations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bio_resource_disease_associations_id_seq OWNED BY public.bio_resource_disease_associations.id;


--
-- Name: bio_resources; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bio_resources (
    id bigint NOT NULL,
    resource_id character varying(50) NOT NULL,
    resource_type character varying(50) NOT NULL,
    chinese_name character varying(500),
    latin_name character varying(500),
    english_name character varying(500),
    pinyin_name character varying(200),
    alias text,
    taxonomy_kingdom character varying(100),
    taxonomy_phylum character varying(100),
    taxonomy_class character varying(100),
    taxonomy_order character varying(100),
    taxonomy_family character varying(200),
    taxonomy_genus character varying(200),
    taxonomy_species character varying(200),
    taxonomy_id character varying(50),
    medicinal_part character varying(200),
    medicinal_part_latin character varying(200),
    origin_region text,
    distribution text,
    habitat text,
    tcm_property character varying(100),
    tcm_flavor character varying(100),
    tcm_meridian character varying(200),
    tcm_toxicity character varying(50),
    functions text,
    indications text,
    contraindications text,
    mineral_composition character varying(500),
    mineral_crystal_system character varying(100),
    mineral_hardness character varying(50),
    mineral_color character varying(100),
    microbe_strain character varying(200),
    microbe_culture_condition text,
    microbe_fermentation_product text,
    animal_class character varying(100),
    animal_conservation_status character varying(50),
    tcmid_id character varying(50),
    tcmsp_id character varying(50),
    herb_id character varying(50),
    pharmacopoeia_ref character varying(200),
    literature_ref text,
    image_url text,
    num_of_natural_products integer DEFAULT 0,
    num_of_prescriptions integer DEFAULT 0,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    species_tax_id character varying(50),
    genus_tax_id character varying(50),
    family_tax_id character varying(50),
    cmaup_id character varying(50)
);


--
-- Name: TABLE bio_resources; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.bio_resources IS '生物资源表 - 存储植物、动物、微生物、矿物等天然产物来源，包含分类学信息和药用属性';


--
-- Name: COLUMN bio_resources.resource_type; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.bio_resources.resource_type IS '资源类型: Plant(植物), Animal(动物), Microorganism(微生物), Mineral(矿物), Fungus(真菌)';


--
-- Name: COLUMN bio_resources.tcm_property; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.bio_resources.tcm_property IS '中医药性: 寒、热、温、凉、平';


--
-- Name: COLUMN bio_resources.tcm_flavor; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.bio_resources.tcm_flavor IS '中医药味: 酸、苦、甘、辛、咸、淡、涩';


--
-- Name: COLUMN bio_resources.num_of_natural_products; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.bio_resources.num_of_natural_products IS '包含的天然产物数量';


--
-- Name: COLUMN bio_resources.species_tax_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.bio_resources.species_tax_id IS '种的Taxonomy ID';


--
-- Name: COLUMN bio_resources.genus_tax_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.bio_resources.genus_tax_id IS '属的Taxonomy ID';


--
-- Name: COLUMN bio_resources.family_tax_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.bio_resources.family_tax_id IS '科的Taxonomy ID';


--
-- Name: COLUMN bio_resources.cmaup_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.bio_resources.cmaup_id IS 'CMAUP数据库ID';


--
-- Name: bio_resources_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bio_resources_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bio_resources_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bio_resources_id_seq OWNED BY public.bio_resources.id;


--
-- Name: bioactivity; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bioactivity (
    id bigint NOT NULL,
    natural_product_id bigint NOT NULL,
    target_id bigint NOT NULL,
    activity_type character varying(100),
    activity_type_grouped character varying(100),
    activity_relation character varying(10),
    activity_value numeric(20,6),
    activity_units character varying(100),
    activity_value_std numeric(20,6),
    activity_units_std character varying(20) DEFAULT 'nM'::character varying,
    assay_organism character varying(200),
    assay_tax_id character varying(100),
    assay_strain character varying(100),
    assay_tissue character varying(200),
    assay_cell_type character varying(100),
    ref_id character varying(300),
    ref_id_type character varying(20),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_activity_value CHECK (((activity_value IS NULL) OR (activity_value >= (0)::numeric))),
    CONSTRAINT chk_activity_value_std CHECK (((activity_value_std IS NULL) OR (activity_value_std >= (0)::numeric)))
);


--
-- Name: TABLE bioactivity; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.bioactivity IS '活性记录表 - 存储天然产物对靶点的生物活性数据';


--
-- Name: COLUMN bioactivity.natural_product_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.bioactivity.natural_product_id IS '关联的天然产物 ID';


--
-- Name: COLUMN bioactivity.activity_relation; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.bioactivity.activity_relation IS '活性关系: = (等于), > (大于), < (小于)';


--
-- Name: COLUMN bioactivity.activity_value_std; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.bioactivity.activity_value_std IS '标准化活性值 (统一转换为 nM)';


--
-- Name: bioactivity_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bioactivity_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bioactivity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bioactivity_id_seq OWNED BY public.bioactivity.id;


--
-- Name: natural_products; Type: TABLE; Schema: public; Owner: -
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
    gene_cluster text,
    if_quantity boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_mw CHECK (((molecular_weight IS NULL) OR (molecular_weight > (0)::numeric)))
);


--
-- Name: TABLE natural_products; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.natural_products IS '天然产物表 - 存储天然产物的基本信息、结构和理化性质';


--
-- Name: COLUMN natural_products.np_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.natural_products.np_id IS 'NPASS 天然产物 ID (如 NPC491451)';


--
-- Name: COLUMN natural_products.molecular_weight; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.natural_products.molecular_weight IS '分子量 (g/mol)';


--
-- Name: COLUMN natural_products.xlogp; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.natural_products.xlogp IS '脂水分配系数 (计算值)';


--
-- Name: COLUMN natural_products.psa; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.natural_products.psa IS '极性表面积 (Å²)';


--
-- Name: compounds_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.compounds_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: compounds_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.compounds_id_seq OWNED BY public.natural_products.id;


--
-- Name: diseases; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.diseases (
    id bigint NOT NULL,
    disease_id character varying(50) NOT NULL,
    icd11_code character varying(50) NOT NULL,
    disease_name character varying(500) NOT NULL,
    disease_name_zh character varying(500),
    disease_category character varying(200),
    description text,
    symptoms text,
    num_of_related_plants integer DEFAULT 0,
    num_of_related_targets integer DEFAULT 0,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: TABLE diseases; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.diseases IS '疾病表 - 存储疾病信息（基于ICD-11分类）';


--
-- Name: COLUMN diseases.disease_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.diseases.disease_id IS '疾病唯一标识符（自动生成，如 DIS0001）';


--
-- Name: COLUMN diseases.icd11_code; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.diseases.icd11_code IS 'ICD-11疾病分类编码';


--
-- Name: COLUMN diseases.disease_name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.diseases.disease_name IS '疾病英文名称';


--
-- Name: COLUMN diseases.disease_name_zh; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.diseases.disease_name_zh IS '疾病中文名称';


--
-- Name: COLUMN diseases.disease_category; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.diseases.disease_category IS '疾病分类';


--
-- Name: COLUMN diseases.description; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.diseases.description IS '疾病描述';


--
-- Name: COLUMN diseases.symptoms; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.diseases.symptoms IS '疾病症状';


--
-- Name: COLUMN diseases.num_of_related_plants; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.diseases.num_of_related_plants IS '关联植物数量';


--
-- Name: COLUMN diseases.num_of_related_targets; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.diseases.num_of_related_targets IS '关联靶点数量';


--
-- Name: diseases_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.diseases_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: diseases_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.diseases_id_seq OWNED BY public.diseases.id;


--
-- Name: prescription_natural_products; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.prescription_natural_products (
    id bigint NOT NULL,
    prescription_id bigint NOT NULL,
    natural_product_id bigint NOT NULL,
    source_resource_id bigint,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: TABLE prescription_natural_products; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.prescription_natural_products IS '处方-天然产物关联表 - 记录处方包含的天然产物（直接关联）';


--
-- Name: prescription_compounds_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.prescription_compounds_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: prescription_compounds_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.prescription_compounds_id_seq OWNED BY public.prescription_natural_products.id;


--
-- Name: prescription_resources; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.prescription_resources (
    id bigint NOT NULL,
    prescription_id bigint NOT NULL,
    bio_resource_id bigint NOT NULL,
    dosage_value numeric(10,2),
    dosage_unit character varying(20),
    dosage_text character varying(100),
    role character varying(50),
    role_chinese character varying(20),
    processing_method character varying(200),
    processing_note text,
    sort_order integer DEFAULT 0,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    tcmid_component_id character varying(50),
    barcode character varying(100),
    latin_name character varying(500),
    chinese_name character varying(500)
);


--
-- Name: TABLE prescription_resources; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.prescription_resources IS '处方-生物资源关联表 - 记录处方的组成药材';


--
-- Name: COLUMN prescription_resources.dosage_text; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prescription_resources.dosage_text IS '药材用量文本（来自TCMID的ComponentQuantity）';


--
-- Name: COLUMN prescription_resources.role; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prescription_resources.role IS '君臣佐使: Monarch(君), Minister(臣), Assistant(佐), Guide(使)';


--
-- Name: COLUMN prescription_resources.tcmid_component_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prescription_resources.tcmid_component_id IS 'TCMID药材组分ID（如 TCMH1398）';


--
-- Name: COLUMN prescription_resources.barcode; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prescription_resources.barcode IS 'TCMID药材条形码（如 ITSAM882-14）';


--
-- Name: COLUMN prescription_resources.latin_name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prescription_resources.latin_name IS '药材拉丁名（来自TCMID）';


--
-- Name: COLUMN prescription_resources.chinese_name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prescription_resources.chinese_name IS '药材中文名（来自TCMID）';


--
-- Name: prescription_resources_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.prescription_resources_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: prescription_resources_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.prescription_resources_id_seq OWNED BY public.prescription_resources.id;


--
-- Name: prescriptions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.prescriptions (
    id bigint NOT NULL,
    prescription_id character varying(50) NOT NULL,
    chinese_name character varying(500),
    pinyin_name character varying(200),
    english_name character varying(500),
    alias text,
    source_book character varying(200),
    source_dynasty character varying(100),
    source_author character varying(100),
    category character varying(100),
    subcategory character varying(100),
    functions text,
    indications text,
    indications_modern text,
    syndrome character varying(500),
    composition_text text,
    dosage_form character varying(100),
    preparation_method text,
    usage_method text,
    dosage text,
    contraindications text,
    precautions text,
    adverse_reactions text,
    pharmacology text,
    clinical_application text,
    target_tissues text,
    related_diseases text,
    tcmid_id character varying(50),
    tcmsp_id character varying(50),
    symmap_id character varying(50),
    pharmacopoeia_ref character varying(200),
    literature_ref text,
    num_of_herbs integer DEFAULT 0,
    num_of_natural_products integer DEFAULT 0,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    disease_icd11_category text,
    human_tissues text,
    reference text,
    reference_book text
);


--
-- Name: TABLE prescriptions; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.prescriptions IS '处方表 - 存储中医方剂/处方信息';


--
-- Name: COLUMN prescriptions.prescription_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prescriptions.prescription_id IS '处方唯一标识符（TCMID格式: TCMF1, TCMF2等）';


--
-- Name: COLUMN prescriptions.chinese_name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prescriptions.chinese_name IS '处方中文名称';


--
-- Name: COLUMN prescriptions.pinyin_name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prescriptions.pinyin_name IS '处方拼音名称';


--
-- Name: COLUMN prescriptions.english_name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prescriptions.english_name IS '处方英文名称';


--
-- Name: COLUMN prescriptions.category; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prescriptions.category IS '方剂分类: 补益剂、解表剂、清热剂、泻下剂、祛湿剂、理气剂、理血剂、治风剂等';


--
-- Name: COLUMN prescriptions.functions; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prescriptions.functions IS '功能描述（功效）';


--
-- Name: COLUMN prescriptions.indications; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prescriptions.indications IS '适应症';


--
-- Name: COLUMN prescriptions.dosage_form; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prescriptions.dosage_form IS '剂型: 丸、散、汤、膏、丹、酒、露、锭等';


--
-- Name: COLUMN prescriptions.num_of_natural_products; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prescriptions.num_of_natural_products IS '包含的天然产物数量 (间接)';


--
-- Name: COLUMN prescriptions.disease_icd11_category; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prescriptions.disease_icd11_category IS 'ICD-11疾病分类编码（多个用分号分隔）';


--
-- Name: COLUMN prescriptions.human_tissues; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prescriptions.human_tissues IS '相关人体组织';


--
-- Name: COLUMN prescriptions.reference; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prescriptions.reference IS '参考文献';


--
-- Name: COLUMN prescriptions.reference_book; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prescriptions.reference_book IS '参考书籍';


--
-- Name: prescriptions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.prescriptions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: prescriptions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.prescriptions_id_seq OWNED BY public.prescriptions.id;


--
-- Name: sys_dict; Type: TABLE; Schema: public; Owner: -
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


--
-- Name: TABLE sys_dict; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.sys_dict IS '字典表';


--
-- Name: COLUMN sys_dict.dict_code; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_dict.dict_code IS '字典编码';


--
-- Name: COLUMN sys_dict.dict_sort; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_dict.dict_sort IS '字典排序';


--
-- Name: COLUMN sys_dict.dict_label; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_dict.dict_label IS '字典标签';


--
-- Name: COLUMN sys_dict.dict_value; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_dict.dict_value IS '字典键值';


--
-- Name: COLUMN sys_dict.dict_type; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_dict.dict_type IS '字典类型';


--
-- Name: COLUMN sys_dict.css_class; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_dict.css_class IS '样式属性（其他样式扩展）';


--
-- Name: COLUMN sys_dict.list_class; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_dict.list_class IS '表格回显样式';


--
-- Name: COLUMN sys_dict.is_default; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_dict.is_default IS '是否默认（Y是 N否）';


--
-- Name: COLUMN sys_dict.status; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_dict.status IS '状态（0正常 1停用）';


--
-- Name: COLUMN sys_dict.create_by; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_dict.create_by IS '创建者';


--
-- Name: COLUMN sys_dict.create_time; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_dict.create_time IS '创建时间';


--
-- Name: COLUMN sys_dict.update_by; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_dict.update_by IS '更新者';


--
-- Name: COLUMN sys_dict.update_time; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_dict.update_time IS '更新时间';


--
-- Name: COLUMN sys_dict.remark; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_dict.remark IS '备注';


--
-- Name: sys_menu; Type: TABLE; Schema: public; Owner: -
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


--
-- Name: TABLE sys_menu; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.sys_menu IS '菜单权限表';


--
-- Name: COLUMN sys_menu.menu_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_menu.menu_id IS '菜单ID';


--
-- Name: COLUMN sys_menu.menu_name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_menu.menu_name IS '菜单名称';


--
-- Name: COLUMN sys_menu.parent_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_menu.parent_id IS '父菜单ID';


--
-- Name: COLUMN sys_menu.order_num; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_menu.order_num IS '显示顺序';


--
-- Name: COLUMN sys_menu.path; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_menu.path IS '路由地址';


--
-- Name: COLUMN sys_menu.component; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_menu.component IS '组件路径';


--
-- Name: COLUMN sys_menu.query_param; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_menu.query_param IS '路由参数';


--
-- Name: COLUMN sys_menu.is_frame; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_menu.is_frame IS '是否为外链 (0是1否)';


--
-- Name: COLUMN sys_menu.is_cache; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_menu.is_cache IS '是否缓存 (0缓存1不缓存)';


--
-- Name: COLUMN sys_menu.menu_type; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_menu.menu_type IS '菜单类型 (M目录C菜单F按钮)';


--
-- Name: COLUMN sys_menu.visible; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_menu.visible IS '显示状态 (0显示1隐藏)';


--
-- Name: COLUMN sys_menu.status; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_menu.status IS '菜单状态 (0正常1停用)';


--
-- Name: COLUMN sys_menu.perms; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_menu.perms IS '权限标识';


--
-- Name: COLUMN sys_menu.icon; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_menu.icon IS '菜单图标';


--
-- Name: COLUMN sys_menu.create_by; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_menu.create_by IS '创建者';


--
-- Name: COLUMN sys_menu.create_time; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_menu.create_time IS '创建时间';


--
-- Name: COLUMN sys_menu.update_by; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_menu.update_by IS '更新者';


--
-- Name: COLUMN sys_menu.update_time; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_menu.update_time IS '更新时间';


--
-- Name: COLUMN sys_menu.remark; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.sys_menu.remark IS '备注';


--
-- Name: targets; Type: TABLE; Schema: public; Owner: -
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


--
-- Name: TABLE targets; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.targets IS '靶点表 - 存储生物靶点信息（蛋白、细胞系、基因等）';


--
-- Name: COLUMN targets.target_type; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.targets.target_type IS '靶点类型: Cell line, Protein, Gene, Enzyme';


--
-- Name: COLUMN targets.gene_name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.targets.gene_name IS '基因名称';


--
-- Name: COLUMN targets.synonyms; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.targets.synonyms IS '同义词（多个用分号分隔）';


--
-- Name: COLUMN targets.function; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.targets.function IS '功能描述';


--
-- Name: COLUMN targets.pdb_structure; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.targets.pdb_structure IS 'PDB结构ID（多个用分号分隔）';


--
-- Name: COLUMN targets.bioclass; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.targets.bioclass IS '生物分类';


--
-- Name: COLUMN targets.ec_number; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.targets.ec_number IS 'EC编号';


--
-- Name: COLUMN targets.sequence; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.targets.sequence IS '蛋白质序列';


--
-- Name: COLUMN targets.ttd_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.targets.ttd_id IS 'TTD数据库ID';


--
-- Name: targets_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.targets_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: targets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.targets_id_seq OWNED BY public.targets.id;


--
-- Name: toxicity; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.toxicity (
    id bigint NOT NULL,
    natural_product_id bigint NOT NULL,
    toxicity_type character varying(100),
    toxicity_value numeric(20,6),
    toxicity_units character varying(50),
    dose character varying(100),
    symptoms text,
    assay_organism character varying(200),
    assay_method character varying(200),
    ref_id character varying(50),
    ref_id_type character varying(20),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: TABLE toxicity; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.toxicity IS '毒性表 - 存储天然产物的毒性数据';


--
-- Name: toxicity_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.toxicity_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: toxicity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.toxicity_id_seq OWNED BY public.toxicity.id;


--
-- Name: v_bio_resource_detail; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_bio_resource_detail AS
SELECT
    NULL::bigint AS id,
    NULL::character varying(50) AS resource_id,
    NULL::character varying(50) AS resource_type,
    NULL::character varying(500) AS chinese_name,
    NULL::character varying(500) AS latin_name,
    NULL::character varying(500) AS english_name,
    NULL::character varying(200) AS pinyin_name,
    NULL::text AS alias,
    NULL::character varying(100) AS taxonomy_kingdom,
    NULL::character varying(100) AS taxonomy_phylum,
    NULL::character varying(100) AS taxonomy_class,
    NULL::character varying(100) AS taxonomy_order,
    NULL::character varying(200) AS taxonomy_family,
    NULL::character varying(200) AS taxonomy_genus,
    NULL::character varying(200) AS taxonomy_species,
    NULL::character varying(50) AS taxonomy_id,
    NULL::character varying(200) AS medicinal_part,
    NULL::character varying(200) AS medicinal_part_latin,
    NULL::text AS origin_region,
    NULL::text AS distribution,
    NULL::text AS habitat,
    NULL::character varying(100) AS tcm_property,
    NULL::character varying(100) AS tcm_flavor,
    NULL::character varying(200) AS tcm_meridian,
    NULL::character varying(50) AS tcm_toxicity,
    NULL::text AS functions,
    NULL::text AS indications,
    NULL::text AS contraindications,
    NULL::character varying(500) AS mineral_composition,
    NULL::character varying(100) AS mineral_crystal_system,
    NULL::character varying(50) AS mineral_hardness,
    NULL::character varying(100) AS mineral_color,
    NULL::character varying(200) AS microbe_strain,
    NULL::text AS microbe_culture_condition,
    NULL::text AS microbe_fermentation_product,
    NULL::character varying(100) AS animal_class,
    NULL::character varying(50) AS animal_conservation_status,
    NULL::character varying(50) AS tcmid_id,
    NULL::character varying(50) AS tcmsp_id,
    NULL::character varying(50) AS herb_id,
    NULL::character varying(200) AS pharmacopoeia_ref,
    NULL::text AS literature_ref,
    NULL::text AS image_url,
    NULL::integer AS num_of_compounds,
    NULL::integer AS num_of_prescriptions,
    NULL::timestamp without time zone AS created_at,
    NULL::timestamp without time zone AS updated_at,
    NULL::bigint AS natural_product_count,
    NULL::bigint AS prescription_count;


--
-- Name: VIEW v_bio_resource_detail; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.v_bio_resource_detail IS '生物资源详情视图 - 包含统计信息';


--
-- Name: v_natural_product_detail; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_natural_product_detail AS
SELECT
    NULL::bigint AS id,
    NULL::character varying(50) AS np_id,
    NULL::character varying(100) AS inchikey,
    NULL::text AS pref_name,
    NULL::text AS iupac_name,
    NULL::character varying(10) AS name_initial,
    NULL::text AS inchi,
    NULL::text AS smiles,
    NULL::character varying(50) AS chembl_id,
    NULL::character varying(50) AS pubchem_id,
    NULL::numeric(10,2) AS molecular_weight,
    NULL::numeric(10,2) AS xlogp,
    NULL::numeric(10,2) AS psa,
    NULL::character varying(200) AS formula,
    NULL::integer AS h_bond_donors,
    NULL::integer AS h_bond_acceptors,
    NULL::integer AS rotatable_bonds,
    NULL::integer AS num_of_organism,
    NULL::integer AS num_of_target,
    NULL::integer AS num_of_activity,
    NULL::text AS gene_cluster,
    NULL::boolean AS if_quantity,
    NULL::timestamp without time zone AS created_at,
    NULL::timestamp without time zone AS updated_at,
    NULL::bigint AS bioactivity_count,
    NULL::bigint AS target_count,
    NULL::bigint AS bio_resource_count,
    NULL::numeric AS best_activity_value,
    NULL::boolean AS has_toxicity;


--
-- Name: v_prescription_detail; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_prescription_detail AS
SELECT
    NULL::bigint AS id,
    NULL::character varying(50) AS prescription_id,
    NULL::character varying(500) AS chinese_name,
    NULL::character varying(200) AS pinyin_name,
    NULL::character varying(500) AS english_name,
    NULL::text AS alias,
    NULL::character varying(200) AS source_book,
    NULL::character varying(100) AS source_dynasty,
    NULL::character varying(100) AS source_author,
    NULL::character varying(100) AS category,
    NULL::character varying(100) AS subcategory,
    NULL::text AS functions,
    NULL::text AS indications,
    NULL::text AS indications_modern,
    NULL::character varying(500) AS syndrome,
    NULL::text AS composition_text,
    NULL::character varying(100) AS dosage_form,
    NULL::text AS preparation_method,
    NULL::text AS usage_method,
    NULL::text AS dosage,
    NULL::text AS contraindications,
    NULL::text AS precautions,
    NULL::text AS adverse_reactions,
    NULL::text AS pharmacology,
    NULL::text AS clinical_application,
    NULL::text AS target_tissues,
    NULL::text AS related_diseases,
    NULL::character varying(50) AS tcmid_id,
    NULL::character varying(50) AS tcmsp_id,
    NULL::character varying(50) AS symmap_id,
    NULL::character varying(200) AS pharmacopoeia_ref,
    NULL::text AS literature_ref,
    NULL::integer AS num_of_herbs,
    NULL::integer AS num_of_compounds,
    NULL::timestamp without time zone AS created_at,
    NULL::timestamp without time zone AS updated_at,
    NULL::bigint AS herb_count,
    NULL::bigint AS direct_natural_product_count;


--
-- Name: VIEW v_prescription_detail; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON VIEW public.v_prescription_detail IS '处方详情视图 - 包含统计信息';


--
-- Name: v_target_detail; Type: VIEW; Schema: public; Owner: -
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


--
-- Name: bio_resource_disease_associations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bio_resource_disease_associations ALTER COLUMN id SET DEFAULT nextval('public.bio_resource_disease_associations_id_seq'::regclass);


--
-- Name: bio_resource_natural_products id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bio_resource_natural_products ALTER COLUMN id SET DEFAULT nextval('public.bio_resource_compounds_id_seq'::regclass);


--
-- Name: bio_resources id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bio_resources ALTER COLUMN id SET DEFAULT nextval('public.bio_resources_id_seq'::regclass);


--
-- Name: bioactivity id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bioactivity ALTER COLUMN id SET DEFAULT nextval('public.bioactivity_id_seq'::regclass);


--
-- Name: diseases id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.diseases ALTER COLUMN id SET DEFAULT nextval('public.diseases_id_seq'::regclass);


--
-- Name: natural_products id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.natural_products ALTER COLUMN id SET DEFAULT nextval('public.compounds_id_seq'::regclass);


--
-- Name: prescription_natural_products id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prescription_natural_products ALTER COLUMN id SET DEFAULT nextval('public.prescription_compounds_id_seq'::regclass);


--
-- Name: prescription_resources id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prescription_resources ALTER COLUMN id SET DEFAULT nextval('public.prescription_resources_id_seq'::regclass);


--
-- Name: prescriptions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prescriptions ALTER COLUMN id SET DEFAULT nextval('public.prescriptions_id_seq'::regclass);


--
-- Name: targets id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.targets ALTER COLUMN id SET DEFAULT nextval('public.targets_id_seq'::regclass);


--
-- Name: toxicity id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.toxicity ALTER COLUMN id SET DEFAULT nextval('public.toxicity_id_seq'::regclass);


--
-- Name: bio_resource_natural_products bio_resource_compounds_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bio_resource_natural_products
    ADD CONSTRAINT bio_resource_compounds_pkey PRIMARY KEY (id);


--
-- Name: bio_resource_disease_associations bio_resource_disease_associations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bio_resource_disease_associations
    ADD CONSTRAINT bio_resource_disease_associations_pkey PRIMARY KEY (id);


--
-- Name: bio_resources bio_resources_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bio_resources
    ADD CONSTRAINT bio_resources_pkey PRIMARY KEY (id);


--
-- Name: bio_resources bio_resources_resource_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bio_resources
    ADD CONSTRAINT bio_resources_resource_id_key UNIQUE (resource_id);


--
-- Name: bioactivity bioactivity_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bioactivity
    ADD CONSTRAINT bioactivity_pkey PRIMARY KEY (id);


--
-- Name: natural_products compounds_np_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.natural_products
    ADD CONSTRAINT compounds_np_id_key UNIQUE (np_id);


--
-- Name: natural_products compounds_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.natural_products
    ADD CONSTRAINT compounds_pkey PRIMARY KEY (id);


--
-- Name: diseases diseases_disease_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.diseases
    ADD CONSTRAINT diseases_disease_id_key UNIQUE (disease_id);


--
-- Name: diseases diseases_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.diseases
    ADD CONSTRAINT diseases_pkey PRIMARY KEY (id);


--
-- Name: prescription_natural_products prescription_compounds_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prescription_natural_products
    ADD CONSTRAINT prescription_compounds_pkey PRIMARY KEY (id);


--
-- Name: prescription_resources prescription_resources_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prescription_resources
    ADD CONSTRAINT prescription_resources_pkey PRIMARY KEY (id);


--
-- Name: prescriptions prescriptions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prescriptions
    ADD CONSTRAINT prescriptions_pkey PRIMARY KEY (id);


--
-- Name: prescriptions prescriptions_prescription_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prescriptions
    ADD CONSTRAINT prescriptions_prescription_id_key UNIQUE (prescription_id);


--
-- Name: sys_dict sys_dict_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sys_dict
    ADD CONSTRAINT sys_dict_pkey PRIMARY KEY (dict_code);


--
-- Name: sys_menu sys_menu_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sys_menu
    ADD CONSTRAINT sys_menu_pkey PRIMARY KEY (menu_id);


--
-- Name: targets targets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.targets
    ADD CONSTRAINT targets_pkey PRIMARY KEY (id);


--
-- Name: targets targets_target_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.targets
    ADD CONSTRAINT targets_target_id_key UNIQUE (target_id);


--
-- Name: toxicity toxicity_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.toxicity
    ADD CONSTRAINT toxicity_pkey PRIMARY KEY (id);


--
-- Name: bio_resource_disease_associations uk_bio_resource_disease; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bio_resource_disease_associations
    ADD CONSTRAINT uk_bio_resource_disease UNIQUE (bio_resource_id, disease_id);


--
-- Name: bio_resource_natural_products uk_bio_resource_natural_product; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bio_resource_natural_products
    ADD CONSTRAINT uk_bio_resource_natural_product UNIQUE (bio_resource_id, natural_product_id);


--
-- Name: prescription_natural_products uk_prescription_natural_product; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prescription_natural_products
    ADD CONSTRAINT uk_prescription_natural_product UNIQUE (prescription_id, natural_product_id);


--
-- Name: prescription_resources uk_prescription_resource; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prescription_resources
    ADD CONSTRAINT uk_prescription_resource UNIQUE (prescription_id, bio_resource_id);


--
-- Name: idx_bio_resources_chinese_gin; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bio_resources_chinese_gin ON public.bio_resources USING gin (to_tsvector('simple'::regconfig, (COALESCE(chinese_name, ''::character varying))::text));


--
-- Name: idx_bio_resources_chinese_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bio_resources_chinese_name ON public.bio_resources USING btree (chinese_name);


--
-- Name: idx_bio_resources_cmaup_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bio_resources_cmaup_id ON public.bio_resources USING btree (cmaup_id);


--
-- Name: idx_bio_resources_family; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bio_resources_family ON public.bio_resources USING btree (taxonomy_family);


--
-- Name: idx_bio_resources_family_tax_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bio_resources_family_tax_id ON public.bio_resources USING btree (family_tax_id);


--
-- Name: idx_bio_resources_functions_gin; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bio_resources_functions_gin ON public.bio_resources USING gin (to_tsvector('simple'::regconfig, COALESCE(functions, ''::text)));


--
-- Name: idx_bio_resources_genus; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bio_resources_genus ON public.bio_resources USING btree (taxonomy_genus);


--
-- Name: idx_bio_resources_genus_tax_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bio_resources_genus_tax_id ON public.bio_resources USING btree (genus_tax_id);


--
-- Name: idx_bio_resources_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bio_resources_id ON public.bio_resources USING btree (resource_id);


--
-- Name: idx_bio_resources_latin_gin; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bio_resources_latin_gin ON public.bio_resources USING gin (to_tsvector('english'::regconfig, (COALESCE(latin_name, ''::character varying))::text));


--
-- Name: idx_bio_resources_latin_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bio_resources_latin_name ON public.bio_resources USING btree (latin_name);


--
-- Name: idx_bio_resources_pinyin; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bio_resources_pinyin ON public.bio_resources USING btree (pinyin_name);


--
-- Name: idx_bio_resources_species_tax_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bio_resources_species_tax_id ON public.bio_resources USING btree (species_tax_id);


--
-- Name: idx_bio_resources_tcm_meridian; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bio_resources_tcm_meridian ON public.bio_resources USING btree (tcm_meridian);


--
-- Name: idx_bio_resources_tcm_property; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bio_resources_tcm_property ON public.bio_resources USING btree (tcm_property);


--
-- Name: idx_bio_resources_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bio_resources_type ON public.bio_resources USING btree (resource_type);


--
-- Name: idx_bioactivity_natural_product; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bioactivity_natural_product ON public.bioactivity USING btree (natural_product_id);


--
-- Name: idx_bioactivity_natural_product_target; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bioactivity_natural_product_target ON public.bioactivity USING btree (natural_product_id, target_id);


--
-- Name: idx_bioactivity_ref_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bioactivity_ref_id ON public.bioactivity USING btree (ref_id);


--
-- Name: idx_bioactivity_relation; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bioactivity_relation ON public.bioactivity USING btree (activity_relation);


--
-- Name: idx_bioactivity_target; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bioactivity_target ON public.bioactivity USING btree (target_id);


--
-- Name: idx_bioactivity_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bioactivity_type ON public.bioactivity USING btree (activity_type);


--
-- Name: idx_bioactivity_type_grouped; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bioactivity_type_grouped ON public.bioactivity USING btree (activity_type_grouped);


--
-- Name: idx_bioactivity_type_value_std; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bioactivity_type_value_std ON public.bioactivity USING btree (activity_type, activity_value_std);


--
-- Name: idx_bioactivity_value_std; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bioactivity_value_std ON public.bioactivity USING btree (activity_value_std);


--
-- Name: idx_brda_bio_resource; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_brda_bio_resource ON public.bio_resource_disease_associations USING btree (bio_resource_id);


--
-- Name: idx_brda_confidence; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_brda_confidence ON public.bio_resource_disease_associations USING btree (confidence_score);


--
-- Name: idx_brda_disease; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_brda_disease ON public.bio_resource_disease_associations USING btree (disease_id);


--
-- Name: idx_brnp_bio_resource; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_brnp_bio_resource ON public.bio_resource_natural_products USING btree (bio_resource_id);


--
-- Name: idx_brnp_natural_product; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_brnp_natural_product ON public.bio_resource_natural_products USING btree (natural_product_id);


--
-- Name: idx_diseases_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_diseases_category ON public.diseases USING btree (disease_category);


--
-- Name: idx_diseases_disease_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_diseases_disease_id ON public.diseases USING btree (disease_id);


--
-- Name: idx_diseases_icd11_code; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_diseases_icd11_code ON public.diseases USING btree (icd11_code);


--
-- Name: idx_diseases_name_gin; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_diseases_name_gin ON public.diseases USING gin (to_tsvector('english'::regconfig, (COALESCE(disease_name, ''::character varying))::text));


--
-- Name: idx_natural_products_chembl_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_natural_products_chembl_id ON public.natural_products USING btree (chembl_id);


--
-- Name: idx_natural_products_inchikey; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_natural_products_inchikey ON public.natural_products USING btree (inchikey);


--
-- Name: idx_natural_products_iupac_name_gin; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_natural_products_iupac_name_gin ON public.natural_products USING gin (to_tsvector('english'::regconfig, COALESCE(iupac_name, ''::text)));


--
-- Name: idx_natural_products_mw; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_natural_products_mw ON public.natural_products USING btree (molecular_weight);


--
-- Name: idx_natural_products_np_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_natural_products_np_id ON public.natural_products USING btree (np_id);


--
-- Name: idx_natural_products_num_activity; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_natural_products_num_activity ON public.natural_products USING btree (num_of_activity);


--
-- Name: idx_natural_products_num_target; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_natural_products_num_target ON public.natural_products USING btree (num_of_target);


--
-- Name: idx_natural_products_pref_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_natural_products_pref_name ON public.natural_products USING btree (pref_name);


--
-- Name: idx_natural_products_pref_name_gin; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_natural_products_pref_name_gin ON public.natural_products USING gin (to_tsvector('english'::regconfig, COALESCE(pref_name, (''::character varying)::text)));


--
-- Name: idx_natural_products_psa; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_natural_products_psa ON public.natural_products USING btree (psa);


--
-- Name: idx_natural_products_pubchem_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_natural_products_pubchem_id ON public.natural_products USING btree (pubchem_id);


--
-- Name: idx_natural_products_xlogp; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_natural_products_xlogp ON public.natural_products USING btree (xlogp);


--
-- Name: idx_pnp_natural_product; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_pnp_natural_product ON public.prescription_natural_products USING btree (natural_product_id);


--
-- Name: idx_pnp_prescription; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_pnp_prescription ON public.prescription_natural_products USING btree (prescription_id);


--
-- Name: idx_pr_barcode; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_pr_barcode ON public.prescription_resources USING btree (barcode);


--
-- Name: idx_pr_bio_resource; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_pr_bio_resource ON public.prescription_resources USING btree (bio_resource_id);


--
-- Name: idx_pr_prescription; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_pr_prescription ON public.prescription_resources USING btree (prescription_id);


--
-- Name: idx_pr_role; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_pr_role ON public.prescription_resources USING btree (role);


--
-- Name: idx_pr_tcmid_component; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_pr_tcmid_component ON public.prescription_resources USING btree (tcmid_component_id);


--
-- Name: idx_prescriptions_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_prescriptions_category ON public.prescriptions USING btree (category);


--
-- Name: idx_prescriptions_chinese_gin; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_prescriptions_chinese_gin ON public.prescriptions USING gin (to_tsvector('simple'::regconfig, (COALESCE(chinese_name, ''::character varying))::text));


--
-- Name: idx_prescriptions_chinese_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_prescriptions_chinese_name ON public.prescriptions USING btree (chinese_name);


--
-- Name: idx_prescriptions_dosage_form; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_prescriptions_dosage_form ON public.prescriptions USING btree (dosage_form);


--
-- Name: idx_prescriptions_functions_gin; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_prescriptions_functions_gin ON public.prescriptions USING gin (to_tsvector('simple'::regconfig, COALESCE(functions, ''::text)));


--
-- Name: idx_prescriptions_icd11_gin; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_prescriptions_icd11_gin ON public.prescriptions USING gin (to_tsvector('english'::regconfig, COALESCE(disease_icd11_category, ''::text)));


--
-- Name: idx_prescriptions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_prescriptions_id ON public.prescriptions USING btree (prescription_id);


--
-- Name: idx_prescriptions_indications_gin; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_prescriptions_indications_gin ON public.prescriptions USING gin (to_tsvector('simple'::regconfig, COALESCE(indications, ''::text)));


--
-- Name: idx_prescriptions_pinyin; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_prescriptions_pinyin ON public.prescriptions USING btree (pinyin_name);


--
-- Name: idx_prescriptions_source_book; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_prescriptions_source_book ON public.prescriptions USING btree (source_book);


--
-- Name: idx_targets_ec_number; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_targets_ec_number ON public.targets USING btree (ec_number);


--
-- Name: idx_targets_function_gin; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_targets_function_gin ON public.targets USING gin (to_tsvector('english'::regconfig, COALESCE(function, ''::text)));


--
-- Name: idx_targets_gene_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_targets_gene_name ON public.targets USING btree (gene_name);


--
-- Name: idx_targets_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_targets_name ON public.targets USING btree (target_name);


--
-- Name: idx_targets_name_gin; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_targets_name_gin ON public.targets USING gin (to_tsvector('english'::regconfig, (COALESCE(target_name, ''::character varying))::text));


--
-- Name: idx_targets_organism; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_targets_organism ON public.targets USING btree (target_organism);


--
-- Name: idx_targets_synonyms_gin; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_targets_synonyms_gin ON public.targets USING gin (to_tsvector('english'::regconfig, COALESCE(synonyms, ''::text)));


--
-- Name: idx_targets_target_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_targets_target_id ON public.targets USING btree (target_id);


--
-- Name: idx_targets_ttd_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_targets_ttd_id ON public.targets USING btree (ttd_id);


--
-- Name: idx_targets_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_targets_type ON public.targets USING btree (target_type);


--
-- Name: idx_targets_uniprot; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_targets_uniprot ON public.targets USING btree (uniprot_id);


--
-- Name: idx_toxicity_natural_product; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_toxicity_natural_product ON public.toxicity USING btree (natural_product_id);


--
-- Name: idx_toxicity_ref_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_toxicity_ref_id ON public.toxicity USING btree (ref_id);


--
-- Name: idx_toxicity_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_toxicity_type ON public.toxicity USING btree (toxicity_type);


--
-- Name: v_bio_resource_detail _RETURN; Type: RULE; Schema: public; Owner: -
--

CREATE OR REPLACE VIEW public.v_bio_resource_detail AS
 SELECT br.id,
    br.resource_id,
    br.resource_type,
    br.chinese_name,
    br.latin_name,
    br.english_name,
    br.pinyin_name,
    br.alias,
    br.taxonomy_kingdom,
    br.taxonomy_phylum,
    br.taxonomy_class,
    br.taxonomy_order,
    br.taxonomy_family,
    br.taxonomy_genus,
    br.taxonomy_species,
    br.taxonomy_id,
    br.medicinal_part,
    br.medicinal_part_latin,
    br.origin_region,
    br.distribution,
    br.habitat,
    br.tcm_property,
    br.tcm_flavor,
    br.tcm_meridian,
    br.tcm_toxicity,
    br.functions,
    br.indications,
    br.contraindications,
    br.mineral_composition,
    br.mineral_crystal_system,
    br.mineral_hardness,
    br.mineral_color,
    br.microbe_strain,
    br.microbe_culture_condition,
    br.microbe_fermentation_product,
    br.animal_class,
    br.animal_conservation_status,
    br.tcmid_id,
    br.tcmsp_id,
    br.herb_id,
    br.pharmacopoeia_ref,
    br.literature_ref,
    br.image_url,
    br.num_of_natural_products AS num_of_compounds,
    br.num_of_prescriptions,
    br.created_at,
    br.updated_at,
    count(DISTINCT brnp.natural_product_id) AS natural_product_count,
    count(DISTINCT pr.prescription_id) AS prescription_count
   FROM ((public.bio_resources br
     LEFT JOIN public.bio_resource_natural_products brnp ON ((br.id = brnp.bio_resource_id)))
     LEFT JOIN public.prescription_resources pr ON ((br.id = pr.bio_resource_id)))
  GROUP BY br.id;


--
-- Name: v_prescription_detail _RETURN; Type: RULE; Schema: public; Owner: -
--

CREATE OR REPLACE VIEW public.v_prescription_detail AS
 SELECT p.id,
    p.prescription_id,
    p.chinese_name,
    p.pinyin_name,
    p.english_name,
    p.alias,
    p.source_book,
    p.source_dynasty,
    p.source_author,
    p.category,
    p.subcategory,
    p.functions,
    p.indications,
    p.indications_modern,
    p.syndrome,
    p.composition_text,
    p.dosage_form,
    p.preparation_method,
    p.usage_method,
    p.dosage,
    p.contraindications,
    p.precautions,
    p.adverse_reactions,
    p.pharmacology,
    p.clinical_application,
    p.target_tissues,
    p.related_diseases,
    p.tcmid_id,
    p.tcmsp_id,
    p.symmap_id,
    p.pharmacopoeia_ref,
    p.literature_ref,
    p.num_of_herbs,
    p.num_of_natural_products AS num_of_compounds,
    p.created_at,
    p.updated_at,
    count(DISTINCT pr.bio_resource_id) AS herb_count,
    count(DISTINCT pnp.natural_product_id) AS direct_natural_product_count
   FROM ((public.prescriptions p
     LEFT JOIN public.prescription_resources pr ON ((p.id = pr.prescription_id)))
     LEFT JOIN public.prescription_natural_products pnp ON ((p.id = pnp.prescription_id)))
  GROUP BY p.id;


--
-- Name: v_natural_product_detail _RETURN; Type: RULE; Schema: public; Owner: -
--

CREATE OR REPLACE VIEW public.v_natural_product_detail AS
 SELECT np.id,
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
    np.gene_cluster,
    np.if_quantity,
    np.created_at,
    np.updated_at,
    count(DISTINCT b.id) AS bioactivity_count,
    count(DISTINCT b.target_id) AS target_count,
    count(DISTINCT brnp.bio_resource_id) AS bio_resource_count,
    min(b.activity_value_std) AS best_activity_value,
    (EXISTS ( SELECT 1
           FROM public.toxicity t
          WHERE (t.natural_product_id = np.id))) AS has_toxicity
   FROM ((public.natural_products np
     LEFT JOIN public.bioactivity b ON ((np.id = b.natural_product_id)))
     LEFT JOIN public.bio_resource_natural_products brnp ON ((np.id = brnp.natural_product_id)))
  GROUP BY np.id;


--
-- Name: v_target_detail _RETURN; Type: RULE; Schema: public; Owner: -
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
-- Name: bio_resources update_bio_resources_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER update_bio_resources_updated_at BEFORE UPDATE ON public.bio_resources FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: diseases update_diseases_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER update_diseases_updated_at BEFORE UPDATE ON public.diseases FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: natural_products update_natural_products_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER update_natural_products_updated_at BEFORE UPDATE ON public.natural_products FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: prescriptions update_prescriptions_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER update_prescriptions_updated_at BEFORE UPDATE ON public.prescriptions FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: targets update_targets_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER update_targets_updated_at BEFORE UPDATE ON public.targets FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: bioactivity fk_bioactivity_natural_product; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bioactivity
    ADD CONSTRAINT fk_bioactivity_natural_product FOREIGN KEY (natural_product_id) REFERENCES public.natural_products(id) ON DELETE CASCADE;


--
-- Name: bioactivity fk_bioactivity_target; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bioactivity
    ADD CONSTRAINT fk_bioactivity_target FOREIGN KEY (target_id) REFERENCES public.targets(id) ON DELETE CASCADE;


--
-- Name: bio_resource_disease_associations fk_brda_bio_resource; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bio_resource_disease_associations
    ADD CONSTRAINT fk_brda_bio_resource FOREIGN KEY (bio_resource_id) REFERENCES public.bio_resources(id) ON DELETE CASCADE;


--
-- Name: bio_resource_disease_associations fk_brda_disease; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bio_resource_disease_associations
    ADD CONSTRAINT fk_brda_disease FOREIGN KEY (disease_id) REFERENCES public.diseases(id) ON DELETE CASCADE;


--
-- Name: bio_resource_natural_products fk_brnp_bio_resource; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bio_resource_natural_products
    ADD CONSTRAINT fk_brnp_bio_resource FOREIGN KEY (bio_resource_id) REFERENCES public.bio_resources(id) ON DELETE CASCADE;


--
-- Name: bio_resource_natural_products fk_brnp_natural_product; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bio_resource_natural_products
    ADD CONSTRAINT fk_brnp_natural_product FOREIGN KEY (natural_product_id) REFERENCES public.natural_products(id) ON DELETE CASCADE;


--
-- Name: prescription_natural_products fk_pnp_natural_product; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prescription_natural_products
    ADD CONSTRAINT fk_pnp_natural_product FOREIGN KEY (natural_product_id) REFERENCES public.natural_products(id) ON DELETE CASCADE;


--
-- Name: prescription_natural_products fk_pnp_prescription; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prescription_natural_products
    ADD CONSTRAINT fk_pnp_prescription FOREIGN KEY (prescription_id) REFERENCES public.prescriptions(id) ON DELETE CASCADE;


--
-- Name: prescription_natural_products fk_pnp_source_resource; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prescription_natural_products
    ADD CONSTRAINT fk_pnp_source_resource FOREIGN KEY (source_resource_id) REFERENCES public.bio_resources(id) ON DELETE SET NULL;


--
-- Name: prescription_resources fk_pr_bio_resource; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prescription_resources
    ADD CONSTRAINT fk_pr_bio_resource FOREIGN KEY (bio_resource_id) REFERENCES public.bio_resources(id) ON DELETE CASCADE;


--
-- Name: prescription_resources fk_pr_prescription; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prescription_resources
    ADD CONSTRAINT fk_pr_prescription FOREIGN KEY (prescription_id) REFERENCES public.prescriptions(id) ON DELETE CASCADE;


--
-- Name: toxicity fk_toxicity_natural_product; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.toxicity
    ADD CONSTRAINT fk_toxicity_natural_product FOREIGN KEY (natural_product_id) REFERENCES public.natural_products(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

