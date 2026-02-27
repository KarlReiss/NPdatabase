<script setup lang="ts">
import { ConfigGlobal } from '@/components/ConfigGlobal'
import { useDesign } from '@/app/hooks/web/useDesign'
import { useAppStore } from '@/store/modules/app'
import { computed } from 'vue'

const { getPrefixCls } = useDesign()
const prefixCls = getPrefixCls('app')
const appStore = useAppStore()
const currentSize = computed(() => appStore.getCurrentSize)
const greyMode = computed(() => appStore.getGreyMode)

// import { useWatermark } from '@/app/hooks/web/useWatermark'
// const { setWatermark, clear } = useWatermark()
// if (['base', 'dev', 'test'].includes(import.meta.env.MODE)) {
//   setWatermark(`${import.meta.env.VITE_APP_TITLE}-测试端`)
// } else { clear() }

// appStore.initTheme()
// 根据浏览器当前主题设置系统主题色
const setDefaultTheme = () => {
  appStore.setIsDark(false)
}
// setDefaultTheme()
</script>

<template>
  <ConfigGlobal :size="currentSize">
    <RouterView :class="greyMode ? `${prefixCls}-grey-mode` : ''" />
  </ConfigGlobal>
</template>

<style lang="less">
@prefix-cls: ~'@{adminNamespace}-app';

.size {
  width: 100%;
  height: 100%;
}

html,
body {
  padding: 0 !important;
  margin: 0;
  overflow: hidden;
  .size;
  #app {
    .size;
  }
}

.@{prefix-cls}-grey-mode {
  filter: grayscale(100%);
}
</style>
