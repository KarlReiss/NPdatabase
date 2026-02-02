export interface Compound {
  npId: string;
  prefName?: string;
  iupacName?: string;
  structureUrl?: string;
  molecularWeight?: number;
  formula?: string;
  pubchemId?: string;
  xlogp?: number;
  psa?: number;
  hBondDonors?: number;
  hBondAcceptors?: number;
  rotatableBonds?: number;
  bestActivityValue?: number;
  numOfTarget?: number;
  description?: string;
}

export interface BioactivityRecord {
  id: string;
  target: string;
  type: string;
  rawValue: string;
  stdValue: string;
  reference: {
    pmid?: string;
    doi?: string;
  };
}

export interface Target {
  id: string;
  symbol: string;
  name: string;
  diseaseInferred: string[];
}

export interface BioResource {
  resourceId: string;
  chineseName: string;
  latinName?: string;
  resourceType: string;
  taxonomyFamily?: string;
  taxonomyGenus?: string;
  tcmProperty?: string;
  tcmFlavor?: string;
  tcmMeridian?: string;
  tcmToxicity?: string;
  numOfNaturalProducts: number;
  numOfPrescriptions: number;
}

export interface Prescription {
  prescriptionId: string;
  chineseName: string;
  pinyinName?: string;
  category?: string;
  subcategory?: string;
  functions?: string;
  indications?: string;
  numOfHerbs: number;
  numOfNaturalProducts: number;
}

export interface Disease {
  diseaseId: string;
  icd11Code: string;
  diseaseName: string;
  diseaseNameZh?: string;
  diseaseCategory?: string;
  numOfRelatedPlants: number;
  numOfRelatedTargets: number;
}
