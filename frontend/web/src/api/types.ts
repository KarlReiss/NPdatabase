export interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

export interface PageResponse<T> {
  records: T[];
  page: number;
  pageSize: number;
  total: number;
}

export interface NaturalProductDetailView {
  id: number;
  npId: string;
  inchikey?: string;
  prefName?: string;
  iupacName?: string;
  nameInitial?: string;
  inchi?: string;
  smiles?: string;
  chemblId?: string;
  pubchemId?: string;
  molecularWeight?: number;
  xlogp?: number;
  psa?: number;
  formula?: string;
  hBondDonors?: number;
  hBondAcceptors?: number;
  rotatableBonds?: number;
  logS?: number;
  logD?: number;
  logP?: number;
  tpsa?: number;
  ringCount?: number;
  numOfOrganism?: number;
  numOfTarget?: number;
  numOfActivity?: number;
  ifQuantity?: boolean;
  bioactivityCount?: number;
  targetCount?: number;
  bioResourceCount?: number;
  bestActivityValue?: number;
  createdAt?: string;
  updatedAt?: string;
}

export interface Target {
  id: number;
  targetId: string;
  targetType?: string;
  targetName?: string;
  geneName?: string;
  targetOrganism?: string;
  targetOrganismTaxId?: string;
  uniprotId?: string;
  synonyms?: string;
  function?: string;
  pdbStructure?: string;
  bioclass?: string;
  ecNumber?: string;
  sequence?: string;
  ttdId?: string;
  numOfNaturalProducts?: number;
  numOfCompounds?: number;
  numOfActivities?: number;
  createdAt?: string;
  updatedAt?: string;
}

export interface TargetDetailView {
  id: number;
  targetId: string;
  targetType?: string;
  targetName?: string;
  geneName?: string;
  targetOrganism?: string;
  targetOrganismTaxId?: string;
  uniprotId?: string;
  synonyms?: string;
  function?: string;
  pdbStructure?: string;
  bioclass?: string;
  ecNumber?: string;
  sequence?: string;
  ttdId?: string;
  numOfNaturalProducts?: number;
  numOfCompounds?: number;
  numOfActivities?: number;
  naturalProductCount?: number;
  bioactivityCount?: number;
  bestActivityValue?: number;
  createdAt?: string;
  updatedAt?: string;
}

export interface Bioactivity {
  id: number;
  naturalProductId: number;
  targetId: number;
  activityType?: string;
  activityTypeGrouped?: string;
  activityRelation?: string;
  activityValue?: number;
  activityUnits?: string;
  activityValueStd?: number;
  activityUnitsStd?: string;
  assayOrganism?: string;
  assayTaxId?: string;
  assayStrain?: string;
  assayTissue?: string;
  assayCellType?: string;
  refId?: string;
  refIdType?: string;
  createdAt?: string;
}

export interface BioactivityTargetSummary {
  targetDbId: number;
  targetId?: string;
  targetName?: string;
  targetType?: string;
  targetOrganism?: string;
  uniprotId?: string;
  bioactivityCount?: number;
  bestActivityValue?: number;
}

export interface BioResource {
  id: number;
  resourceId?: string;
  resourceType?: string;
  chineseName?: string;
  translationSource?: string;
  familyChinese?: string;
  genusChinese?: string;
  latinName?: string;
  englishName?: string;
  pinyinName?: string;
  alias?: string;
  taxonomyKingdom?: string;
  taxonomyPhylum?: string;
  taxonomyClass?: string;
  taxonomyOrder?: string;
  taxonomyFamily?: string;
  taxonomyGenus?: string;
  taxonomySpecies?: string;
  taxonomyId?: string;
  speciesTaxId?: string;
  genusTaxId?: string;
  familyTaxId?: string;
  cmaupId?: string;
  translationSource?: string;
  familyChinese?: string;
  genusChinese?: string;
  medicinalPart?: string;
  medicinalPartLatin?: string;
  originRegion?: string;
  distribution?: string;
  habitat?: string;
  tcmProperty?: string;
  tcmFlavor?: string;
  tcmMeridian?: string;
  tcmToxicity?: string;
  functions?: string;
  indications?: string;
  contraindications?: string;
  mineralComposition?: string;
  mineralCrystalSystem?: string;
  mineralHardness?: string;
  mineralColor?: string;
  microbeStrain?: string;
  microbeCultureCondition?: string;
  microbeFermentationProduct?: string;
  animalClass?: string;
  animalConservationStatus?: string;
  tcmidId?: string;
  tcmspId?: string;
  herbId?: string;
  pharmacopoeiaRef?: string;
  literatureRef?: string;
  imageUrl?: string;
  numOfNaturalProducts?: number;
  numOfPrescriptions?: number;
  createdAt?: string;
  updatedAt?: string;
}

export interface Prescription {
  id: number;
  prescriptionId?: string;
  chineseName?: string;
  pinyinName?: string;
  englishName?: string;
  functions?: string;
  indications?: string;
  tcmidId?: string;
  diseaseIcd11Category?: string;
  reference?: string;
  createdAt?: string;
  updatedAt?: string;
}

export interface PrescriptionListItem {
  prescriptionId?: string;
  chineseName?: string;
  functions?: string;
  diseaseIcd11Category?: string;
  bioResourceCount?: number;
}

export interface BioResourceNaturalProductItem {
  npId: string;
  prefName?: string;
  iupacName?: string;
  molecularWeight?: number;
  xlogp?: number;
  psa?: number;
  formula?: string;
  orgIsolationPart?: string;
  orgCollectLocation?: string;
  orgCollectTime?: string;
  refType?: string;
  refId?: string;
  refIdType?: string;
  refUrl?: string;
  newCpFound?: string;
  sourceCount?: number;
}

export interface Disease {
  id: number;
  icd11Code?: string;
  diseaseName?: string;
  diseaseNameZh?: string;
  diseaseNameCmaup?: string;
  diseaseCategory?: string;
  createdAt?: string;
  updatedAt?: string;
}

export interface SearchResponse {
  naturalProducts: NaturalProductDetailView[];
  targets: TargetDetailView[];
}

export interface StatsResponse {
  bioResources: number;
  naturalProducts: number;
  prescriptions: number;
  targets: number;
  diseases: number;
  bioactivity?: number;
}

export interface NaturalProductListParams {
  page?: number;
  pageSize?: number;
  q?: string;
  mwMin?: number;
  mwMax?: number;
  xlogpMin?: number;
  xlogpMax?: number;
  psaMin?: number;
  psaMax?: number;
  activityType?: string;
  activityMaxNm?: number;
  targetType?: string;
}

export interface TargetListParams {
  page?: number;
  pageSize?: number;
  q?: string;
  targetType?: string;
}

export type NaturalProductApi = NaturalProductDetailView;
export type TargetApi = Target;
export type TargetDetailApi = TargetDetailView;
export type BioactivityApi = Bioactivity;
export type BioactivityTargetSummaryApi = BioactivityTargetSummary;
export type BioResourceApi = BioResource;
