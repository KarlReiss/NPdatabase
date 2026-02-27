import { apiGet } from './client'
export interface NaturalProductQuery {
  page?: number
  pageSize?: number
  q?: string
  mwMin?: number
  mwMax?: number
  xlogpMin?: number
  xlogpMax?: number
  psaMin?: number
  psaMax?: number
  activityType?: string
  activityMaxNm?: number
  targetType?: string
  hasToxicity?: boolean
}

export const fetchNaturalProducts = (params: any) => apiGet('/api/natural-products', params)
export const fetchNaturalProductDetail = (npId: string) => apiGet(`/api/natural-products/${npId}`)
export const fetchNaturalProductBioactivity = (
  npId: string,
  params: { page?: number; pageSize?: number }
) => apiGet(`/api/natural-products/${npId}/bioactivity`, params)
export const fetchNaturalProductBioactivityTargets = (
  npId: string,
  params: { page?: number; pageSize?: number }
) => apiGet(`/api/natural-products/${npId}/bioactivity-targets`, params)
export const fetchNaturalProductResources = (
  npId: string,
  params: { page?: number; pageSize?: number }
) => apiGet(`/api/natural-products/${npId}/bio-resources`, params)
export const fetchNaturalProductToxicity = (
  npId: string,
  params: { page?: number; pageSize?: number }
) => apiGet(`/api/natural-products/${npId}/toxicity`, params)
