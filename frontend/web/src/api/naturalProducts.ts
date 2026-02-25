import { apiGet, type PageResponse } from './client';
import type {
  BioactivityApi,
  BioactivityTargetSummaryApi,
  BioResourceApi,
  NaturalProductApi,
} from './types';

export interface NaturalProductQuery {
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

export const fetchNaturalProducts = (params: NaturalProductQuery) =>
  apiGet<PageResponse<NaturalProductApi>>('/api/natural-products', params);

export const fetchNaturalProductDetail = (npId: string) =>
  apiGet<NaturalProductApi>(`/api/natural-products/${npId}`);

export const fetchNaturalProductBioactivity = (npId: string, params: { page?: number; pageSize?: number }) =>
  apiGet<PageResponse<BioactivityApi>>(`/api/natural-products/${npId}/bioactivity`, params);

export const fetchNaturalProductBioactivityTargets = (npId: string, params: { page?: number; pageSize?: number }) =>
  apiGet<PageResponse<BioactivityTargetSummaryApi>>(`/api/natural-products/${npId}/bioactivity-targets`, params);
export const fetchNaturalProductResources = (npId: string, params: { page?: number; pageSize?: number }) =>
  apiGet<PageResponse<BioResourceApi>>(`/api/natural-products/${npId}/bio-resources`, params);
