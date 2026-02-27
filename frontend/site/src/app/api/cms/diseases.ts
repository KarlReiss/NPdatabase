import { apiGet } from './client'

export interface DiseaseQuery {
  page?: number
  pageSize?: number
  q?: string
  category?: string
}

export const fetchDiseases = (params: any) => apiGet('/api/diseases', params)
export const fetchDiseaseDetail = (diseaseId: string) => apiGet(`/api/diseases/${diseaseId}`)
export const fetchDiseaseBioResources = (diseaseId: string, params: any) =>
  apiGet(`/api/diseases/${diseaseId}/bio-resources`, params)
export const fetchDiseaseNaturalProducts = (diseaseId: string, params: any) =>
  apiGet(`/api/diseases/${diseaseId}/natural-products`, params)
export const fetchDiseasesCategories = () => apiGet('/api/diseases/categories')
