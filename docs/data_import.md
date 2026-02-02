# 天然产物数据库数据补充方案

## 需求概述

用户需要补充和增强数据库中的数据，具体包括：

1. **TCMID处方数据**: 添加中医处方信息，包括处方基本信息和药材组成，需要将药材与现有天然产物进行匹配
2. **TTD靶点数据**: 补充现有靶点的详细信息（当前靶点信息过于单薄）
3. **CMAUP植物数据**: 补充生物资源的分类学信息
4. **CMAUP疾病关联数据**: 添加植物-疾病关联信息

---

## 数据源分析

### 1. TCMID处方数据

**数据文件**:
- `/home/yfguo/NPdatabase/data/TCMID/prescription_basic_info.csv`
- `/home/yfguo/NPdatabase/data/TCMID/prescription_herbs.csv`

**prescription_basic_info.csv 结构**:
```
PrescriptionID, PinyinName, ChineseName, EnglishName, FunctionDescription,
Indications, DiseaseICD11Category, HumanTissues, Reference, ReferenceBook
```

**prescription_herbs.csv 结构**:
```
PrescriptionID, ComponentID, LatinName, ChineseName, ComponentQuantity, Barcode
```

**关键特点**:
- 包含ICD-11疾病分类代码
- 药材有拉丁名和中文名
- 需要将药材匹配到现有的 bio_resources 或 natural_products

---

### 2. TTD靶点数据

**数据文件**:
- `/home/yfguo/NPdatabase/data/TTD/TTD_target_basic_info.csv`

**数据结构**:
```
TARGETID, FORMERID, UNIPROID, TARGNAME, GENENAME, TARGTYPE, SYNONYMS,
FUNCTION, PDBSTRUC, BIOCLASS, ECNUMBER, SEQUENCE
```

**关键特点**:
- 包含UniProt ID、基因名、蛋白序列
- 包含功能描述、PDB结构ID
- 包含生物分类、EC编号
- 包含同义词信息

**现有targets表字段** (来自schema.sql):
```sql
target_id, target_type, target_name, target_organism,
target_organism_tax_id, uniprot_id
```

**需要补充的字段**:
- gene_name (基因名)
- synonyms (同义词)
- function (功能描述)
- pdb_structure (PDB结构ID)
- bioclass (生物分类)
- ec_number (EC编号)
- sequence (蛋白序列)

---

### 3. CMAUP植物数据

**数据文件**:
- `/home/yfguo/NPdatabase/data/CMAUP/CMAUPv2.0_download_Plants.txt`

**数据结构** (Tab分隔):
```
Plant_ID, Plant_Name, Species_Tax_ID, Species_Name,
Genus_Tax_ID, Genus_Name, Family_Tax_ID, Family_Name
```

**关键特点**:
- 包含完整的分类学层级（科、属、种）
- 包含Taxonomy ID
- 可以补充到 bio_resources 表

**现有bio_resources表相关字段**:
```sql
taxonomy_family, taxonomy_genus, taxonomy_species, taxonomy_id
```

**需要补充**:
- species_tax_id (种的Taxonomy ID)
- genus_tax_id (属的Taxonomy ID)
- family_tax_id (科的Taxonomy ID)

---

### 4. CMAUP疾病关联数据

**数据文件**:
- `/home/yfguo/NPdatabase/data/CMAUP/CMAUPv2.0_download_Plant_Human_Disease_Associations.txt`

**数据结构** (Tab分隔):
```
Plant_ID, ICD-11 Code, Disease_Category, Disease,
Association_by_Therapeutic_Target, Association_by_Disease_Transcriptiome_Reversion,
Association_by_Clinical_Trials_of_Plant, Association_by_Clinical_Trials_of_Plant_Ingredients
```

**关键特点**:
- 使用ICD-11疾病编码
- 包含4种证据类型（靶点、转录组、临床试验）
- 需要创建新的 diseases 表和关联表

---

## 数据库设计方案

### 方案1: 增强现有表 + 新增表

#### 1.1 增强 targets 表

