import { LocaleDropdownType } from '@/components/LocaleDropdown'
import { EventsConfigs } from '@/app/hooks/event/event'
import { useStorage } from '@/app/hooks/web/useStorage'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import en from 'element-plus/es/locale/lang/en'
import { defineStore } from 'pinia'
import { store } from '../index'
const { getStorage, setStorage } = useStorage('localStorage')

const elLocaleMap = {
  'zh-CN': zhCn,
  en: en
}
interface LocaleState {
  currentLocale: LocaleDropdownType
  localeMap: LocaleDropdownType[]
}

export const useLocaleStore = defineStore(EventsConfigs.pinia.locales, {
  state: (): LocaleState => {
    return {
      currentLocale: {
        lang: getStorage('lang') || 'zh-CN',
        elLocale: elLocaleMap[getStorage('lang') || 'zh-CN']
      },
      // 多语言
      localeMap: [
        {
          lang: 'zh-CN',
          name: '简体中文'
        },
        {
          lang: 'en',
          name: 'English'
        }
      ]
    }
  },
  getters: {
    getCurrentLocale(): LocaleDropdownType {
      return this.currentLocale
    },
    getLocaleMap(): LocaleDropdownType[] {
      return this.localeMap
    }
  },
  actions: {
    setCurrentLocale(localeMap: LocaleDropdownType) {
      // this.locale = Object.assign(this.locale, localeMap)
      this.currentLocale.lang = localeMap?.lang
      this.currentLocale.elLocale = elLocaleMap[localeMap?.lang]
      setStorage('lang', localeMap?.lang)
    }
  }
})

export const useLocaleStoreWithOut = () => {
  return useLocaleStore(store)
}
