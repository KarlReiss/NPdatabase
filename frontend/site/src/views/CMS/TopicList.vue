<template>
  <div class="max-w-[1440px] mx-auto px-6 py-10">
    <nav
      class="text-xs text-slate-500 mb-5 flex items-center space-x-2 bg-[#f1f1f1] dark:bg-[var(--el-bg-color)] p-4 rounded-1"
    >
      <RouterLink
        to="/"
        class="color-[#212121] dark:color-white hover:color-[var(--el-color-primary)] select-none no-underline hover:no-underline"
        >首页</RouterLink
      >
      <span class="dark:color-white">></span>
      <span class="text-slate-700 font-medium">专题库</span>
    </nav>

    <h1 class="text-2xl font-bold text-slate-800 mb-6">专题库</h1>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <RouterLink
        v-for="topic in topicList"
        :key="topic.id"
        :to="`/web/topics/${topic.id}`"
        class="bg-white p-6 select-none no-underline hover:no-underline"
        :class="[
          'bg-[#EBEBEB] pl-7.5 py-7.5 pr-26 rounded-md overflow-hidden border border-gray-100',
          'shadow-sm hover:shadow-md hover:-translate-y-1 duration-300 group',
          'relative cursor-pointer transition-all'
        ]"
      >
        <div
          class="absolute top-9 right-7.5 w-13.5 h-13.5 rounded-lg flex items-center justify-center"
        >
          <Icon :icon="topic.icon" :size="54" class="mr-10px" />
        </div>
        <h3 class="text-6 leading-7 text-slate-800 font-bold mb-1">{{ topic.label }}</h3>
        <p class="text-sm leading-7 text-[#0033BD] font-medium mb-2">{{ topic.value }}</p>
        <p class="text-xs leading-7 text-slate-500">{{ topic.bref }}</p>

        <div class="absolute bottom-0 left-0 right-0 h-2 bg-[var(--el-color-primary)]"></div>
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue'

const topics = [
  {
    id: 'anti-tumor',
    name: '抗肿瘤',
    en: 'Anti-tumor',
    description: '按靶点/活性筛选的抗肿瘤专题'
  },
  {
    id: 'cardiovascular',
    name: '心脑血管',
    en: 'Cardiovascular',
    description: '心脑血管相关靶点与天然产物'
  },
  {
    id: 'toxic-herbs',
    name: '有毒药材',
    en: 'Toxic Herbs',
    description: '包含毒性记录的天然产物与来源'
  },
  {
    id: 'anti-inflammatory',
    name: '抗炎免疫',
    en: 'Anti-inflammatory',
    description: '炎症相关靶点与活性数据'
  }
]

const topicList = computed(() => {
  return [
    {
      id: 'anti-tumor',
      icon: 'svg-icon:anti-tumor',
      label: '抗肿瘤（Anti-tumor）',
      en: 'Anti-tumor',
      value: '1,245+ 个化合物',
      bref: '浏览具有抗肿瘤活性的天然产物集合。'
    },
    {
      id: 'cardiovascular',
      icon: 'svg-icon:cardiovascular',
      label: '心脑血管（Cardiovascular）',
      en: 'Cardiovascular',
      value: '892+ 个化合物',
      bref: '探索心脑血管相关靶点的活性天然产物。'
    },
    {
      id: 'toxic-herbs',
      icon: 'svg-icon:toxic-herbs',
      label: '有毒药材（Toxic Herbs）',
      en: 'Toxic Herbs',
      value: '310+ 条记录',
      bref: '传统用药的毒性与安全性信息汇总。'
    },
    {
      id: 'anti-inflammatory',
      icon: 'svg-icon:anti-tumor',
      label: '抗炎免疫（Anti-inflammatory）',
      en: 'Anti-inflammatory',
      value: '176+ 条记录',
      bref: '炎症相关靶点与活性数据'
    }
  ]
})

const tableRef = ref()
const pager = reactive<any>({
  currentPage: 1,
  pageSize: 10,
  totalCount: 0,
  fristLoading: true,
  isLoading: true,
  dataList: []
})

const currentChange = (page: number) => {
  pager.currentPage = page
  onQueryList()
}

const sizeChange = (size: number) => {
  pager.currentPage = 1
  pager.pageSize = size
  onQueryList()
}

/**
 * 列表
 */
const onQueryList = (isLoading: boolean = true): void => {
  const query = {
    maxResultCount: pager.pageSize,
    skipCount: (pager.currentPage - 1) * pager.pageSize
  }
  pager.isLoading = isLoading
  pager.isLoading = false
}
</script>

<style lang="less" scoped>
.header-search {
  :deep(.el-input-group__append),
  :deep(.el-input-group__prepend) {
    background-color: var(--el-color-primary);
    cursor: pointer;
  }
}
:deep(.el-collapse) {
  border-top-width: 0;
  border-bottom-width: 0;
}
:deep(.el-collapse-item__wrap) {
  border-bottom-width: 0;
}
:deep(.el-collapse-item__header) {
  font-size: 16px;
  font-weight: bold;
  border-bottom-width: 0;
  justify-content: space-between;
}
:deep(.el-collapse-item__content) {
  padding-bottom: 0;
}
</style>
