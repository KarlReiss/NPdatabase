import { apiGet } from './client'
import type { NaturalProductApi, TargetDetailApi } from './types'

export interface SearchResponseApi {
  naturalProducts: NaturalProductApi[]
  targets: TargetDetailApi[]
}
export const fetchHealth = () => apiGet('/api/health')

export const fetchStats = () => apiGet('/api/stats')

export const fetchSearch = (q: string, type: 'natural_product' | 'target' | 'all' = 'all') =>
  apiGet('/api/search', { q, type })
