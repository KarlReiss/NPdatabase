import { apiGet } from './client'

export interface TargetQuery {
  page?: number
  pageSize?: number
  q?: string
  targetType?: string
}

export const fetchTargets = (params: any) => apiGet('/api/targets', params)
export const fetchTargetDetail = (targetId: string) => apiGet(`/api/targets/${targetId}`)
export const fetchTargetNaturalProducts = (
  targetId: string,
  params: { page?: number; pageSize?: number }
) => apiGet(`/api/targets/${targetId}/natural-products`, params)

export const fetchTargetsTargetTypes = () => apiGet('/api/targets/targetTypes')
export const fetchTargetsBioclasses = () => apiGet('/api/targets/bioclasses')
