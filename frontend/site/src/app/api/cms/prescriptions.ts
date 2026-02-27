import { apiGet } from './client'

export interface PrescriptionQuery {
  page?: number
  pageSize?: number
  q?: string
  category?: string
}

export const fetchPrescriptions = (params: any) => apiGet('/api/prescriptions', params)
export const fetchPrescriptionDetail = (prescriptionId: string) =>
  apiGet(`/api/prescriptions/${prescriptionId}`)
export const fetchPrescriptionBioResources = (
  prescriptionId: string,
  params: { page?: number; pageSize?: number }
) => apiGet(`/api/prescriptions/${prescriptionId}/bio-resources`, params)
export const fetchPrescriptionNaturalProducts = (
  prescriptionId: string,
  params: { page?: number; pageSize?: number }
) => apiGet(`/api/prescriptions/${prescriptionId}/natural-products`, params)
