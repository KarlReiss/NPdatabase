# PubChem CID 123631 数据提取测试报告

**测试日期**: 2026-02-25  
**化合物**: Gefitinib (吉非替尼) - 抗肿瘤药物

---

## ✅ 测试结果汇总

| 类别 | API | 状态 | 备注 |
|------|-----|------|------|
| 计算属性 | PUG REST | ✅ 成功 | 15个字段全部获取 |
| 实验属性 | PUG View | ✅ 成功 | 物理描述、溶解度、解离常数 |
| 同义词 | PUG View | ✅ 成功 | 包含 CAS 号 (184475-35-2) |
| 化学分类 | PUG View | ✅ 成功 | 药物分类 |
| 安全与毒性 | PUG View | ✅ 成功 | 肝毒性、药物性肝损伤 |
| 药理信息 | PUG View | ✅ 成功 | 药代动力学、作用机制等 |
| 光谱数据 | PUG View | ✅ 成功 | NMR、质谱 |
| 蛋白靶点 | PUG View | ✅ 成功 | 10个蛋白结构 (PDB) |
| 药物信息 | PUG View | ✅ 成功 | FDA批准、临床试验等 |
| 疾病关联 | PUG View | ⚠️ 无数据 | 该化合物无此部分 |

---

## 一、计算属性 (PUG REST)

```json
{
  "CID": 123631,
  "MolecularFormula": "C22H24ClFN4O3",
  "MolecularWeight": "446.9",
  "IUPACName": "N-(3-chloro-4-fluorophenyl)-7-methoxy-6-(3-morpholin-4-ylpropoxy)quinazolin-4-amine",
  "InChI": "InChI=1S/C22H24ClFN4O3/c1-29-20-13-19-16(12-21(20)31-8-2-5-28-6-9-30-10-7-28)22(26-14-25-19)27-15-3-4-18(24)17(23)11-15/h3-4,11-14H,2,5-10H2,1H3,(H,25,26,27)",
  "InChIKey": "XGALLCVXEZPNRQ-UHFFFAOYSA-N",
  "CanonicalSMILES": "COC1=C(C=C2C(=C1)N=CN=C2NC3=CC(=C(C=C3)F)Cl)OCCCN4CCOCC4",
  "XLogP": 4.1,
  "TPSA": 68.7,
  "HBondDonorCount": 1,
  "HBondAcceptorCount": 8,
  "RotatableBondCount": 8,
  "HeavyAtomCount": 31,
  "ExactMass": "446.1520965",
  "MonoisotopicMass": "446.1520965",
  "Complexity": 545,
  "Charge": 0
}
```

### 字段映射到数据库

