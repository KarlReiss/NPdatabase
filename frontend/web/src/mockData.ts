import type { BioactivityRecord, BioResource, Compound, Disease, Prescription, Target } from './types';

export const MOCK_COMPOUNDS: Compound[] = [
  {
    npId: 'NPC000001',
    prefName: 'Curcumin',
    iupacName: '1,7-bis(4-hydroxy-3-methoxyphenyl)-1,6-heptadiene-3,5-dione',
    structureUrl: 'https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid=969516&t=l',
    molecularWeight: 368.38,
    formula: 'C21H20O6',
    pubchemId: '969516',
    xlogp: 3.2,
    psa: 93.1,
    hBondDonors: 2,
    hBondAcceptors: 6,
    rotatableBonds: 8,
    bestActivityValue: 0.5,
    numOfTarget: 15,
    description:
      'A bright yellow chemical produced by plants of the Curcuma longa species. It is the principal curcuminoid of turmeric (Curcuma longa).',
  },
  {
    npId: 'NPC000002',
    prefName: 'Quercetin',
    iupacName: '3,3′,4′,5,7-pentahydroxyflavone',
    structureUrl: 'https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid=5280343&t=l',
    molecularWeight: 302.24,
    formula: 'C15H10O7',
    pubchemId: '5280343',
    xlogp: 1.5,
    psa: 127.3,
    hBondDonors: 5,
    hBondAcceptors: 7,
    rotatableBonds: 1,
    bestActivityValue: 1200,
    numOfTarget: 42,
    description:
      'A plant flavonol from the flavonoid group of polyphenols. It is found in many fruits, vegetables, leaves, seeds, and grains.',
  },
  {
    npId: 'NPC000003',
    prefName: 'Resveratrol',
    iupacName: '3,5,4′-trihydroxy-trans-stilbene',
    structureUrl: 'https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid=445154&t=l',
    molecularWeight: 228.24,
    formula: 'C14H12O3',
    pubchemId: '445154',
    xlogp: 3.1,
    psa: 60.7,
    hBondDonors: 3,
    hBondAcceptors: 3,
    rotatableBonds: 2,
    bestActivityValue: 15,
    numOfTarget: 28,
    description:
      'A stilbenoid, a type of natural phenol, and a phytoalexin produced by several plants in response to injury.',
  },
];

export const MOCK_BIOACTIVITY: BioactivityRecord[] = [
  {
    id: 'ACT_001',
    target: 'EGFR',
    type: 'IC50',
    rawValue: '0.5 nM',
    stdValue: '0.5 nM',
    reference: { pmid: '34567812', doi: '10.1038/s41586-021-03123-y' },
  },
  {
    id: 'ACT_002',
    target: 'COX-2',
    type: 'Ki',
    rawValue: '120 nM',
    stdValue: '120 nM',
    reference: { pmid: '29881722' },
  },
  {
    id: 'ACT_003',
    target: 'NF-kappaB',
    type: 'IC50',
    rawValue: '5.4 uM',
    stdValue: '5400 nM',
    reference: { doi: '10.1158/0008-5472.CAN-05-3412' },
  },
];

export const MOCK_TARGETS: Target[] = [
  {
    id: 'T_001',
    symbol: 'EGFR',
    name: 'Epidermal Growth Factor Receptor',
    diseaseInferred: ['NSCLC', 'Breast Cancer'],
  },
  {
    id: 'T_002',
    symbol: 'COX-2',
    name: 'Cyclooxygenase-2',
    diseaseInferred: ['Inflammation', 'Arthritis'],
  },
  {
    id: 'T_003',
    symbol: 'TNF-alpha',
    name: 'Tumor Necrosis Factor alpha',
    diseaseInferred: ["Crohn's Disease", 'Psoriasis'],
  },
];

export const MOCK_RESOURCES: BioResource[] = [
  {
    resourceId: 'BR0001',
    chineseName: '人参',
    latinName: 'Panax ginseng',
    resourceType: 'Plant',
    taxonomyFamily: 'Araliaceae',
    taxonomyGenus: 'Panax',
    tcmProperty: '温',
    tcmFlavor: '甘、微苦',
    tcmMeridian: '脾、肺、心',
    tcmToxicity: '无',
    numOfNaturalProducts: 42,
    numOfPrescriptions: 18,
  },
  {
    resourceId: 'BR0002',
    chineseName: '黄芪',
    latinName: 'Astragalus membranaceus',
    resourceType: 'Plant',
    taxonomyFamily: 'Fabaceae',
    taxonomyGenus: 'Astragalus',
    tcmProperty: '微温',
    tcmFlavor: '甘',
    tcmMeridian: '脾、肺',
    tcmToxicity: '无',
    numOfNaturalProducts: 33,
    numOfPrescriptions: 25,
  },
];

export const MOCK_PRESCRIPTIONS: Prescription[] = [
  {
    id: 1,
    prescriptionId: 'PR0001',
    chineseName: '补中益气汤',
    pinyinName: 'Buzhong Yiqi Tang',
    functions: '补中益气，升阳举陷',
    indications: '脾胃气虚，倦怠乏力',
  },
  {
    id: 2,
    prescriptionId: 'PR0002',
    chineseName: '四君子汤',
    pinyinName: 'Sijunzi Tang',
    functions: '益气健脾',
    indications: '脾胃气虚，食少便溏',
  },
];

export const MOCK_DISEASES: Disease[] = [
  {
    diseaseId: 'DIS0001',
    icd11Code: '2C25.0',
    diseaseName: 'Non-small cell lung cancer',
    diseaseNameZh: '非小细胞肺癌',
    diseaseCategory: '肿瘤',
    numOfRelatedPlants: 120,
    numOfRelatedTargets: 35,
  },
  {
    diseaseId: 'DIS0002',
    icd11Code: 'FA20',
    diseaseName: 'Rheumatoid arthritis',
    diseaseNameZh: '类风湿关节炎',
    diseaseCategory: '免疫',
    numOfRelatedPlants: 64,
    numOfRelatedTargets: 18,
  },
];
