# PubChem 字段提取方案

**参考化合物**: CID 5280445 (Luteolin/木犀草素)  
**生成日期**: 2026-02-25

---

## 一、现有数据库字段 vs PubChem 字段对比

### 1. natural_products 表字段映射

| 数据库字段 | 类型 | 现有数据 | PubChem 字段 | 数据类型 | 建议操作 |
|------------|------|----------|--------------|----------|----------|
| `pubchem_id` | VARCHAR(50) | ✅ 有 | CID | 计算值 | 保持，用于匹配 |
| `inchikey` | VARCHAR(100) | ✅ 有 | InChIKey | 计算值 | 可补充缺失 |
| `pref_name` | TEXT | ✅ 有 | - | - | 保持 |
| `iupac_name` | TEXT | ⚠️ 部分 | IUPACName | 计算值 | **补充缺失** |
| `inchi` | TEXT | ✅ 有 | InChI | 计算值 | 可补充缺失 |
| `smiles` | TEXT | ✅ 有 | CanonicalSMILES / IsomericSMILES | 计算值 | 可补充缺失 |
| `molecular_weight` | NUMERIC(10,2) | ✅ 有 | MolecularWeight | 计算值 | 保持 |
| `formula` | VARCHAR(200) | ✅ 有 | MolecularFormula | 计算值 | 保持 |
| `xlogp` | NUMERIC(10,2) | ⚠️ 缺失多 | XLogP | 计算值 | **补充缺失** |
| `psa` / `tpsa` | NUMERIC(10,2) | ⚠️ 缺失多 | TPSA | 计算值 | **补充缺失** |
| `h_bond_donors` | INTEGER | ⚠️ 缺失多 | HBondDonorCount | 计算值 | **补充缺失** |
| `h_bond_acceptors` | INTEGER | ⚠️ 缺失多 | HBondAcceptorCount | 计算值 | **补充缺失** |
| `rotatable_bonds` | INTEGER | ⚠️ 缺失多 | RotatableBondCount | 计算值 | **补充缺失** |
| `log_p` | NUMERIC(10,2) | ⚠️ 部分 | LogP (Experimental) | **实验值** | **新增，优先实验值** |
| `log_s` | NUMERIC(10,2) | ⚠️ 部分 | - | - | PubChem 无此字段 |
| `log_d` | NUMERIC(10,2) | ⚠️ 部分 | - | - | PubChem 无此字段 |
| `ring_count` | INTEGER | ⚠️ 部分 | - | - | 需从结构计算 |

---

## 二、建议从 PubChem 提取的字段

### 📦 第一类：补充现有缺失字段 (优先级: ⭐⭐⭐⭐⭐)

