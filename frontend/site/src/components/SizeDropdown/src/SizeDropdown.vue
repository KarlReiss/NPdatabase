<script setup lang="ts">
import { ElDropdown, ElDropdownMenu, ElDropdownItem, ComponentSize } from 'element-plus'
import { useDesign } from '@/app/hooks/web/useDesign'
import { useAppStore } from '@/store/modules/app'
import { useI18n } from '@/app/hooks/web/useI18n'
import { propTypes } from '@/app/utils/propTypes'
import { computed } from 'vue'

const { getPrefixCls } = useDesign()

const prefixCls = getPrefixCls('size-dropdown')

defineProps({
  color: propTypes.string.def('')
})

const { t } = useI18n()

const appStore = useAppStore()

const sizeMap = computed(() => appStore.sizeMap)

const setCurrentSize = (size: ComponentSize) => {
  appStore.setCurrentSize(size)
}
</script>

<template>
  <ElDropdown :class="prefixCls" trigger="click" @command="setCurrentSize">
    <Icon :size="18" icon="vi-mdi:format-size" :color="color" class="cursor-pointer" />
    <template #dropdown>
      <ElDropdownMenu>
        <ElDropdownItem v-for="item in sizeMap" :key="item" :command="item">
          {{ t(`size.${item}`) }}
        </ElDropdownItem>
      </ElDropdownMenu>
    </template>
  </ElDropdown>
</template>
