import { ref } from 'vue'

/**
 *
 * @param component 需要注册的组件
 * @param alias 组件别名
 * @returns any
 */
export const withInstall = <T>(component: T, alias?: string) => {
  const comp = component as any
  comp.install = (app: any) => {
    app.component(comp.name || comp.displayName, component)
    if (alias) {
      app.config.globalProperties[alias] = component
    }
  }
  return component as T & Plugin
}

/**
 * @param str 需要转下划线的驼峰字符串
 * @returns 字符串下划线
 */
export const humpToUnderline = (str: string): string => {
  return str.replace(/([A-Z])/g, '-$1').toLowerCase()
}

/**
 * @param str 需要转驼峰的下划线字符串
 * @returns 字符串驼峰
 */
export const underlineToHump = (str: string): string => {
  if (!str) return ''
  return str.replace(/\-(\w)/g, (_, letter: string) => {
    return letter.toUpperCase()
  })
}

/**
 * 驼峰转横杠
 */
export const humpToDash = (str: string): string => {
  return str.replace(/([A-Z])/g, '-$1').toLowerCase()
}

export const setCssVar = (prop: string, val: any, dom = document.documentElement) => {
  dom.style.setProperty(prop, val)
}

export const getCssVar = (prop: string, dom = document.documentElement) => {
  return getComputedStyle(dom).getPropertyValue(prop)
}

/**
 * 查找数组对象的某个下标
 * @param {Array} ary 查找的数组
 * @param {Functon} fn 判断的方法
 */
export const findIndex = <T = Recordable>(ary: Array<T>, fn: Fn): number => {
  if (ary.findIndex) {
    return ary.findIndex(fn)
  }
  let index = -1
  ary.some((item: T, i: number, ary: Array<T>) => {
    const ret: T = fn(item, i, ary)
    if (ret) {
      index = i
      return ret
    }
  })
  return index
}

export const trim = (str: string) => {
  return str.replace(/(^\s*)|(\s*$)/g, '')
}

/**
 * @param {Date | number | string} time 需要转换的时间
 * @param {String} fmt 需要转换的格式 如 yyyy-MM-dd、yyyy-MM-dd HH:mm:ss
 */
export function formatTime(time: Date | number | string, fmt: string) {
  if (!time) return ''
  else {
    const date = new Date(time)
    const o = {
      'M+': date.getMonth() + 1,
      'd+': date.getDate(),
      'H+': date.getHours(),
      'm+': date.getMinutes(),
      's+': date.getSeconds(),
      'q+': Math.floor((date.getMonth() + 3) / 3),
      S: date.getMilliseconds()
    }
    if (/(y+)/.test(fmt)) {
      fmt = fmt.replace(RegExp.$1, (date.getFullYear() + '').substr(4 - RegExp.$1.length))
    }
    for (const k in o) {
      if (new RegExp('(' + k + ')').test(fmt)) {
        fmt = fmt.replace(
          RegExp.$1,
          RegExp.$1.length === 1 ? o[k] : ('00' + o[k]).substr(('' + o[k]).length)
        )
      }
    }
    return fmt
  }
}

/**
 * 生成随机字符串
 */
export function toAnyString() {
  const str: string = 'xxxxx-xxxxx-4xxxx-yxxxx-xxxxx'.replace(/[xy]/g, (c: string) => {
    const r: number = (Math.random() * 16) | 0
    const v: number = c === 'x' ? r : (r & 0x3) | 0x8
    return v.toString()
  })
  return str
}

/**
 * 首字母大写
 */
export function firstUpperCase(str: string) {
  return str.toLowerCase().replace(/( |^)[a-z]/g, (L) => L.toUpperCase())
}

/**
 * 把对象转为formData
 */
export function objToFormData(obj: Recordable) {
  const formData = new FormData()
  Object.keys(obj).forEach((key) => {
    formData.append(key, obj[key])
  })
  return formData
}

/**
 * 防抖
 * @param {Function} fn
 * @param {number} wait
 */
export const debounce = (fn: Function, delay: number) => {
  let timer: ReturnType<typeof setTimeout>
  return (...args: any[]) => {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => {
      fn(...args)
    }, delay)
  }
}

/**
 * 节流
 * @param {Function} fn
 * @param {number} delay
 */
export const throttle = (fn: Function, delay: number) => {
  const canRun = ref(true)
  return (...args: any[]) => {
    if (!canRun.value) return
    canRun.value = false
    setTimeout(() => {
      fn(...args)
      canRun.value = true
    }, delay)
  }
}

