import { apiGet, type PageResponse } from './client';
import type { BioResource, NaturalProductApi, Prescription } from './types';

export interface PrescriptionQuery {
  page?: number;
  pageSize?: number;
  q?: string;
  category?: string;
}

export const fetchPrescriptions = (params: PrescriptionQuery) =>
  apiGet<PageResponse<Prescription>>('/api/prescriptions', params);

export const fetchPrescriptionDetail = (prescriptionId: string) =>
  apiGet<Prescription>(`/api/prescriptions/${prescriptionId}`);

export const fetchPrescriptionBioResources = (prescriptionId: string) =>
  apiGet<BioResource[]>(`/api/prescriptions/${prescriptionId}/bio-resources`);

export const fetchPrescriptionNaturalProducts = (prescriptionId: string) =>
  apiGet<NaturalProductApi[]>(`/api/prescriptions/${prescriptionId}/natural-products`);
