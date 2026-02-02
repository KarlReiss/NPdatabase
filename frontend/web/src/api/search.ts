import { apiGet } from './client';
import type { NaturalProductApi, TargetDetailApi } from './types';

export interface SearchResponseApi {
  naturalProducts: NaturalProductApi[];
  targets: TargetDetailApi[];
}

export const fetchSearch = (q: string, type: 'natural_product' | 'target' | 'all' = 'all') =>
  apiGet<SearchResponseApi>('/api/search', { q, type });