**新增字段**:
```sql
ALTER TABLE targets ADD COLUMN IF NOT EXISTS gene_name VARCHAR(100);
ALTER TABLE targets ADD COLUMN IF NOT EXISTS synonyms TEXT;
ALTER TABLE targets ADD COLUMN IF NOT EXISTS function TEXT;
ALTER TABLE targets ADD COLUMN IF NOT EXISTS pdb_structure VARCHAR(500);
ALTER TABLE targets ADD COLUMN IF NOT EXISTS bioclass VARCHAR(200);
ALTER TABLE targets ADD COLUMN IF NOT EXISTS ec_number VARCHAR(50);
ALTER TABLE targets ADD COLUMN IF NOT EXISTS sequence TEXT;
ALTER TABLE targets ADD COLUMN IF NOT EXISTS ttd_id VARCHAR(50);

-- 添加索引
CREATE INDEX IF NOT EXISTS idx_targets_gene_name ON targets(gene_name);
CREATE INDEX IF NOT EXISTS idx_targets_ttd_id ON targets(ttd_id);
CREATE INDEX IF NOT EXISTS idx_targets_ec_number ON targets(ec_number);

-- 全文搜索索引
CREATE INDEX IF NOT EXISTS idx_targets_function_gin
ON targets USING gin(to_tsvector('english', COALESCE(function, '')));
CREATE INDEX IF NOT EXISTS idx_targets_synonyms_gin
ON targets USING gin(to_tsvector('english', COALESCE(synonyms, '')));
```

---

#### 1.2 增强 bio_resources 表

**新增字段**:
```sql
ALTER TABLE bio_resources ADD COLUMN IF NOT EXISTS species_tax_id VARCHAR(50);
ALTER TABLE bio_resources ADD COLUMN IF NOT EXISTS genus_tax_id VARCHAR(50);
ALTER TABLE bio_resources ADD COLUMN IF NOT EXISTS family_tax_id VARCHAR(50);
ALTER TABLE bio_resources ADD COLUMN IF NOT EXISTS cmaup_id VARCHAR(50);

-- 添加索引
CREATE INDEX IF NOT EXISTS idx_bio_resources_species_tax_id ON bio_resources(species_tax_id);
CREATE INDEX IF NOT EXISTS idx_bio_resources_genus_tax_id ON bio_resources(genus_tax_id);
CREATE INDEX IF NOT EXISTS idx_bio_resources_family_tax_id ON bio_resources(family_tax_id);
CREATE INDEX IF NOT EXISTS idx_bio_resources_cmaup_id ON bio_resources(cmaup_id);
```

---

#### 1.3 新增 diseases 表

**表结构**:
```sql
CREATE TABLE diseases (
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
CREATE INDEX idx_diseases_disease_id ON diseases(disease_id);
CREATE INDEX idx_diseases_icd11_code ON diseases(icd11_code);
CREATE INDEX idx_diseases_category ON diseases(disease_category);
CREATE INDEX idx_diseases_name_gin ON diseases
    USING gin(to_tsvector('english', COALESCE(disease_name, '')));

COMMENT ON TABLE diseases IS '疾病表 - 存储疾病信息（基于ICD-11分类）';
```

---

#### 1.4 新增 bio_resource_disease_associations 表

**表结构**:
```sql
CREATE TABLE bio_resource_disease_associations (
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
CREATE INDEX idx_brda_bio_resource ON bio_resource_disease_associations(bio_resource_id);
CREATE INDEX idx_brda_disease ON bio_resource_disease_associations(disease_id);
CREATE INDEX idx_brda_confidence ON bio_resource_disease_associations(confidence_score);

COMMENT ON TABLE bio_resource_disease_associations IS '生物资源-疾病关联表 - 记录植物与疾病的关联及证据';
```

---

#### 1.5 处方表已存在

根据 `add_prescription_bioresource.sql`，处方相关表已经创建：
- `prescriptions` - 处方表
- `prescription_resources` - 处方-生物资源关联表
- `prescription_natural_products` - 处方-天然产物关联表

**需要确认**:
- 表结构是否与TCMID数据匹配
- 是否需要调整字段

---

## 数据匹配策略

### 策略1: 药材匹配到生物资源

**TCMID药材 → bio_resources 匹配规则**:

1. **优先级1**: 拉丁名精确匹配
   ```sql
   SELECT id FROM bio_resources
   WHERE LOWER(latin_name) = LOWER('Ephedra sinica')
   ```

