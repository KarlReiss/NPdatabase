# PubChem CID 5280445 (Luteolin/木犀草素) 属性表

**获取日期**: 2026-02-25  
**数据来源**: PubChem PUG REST API + PUG View API

---

## 基本信息

| 属性 | 值 |
|------|-----|
| CID | 5280445 |
| 化合物名称 | Luteolin (木犀草素) |
| IUPAC名称 | 2-(3,4-dihydroxyphenyl)-5,7-dihydroxychromen-4-one |
| 分子式 | C15H10O6 |
| InChIKey | IQPNAANSBPBGFQ-UHFFFAOYSA-N |
| SMILES | C1=CC(=C(C=C1C2=CC(=O)C3=C(C=C(C=C3O2)O)O)O)O |

---

## 计算属性 (Computed Properties)

| 属性名称 | 值 | 单位 | 计算来源 |
|----------|-----|------|----------|
| 分子量 (Molecular Weight) | 286.24 | g/mol | PubChem 2.2 |
| 脂水分配系数 (XLogP3) | 1.4 | - | XLogP3 3.0 |
| 氢键供体数 (HBond Donor Count) | 4 | - | Cactvs 3.4.8.18 |
| 氢键受体数 (HBond Acceptor Count) | 6 | - | Cactvs 3.4.8.18 |
| 可旋转键数 (Rotatable Bond Count) | 1 | - | Cactvs 3.4.8.18 |
| 精确质量 (Exact Mass) | 286.04773803 | Da | PubChem 2.2 |
| 单同位素质量 (Monoisotopic Mass) | 286.04773803 | Da | PubChem 2.2 |
| 拓扑极性表面积 (TPSA) | 107 | Å² | Cactvs 3.4.8.18 |
| 重原子数 (Heavy Atom Count) | 21 | - | PubChem |
| 形式电荷 (Formal Charge) | 0 | - | PubChem |
| 复杂度 (Complexity) | 447 | - | Cactvs 3.4.8.18 |
| 同位素原子数 (Isotope Atom Count) | 0 | - | PubChem |
| 已定义原子立体中心数 | 0 | - | PubChem |
| 未定义原子立体中心数 | 0 | - | PubChem |
| 已定义键立体中心数 | 0 | - | PubChem |
| 未定义键立体中心数 | 0 | - | PubChem |
| 共价键单元数 | 1 | - | PubChem |

---

## 实验属性 (Experimental Properties)

| 属性名称 | 值 | 单位 | 数据来源 |
|----------|-----|------|----------|
| 物理描述 (Physical Description) | Solid | - | HMDB |
| 熔点 (Melting Point) | 329.5 | °C | HMDB |
| 脂水分配系数 LogP (实验值) | 2.53 | - | PERRISSOUD & TESTA (1986) |
| 碰撞截面积 (CCS) | 158.43 | Å² [M+H]+ | Ross et al. JASMS 2022 |

---

## LogP 对比

| 类型 | 值 | 来源 |
|------|-----|------|
| 计算值 (XLogP3) | 1.4 | PubChem 计算 |
| 实验值 (LogP) | 2.53 | PERRISSOUD & TESTA (1986) |

> **注意**: 计算值和实验值存在差异，实验值更可靠。

---

## 化学分类 (Chemical Classes)

- Potential endocrine disrupting compound (潜在内分泌干扰物)
- Polyketides → Flavonoids → Flavones and Flavonols (聚酮类 → 黄酮类 → 黄酮和黄酮醇)

---

## API 调用示例

### PUG REST (计算属性)
\`\`\`bash
curl "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/5280445/property/MolecularWeight,XLogP,TPSA/JSON"
\`\`\`

### PUG View (实验属性)
\`\`\`bash
curl "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/5280445/JSON?heading=Experimental+Properties"
\`\`\`
