// 获取传入的值的类型
const getValueType = (value: any) => {
  const type = Object.prototype.toString.call(value)
  return type.slice(8, -1)
}

export const useStorage = (type: 'sessionStorage' | 'localStorage' = 'localStorage') => {
  const setStorage = (key: string, value: any) => {
    const valueType = getValueType(value)
    window[type].setItem(`app.wsStorage.${type}:${key}`, JSON.stringify({ type: valueType, value }))
  }

  const getStorage = (key: string) => {
    const value = window[type].getItem(`app.wsStorage.${type}:${key}`)
    if (value) {
      const { value: val } = JSON.parse(value)
      return val
    } else {
      return value
    }
  }

  const removeStorage = (key: string) => {
    window[type].removeItem(`app.wsStorage.${type}:${key}`)
  }

  const clear = (excludes?: string[]) => {
    // 获取排除项
    const keys = Object.keys(window[type])
    const defaultExcludes = ['dynamicRouter', 'serverDynamicRouter']
    const excludesArr = excludes ? [...excludes, ...defaultExcludes] : defaultExcludes
    const excludesKeys = excludesArr ? keys.filter((key) => !excludesArr.includes(key)) : keys
    // 排除项不清除
    excludesKeys.forEach((key) => {
      window[type].removeItem(`app.wsStorage.locales:${key}`)
    })
    // window[type].clear()
  }

  return {
    setStorage,
    getStorage,
    removeStorage,
    clear
  }
}
