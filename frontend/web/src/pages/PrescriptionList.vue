<template>
  <div
    class="min-h-screen bg-[#F8FAFC]"
    :style="{ '--theme': '#7A5A2E', '--theme-soft': '#EFE6D8', '--theme-bg': '#F7F1E6' }"
  >
    <div class="max-w-[1200px] mx-auto px-6 py-6">
      <nav class="text-xs text-slate-500 mb-4 flex items-center space-x-2">
        <RouterLink to="/" class="hover:text-[#10B981]">首页</RouterLink>
        <span>/</span>
        <span class="text-slate-700 font-medium">处方列表</span>
      </nav>

      <div class="bg-white rounded-md border border-[#E2E8F0] overflow-hidden">
        <div
          class="p-4 border-b border-[#E2E8F0] flex flex-wrap items-center justify-between gap-4"
          style="background: var(--theme-soft);"
        >
          <div class="flex items-center space-x-3">
            <span class="text-sm text-slate-600">总记录数：<span class="font-bold">{{ prescriptions.length }}</span></span>
            <div class="relative">
              <input
                v-model="listQuery"
                type="text"
                placeholder="在本列表中搜索..."
                class="w-[240px] h-10 pl-9 pr-3 bg-white border border-[#E2E8F0] rounded-md text-sm focus:outline-none focus:ring-2"
                :style="{ '--tw-ring-color': 'var(--theme)' }"
              />
              <svg class="w-4 h-4 absolute left-3 top-2.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>
          <div class="text-sm text-slate-500">点击表头排序</div>
        </div>

        <div v-if="error" class="px-4 py-3 text-sm text-red-500 bg-red-50/40 border-b border-[#E2E8F0]">
          {{ error }}
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse min-w-[1000px]">
            <thead>
              <tr style="background: var(--theme-bg);">
                <th class="p-3 text-sm font-bold text-slate-700 border-b w-32">
                  <button class="flex items-center space-x-1" @click="toggleSort('prescriptionId')">
                    <span>编号</span>
                    <SortIcon :active="sortKey === 'prescriptionId'" :dir="sortDir" />
                  </button>
                </th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">
                  <button class="flex items-center space-x-1" @click="toggleSort('chineseName')">
                    <span>处方名称</span>
                    <SortIcon :active="sortKey === 'chineseName'" :dir="sortDir" />
                  </button>
                </th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">拼音</th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">分类</th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">功效/主治</th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">
                  <button class="flex items-center space-x-1" @click="toggleSort('numOfHerbs')">
                    <span>药材数</span>
                    <SortIcon :active="sortKey === 'numOfHerbs'" :dir="sortDir" />
                  </button>
                </th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">
                  <button class="flex items-center space-x-1" @click="toggleSort('numOfNaturalProducts')">
                    <span>天然产物数</span>
                    <SortIcon :active="sortKey === 'numOfNaturalProducts'" :dir="sortDir" />
                  </button>
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-if="loading">
                <td colspan="7" class="p-6 text-sm text-slate-500 text-center">加载中...</td>
              </tr>
              <tr v-else-if="filteredPrescriptions.length === 0">
                <td colspan="7" class="p-6 text-sm text-slate-400 text-center">暂无匹配记录</td>
              </tr>
              <tr
                v-for="(pres, idx) in filteredPrescriptions"
                :key="pres.prescriptionId"
                :class="[idx % 2 === 0 ? 'bg-white' : 'bg-slate-50/30', 'hover:bg-slate-50 transition-colors']"
              >
                <td class="p-3 text-sm">
                  <RouterLink :to="`/prescriptions/${pres.prescriptionId}`" class="text-[#3B82F6] hover:underline font-medium">
                    {{ pres.prescriptionId }}
                  </RouterLink>
                </td>
                <td class="p-3 text-sm text-slate-800 font-medium">{{ pres.chineseName }}</td>
                <td class="p-3 text-sm text-slate-600">{{ pres.pinyinName ?? '—' }}</td>
                <td class="p-3 text-sm text-slate-600">{{ pres.category ?? '—' }} / {{ pres.subcategory ?? '—' }}</td>
                <td class="p-3 text-sm text-slate-600">
                  {{ pres.functions ?? '—' }}
                </td>
                <td class="p-3 text-sm text-slate-600">{{ pres.numOfHerbs }}</td>
                <td class="p-3 text-sm text-slate-600">{{ pres.numOfNaturalProducts }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import SortIcon from '@/components/SortIcon.vue';
import { fetchPrescriptions } from '@/api/prescriptions';
import type { Prescription } from '@/api/types';

const prescriptions = ref<Prescription[]>([]);
const loading = ref(false);
const error = ref('');

const listQuery = ref('');
const sortKey = ref<'prescriptionId' | 'chineseName' | 'numOfHerbs' | 'numOfNaturalProducts'>('numOfNaturalProducts');
const sortDir = ref<'asc' | 'desc'>('desc');

const normalize = (value: string) => value.trim().toLowerCase();

const matchesQuery = (item: Prescription, query: string) => {
  if (!query) return true;
  const keyword = normalize(query);
  return (
    normalize(item.prescriptionId ?? '').includes(keyword) ||
    normalize(item.chineseName ?? '').includes(keyword) ||
    normalize(item.pinyinName ?? '').includes(keyword)
  );
};

const sortedPrescriptions = computed(() => {
  const data = [...prescriptions.value];
  const key = sortKey.value;
  const dir = sortDir.value;
  return data.sort((a, b) => {
    const aValue = a[key] ?? '';
    const bValue = b[key] ?? '';
    if (aValue === bValue) return 0;
    const order = aValue > bValue ? 1 : -1;
    return dir === 'asc' ? order : -order;
  });
});

const filteredPrescriptions = computed(() =>
  sortedPrescriptions.value.filter((pres) => matchesQuery(pres, listQuery.value))
);

const toggleSort = (key: typeof sortKey.value) => {
  if (sortKey.value === key) {
    sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc';
    return;
  }
  sortKey.value = key;
  sortDir.value = 'desc';
};

const fetchList = async () => {
  loading.value = true;
  error.value = '';
  try {
    const result = await fetchPrescriptions({ page: 1, pageSize: 200 });
    prescriptions.value = result.records ?? [];
  } catch (err) {
    error.value = err instanceof Error ? err.message : '数据加载失败';
    prescriptions.value = [];
  } finally {
    loading.value = false;
  }
};

onMounted(fetchList);
</script>