2. **优先级2**: 中文名精确匹配
   ```sql
   SELECT id FROM bio_resources
   WHERE chinese_name = '麻黄'
   ```

3. **优先级3**: 拉丁名模糊匹配（属名匹配）
   ```sql
   SELECT id FROM bio_resources
   WHERE latin_name LIKE 'Ephedra%'
   ```

4. **优先级4**: 创建新的bio_resource记录
   - 如果完全无法匹配，创建新记录
   - 标记来源为 'TCMID'

**匹配结果记录**:
- 创建匹配日志表记录匹配情况
- 记录匹配方式、置信度

---

### 策略2: TTD靶点匹配到现有靶点

**TTD靶点 → targets 匹配规则**:

1. **优先级1**: UniProt ID精确匹配
   ```sql
   SELECT id FROM targets
   WHERE uniprot_id = 'P11362'
   ```

2. **优先级2**: 靶点名称精确匹配
   ```sql
   SELECT id FROM targets
   WHERE LOWER(target_name) = LOWER('Fibroblast growth factor receptor 1')
   ```

3. **优先级3**: 基因名匹配（需要先添加gene_name字段）
   ```sql
   SELECT id FROM targets
   WHERE gene_name = 'FGFR1'
   ```

4. **优先级4**: 创建新的target记录
   - 如果完全无法匹配，创建新记录
   - 标记来源为 'TTD'

---

### 策略3: CMAUP植物匹配到生物资源

**CMAUP植物 → bio_resources 匹配规则**:

1. **优先级1**: 拉丁名精确匹配
   ```sql
   SELECT id FROM bio_resources
   WHERE LOWER(latin_name) = LOWER('Eucalyptus apodophylla')
   ```

2. **优先级2**: 属名 + 科名匹配
   ```sql
   SELECT id FROM bio_resources
   WHERE taxonomy_genus = 'Eucalyptus'
   AND taxonomy_family = 'Myrtaceae'
   ```

3. **优先级3**: 仅属名匹配（需要人工确认）
   ```sql
   SELECT id FROM bio_resources
   WHERE taxonomy_genus = 'Eucalyptus'
   ```

4. **补充策略**:
   - 匹配成功后，补充 taxonomy ID 信息
   - 不创建新记录，仅补充现有记录

---

## 数据导入流程

### 阶段1: 数据库结构调整

**步骤1.1**: 创建数据库变更脚本
- 文件: `/scripts/database/enhance_schema_for_enrichment.sql`
- 内容: 包含所有ALTER TABLE和CREATE TABLE语句

**步骤1.2**: 执行数据库变更
```bash
psql -U postgres -d npdb -f scripts/database/enhance_schema_for_enrichment.sql
```

**步骤1.3**: 验证表结构
```bash
psql -U postgres -d npdb -c "\d targets"
psql -U postgres -d npdb -c "\d bio_resources"
psql -U postgres -d npdb -c "\d diseases"
```

---

### 阶段2: 数据清洗与转换

**步骤2.1**: TTD靶点数据清洗
- 文件: `/scripts/data-import/clean_ttd_targets.py`
- 功能:
  - 读取 TTD_target_basic_info.csv
  - 清洗数据（去除空值、标准化格式）
  - 生成中间JSON文件

**步骤2.2**: TCMID处方数据清洗
- 文件: `/scripts/data-import/clean_tcmid_prescriptions.py`
- 功能:
  - 读取 prescription_basic_info.csv 和 prescription_herbs.csv
  - 解析ICD-11编码
  - 生成中间JSON文件

**步骤2.3**: CMAUP数据清洗
- 文件: `/scripts/data-import/clean_cmaup_data.py`
- 功能:
  - 读取 Plants.txt 和 Plant_Human_Disease_Associations.txt
  - 清洗数据
  - 生成中间JSON文件

---

### 阶段3: 数据匹配

**步骤3.1**: TTD靶点匹配
- 文件: `/scripts/data-import/match_ttd_targets.py`
- 功能:
  - 根据匹配策略匹配TTD靶点到现有targets
  - 生成匹配报告（匹配率、未匹配列表）
  - 生成更新SQL或JSON

