import { usePermissionStoreWithOut } from '@/store/modules/permission'
import { usePageLoading } from '@/app/hooks/web/usePageLoading'
// import { useAppStoreWithOut } from '@/store/modules/app'
import { useNProgress } from '@/app/hooks/web/useNProgress'
import { useUserStoreWithOut } from '@/store/modules/user'
import { NO_REDIRECT_WHITE_LIST } from '@/app/constants'
import { useTitle } from '@/app/hooks/web/useTitle'
import { type RouteRecordRaw } from 'vue-router'
import router from '@/app/router'

const { start, done } = useNProgress()
const { loadStart, loadDone } = usePageLoading()

router.beforeEach(async (to, from, next) => {
  start()
  loadStart()
  const permissionStore = usePermissionStoreWithOut()
  const userStore = useUserStoreWithOut()
  /* const appStore = useAppStoreWithOut() */
  if (userStore.getUserInfo) {
    if (to.path === '/login') {
      next({ path: '/' })
    } else {
      if (permissionStore.getIsAddRouters) {
        next()
        return
      }

      await permissionStore.generateRoutes('static')

      permissionStore.getAddRouters.forEach((route) => {
        router.addRoute(route as unknown as RouteRecordRaw) /* 动态添加可访问路由表 */
      })
      const redirectPath = from.query.redirect || to.path
      const redirect = decodeURIComponent(redirectPath as string)
      const nextData = to.path === redirect ? { ...to, replace: true } : { path: redirect }
      permissionStore.setIsAddRouters(true)
      next(nextData)
    }
  } else {
    if (NO_REDIRECT_WHITE_LIST.indexOf(to.path) !== -1) {
      next()
    } else {
      // 暂时没登录写死
      userStore.setUserInfo({
        username: 'guo',
        password: 'password',
        role: 'role',
        roleId: 'roleId'
      })
      await permissionStore.generateRoutes('static')
      permissionStore.getAddRouters.forEach((route) => {
        router.addRoute(route as unknown as RouteRecordRaw) /* 动态添加可访问路由表 */
      })
      permissionStore.setIsAddRouters(true)
      setTimeout(() => {
        /* 否则全部重定向到登录页 */
        location.href = `#/web/home`
        // next(`/web/home`)
      }, 1200)
      // next(`/login?redirect=${to.path}`) /* 否则全部重定向到登录页 */
    }
  }
})

router.afterEach((to) => {
  useTitle(to?.meta?.title as string)
  done() /* 结束Progress */
  loadDone()
})
