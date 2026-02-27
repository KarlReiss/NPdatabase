import { AxiosError, AxiosResponse, InternalAxiosRequestConfig } from './types'
import { SUCCESS_CODE, TRANSFORM_REQUEST_DATA } from '@/app/constants'
import { useUserStoreWithOut } from '@/store/modules/user'
import { formatToDateTime } from '@/app/utils/dateUtil'
import { objToFormData } from '@/app/utils'
import { ElMessage } from 'element-plus'
import qs from 'qs'

/**
 * 移除 空值、null值、undefined值以及一些特殊字段值
 * 处理 area searchTimeInterval timeInterval latLng pictures 值
 * @param some
 * @param method
 * @returns
 */
const noEmpty = (some: any) => {
  const hasEmpty = (str: string) => {
    if (typeof str != 'number' && typeof str != 'boolean') {
      return !str || str == null
    }
    return false
  }
  for (const key in some) {
    if (
      ['', undefined, 'undefined', null, 'null'].includes(some[key]) ||
      ['hasChildren', 'undefined'].includes(key) ||
      (typeof some[key] == 'string' && some[key].length == 0) ||
      key.slice(0, 1).indexOf('$') > -1 ||
      hasEmpty(some[key])
    ) {
      delete some[key]
    }

    if (typeof some[key] == 'object') {
      some[key] = noEmpty(some[key])
    }
  }
  return some
}

/**
 *
 * @param some
 * @returns
 */
const checkData = (some: any) => {
  const hasEmpty = (str: string) => {
    if (typeof str != 'number' && typeof str != 'boolean') {
      return !str || str == null
    }
    return false
  }
  for (const key in some) {
    if (some[key] == null || some[key] == undefined) {
      some[key] = ''
    }
    if (['createdAt', 'updatedAt'].includes(key) && typeof some[key] == 'number') {
      some[`${key}Tm`] = formatToDateTime(new Date(some[key]))
    }

    if (typeof some[key] == 'object') {
      some[key] = checkData(some[key])
    }
  }
  return some
}

const defaultRequestInterceptors = (config: InternalAxiosRequestConfig) => {
  if (
    config.method === 'post' &&
    config.headers['Content-Type'] === 'application/x-www-form-urlencoded'
  ) {
    config.data = qs.stringify(config.data)
  } else if (
    TRANSFORM_REQUEST_DATA &&
    config.method === 'post' &&
    config.headers['Content-Type'] === 'multipart/form-data' &&
    !(config.data instanceof FormData)
  ) {
    config.data = objToFormData(config.data)
  }
  if (config.method === 'get' && config.params) {
    let url = config.url as string
    url += '?'
    const keys = Object.keys(noEmpty(config.params))
    for (const key of keys) {
      if (config.params[key] !== void 0 && config.params[key] !== null) {
        url += `${key}=${encodeURIComponent(config.params[key])}&`
      }
    }
    url = url.substring(0, url.length - 1)
    config.params = {}
    config.url = url
  }
  return config
}

const defaultResponseInterceptors = async (response: AxiosResponse) => {
  if (response?.config?.responseType === 'blob') {
    // 如果是文件流，直接过
    return response
  } else if (response.data.code === SUCCESS_CODE) {
    return checkData(response.data.data)
  } else {
    const config = response.config as any
    const url = response.config.url as any
    const data = response.data
    const msgTxt = data?.data.message || ''
    const userStore = useUserStoreWithOut()
    if (data?.code === 401) {
      userStore.logout()
    } else if ([204, 404, 500].includes[data?.code]) {
      if (data?.code === 500) {
        if (config && url && url.indexOf('/customer/current') > 0) {
          userStore.logout()
        } else {
          ElMessage({ type: 'error', dangerouslyUseHTMLString: msgTxt })
        }
      } else {
        ElMessage({ type: 'error', dangerouslyUseHTMLString: msgTxt })
      }
    }
  }
  return response.data.data
}

const defaultResponseErrorInterceptors = async (error: AxiosError | any) => {
  if (!error) return
  if (!error.response) return
  const config = error.response.config
  const data = error.response.data
  const userStore = useUserStoreWithOut()
  const msgTxt = data.message || error.response.message || '请求失败'
  if (data && ![0, 200].includes[data?.code]) {
    if (data?.code === 401) {
      userStore.logout()
    } else if ([204, 404, 500].includes[data?.code]) {
      if (data?.code === 500) {
        if (config && config?.url && config?.url.indexOf('/customer/current') > 0) {
          userStore.logout()
        } else {
          ElMessage({ type: 'error', dangerouslyUseHTMLString: msgTxt })
        }
      } else {
        ElMessage({ type: 'error', dangerouslyUseHTMLString: msgTxt })
      }
    } else {
      ElMessage({ type: 'error', dangerouslyUseHTMLString: msgTxt })
    }
    return Promise.reject(data)
  }
  return Promise.reject(data)
}

export {
  noEmpty,
  checkData,
  defaultResponseInterceptors,
  defaultRequestInterceptors,
  defaultResponseErrorInterceptors
}
