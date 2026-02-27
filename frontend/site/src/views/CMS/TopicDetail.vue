<template>
  <div class="max-w-[1440px] mx-auto px-6 py-6">
    <nav
      class="text-xs text-slate-500 mb-5 flex items-center space-x-2 bg-[#f1f1f1] dark:bg-[var(--el-bg-color)] p-4 rounded-1"
    >
      <RouterLink
        to="/"
        class="color-[#212121] dark:color-white hover:color-[var(--el-color-primary)] select-none no-underline hover:no-underline"
        >首页</RouterLink
      >
      <span class="dark:color-white">></span>
      <RouterLink
        to="/web/topics"
        class="text-[var(--el-color-primary)] hover:text-[var(--el-color-primary)] select-none no-underline hover:no-underline"
        >专题库</RouterLink
      >
      <span class="dark:color-white">></span>
      <span class="text-slate-700 font-medium select-none">{{ topic.label }}</span>
    </nav>

    <section
      class="bg-white rounded-md border dark:bg-[var(--el-bg-color)] border-[#E2E8F0] shadow-sm p-8 min-h-[220px] mb-6"
    >
      <h1 class="text-2xl font-bold text-slate-800">{{ topic.label }}</h1>
      <p class="text-sm leading-7 text-[#0033BD] font-medium mb-2">{{ topic.value }}</p>
      <p class="text-sm text-slate-500 mt-2">{{ topic.bref }}</p>
    </section>

    <section
      class="bg-white rounded-md border dark:bg-[var(--el-bg-color)] border-[#E2E8F0] shadow-sm p-6 text-sm text-slate-500"
    >
      专题数据与筛选逻辑将在后续补充。
    </section>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { computed } from 'vue'
const route = useRoute()

const topicList = computed(() => {
  return [
    {
      id: 'anti-tumor',
      icon: 'svg-icon:anti-tumor',
      label: '抗肿瘤（Anti-tumor）',
      value: '1,245+ 个化合物',
      bref: '浏览具有抗肿瘤活性的天然产物集合。'
    },
    {
      id: 'cardiovascular',
      icon: 'svg-icon:cardiovascular',
      label: '心脑血管（Cardiovascular）',
      value: '892+ 个化合物',
      bref: '探索心脑血管相关靶点的活性天然产物。'
    },
    {
      id: 'toxic-herbs',
      icon: 'svg-icon:toxic-herbs',
      label: '有毒药材（Toxic Herbs）',
      value: '310+ 条记录',
      bref: '传统用药的毒性与安全性信息汇总。'
    },
    {
      id: 'anti-inflammatory',
      icon: 'svg-icon:anti-tumor',
      label: '抗炎免疫（Anti-inflammatory）',
      value: '176+ 条记录',
      bref: '炎症相关靶点与活性数据'
    }
  ]
})

const topic = computed(() => {
  const id = String(route.params.id || '')
  return topicList.value.find((item) => item.id === id) ?? topicList.value[0]
})
</script>
