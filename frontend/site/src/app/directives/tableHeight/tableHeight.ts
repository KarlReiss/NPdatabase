import { vhToPx } from '@/app/utils'
import type { App } from 'vue'
import { nextTick } from 'vue'

/**
 * ! TODO 低版本浏览器不支持 ResizeObserver
 * 监听同级dom元素高度变化
 */
const heightChangeHandler = (entries: ResizeObserverEntry[], el: any, binding: any, vnode: any) => {
  setHeight(el, binding, vnode)
}

let heightChangeObserver: any = null
/**
 * 查找同级组件, 获取高度
 */
function findElement(el: any, sibling: any) {
  if (el === null || el === undefined) {
    return 0
  }
  const element = el[sibling]
  if (element === null || element === undefined) {
    return 0
  }
  const classStr = element.className
  if (classStr.includes('el-overlay')) {
    return 0
  }
  /* 获取元素margin值 */
  if (element) {
    const style = window.getComputedStyle(element)
    const marginTop = parseInt(style.marginTop) || 0
    const marginBottom = parseInt(style.marginBottom) || 0
    let height = element.offsetHeight || 0
    if (element) {
      height += findElement(element, sibling)
    }
    return height + marginTop + marginBottom
  }
  return 0
}

/**
 * 计算高度
 * @param {*} el
 * @param {*} binding
 */
function setHeight(el: any, binding: any, vnode: any) {
  nextTick(() => {
    let diffValue = 0
    if (binding.value) {
      diffValue = binding.value.diffValue || 0
    }
    let previousElementSiblingHeight = 0
    if (el.previousElementSibling) {
      previousElementSiblingHeight += findElement(el, 'previousElementSibling')
    }
    let nextElementSiblingHeight = 0
    if (el.nextElementSibling) {
      nextElementSiblingHeight += findElement(el, 'nextElementSibling')
    }

    const isDialog = binding.arg === 'dialog'
    let height =
      90 + 64 + 48 + 100 + 52 + nextElementSiblingHeight + previousElementSiblingHeight + diffValue
    if (nextElementSiblingHeight) {
      height += 20
    }
    if (isDialog) {
      height = 100 + 40 + 62 + nextElementSiblingHeight + previousElementSiblingHeight + diffValue
    }
    const fullVh = isDialog ? 78 : 100
    if (el.offsetHeight >= vhToPx(fullVh) - height - 20) {
      el.style.height = `${isDialog ? 'calc(78vh - ' : 'calc(100vh - '}${height}px)`
    } else {
      el.style.height = 'auto'
    }
  })

  /* const table = el.querySelector('.el-table') */
  /* if (!table) return */

  /* const viewportHeight = window.innerHeight */
  /* const tableTopOffset = 85 // 表头的高度 */
  /* const tableBottomOffset = 78 // 表格底部工具栏的高度 */
  /* const maxHeight = viewportHeight - tableTopOffset - tableBottomOffset */
  /* vnode.context.maxHeight.value = maxHeight */
}

export const setupTableHeightDirective = (app: App<Element>) => {
  /**
   * @description 动态计算el-table高度
   * @param {*} el
   * @param {*} binding
   */
  app.directive('tableHeight', {
    mounted(el: any, binding: any, vnode: any) {
      const siblings = Array.from(el.parentNode?.children || []).filter((child) => child !== el)

      heightChangeObserver = new ResizeObserver((entries) => {
        heightChangeHandler(entries, el, binding, vnode)
      })
      /* 将同级元素添加到 Resize Observer 中进行监听 */
      siblings.forEach((sibling: any) => {
        if (!sibling.className.includes('el-overlay')) {
          heightChangeObserver.observe(sibling)
        }
      })
      /* window.addEventListener('resize', () => { setHeight(el, binding, vnode) }) */
      setHeight(el, binding, vnode)
    },
    updated(el: any, binding: any, vnode: any) {
      setHeight(el, binding, vnode)
    },
    unmounted(el: any, binding: any, vnode: any) {
      /* window.removeEventListener('resize', () => { setHeight(el, binding, vnode) }) */
      /* 停止监听同级元素并解除绑定 */
      heightChangeObserver.disconnect()
    }
  })
}
