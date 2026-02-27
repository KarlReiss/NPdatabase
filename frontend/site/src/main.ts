import { setupPermission, setupTableHeight } from './app/directives'
import { setupElementPlus } from '@/app/plugins/elementPlus'
import { setupI18n } from '@/app/plugins/vueI18n'
import { setupGlobCom } from '@/components'
import { setupRouter } from '@/app/router'
import { setupStore } from '@/store'
import '@/assets/styles/index.less'
import '@/app/plugins/animate.css'
import { createApp } from 'vue'
import '@/app/plugins/svgIcon'
import '@/app/plugins/unocss'
import App from './App.vue'
import './permission'
import 'vue/jsx'

import { set } from 'lodash-es'
const { initRDKitModule } = window as any
if (initRDKitModule) {
  initRDKitModule()
    .then(function (RDKit) {
      console.log('RDKit version: ' + RDKit.version())
      set(window, 'RDKit', RDKit)
    })
    .catch(() => {
      // handle loading errors here...
    })
}
import { fetchHealth } from '@/app/api/cms/common'
const fetchAll = async () => {
  try {
    const headlthPromise = fetchHealth()
    const [headlthResult] = await Promise.allSettled([headlthPromise])

    if (headlthResult.status === 'fulfilled') {
      console.log(headlthResult.value)
    } else {
      throw headlthResult.reason
    }
  } catch (err) {
    console.error(err instanceof Error ? err.message : '数据加载失败')
  }
}

const setupAll = async () => {
  const app = createApp(App)
  await setupI18n(app)
  setupStore(app)
  setupGlobCom(app)
  setupElementPlus(app)
  setupRouter(app)
  setupPermission(app)
  setupTableHeight(app)
  app.mount('#app')
  await fetchAll()
}

console.warn = () => {}
setTimeout(() => {
  document.body.classList.remove('preload')
  setupAll()
}, 1234)
