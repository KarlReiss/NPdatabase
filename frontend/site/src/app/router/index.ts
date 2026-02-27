import { createRouter, createWebHashHistory } from 'vue-router'
import { NO_RESET_WHITE_LIST } from '@/app/constants'
import { Layout } from '@/app/utils/routerHelper'
import { useI18n } from '@/app/hooks/web/useI18n'
import type { RouteRecordRaw } from 'vue-router'
import type { App } from 'vue'

const { t } = useI18n()

export const constantRouterMap: AppRouteRecordRaw[] = [
  {
    path: '/',
    name: 'Root',
    component: Layout,
    redirect: '/web/home',
    meta: {
      hidden: true
    }
  },
  {
    path: '/redirect',
    name: 'RedirectWrap',
    component: Layout,
    children: [
      {
        path: '/redirect/:path(.*)',
        name: 'Redirect',
        component: () => import('@/views/Redirect/Redirect.vue'),
        meta: {}
      }
    ],
    meta: {
      hidden: true,
      noTagsView: true
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login/Login.vue'),
    meta: {
      hidden: true,
      title: t('router.login'),
      noTagsView: true
    }
  },
  {
    path: '/404',
    component: () => import('@/views/Error/404.vue'),
    name: 'NoFind',
    meta: {
      hidden: true,
      title: '404',
      noTagsView: true
    }
  }
]

export const asyncRouterMap: AppRouteRecordRaw[] = [
  {
    path: '/web',
    name: 'Web',
    component: Layout,
    redirect: '/web/home',
    children: [
      {
        path: 'home',
        name: 'Home',
        component: () => import('@/views/CMS/Home.vue'),
        meta: { title: '探索天然产物与活性数据' }
      },
      {
        path: 'bio-resources',
        name: 'bioResourceList',
        component: () => import('@/views/CMS/BioResourceList.vue'),
        meta: { title: '生物资源列表' }
      },
      {
        path: 'bio-resources/:id',
        name: 'bioResourceDetail',
        component: () => import('@/views/CMS/BioResourceDetail.vue'),
        meta: { title: '生物资源' }
      },
      {
        path: 'prescriptions',
        name: 'prescriptionList',
        component: () => import('@/views/CMS/PrescriptionList.vue'),
        meta: { title: '处方列表' }
      },
      {
        path: 'prescriptions/:id',
        name: 'prescriptionDetail',
        component: () => import('@/views/CMS/PrescriptionDetail.vue'),
        meta: { title: '处方' }
      },
      {
        path: 'natural-products',
        name: 'naturalProductList',
        component: () => import('@/views/CMS/NaturalProductList.vue'),
        meta: { title: '化合物列表' }
      },
      {
        path: 'natural-products/:id',
        name: 'naturalProductDetail',
        component: () => import('@/views/CMS/NaturalProductDetail.vue'),
        meta: { title: '化合物' }
      },
      {
        path: 'targets',
        name: 'targetList',
        component: () => import('@/views/CMS/TargetList.vue'),
        meta: { title: '靶点列表' }
      },
      {
        path: 'targets/:id',
        name: 'targetDetail',
        component: () => import('@/views/CMS/TargetDetail.vue'),
        meta: { title: '靶点' }
      },
      {
        path: 'diseases',
        name: 'diseaseList',
        component: () => import('@/views/CMS/DiseaseList.vue'),
        meta: { title: '疾病列表' }
      },
      {
        path: 'diseases/:id',
        name: 'diseaseDetail',
        component: () => import('@/views/CMS/DiseaseDetail.vue'),
        meta: { title: '疾病' }
      },
      {
        path: 'topics',
        name: 'topicList',
        component: () => import('@/views/CMS/TopicList.vue'),
        meta: { title: '专题库' }
      },
      {
        path: 'topics/:id',
        name: 'topicDetail',
        component: () => import('@/views/CMS/TopicDetail.vue'),
        meta: { title: '专题库' }
      },
      {
        path: 'article-detail/:id',
        name: 'articleDetail',
        component: () => import('@/views/CMS/ArticleDetail.vue'),
        meta: { title: '' }
      }
    ]
  },
  // Legacy redirects for backward compatibility
  {
    path: '/compounds',
    name: 'compounds',
    redirect: '/web/natural-products',
    meta: {
      hidden: true,
      noTagsView: true
    }
  },
  {
    path: '/compounds/:id',
    name: 'compoundsId',
    redirect: (to) => `/web/natural-products/${to.params.id}`,
    meta: {
      hidden: true,
      noTagsView: true
    }
  },
  {
    path: '/resources',
    name: 'resources',
    redirect: '/web/bio-resources',
    meta: {
      hidden: true,
      noTagsView: true
    }
  },
  {
    path: '/resources/:id',
    name: 'resourcesId',
    redirect: (to) => `/web/bio-resources/${to.params.id}`,
    meta: {
      hidden: true,
      noTagsView: true
    }
  },
  {
    path: '/list',
    name: 'list',
    redirect: '/web/natural-products',
    meta: {
      hidden: true,
      noTagsView: true
    }
  },
  {
    path: '/detail/:id',
    name: 'detail',
    redirect: (to) => `/web/natural-products/${to.params.id}`,
    meta: {
      hidden: true,
      noTagsView: true
    }
  },
  // {
  //   path: '/dashboard', name: 'Dashboard', component: Layout, redirect: '/dashboard/analysis', meta: { title: t('router.dashboard'), icon: 'vi-ant-design:dashboard-filled', alwaysShow: true },
  //   children: [
  //     { path: 'analysis', name: 'Analysis', component: () => import('@/views/Dashboard/Analysis.vue'), meta: { title: t('router.analysis'), noCache: true, affix: true } },
  //     { path: 'workplace', name: 'Workplace', component: () => import('@/views/Dashboard/Workplace.vue'), meta: { title: t('router.workplace'), noCache: true } }
  //   ]
  // },
  {
    path: '/error',
    name: 'Error',
    redirect: '/error/404',
    component: Layout,
    meta: {
      title: t('router.errorPage'),
      icon: 'vi-ci:error',
      alwaysShow: true
    },
    children: [
      {
        path: '404-demo',
        name: '404Demo',
        component: () => import('@/views/Error/404.vue'),
        meta: { title: '404' }
      },
      {
        path: '403-demo',
        name: '403Demo',
        component: () => import('@/views/Error/403.vue'),
        meta: { title: '403' }
      },
      {
        path: '500-demo',
        name: '500Demo',
        component: () => import('@/views/Error/500.vue'),
        meta: { title: '500' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  strict: true,
  routes: constantRouterMap as RouteRecordRaw[],
  scrollBehavior: () => ({ left: 0, top: 0 })
})

export const resetRouter = (): void => {
  router.getRoutes().forEach((route) => {
    const { name } = route
    if (name && !NO_RESET_WHITE_LIST.includes(name as string)) {
      router.hasRoute(name) && router.removeRoute(name)
    }
  })
}

export const setupRouter = (app: App<Element>) => {
  app.use(router)
}

export default router