**步骤3.2**: TCMID药材匹配
- 文件: `/scripts/data-import/match_tcmid_herbs.py`
- 功能:
  - 根据匹配策略匹配药材到bio_resources
  - 生成匹配报告
  - 对于无法匹配的药材，生成新建bio_resource的SQL

**步骤3.3**: CMAUP植物匹配
- 文件: `/scripts/data-import/match_cmaup_plants.py`
- 功能:
  - 匹配CMAUP植物到bio_resources
  - 生成taxonomy ID补充SQL

---

### 阶段4: 数据导入

**步骤4.1**: 导入TTD靶点补充数据
- 文件: `/scripts/data-import/import_ttd_target_enrichment.py`
- 功能:
  - 更新现有targets记录（补充字段）
  - 插入新的targets记录（如果需要）
  - 记录导入日志

**步骤4.2**: 导入TCMID处方数据
- 文件: `/scripts/data-import/import_tcmid_prescriptions.py`
- 功能:
  - 插入prescriptions记录
  - 插入prescription_resources关联
  - 插入prescription_natural_products关联（如果有）
  - 创建新的bio_resources（对于未匹配的药材）

**步骤4.3**: 导入CMAUP植物补充数据
- 文件: `/scripts/data-import/import_cmaup_plant_enrichment.py`
- 功能:
  - 更新bio_resources的taxonomy ID字段

**步骤4.4**: 导入CMAUP疾病数据
- 文件: `/scripts/data-import/import_cmaup_diseases.py`
- 功能:
  - 插入diseases记录（去重）
  - 插入bio_resource_disease_associations记录
  - 计算置信度评分

---

### 阶段5: 数据验证

**步骤5.1**: 数据完整性验证
- 文件: `/scripts/data-import/validate_enrichment.py`
- 验证内容:
  - 外键完整性
  - 数据量统计
  - 匹配率统计
  - 数据质量检查（空值、异常值）

**步骤5.2**: 生成导入报告
- 文件: `/scripts/data-import/generate_enrichment_report.py`
- 报告内容:
  - 各表新增记录数
  - 匹配成功率
  - 未匹配数据列表
  - 数据质量问题列表

---

## 实施计划

### 第1天: 数据库结构调整

**任务**:
1. 创建 `enhance_schema_for_enrichment.sql` 脚本
2. 执行数据库变更
3. 验证表结构

**交付物**:
- SQL脚本文件
- 表结构验证报告

---

### 第2天: 数据清洗脚本开发

**任务**:
1. 开发 TTD 数据清洗脚本
2. 开发 TCMID 数据清洗脚本
3. 开发 CMAUP 数据清洗脚本
4. 测试清洗脚本

**交付物**:
- 3个Python清洗脚本
- 清洗后的中间JSON文件

---

### 第3天: 数据匹配脚本开发

**任务**:
1. 开发 TTD 靶点匹配脚本
2. 开发 TCMID 药材匹配脚本
3. 开发 CMAUP 植物匹配脚本
4. 生成匹配报告

**交付物**:
- 3个Python匹配脚本
- 匹配报告（匹配率、未匹配列表）

---

### 第4天: 数据导入脚本开发

**任务**:
1. 开发 TTD 靶点导入脚本
2. 开发 TCMID 处方导入脚本
3. 开发 CMAUP 数据导入脚本
4. 测试导入脚本（小批量）

**交付物**:
- 4个Python导入脚本
- 小批量测试结果

---

### 第5天: 全量导入与验证

**任务**:
1. 执行全量数据导入
2. 运行数据验证脚本
3. 生成导入报告
4. 修复数据质量问题

**交付物**:
- 完整的数据导入
- 验证报告
- 导入总结报告

---

## 关键文件清单

### 数据库脚本
- `/scripts/database/enhance_schema_for_enrichment.sql` - 数据库结构增强脚本

### 数据清洗脚本
- `/scripts/data-import/clean_ttd_targets.py` - TTD靶点数据清洗
- `/scripts/data-import/clean_tcmid_prescriptions.py` - TCMID处方数据清洗
- `/scripts/data-import/clean_cmaup_data.py` - CMAUP数据清洗

### 数据匹配脚本
- `/scripts/data-import/match_ttd_targets.py` - TTD靶点匹配
- `/scripts/data-import/match_tcmid_herbs.py` - TCMID药材匹配
- `/scripts/data-import/match_cmaup_plants.py` - CMAUP植物匹配

