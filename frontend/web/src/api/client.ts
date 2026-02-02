const API_BASE = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '');

export interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

export interface PageResponse<T> {
  records: T[];
  page: number;
  pageSize: number;
  total: number;
}

type QueryValue = string | number | boolean | null | undefined;

const buildQuery = (params?: Record<string, QueryValue>) => {
  if (!params) return '';
  const search = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value === null || value === undefined || value === '') return;
    search.append(key, String(value));
  });
  const query = search.toString();
  return query ? `?${query}` : '';
};

export const apiGet = async <T>(path: string, params?: Record<string, QueryValue>) => {
  const url = `${API_BASE}${path}${buildQuery(params)}`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`请求失败（${response.status}）`);
  }
  const payload = (await response.json()) as ApiResponse<T>;
  if (payload.code !== 0) {
    throw new Error(payload.message || '接口返回异常');
  }
  return payload.data;
};
