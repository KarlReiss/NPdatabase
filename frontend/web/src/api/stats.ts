import { apiGet } from './client';
import type { StatsResponse } from './types';

export const fetchStats = () => apiGet<StatsResponse>('/api/stats');

