import { apiGet, type PageResponse } from './client';
import type { BioactivityApi, BioResourceApi, NaturalProductApi, TargetApi, ToxicityApi } from './types';

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
  hasToxicity?: boolean;
}

export const fetchNaturalProducts = (params: NaturalProductQuery) =>
  apiGet<PageResponse<NaturalProductApi>>('/api/natural-products', params);

export const fetchNaturalProductDetail = (npId: string) =>
  apiGet<NaturalProductApi>(`/api/natural-products/${npId}`);

export const fetchNaturalProductBioactivity = (npId: string, params: { page?: number; pageSize?: number }) =>
  apiGet<PageResponse<BioactivityApi>>(`/api/natural-products/${npId}/bioactivity`, params);

export const fetchNaturalProductTargets = (npId: string) =>
  apiGet<TargetApi[]>(`/api/natural-products/${npId}/targets`);

export const fetchNaturalProductResources = (npId: string) =>
  apiGet<BioResourceApi[]>(`/api/natural-products/${npId}/bio-resources`);

export const fetchNaturalProductToxicity = (npId: string) =>
  apiGet<ToxicityApi[]>(`/api/natural-products/${npId}/toxicity`);

