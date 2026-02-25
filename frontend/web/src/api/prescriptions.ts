import { apiGet, type PageResponse } from './client';
import type { BioResource, Prescription, PrescriptionListItem } from './types';

export interface PrescriptionQuery {
  page?: number;
  pageSize?: number;
  q?: string;
}

export const fetchPrescriptions = (params: PrescriptionQuery) =>
  apiGet<PageResponse<PrescriptionListItem>>('/api/prescriptions', params);

export const fetchPrescriptionDetail = (prescriptionId: string) =>
  apiGet<Prescription>(`/api/prescriptions/${prescriptionId}`);

export const fetchPrescriptionBioResources = (prescriptionId: string) =>
  apiGet<PageResponse<BioResource>>(`/api/prescriptions/${prescriptionId}/bio-resources`);