### 数据导入脚本
- `/scripts/data-import/import_ttd_target_enrichment.py` - TTD靶点导入
- `/scripts/data-import/import_tcmid_prescriptions.py` - TCMID处方导入
- `/scripts/data-import/import_cmaup_plant_enrichment.py` - CMAUP植物补充导入
- `/scripts/data-import/import_cmaup_diseases.py` - CMAUP疾病导入

### 验证脚本
- `/scripts/data-import/validate_enrichment.py` - 数据验证
- `/scripts/data-import/generate_enrichment_report.py` - 报告生成

---

## 数据质量保证

### 1. 匹配质量控制

**目标匹配率**:
- TTD靶点匹配率: ≥ 80%
- TCMID药材匹配率: ≥ 70%
- CMAUP植物匹配率: ≥ 85%

**质量检查点**:
- 匹配置信度评分
- 人工抽样验证（10%样本）
- 未匹配数据人工审核

---

### 2. 数据完整性检查

**检查项**:
- 外键完整性（所有关联ID有效）
- 必填字段非空
- 数据格式正确（ICD-11编码、UniProt ID等）
- 无重复记录

---

### 3. 数据一致性检查

**检查项**:
- 统计字段与实际关联数一致
- 视图数据与表数据一致
- 跨表数据逻辑一致

---

## 风险评估

### 低风险
- 新增表（diseases, bio_resource_disease_associations）
- 新增字段（不影响现有功能）
- 数据清洗脚本（只读操作）

### 中风险
- 数据匹配（可能匹配错误）
  - 缓解措施: 人工抽样验证、匹配置信度评分
- 大量数据导入（可能影响性能）
  - 缓解措施: 分批导入、在非高峰时段执行

### 高风险
- 更新现有记录（targets, bio_resources）
  - 缓解措施: 数据库备份、先在测试环境验证
- 创建新bio_resources记录（可能重复）
  - 缓解措施: 严格的去重逻辑、人工审核

---

## 验证方案

### 数据库验证

```sql
-- 1. 检查新增字段
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'targets'
AND column_name IN ('gene_name', 'synonyms', 'function');

-- 2. 检查新增表
SELECT COUNT(*) FROM diseases;
SELECT COUNT(*) FROM bio_resource_disease_associations;

-- 3. 检查数据完整性
SELECT COUNT(*) FROM targets WHERE gene_name IS NOT NULL;
SELECT COUNT(*) FROM bio_resources WHERE species_tax_id IS NOT NULL;

-- 4. 检查关联完整性
SELECT COUNT(*) FROM bio_resource_disease_associations brda
LEFT JOIN bio_resources br ON brda.bio_resource_id = br.id
WHERE br.id IS NULL;  -- 应该为0
```

### 匹配质量验证

```python
# 生成匹配报告
python scripts/data-import/generate_enrichment_report.py

# 报告内容应包括:
# - TTD靶点匹配率: X%
# - TCMID药材匹配率: X%
# - CMAUP植物匹配率: X%
# - 未匹配数据列表
```

### 端到端验证

1. **靶点详情页验证**
   - 访问靶点详情页
   - 验证新增字段显示（基因名、功能描述等）
   - 验证数据完整性

2. **生物资源详情页验证**
   - 访问生物资源详情页
   - 验证taxonomy ID显示
   - 验证疾病关联显示

3. **处方列表页验证**
   - 访问处方列表页
   - 验证处方数据显示
   - 验证处方-药材关联

---

## 总结

本方案采用**分阶段、可控**的数据补充策略：

1. **数据库层**: 增强现有表 + 新增疾病表
2. **数据处理层**: 清洗 → 匹配 → 导入
3. **质量保证层**: 匹配验证 + 数据验证 + 人工审核

**预期成果**:
- 靶点信息完整度提升 80%+
- 新增处方数据 1000+ 条
- 新增疾病关联数据 10000+ 条
- 生物资源分类学信息完整度提升 90%+

**实施周期**: 5个工作日

**关键成功因素**:
- 高质量的数据匹配算法
- 完善的数据验证机制
- 充分的数据库备份