| 字段名 | PubChem API | 示例值 (CID 5280445) | 说明 |
|--------|-------------|---------------------|------|
| IUPAC Name | PUG REST | 2-(3,4-dihydroxyphenyl)-5,7-dihydroxychromen-4-one | 标准命名 |
| XLogP | PUG REST | 1.4 | 脂水分配系数（计算） |
| TPSA | PUG REST | 107 | 拓扑极性表面积 |
| HBond Donor Count | PUG REST | 4 | 氢键供体数 |
| HBond Acceptor Count | PUG REST | 6 | 氢键受体数 |
| Rotatable Bond Count | PUG REST | 1 | 可旋转键数 |
| Heavy Atom Count | PUG REST | 21 | 重原子数 |
| Exact Mass | PUG REST | 286.04773803 | 精确质量 |
| Complexity | PUG REST | 447 | 分子复杂度 |
| InChIKey | PUG REST | IQPNAANSBPBGFQ-UHFFFAOYSA-N | 标准化标识符 |
| CanonicalSMILES | PUG REST | C1=CC(=C(C=C1...)O | 标准化 SMILES |

### 📦 第二类：实验属性 (优先级: ⭐⭐⭐⭐)

| 字段名 | PubChem API | 示例值 (CID 5280445) | 说明 |
|--------|-------------|---------------------|------|
| LogP (Experimental) | PUG View | 2.53 | 脂水分配系数（实验值，更准确）|
| Melting Point | PUG View | 329.5 °C | 熔点 |
| Physical Description | PUG View | Solid | 物理状态 |
| Boiling Point | PUG View | - | 沸点（如有）|
| Solubility | PUG View | - | 溶解度（如有）|
| Density | PUG View | - | 密度（如有）|
| Vapor Pressure | PUG View | - | 蒸气压（如有）|

### 📦 第三类：天然产物特有需求 (优先级: ⭐⭐⭐⭐)

| 字段名 | PubChem API | 示例值 (CID 5280445) | 说明 |
|--------|-------------|---------------------|------|
| Synonyms | PUG View | Luteolin, Digitoflavone, 木犀草素... | 同义词（包含中文名、CAS号等）|
| CAS Number | PUG View (Synonyms) | 491-70-3 | CAS 登记号 |
| Chemical Classes | PUG View | Flavonoids → Flavones | 化学分类 |
| Natural Product Classification | PUG View | Polyketides → Flavonoids | 天然产物分类 |
| Taxonomy | PUG View | - | 来源物种分类（如有）|

### 📦 第四类：安全与毒性 (优先级: ⭐⭐⭐)

| 字段名 | PubChem API | 说明 |
|--------|-------------|------|
| GHS Hazard Statements | PUG View (Safety) | GHS 危险说明 |
| GHS Precautionary Statements | PUG View (Safety) | GHS 预防说明 |
| NFPA Hazard Rating | PUG View (Safety) | NFPA 危险等级 |
| Acute Toxicity | PUG View (Toxicity) | 急性毒性 |
| Carcinogenicity | PUG View (Toxicity) | 致癌性 |
| Mutagenicity | PUG View (Toxicity) | 致突变性 |

### 📦 第五类：药理与生物活性 (优先级: ⭐⭐⭐)

| 字段名 | PubChem API | 说明 |
|--------|-------------|------|
| Drug Indication | PUG View (Drug Info) | 药物适应症 |
| Mechanism of Action | PUG View (Pharmacology) | 作用机制 |
| Metabolism | PUG View (Pharmacology) | 代谢信息 |
| Protein Targets | PUG View (Interactions) | 蛋白靶点 |
| Biological Pathways | PUG View (Pathways) | 生物通路 |
| Associated Diseases | PUG View (Diseases) | 相关疾病 |

### 📦 第六类：光谱数据 (优先级: ⭐⭐)

| 字段名 | PubChem API | 说明 |
|--------|-------------|------|
| 1D NMR Spectra | PUG View (Spectral) | 一维核磁共振谱 |
| 2D NMR Spectra | PUG View (Spectral) | 二维核磁共振谱 |
| Mass Spectrometry | PUG View (Spectral) | 质谱数据 |
| IR Spectra | PUG View (Spectral) | 红外光谱 |
| UV-Vis Spectra | PUG View (Spectral) | 紫外可见光谱 |

---

## 三、建议新增的数据库字段

### 新增字段建议

```sql
-- 建议在 natural_products 表新增以下字段
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS cas_number VARCHAR(50);
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS exact_mass NUMERIC(15,8);
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS heavy_atom_count INTEGER;
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS complexity INTEGER;
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS melting_point NUMERIC(10,2);
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS physical_state VARCHAR(50);
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS xlogp_experimental NUMERIC(10,4);
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS chemical_class TEXT;
ALTER TABLE natural_products ADD COLUMN IF NOT EXISTS synonyms TEXT[];  -- 同义词数组
```

---

## 四、API 调用示例

### PUG REST (计算属性)
\`\`\`bash
# 获取单个 CID 的属性
curl "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/5280445/property/MolecularFormula,MolecularWeight,XLogP,TPSA,HBondDonorCount,HBondAcceptorCount,RotatableBondCount,HeavyAtomCount,ExactMass,Complexity,InChI,InChIKey,CanonicalSMILES,IUPACName/JSON"

# 批量获取（最多 100 个 CID）
curl "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/5280445,5280446,5280447/property/MolecularWeight,XLogP/JSON"
\`\`\`

### PUG View (实验属性)
\`\`\`bash
# 获取实验属性
curl "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/5280445/JSON?heading=Experimental+Properties"

# 获取同义词
curl "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/5280445/JSON?heading=Synonyms"

# 获取毒性数据
curl "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/5280445/JSON?heading=Toxicity"

# 获取安全数据
curl "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/5280445/JSON?heading=Safety+and+Hazards"
\`\`\`

---

## 五、实施建议

### 第一阶段：补充缺失的计算属性
1. 遍历 `natural_products` 表中 `pubchem_id` 不为空的记录
2. 调用 PUG REST API 获取计算属性
3. 更新缺失的 `xlogp`, `tpsa`, `h_bond_donors`, `h_bond_acceptors`, `rotatable_bonds` 等字段

### 第二阶段：获取实验属性
1. 新增数据库字段
2. 调用 PUG View API 获取实验数据
3. 优先使用实验值覆盖计算值

### 第三阶段：获取同义词和分类
1. 获取 Synonyms（包含中文名、CAS号）
2. 获取 Chemical Classes 分类信息
3. 建立同义词搜索索引

---

## 六、示例数据 (CID 5280445)

### 计算属性
| 字段 | 值 |
|------|-----|
| MolecularFormula | C15H10O6 |
| MolecularWeight | 286.24 g/mol |
| XLogP3 | 1.4 |
| TPSA | 107 Å² |
| HBondDonorCount | 4 |
| HBondAcceptorCount | 6 |
| RotatableBondCount | 1 |
| HeavyAtomCount | 21 |
| ExactMass | 286.04773803 Da |
| Complexity | 447 |
| InChIKey | IQPNAANSBPBGFQ-UHFFFAOYSA-N |
| IUPACName | 2-(3,4-dihydroxyphenyl)-5,7-dihydroxychromen-4-one |

### 实验属性
| 字段 | 值 |
|------|-----|
| Physical Description | Solid |
| Melting Point | 329.5 °C |
| LogP (Experimental) | 2.53 |

### 同义词（部分）
- Luteolin
- 3',4',5,7-Tetrahydroxyflavone
- Digitoflavone
- 木犀草素（如有）
- CAS: 491-70-3

### 化学分类
- Polyketides → Flavonoids → Flavones and Flavonols
- Potential endocrine disrupting compound
