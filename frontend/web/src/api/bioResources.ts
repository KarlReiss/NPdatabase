import { apiGet, type PageResponse } from './client';
import type { BioResource, BioResourceNaturalProductItem, Prescription } from './types';

export interface BioResourceQuery {
  page?: number;
  pageSize?: number;
  q?: string;
  resourceType?: string;
}

export const fetchBioResources = (params: BioResourceQuery) =>
  apiGet<PageResponse<BioResource>>('/api/bio-resources', params);

export const fetchBioResourceDetail = (resourceId: string) =>
  apiGet<BioResource>(`/api/bio-resources/${resourceId}`);

export const fetchBioResourceNaturalProducts = (resourceId: string) =>
  apiGet<PageResponse<BioResourceNaturalProductItem>>(`/api/bio-resources/${resourceId}/natural-products`);

export const fetchBioResourcePrescriptions = (resourceId: string) =>
  apiGet<PageResponse<Prescription>>(`/api/bio-resources/${resourceId}/prescriptions`);
