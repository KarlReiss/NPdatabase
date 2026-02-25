<template>
  <div class="pb-20">
    <section class="mt-20 flex flex-col items-center px-6">
      <h1 class="text-3xl md:text-4xl font-bold text-slate-800 mb-10 text-center">
        探索天然产物与活性数据
      </h1>

      <div class="w-full max-w-[800px]">
        <div class="flex space-x-6 mb-3 ml-4">
          <button
            type="button"
            @click="searchTab = 'keyword'"
            :class="[
              'text-sm font-medium pb-2 transition-all',
              searchTab === 'keyword'
                ? 'text-[#10B981] border-b-2 border-[#10B981]'
                : 'text-slate-500 hover:text-slate-700'
            ]"
          >
            关键词搜索
          </button>
          <button
            type="button"
            @click="searchTab = 'smiles'"
            :class="[
              'text-sm font-medium pb-2 transition-all',
              searchTab === 'smiles'
                ? 'text-[#10B981] border-b-2 border-[#10B981]'
                : 'text-slate-500 hover:text-slate-700'
            ]"
          >
            SMILES结构搜索
          </button>
        </div>

        <form @submit="handleSearch" class="relative group">
          <input
            v-model="searchValue"
            type="text"
            :placeholder="searchTab === 'keyword' ? '输入名称、CAS号、编号...' : '输入SMILES序列...'"
            class="w-full h-14 pl-6 pr-16 bg-white border border-[#E2E8F0] rounded-full shadow-sm focus:outline-none focus:ring-2 focus:ring-[#10B981]/20 focus:border-[#10B981] transition-all text-slate-700 placeholder-slate-400"
          />
          <button
            class="absolute right-2 top-2 bottom-2 w-12 bg-[#10B981] rounded-full flex items-center justify-center text-white hover:bg-[#059669] transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </button>
        </form>

        <div class="mt-4 flex flex-wrap items-center gap-3 text-sm px-4">
          <span class="text-slate-600 font-medium">示例：</span>
          <RouterLink to="/bio-resources/NPO7154" class="text-[#10B981] hover:text-[#059669] font-medium hover:underline">甘草</RouterLink>
          <span class="text-slate-400">•</span>
          <RouterLink to="/natural-products/NPC56271" class="text-[#10B981] hover:text-[#059669] font-medium hover:underline">Gefitinib</RouterLink>
          <span class="text-slate-400">•</span>
          <RouterLink to="/prescriptions/PRES08926" class="text-[#10B981] hover:text-[#059669] font-medium hover:underline">漳州神曲</RouterLink>
          <span class="text-slate-400">•</span>
          <RouterLink to="/targets/NPT16" class="text-[#10B981] hover:text-[#059669] font-medium hover:underline">金黄色葡萄球菌</RouterLink>
          <span class="text-slate-400">•</span>
          <RouterLink to="/diseases/2C10.0" class="text-[#10B981] hover:text-[#059669] font-medium hover:underline">胰腺腺癌</RouterLink>
        </div>
      </div>
    </section>

    <section class="max-w-[1200px] mx-auto mt-10 px-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-sm font-bold text-slate-700">数据库概览</h2>
        <span v-if="statsError" class="text-xs text-red-500">{{ statsError }}</span>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <div class="bg-white border border-[#E2E8F0] rounded-md p-4">
          <div class="text-[11px] text-slate-400">生物资源</div>
          <div class="text-xl font-bold text-slate-800">{{ formatCount(stats?.bioResources) }}</div>
        </div>
        <div class="bg-white border border-[#E2E8F0] rounded-md p-4">
          <div class="text-[11px] text-slate-400">天然产物</div>
          <div class="text-xl font-bold text-slate-800">{{ formatCount(stats?.naturalProducts) }}</div>
        </div>
        <div class="bg-white border border-[#E2E8F0] rounded-md p-4">
          <div class="text-[11px] text-slate-400">处方</div>
          <div class="text-xl font-bold text-slate-800">{{ formatCount(stats?.prescriptions) }}</div>
        </div>
        <div class="bg-white border border-[#E2E8F0] rounded-md p-4">
          <div class="text-[11px] text-slate-400">靶点</div>
          <div class="text-xl font-bold text-slate-800">{{ formatCount(stats?.targets) }}</div>
        </div>
        <div class="bg-white border border-[#E2E8F0] rounded-md p-4">
          <div class="text-[11px] text-slate-400">生物活性</div>
          <div class="text-xl font-bold text-slate-800">{{ formatCount(stats?.bioactivity) }}</div>
        </div>
        <div class="bg-white border border-[#E2E8F0] rounded-md p-4">
          <div class="text-[11px] text-slate-400">疾病</div>
          <div class="text-xl font-bold text-slate-800">{{ formatCount(stats?.diseases) }}</div>
        </div>
      </div>
    </section>

    <section class="max-w-[1200px] mx-auto mt-16 px-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
      <div
        class="bg-white p-6 rounded-md shadow-sm border border-gray-100 hover:shadow-md hover:-translate-y-1 transition-all duration-300 cursor-pointer group"
      >
        <div class="w-12 h-12 rounded-lg bg-[#F1F5F9] flex items-center justify-center mb-4 group-hover:bg-[#E1F5EA] transition-colors">
          <svg class="w-6 h-6 text-[#10B981]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
            />
          </svg>
        </div>
        <h3 class="text-slate-800 font-bold mb-1">抗肿瘤（Anti-tumor）</h3>
        <p class="text-[#10B981] text-sm font-medium mb-2">1,245+ 个化合物</p>
        <p class="text-slate-500 text-xs">浏览具有抗肿瘤活性的天然产物集合。</p>
      </div>

      <div
        class="bg-white p-6 rounded-md shadow-sm border border-gray-100 hover:shadow-md hover:-translate-y-1 transition-all duration-300 cursor-pointer group"
      >
        <div class="w-12 h-12 rounded-lg bg-[#F1F5F9] flex items-center justify-center mb-4 group-hover:bg-[#E1F5EA] transition-colors">
          <svg class="w-6 h-6 text-[#3B82F6]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
        </div>
        <h3 class="text-slate-800 font-bold mb-1">心脑血管（Cardiovascular）</h3>
        <p class="text-[#10B981] text-sm font-medium mb-2">892+ 个化合物</p>
        <p class="text-slate-500 text-xs">探索心脑血管相关靶点的活性天然产物。</p>
      </div>

      <div
        class="bg-white p-6 rounded-md shadow-sm border border-gray-100 hover:shadow-md hover:-translate-y-1 transition-all duration-300 cursor-pointer group"
      >
        <div class="w-12 h-12 rounded-lg bg-[#F1F5F9] flex items-center justify-center mb-4 group-hover:bg-[#E1F5EA] transition-colors">
          <svg class="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
            />
          </svg>
        </div>
        <h3 class="text-slate-800 font-bold mb-1">有毒药材（Toxic Herbs）</h3>
        <p class="text-[#10B981] text-sm font-medium mb-2">310+ 条记录</p>
        <p class="text-slate-500 text-xs">传统用药的毒性与安全性信息汇总。</p>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { fetchStats } from '@/api/stats';
