import request from '@/app/axios'

export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

export interface PageResponse<T> {
  records: T[]
  page: number
  pageSize: number
  total: number
}

type QueryValue = string | number | boolean | null | undefined

export const apiGet = (url: string, params?: Record<string, QueryValue>) =>
  request.get({ url, params })
