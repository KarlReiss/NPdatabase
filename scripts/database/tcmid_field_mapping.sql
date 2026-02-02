-- ============================================================================
-- TCMID 数据到数据库表的字段映射文档
-- ============================================================================
-- 文件: tcmid_field_mapping.sql
-- 描述: TCMID 数据字段与数据库表字段的完整映射关系
-- 日期: 2026-01-29
-- ============================================================================

-- ============================================================================
-- 1. TCMID prescription_basic_info.csv -> prescriptions 表
-- ============================================================================

/*
TCMID 字段                    数据库字段                    说明
---------------------------------------------------------------------------
PrescriptionID            -> prescription_id           处方唯一标识符（TCMF1, TCMF2等）
PinyinName                -> pinyin_name               处方拼音名称
ChineseName               -> chinese_name              处方中文名称
EnglishName               -> english_name              处方英文名称
FunctionDescription       -> functions                 功能描述（功效）
Indications               -> indications               适应症
DiseaseICD11Category      -> disease_icd11_category    ICD-11疾病分类编码（多个用分号分隔）
HumanTissues              -> human_tissues             相关人体组织
Reference                 -> reference                 参考文献
ReferenceBook             -> reference_book            参考书籍

示例数据:
PrescriptionID: TCMF1
PinyinName: San Niu Pian
ChineseName: 三拗片
EnglishName: San Niu Tablets
FunctionDescription: 风寒袭肺证, 证见咳嗽声重, 咳嗽痰多, 痰白清稀; 急性支气管炎病情轻者见上述症候者
Indications: Acute bronchitis
DiseaseICD11Category: CA42 [Acute bronchitis, 急性支气管炎 ];
HumanTissues: (空)
Reference: Chinese pharmacopoeia (2015)
ReferenceBook: (空)
*/

-- ============================================================================
-- 2. TCMID prescription_herbs.csv -> prescription_resources 表
-- ============================================================================

/*
TCMID 字段                    数据库字段                    说明
---------------------------------------------------------------------------
PrescriptionID            -> prescription_id           处方ID（通过外键关联到prescriptions表）
ComponentID               -> tcmid_component_id        TCMID药材组分ID（如 TCMH1398）
                          -> bio_resource_id           匹配后的生物资源ID（外键）
LatinName                 -> latin_name                药材拉丁名（用于匹配和验证）
ChineseName               -> chinese_name              药材中文名（用于匹配和验证）
ComponentQuantity         -> dosage_text               药材用量文本
Barcode                   -> barcode                   TCMID药材条形码（如 ITSAM882-14）

示例数据:
PrescriptionID: TCMF1
ComponentID: TCMH1398
LatinName: Ephedra sinica
ChineseName: 麻黄
ComponentQuantity: TCMH1398
Barcode: ITSAM882-14

注意:
1. bio_resource_id 需要通过匹配算法从 bio_resources 表中查找
2. 匹配优先级: 拉丁名精确匹配 > 中文名精确匹配 > 拉丁名模糊匹配 > 创建新记录
3. latin_name 和 chinese_name 保留TCMID原始数据，便于后续验证和追溯
*/

-- ============================================================================
-- 3. 数据导入流程
-- ============================================================================

/*
步骤1: 导入处方基本信息
- 读取 prescription_basic_info.csv
- 插入到 prescriptions 表
- prescription_id 使用 TCMID 的 PrescriptionID（如 TCMF1）

步骤2: 匹配药材到生物资源
- 读取 prescription_herbs.csv
- 对每个药材，按优先级匹配到 bio_resources:
  a. 拉丁名精确匹配: WHERE LOWER(latin_name) = LOWER('Ephedra sinica')
  b. 中文名精确匹配: WHERE chinese_name = '麻黄'
  c. 拉丁名模糊匹配: WHERE latin_name LIKE 'Ephedra%'
  d. 创建新记录: 如果完全无法匹配

步骤3: 导入处方-药材关联
- 插入到 prescription_resources 表
- 记录匹配结果和原始TCMID数据
*/

-- ============================================================================
-- 4. 数据验证查询
-- ============================================================================

-- 查看处方总数
-- SELECT COUNT(*) FROM prescriptions WHERE prescription_id LIKE 'TCMF%';

-- 查看处方详情（包含ICD-11编码）
-- SELECT prescription_id, chinese_name, english_name,
--        disease_icd11_category, reference
-- FROM prescriptions
-- WHERE prescription_id = 'TCMF1';

-- 查看处方的药材组成
-- SELECT p.prescription_id, p.chinese_name as prescription_name,
--        pr.tcmid_component_id, pr.latin_name, pr.chinese_name as herb_name,
--        pr.dosage_text, pr.barcode,
--        br.resource_id, br.latin_name as matched_latin_name
-- FROM prescriptions p
-- JOIN prescription_resources pr ON p.id = pr.prescription_id
-- LEFT JOIN bio_resources br ON pr.bio_resource_id = br.id
-- WHERE p.prescription_id = 'TCMF1'
-- ORDER BY pr.sort_order;

-- 查看未匹配到生物资源的药材
-- SELECT DISTINCT pr.tcmid_component_id, pr.latin_name, pr.chinese_name
-- FROM prescription_resources pr
-- WHERE pr.bio_resource_id IS NULL;

-- 统计每个处方的药材数量
-- SELECT p.prescription_id, p.chinese_name, COUNT(pr.id) as herb_count
-- FROM prescriptions p
-- LEFT JOIN prescription_resources pr ON p.id = pr.prescription_id
-- WHERE p.prescription_id LIKE 'TCMF%'
-- GROUP BY p.prescription_id, p.chinese_name
-- ORDER BY p.prescription_id;
