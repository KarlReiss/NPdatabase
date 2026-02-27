// copy to vben-admin

const toString = Object.prototype.toString

export const is = (val: unknown, type: string) => {
  return toString.call(val) === `[object ${type}]`
}

export const isDef = <T = unknown>(val?: T): val is T => {
  return typeof val !== 'undefined'
}

export const isUnDef = <T = unknown>(val?: T): val is T => {
  return !isDef(val)
}

export const isObject = (val: any): val is Record<any, any> => {
  return val !== null && is(val, 'Object')
}

export const isEmpty = <T = unknown>(val: T): val is T => {
  if (isArray(val) || isString(val)) {
    return val.length === 0
  }

  if (val instanceof Map || val instanceof Set) {
    return val.size === 0
  }

  if (isObject(val)) {
    return Object.keys(val).length === 0
  }

  return false
}

export const isDate = (val: unknown): val is Date => {
  return is(val, 'Date')
}

export const isNull = (val: unknown): val is null => {
  return val === null
}

export const isNullAndUnDef = (val: unknown): val is null | undefined => {
  return isUnDef(val) && isNull(val)
}

export const isNullOrUnDef = (val: unknown): val is null | undefined => {
  return isUnDef(val) || isNull(val)
}

export const isNumber = (val: unknown): val is number => {
  return is(val, 'Number')
}

export const isPromise = <T = any>(val: unknown): val is Promise<T> => {
  return is(val, 'Promise') && isObject(val) && isFunction(val.then) && isFunction(val.catch)
}

export const isString = (val: unknown): val is string => {
  return is(val, 'String')
}

export const isFunction = (val: unknown): val is Function => {
  return typeof val === 'function'
}

export const isBoolean = (val: unknown): val is boolean => {
  return is(val, 'Boolean')
}

export const isRegExp = (val: unknown): val is RegExp => {
  return is(val, 'RegExp')
}

export const isArray = (val: any): val is Array<any> => {
  return val && Array.isArray(val)
}

export const isWindow = (val: any): val is Window => {
  return typeof window !== 'undefined' && is(val, 'Window')
}

export const isElement = (val: unknown): val is Element => {
  return isObject(val) && !!val.tagName
}

export const isMap = (val: unknown): val is Map<any, any> => {
  return is(val, 'Map')
}

export const isServer = typeof window === 'undefined'

export const isClient = !isServer

export const isUrl = (path: string): boolean => {
  try {
    new URL(path)
    return true
  } catch (_error) {
    return false
  }
}

export const isDark = (): boolean => {
  return window.matchMedia('(prefers-color-scheme: dark)').matches
}

// 是否是图片链接
export const isImgPath = (path: string): boolean => {
  return /(https?:\/\/|data:image\/).*?\.(png|jpg|jpeg|gif|svg|webp|ico)/gi.test(path)
}

export const isEmptyVal = (val: any): boolean => {
  return val === '' || val === null || val === undefined
}

/**
 * 判断是否是移动端
 */
export function isMobile() {
  if (
    navigator.userAgent.match(
      /('phone|pad|pod|iPhone|iPod|ios|iPad|Android|Mobile|BlackBerry|IEMobile|MQQBrowser|JUC|Fennec|wOSBrowser|BrowserNG|WebOS|Symbian|Windows Phone')/i
    )
  ) {
    return true
  } else {
    return false
  }
}

/**
 * 是否是字符串数组
 * @param val
 * @returns
 */
export const isStringArray = (val: any): val is Array<any> => {
  if (!!val && val != null && typeof val == 'string') {
    const start = val.slice(0, 1)
    const end = val.slice(-1)
    if (start == '[' && end == ']') {
      return true
    } else {
      return false
    }
  } else {
    return false
  }
}