import { priceToThousands } from '@pureadmin/utils'
export const toNumber = (value: unknown) => {
  if (value === null || value === undefined || value === '') return null
  const num = Number(value)
  return Number.isFinite(num) ? num : null
}

export const formatCount = (value: unknown, fallback = '—') => {
  const num = toNumber(value)
  if (num === null) return fallback
  return priceToThousands(Math.round(num))
}

export const formatDecimal = (value: unknown, digits = 2, fallback = '—') => {
  const num = toNumber(value)
  if (num === null) return fallback
  return num.toFixed(digits)
}

export const formatActivityValue = (value: unknown, unit = 'nM') => {
  const num = toNumber(value)
  if (num === null) return '—'
  return `${formatDecimal(num, 2)} ${unit}`.trim()
}

export const buildPubchemImage = (pubchemId: unknown) => {
  if (pubchemId === null || pubchemId === undefined) return ''
  const id = String(pubchemId).trim()
  if (!id) return ''
  return `https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid=${id}&t=l`
}

/**
 * html反转义
 */
export const htmlDecode = (str: any) => {
  let s = ''
  if (str.length === 0) return ''
  s = str.replace(/&amp;/g, '&')
  s = s.replace(/&lt;/g, '<')
  s = s.replace(/&gt;/g, '>')
  s = s.replace(/&nbsp;/g, ' ')
  s = s.replace(/&#39;/g, "'")
  s = s.replace(/&quot;/g, '"')
  return s
}

/**
 * vh转化px
 */
export const vhToPx = (vh: number) => {
  return window.innerHeight * (vh / 100)
}

/**
 * 判断两数组是否相同
 * @param news 新数据
 * @param old 源数据
 * @returns 两数组相同返回 `true`，反之则反
 */
export function judementSameArr(news: unknown[] | string[], old: string[]): boolean {
  let count = 0
  const leng = old.length
  for (const i in old) {
    for (const j in news) {
      if (old[i] === news[j]) count++
    }
  }
  return count === leng
}

/**
 * 判断两个对象是否相同
 * @param a 要比较的对象一
 * @param b 要比较的对象二
 * @returns 相同返回 true，反之则反
 */
export function isObjectValueEqual(a: { [key: string]: any }, b: { [key: string]: any }) {
  if (!a || !b) return false
  const aProps = Object.getOwnPropertyNames(a)
  const bProps = Object.getOwnPropertyNames(b)
  if (aProps.length != bProps.length) return false
  for (let i = 0; i < aProps.length; i++) {
    const propName = aProps[i]
    const propA = a[propName]
    const propB = b[propName]
    if (!Object.prototype.hasOwnProperty.call(b, propName)) return false
    if (propA instanceof Object) {
      if (!isObjectValueEqual(propA, propB)) return false
    } else if (propA !== propB) {
      return false
    }
  }
  return true
}

/**
 * 移除并截断字符加...
 * @param data
 * @param len
 * @returns
 */
export const removeHtmlTag = (data: any, len: number) => {
  let str = data
  if (data) {
    str = str.replace(/<\/?[^>]*>/g, '') // 去除HTML tag
    str = str.replace(/[ | ]*\n/g, '\n') // 去除行尾空白
    str = str.replace(/\n[\s| | ]*\r/g, '\n') // 去除多余空行
    str = str.replace(/ /gi, '') // 去掉
    const arrEntities: any = { lt: '<', gt: '>', nbsp: ' ', amp: '&', quot: '"' } // 转义符换成普通字符
    str = str.replace(/&(lt|gt|nbsp|amp|quot);/gi, (_all: any, t: any) => {
      return arrEntities[t]
    })
    str = str.length > len ? `${str.slice(0, len)}...` : str
  }
  return str
}

/**
 * 获取随机小数
 */
export const getRandomNumber = () => {
  // eslint-disable-next-line no-loss-of-precision
  const num = Math.random() * 3.14159265358979323846 + 0.23
  return num.toFixed(10)
}

/**
 * 获取随机小数
 * @param min
 * @param max
 */
export const getRandomNum = (min: number, max: number) => {
  const Range = max - min
  const Rand = Math.random()
  return min + Math.round(Rand * Range)
}

/**
 * 获取随机字符串
 * @param len
 */
export const getRandomString = (len: number) => {
  len = len || 32
  const $chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678' // 默认去掉了容易混淆的字符oOLl,9gq,Vv,Uu,I1
  const maxPos = $chars.length
  let pwd = ''
  for (let i = 0; i < len; i++) {
    pwd += $chars.charAt(Math.floor(Math.random() * maxPos))
  }
  return pwd
}
