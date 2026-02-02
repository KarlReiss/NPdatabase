import { apiGet } from './client';
import type { StatsApi } from './types';

export const fetchStats = () => apiGet<StatsApi>('/api/stats');