import { fetchSearch } from '@/api/search';
import type { StatsResponse } from '@/api/types';
import { formatCount } from '@/utils/format';

const searchTab = ref<'keyword' | 'smiles'>('keyword');
const searchValue = ref('');
const router = useRouter();

const stats = ref<StatsResponse | null>(null);
const statsError = ref('');

const handleSearch = async (event: Event) => {
  event.preventDefault();
  const q = searchValue.value.trim();
  if (!q) return;
  if (searchTab.value === 'smiles') {
    router.push({ path: '/compounds', query: { q } });
    return;
  }
  try {
    const result = await fetchSearch(q, 'all');
    const keyword = q.toLowerCase();
    const exactNp = result.naturalProducts.find((item) => (item.npId || '').toLowerCase() === keyword);
    if (exactNp?.npId) {
      router.push({ path: `/compounds/${exactNp.npId}` });
      return;
    }
    const exactTarget = result.targets.find((item) => (item.targetId || '').toLowerCase() === keyword);
    if (exactTarget?.targetId) {
      router.push({ path: `/targets/${exactTarget.targetId}` });
      return;
    }
    if (result.targets.length > 0 && result.naturalProducts.length === 0) {
      router.push({ path: '/targets', query: { q } });
      return;
    }
  } catch (err) {
    // ignore and fallback
  }
  router.push({ path: '/compounds', query: { q } });
};

const applyExample = (value: string) => {
  searchValue.value = value;
  router.push({ path: '/compounds', query: { q: value } });
};

const loadStats = async () => {
  try {
    stats.value = await fetchStats();
  } catch (err) {
    statsError.value = err instanceof Error ? err.message : '统计数据加载失败';
  }
};

onMounted(() => {
  loadStats();
});
</script>
