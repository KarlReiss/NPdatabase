import { apiGet, type PageResponse } from './client';
import type { BioResource, Disease, NaturalProductApi } from './types';

export interface DiseaseQuery {
  page?: number;
  pageSize?: number;
  q?: string;
  category?: string;
}

export const fetchDiseases = (params: DiseaseQuery) =>
  apiGet<PageResponse<Disease>>('/api/diseases', params);

export const fetchDiseaseDetail = (diseaseId: string) =>
  apiGet<Disease>(`/api/diseases/${diseaseId}`);

export const fetchDiseaseBioResources = (diseaseId: string) =>
  apiGet<PageResponse<BioResource>>(`/api/diseases/${diseaseId}/bio-resources`);

export const fetchDiseaseNaturalProducts = (diseaseId: string) =>
  apiGet<PageResponse<NaturalProductApi>>(`/api/diseases/${diseaseId}/natural-products`);
