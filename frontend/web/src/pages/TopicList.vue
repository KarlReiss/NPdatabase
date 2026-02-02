<template>
  <div class="max-w-[1200px] mx-auto px-6 py-10">
    <nav class="text-xs text-slate-500 mb-6 flex items-center space-x-2">
      <RouterLink to="/" class="hover:text-[#10B981]">首页</RouterLink>
      <span>/</span>
      <span class="text-slate-700 font-medium">专题库</span>
    </nav>

    <h1 class="text-2xl font-bold text-slate-800 mb-6">专题库</h1>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <RouterLink
        v-for="topic in topics"
        :key="topic.id"
        :to="`/topics/${topic.id}`"
        class="bg-white p-6 rounded-md shadow-sm border border-gray-100 hover:shadow-md transition-all"
      >
        <div class="text-sm text-slate-500">{{ topic.en }}</div>
        <div class="text-lg font-bold text-slate-800 mt-1">{{ topic.name }}</div>
        <div class="text-xs text-slate-400 mt-2">{{ topic.description }}</div>
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
const topics = [
  { id: 'anti-tumor', name: '抗肿瘤', en: 'Anti-tumor', description: '按靶点/活性筛选的抗肿瘤专题' },
  { id: 'cardiovascular', name: '心脑血管', en: 'Cardiovascular', description: '心脑血管相关靶点与天然产物' },
  { id: 'toxic-herbs', name: '有毒药材', en: 'Toxic Herbs', description: '包含毒性记录的天然产物与来源' },
  { id: 'anti-inflammatory', name: '抗炎免疫', en: 'Anti-inflammatory', description: '炎症相关靶点与活性数据' },
];
</script>
