<template>
  <div class="max-w-[1200px] mx-auto px-6 py-8">
    <nav class="text-xs text-slate-500 mb-6 flex items-center space-x-2">
      <RouterLink to="/" class="hover:text-[#10B981]">首页</RouterLink>
      <span>/</span>
      <RouterLink to="/topics" class="hover:text-[#10B981]">专题库</RouterLink>
      <span>/</span>
      <span class="text-slate-700 font-medium">{{ topic.name }}</span>
    </nav>

    <section class="bg-white rounded-md border border-[#E2E8F0] shadow-sm p-8 min-h-[220px] mb-6">
      <h1 class="text-2xl font-bold text-slate-800">{{ topic.name }}</h1>
      <p class="text-sm text-slate-500 mt-2">{{ topic.description }}</p>
    </section>

    <section class="bg-white rounded-md border border-[#E2E8F0] shadow-sm p-6 text-sm text-slate-500">
      专题数据与筛选逻辑将在后续补充。
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const topics = [
  { id: 'anti-tumor', name: '抗肿瘤', description: '按靶点/活性筛选的抗肿瘤专题' },
  { id: 'cardiovascular', name: '心脑血管', description: '心脑血管相关靶点与天然产物' },
  { id: 'toxic-herbs', name: '有毒药材', description: '包含毒性记录的天然产物与来源' },
  { id: 'anti-inflammatory', name: '抗炎免疫', description: '炎症相关靶点与活性数据' },
];

const topic = computed(() => {
  const id = String(route.params.id || '');
  return topics.find((item) => item.id === id) ?? topics[0];
});
</script>
