<template>
  <header class="h-16 bg-white border-b border-[#E2E8F0] sticky top-0 z-50">
    <div class="max-w-[1440px] mx-auto h-full px-6 flex items-center gap-6">
      <div class="flex items-center space-x-2">
        <div class="w-8 h-8 bg-[#10B981] rounded-md flex items-center justify-center">
          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
            />
          </svg>
        </div>
        <span class="text-[#1E293B] text-lg font-bold tracking-tight">云南天然产物活性数据库</span>
      </div>

      <div class="hidden lg:flex flex-1 justify-center">
        <div class="relative w-full max-w-[520px]">
          <input
            type="text"
            placeholder="快速搜索..."
            class="w-full h-10 pl-10 pr-4 bg-white border border-[#E2E8F0] rounded-md text-sm text-slate-700 focus:outline-none focus:ring-0"
          />
          <svg class="w-4 h-4 absolute left-3 top-3 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>

      <nav class="hidden lg:flex items-center space-x-6 text-[14px] ml-auto">
        <RouterLink
          v-for="item in navItems"
          :key="item.name"
          :to="item.to"
          :class="[
            'hover:text-[#10B981] transition-colors duration-200',
            isActive(item) ? 'text-[#10B981] font-medium' : 'text-[#334155]'
          ]"
        >
          {{ item.name }}
        </RouterLink>

        <div class="h-4 w-px bg-gray-300 mx-2"></div>
        <div class="flex items-center space-x-2 cursor-pointer group">
          <div class="w-8 h-8 rounded-full bg-slate-200 border border-slate-300 flex items-center justify-center overflow-hidden">
            <img src="https://picsum.photos/32/32" alt="Avatar" />
          </div>
          <span class="text-[#334155] group-hover:text-[#10B981]">Dr. Research</span>
        </div>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';

const route = useRoute();

const navItems = [
  { name: '首页', to: { path: '/' } },
  { name: '生物资源', to: { path: '/resources' } },
  { name: '天然产物', to: { path: '/compounds' } },
  { name: '处方', to: { path: '/prescriptions' } },
  { name: '靶点', to: { path: '/targets' } },
  { name: '疾病', to: { path: '/diseases' } },
];

const isActive = (item: typeof navItems[number]) => {
  if (item.to.path === '/') return route.path === '/';
  return route.path.startsWith(item.to.path);
};
</script>
