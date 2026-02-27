<script setup lang="ts">
import { useAppStore } from '@/store/modules/app'
import { propTypes } from '@/app/utils/propTypes'
import { PropType, computed } from 'vue'

const props = defineProps({
  fixed: propTypes.bool.def(false),
  pagerCount: propTypes.number.def(5),
  page: propTypes.number.def(1),
  total: propTypes.number.def(0),
  limit: propTypes.number.def(10),
  layout: propTypes.string.def('sizes,prev, pager, next, ->, total, jumper'),
  pageSizes: {
    type: Array as PropType<number[]>,
    default: () => [10, 20, 30, 40, 50, 100]
  }
})

const changePage = computed(() => {
  return props.page
})

const emit = defineEmits(['changePage', 'changeSize', 'disabled-click'])
const appStore = useAppStore() as any

/**
 * 翻页事件
 * @param page
 */
const currentChange = (page: number) => {
  emit('changePage', page)
}

const sizeChange = (size: number) => {
  emit('changeSize', size)
}
</script>
<template>
  <div
    :class="{ fixedPage: fixed }"
    :style="
      !fixed
        ? 'margin: 10px;'
        : appStore.getCollapse
          ? `bottom: ${appStore.getFooter ? '50px' : '0px'};left: ${
              appStore.getMobile ? '20px' : '86px'
            } !important; margin-bottom: 10px;`
          : `bottom: ${appStore.getFooter ? '50px' : '0px'};left: ${
              appStore.getMobile ? '20px' : '220px'
            } !important; margin-bottom: 10px;`
    "
  >
    <el-pagination
      v-model:current-page="changePage"
      :small="false"
      background
      :pagerCount="pagerCount"
      :layout="layout"
      :page-sizes="pageSizes"
      :disabled="false"
      :hideOnSinglePage="false"
      :total="total"
      :page-size="limit"
      @size-change="sizeChange"
      @current-change="currentChange"
    />
  </div>
</template>
<style lang="less" scoped></style>
