import type { App } from 'vue'
import { Icon } from './Icon'
import { BaseButton } from './Button'
import { Pagination } from './Pagination'
import { Image } from './Image'

export const setupGlobCom = (app: App<Element>): void => {
  app.component('Icon', Icon)
  app.component('BaseButton', BaseButton)
  app.component('Pagination', Pagination)
  app.component('Image', Image)
}
