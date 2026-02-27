import { UserLoginType, UserType } from '@/app/api/login/types'
import { EventsConfigs } from '@/app/hooks/event/event'
import { useI18n } from '@/app/hooks/web/useI18n'
import { useTagsViewStore } from './tagsView'
import { ElMessageBox } from 'element-plus'
import { loginOutApi } from '@/app/api/login'
import { defineStore } from 'pinia'
import { store } from '../index'
import router from '@/app/router'

interface UserState {
  userInfo?: UserType
  tokenKey: string
  token: string
  roleRouters?: string[] | AppCustomRouteRecordRaw[]
  rememberMe: boolean
  loginInfo?: UserLoginType
}

export const useUserStore = defineStore(EventsConfigs.pinia.user, {
  state: (): UserState => {
    return {
      userInfo: undefined,
      tokenKey: 'Authorization',
      token:
        'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiSm9obiIsImFkbWluIjp0cnVlLCJpc3MiOiJpc3MiLCJleHAiOjI1OTEzNjY0MDAsInN1YiI6Inh4eHh4eHh4LXh4eHgteHh4eC14eHh4LXh4eHh4eHh4eHh4eCIsImF1ZCI6Inh4eHh4eHh4LXh4eHgteHh4eC14eHh4LXh4eHh4eHh4eHh4eCIsIm5iZiI6MTc3MDk3MjQxNywiaWF0IjoxNzcwOTcyNDExLCJqdGkiOiJ4eHh4eHh4eC14eHh4LXh4eHgteHh4eC14eHh4eHh4eHh4eHgifQ.58YNMXUXID91BjXESkBoXPgXStzazxplRXw6LuXn7kUAUpBvSftP10evSbFBjwGG1_MPTsl1TnIByAAwBBrOyg',
      roleRouters: undefined,
      // 记住我
      rememberMe: true,
      loginInfo: undefined
    }
  },
  getters: {
    getTokenKey(): string {
      return this.tokenKey
    },
    getToken(): string {
      return this.token
    },
    getUserInfo(): UserType | undefined {
      return this.userInfo
    },
    getRoleRouters(): string[] | AppCustomRouteRecordRaw[] | undefined {
      return this.roleRouters
    },
    getRememberMe(): boolean {
      return this.rememberMe
    },
    getLoginInfo(): UserLoginType | undefined {
      return this.loginInfo
    }
  },
  actions: {
    setTokenKey(tokenKey: string) {
      this.tokenKey = tokenKey
    },
    setToken(token: string) {
      this.token = token
    },
    setUserInfo(userInfo?: UserType) {
      this.userInfo = userInfo
    },
    setRoleRouters(roleRouters: string[] | AppCustomRouteRecordRaw[]) {
      this.roleRouters = roleRouters
    },
    logoutConfirm() {
      const { t } = useI18n()
      ElMessageBox.confirm(t('common.loginOutMessage'), t('common.reminder'), {
        confirmButtonText: t('common.ok'),
        cancelButtonText: t('common.cancel'),
        type: 'warning'
      })
        .then(async () => {
          const res = await loginOutApi().catch(() => {})
          if (res) {
            this.reset()
          }
        })
        .catch(() => {})
    },
    reset() {
      const tagsViewStore = useTagsViewStore()
      tagsViewStore.delAllViews()
      this.setToken('')
      this.setUserInfo(undefined)
      this.setRoleRouters([])
      router.replace('/login')
    },
    logout() {
      this.reset()
    },
    setRememberMe(rememberMe: boolean) {
      this.rememberMe = rememberMe
    },
    setLoginInfo(loginInfo: UserLoginType | undefined) {
      this.loginInfo = loginInfo
    }
  },
  persist: true
})

export const useUserStoreWithOut = () => {
  return useUserStore(store)
}