| PubChem 字段 | 数据库字段 | 值 | 提取状态 |
|--------------|-----------|-----|---------|
| CID | pubchem_id | 123631 | ✅ |
| MolecularFormula | formula | C22H24ClFN4O3 | ✅ |
| MolecularWeight | molecular_weight | 446.9 | ✅ |
| IUPACName | iupac_name | N-(3-chloro... | ✅ |
| InChIKey | inchikey | XGALLCVXEZPNRQ... | ✅ |
| InChI | inchi | InChI=1S/... | ✅ |
| CanonicalSMILES | smiles | COC1=C(C=C2... | ✅ |
| XLogP | xlogp | 4.1 | ✅ |
| TPSA | tpsa | 68.7 | ✅ |
| HBondDonorCount | h_bond_donors | 1 | ✅ |
| HBondAcceptorCount | h_bond_acceptors | 8 | ✅ |
| RotatableBondCount | rotatable_bonds | 8 | ✅ |
| HeavyAtomCount | heavy_atom_count (新) | 31 | ✅ |
| ExactMass | exact_mass (新) | 446.1520965 | ✅ |
| Complexity | complexity (新) | 545 | ✅ |

---

## 二、实验属性 (PUG View)

| 属性 | 值 | 单位 | 来源 |
|------|-----|------|------|
| Physical Description | Solid | - | - |
| Solubility | Sparingly soluble (<pH4) | - | - |
| Dissociation Constants | 5.4 and 7.2 | - | FDA label |

### 新增数据库字段建议

| 字段 | 数据库字段 | 值 | 提取状态 |
|------|-----------|-----|---------|
| Physical State | physical_state (新) | Solid | ✅ |
| Solubility | solubility (新) | Sparingly soluble (<pH4) | ✅ |
| Dissociation Constants | pka (新) | 5.4, 7.2 | ✅ |

---

## 三、同义词 (PUG View)

提取到的同义词（部分）：
- Gefitinib
- ZD1839
- Iressa
- **CAS: 184475-35-2**
- CHEMBL939
- CHEBI:49668
- NSC-759856
- DTXSID8041034

### 新增数据库字段

| 字段 | 数据库字段 | 值 | 提取状态 |
|------|-----------|-----|---------|
| CAS Number | cas_number (新) | 184475-35-2 | ✅ (从同义词提取) |
| Synonyms | synonyms (新) | [数组] | ✅ |

---

## 四、化学分类 (PUG View)

- Pharmaceuticals → Listed in ZINC15
- Pharmaceuticals → Antineoplastic and immunomodulating agents → Antineoplastic agents

| 字段 | 数据库字段 | 值 | 提取状态 |
|------|-----------|-----|---------|
| Chemical Classes | chemical_class (新) | Pharmaceuticals > Antineoplastic agents | ✅ |

---

## 五、安全与毒性 (PUG View)

可用部分：
- Hazards Identification
- Regulatory Information

毒性数据：
- Hepatotoxicity
- Drug Induced Liver Injury
- Effects During Pregnancy and Lactation

| 字段 | 数据库字段 | 提取状态 |
|------|-----------|---------|
| Safety/Hazards | safety_hazards (新) | ✅ |
| Toxicity | toxicity_info (新) | ✅ |

---

## 六、药理与生物活性 (PUG View)

可用部分：
- Pharmacodynamics
- MeSH Pharmacological Classification
- FDA Pharmacological Classification
- ATC Code
- Absorption, Distribution and Excretion
- Protein Binding
- Metabolism/Metabolites
- Biological Half-Life
- Mechanism of Action
- Human Metabolite Information

| 字段 | 数据库字段 | 提取状态 |
|------|-----------|---------|
| Mechanism of Action | mechanism_of_action (新) | ✅ |
| ATC Code | atc_code (新) | ✅ |
| Pharmacology | pharmacology (新) | ✅ |

---

## 七、光谱数据 (PUG View)

可用部分：
- 1D NMR Spectra
- Mass Spectrometry

| 字段 | 数据库字段 | 提取状态 |
|------|-----------|---------|
| NMR Spectra | nmr_spectra_url (新) | ✅ (链接) |
| Mass Spectrometry | ms_spectra_url (新) | ✅ (链接) |

---

## 八、蛋白靶点 (PUG View)

- **10个蛋白结构** 可在 NCBI Structure 查看
- PDBe Ligand Code: **IRE**
- PDBe Structure Code: **2ITO** (EGFR tyrosine kinase)

| 字段 | 数据库字段 | 提取状态 |
|------|-----------|---------|
| Protein Targets | protein_targets (新) | ✅ |

---

## 九、药物信息 (PUG View)

可用部分：
- Drug Indication
- Drug Classes
- FDA Approved Drugs
- Clinical Trials
- Drug-Drug Interactions
- Drug-Food Interactions

| 字段 | 数据库字段 | 提取状态 |
|------|-----------|---------|
| Drug Indication | drug_indication (新) | ✅ |
| Drug Status | drug_status (新) | ✅ (FDA Approved) |
| Clinical Trials | clinical_trials (新) | ✅ |

---

## 十、API 调用命令汇总

### PUG REST (计算属性)
\`\`\`bash
curl "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/123631/property/MolecularFormula,MolecularWeight,XLogP,TPSA,HBondDonorCount,HBondAcceptorCount,RotatableBondCount,HeavyAtomCount,ExactMass,Complexity,InChI,InChIKey,CanonicalSMILES,IUPACName/JSON"
\`\`\`

### PUG View (各类属性)
\`\`\`bash
# 实验属性
curl "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/123631/JSON?heading=Experimental+Properties"

# 同义词
curl "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/123631/JSON?heading=Synonyms"

# 化学分类
curl "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/123631/JSON?heading=Chemical+Classes"

# 毒性
curl "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/123631/JSON?heading=Toxicity"

# 药理
curl "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/123631/JSON?heading=Pharmacology+and+Biochemistry"

# 药物信息
curl "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/123631/JSON?heading=Drug+and+Medication+Information"

# 相互作用
curl "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/123631/JSON?heading=Interactions+and+Pathways"

# 光谱
curl "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/123631/JSON?heading=Spectral+Information"
\`\`\`

---

## 结论

✅ **所有计划提取的字段都可以成功获取**

### 推荐新增的数据库字段

```sql
-- 基础扩展字段
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS cas_number VARCHAR(50);
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS exact_mass NUMERIC(15,8);
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS heavy_atom_count INTEGER;
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS complexity INTEGER;

-- 实验属性字段
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS melting_point VARCHAR(50);
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS physical_state VARCHAR(50);
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS solubility TEXT;
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS xlogp_experimental NUMERIC(10,4);
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS pka VARCHAR(50);

-- 分类与同义词
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS chemical_class TEXT;
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS synonyms TEXT;

-- 药理与安全 (可选，按需添加)
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS drug_indication TEXT;
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS atc_code VARCHAR(20);
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS safety_info TEXT;
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS toxicity_info TEXT;
```
