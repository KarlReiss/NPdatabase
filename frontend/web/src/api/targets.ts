import { apiGet, type PageResponse } from './client';
import type { NaturalProductApi, TargetApi, TargetDetailApi } from './types';

export interface TargetQuery {
  page?: number;
  pageSize?: number;
  q?: string;
  targetType?: string;
}

export const fetchTargets = (params: TargetQuery) =>
  apiGet<PageResponse<TargetApi>>('/api/targets', params);

export const fetchTargetDetail = (targetId: string) =>
  apiGet<TargetDetailApi>(`/api/targets/${targetId}`);

export const fetchTargetNaturalProducts = (targetId: string) =>
  apiGet<PageResponse<NaturalProductApi>>(`/api/targets/${targetId}/natural-products`);

