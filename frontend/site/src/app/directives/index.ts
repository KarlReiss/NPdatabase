import type { App } from 'vue'
import { setupPermissionDirective } from './permission/hasPermi'
import { setupTableHeightDirective } from './tableHeight/tableHeight'

/**
 * 导出指令：v-xxx
 * @methods hasPermi 按钮权限，用法: v-hasPermi
 */
export const setupPermission = (app: App<Element>) => {
  setupPermissionDirective(app)
}

/**
 * 导出指令：v-xxx
 * @methods tableHeight 按钮权限，用法: v-tableHeight
 */
export const setupTableHeight = (app: App<Element>) => {
  setupTableHeightDirective(app)
}
