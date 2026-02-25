import { apiGet, type PageResponse } from './client';
import type { BioResource, BioResourceNaturalProductItem, Prescription } from './types';

export interface BioResourceQuery {
  page?: number;
  pageSize?: number;
  q?: string;
  resourceType?: string;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

export const fetchBioResources = (params: BioResourceQuery) =>
  apiGet<PageResponse<BioResource>>('/api/bio-resources', params);

export const fetchBioResourceDetail = (resourceId: string) =>
  apiGet<BioResource>(`/api/bio-resources/${resourceId}`);

export const fetchBioResourceNaturalProducts = (resourceId: string, params?: { page?: number; pageSize?: number }) =>
  apiGet<PageResponse<BioResourceNaturalProductItem>>(`/api/bio-resources/${resourceId}/natural-products`, params);

export const fetchBioResourcePrescriptions = (resourceId: string, params?: { page?: number; pageSize?: number }) =>
  apiGet<PageResponse<Prescription>>(`/api/bio-resources/${resourceId}/prescriptions`, params);
