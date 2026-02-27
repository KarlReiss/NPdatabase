import { apiGet } from './client'

export interface BioResourceQuery {
  page?: number
  pageSize?: number
  q?: string
  resourceType?: string
}

export const fetchBioResources = (params: any) => apiGet('/api/bio-resources', params)
export const fetchBioResourceDetail = (resourceId: string) =>
  apiGet(`/api/bio-resources/${resourceId}`)
export const fetchBioResourceNaturalProducts = (
  resourceId: string,
  params: { page?: number; pageSize?: number }
) => apiGet(`/api/bio-resources/${resourceId}/natural-products`, params)
export const fetchBioResourcePrescriptions = (
  resourceId: string,
  params: { page?: number; pageSize?: number }
) => apiGet(`/api/bio-resources/${resourceId}/prescriptions`, params)
export const fetchBioResourceResourceType = () => apiGet(`/api/bio-resources/resource-types`)
export const fetchBioResourceCategories = () => apiGet(`/api/bio-resources/categories`)
