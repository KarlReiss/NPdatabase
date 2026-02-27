<script setup lang="ts">
import { useDesign } from '@/app/hooks/web/useDesign'
import { propTypes } from '@/app/utils/propTypes'
import { ref, unref, watch } from 'vue'

const { getPrefixCls } = useDesign()
const prefixCls = getPrefixCls('cus-tab-menu')

const props = defineProps({
  tabs: propTypes.any.def([]),
  modelValue: propTypes.string.def('')
})

watch(
  () => props.modelValue,
  (val: string) => {
    if (val === '') {
      if (props.tabs.length > 0) {
        valueRef.value = props.tabs[0].value
        return
      }
      return
    }
    if (val === unref(valueRef)) return
    valueRef.value = val
  }
)

const emit = defineEmits(['update:modelValue'])

// 输入框的值
const valueRef = ref(props.modelValue)

// 监听
watch(
  () => valueRef.value,
  (val: string) => {
    emit('update:modelValue', val)
  }
)
</script>

<template>
  <div :class="[prefixCls]" class="flex border-b border-[#E2E8F0] pt-3 px-3 space-x-2">
    <span
      v-for="tab in tabs"
      :key="tab.value"
      @click="valueRef = tab.value"
      :class="[
        'px-4 py-3 text-sm font-medium rounded-[16px_16px_0_0] overflow-hidden transition-all relative cursor-pointer',
        valueRef === tab.value
          ? 'text-[var(--el-color-primary)] bg-[#E1F3F8] border-bottom-[1px_solid_var(--el-color-primary)]'
          : 'text-slate-500 hover:text-slate-700 bg-[#f1f1f1]'
      ]"
      :style="`${valueRef == tab.value ? 'border-left: 4px solid var(--el-color-primary); border-bottom:2px solid var(--el-color-primary)' : 'border-left: 4px solid #f1f1f1; border-bottom:2px solid #f1f1f1'}`"
    >
      {{ tab.label }} <span class="text-[11px] opacity-60">({{ tab.count }})</span>
    </span>
  </div>
</template>

<style lang="less" scoped></style>
