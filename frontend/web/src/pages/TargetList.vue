<template>
  <div
    class="min-h-screen bg-[#F8FAFC]"
    :style="{ '--theme': '#6B4C9A', '--theme-soft': '#E9E1F3', '--theme-bg': '#F5F0FA' }"
  >
    <div class="max-w-[1200px] mx-auto px-6 py-6">
      <nav class="text-xs text-slate-500 mb-4 flex items-center space-x-2">
        <RouterLink to="/" class="hover:text-[#10B981]">首页</RouterLink>
        <span>/</span>
        <span class="text-slate-700 font-medium">靶点列表</span>
      </nav>

      <div class="bg-white rounded-md border border-[#E2E8F0] overflow-hidden">
        <div
          class="p-4 border-b border-[#E2E8F0] flex flex-wrap items-center justify-between gap-4"
          style="background: var(--theme-soft);"
        >
          <div class="flex items-center space-x-3">
            <span class="text-sm text-slate-600">总记录数：<span class="font-bold">{{ formatCount(total) }}</span></span>
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="在本列表中搜索..."
                class="w-[260px] h-11 pl-9 pr-3 bg-white border border-[#E2E8F0] rounded-md text-sm focus:outline-none focus:ring-2"
                :style="{ '--tw-ring-color': 'var(--theme)' }"
              />
              <svg class="w-4 h-4 absolute left-3 top-3 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <div class="text-sm text-slate-500">点击表头排序</div>
            <div class="flex items-center space-x-2 text-sm">
              <span class="text-slate-500">每页数量：</span>
              <select v-model.number="pageSize" class="border rounded px-2 py-1 outline-none text-slate-700">
                <option :value="20">20</option>
                <option :value="50">50</option>
                <option :value="100">100</option>
              </select>
            </div>
          </div>
        </div>

        <div v-if="error" class="px-4 py-3 text-sm text-red-500 bg-red-50/40 border-b border-[#E2E8F0]">
          {{ error }}
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse min-w-[1040px]">
            <thead>
              <tr style="background: var(--theme-bg);">
                <th class="p-3 text-sm font-bold text-slate-700 border-b w-32">
                  <button class="flex items-center space-x-1" @click="toggleSort('targetId')">
                    <span>编号</span>
                    <SortIcon :active="sortKey === 'targetId'" :dir="sortDir" />
                  </button>
                </th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">
                  <button class="flex items-center space-x-1" @click="toggleSort('targetName')">
                    <span>靶点名称</span>
                    <SortIcon :active="sortKey === 'targetName'" :dir="sortDir" />
                  </button>
                </th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">基因名</th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">类型</th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">物种</th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">UniProt</th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">
                  <button class="flex items-center space-x-1" @click="toggleSort('numOfNaturalProducts')">
                    <span>关联天然产物数</span>
                    <SortIcon :active="sortKey === 'numOfNaturalProducts'" :dir="sortDir" />
                  </button>
                </th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">
                  <button class="flex items-center space-x-1" @click="toggleSort('numOfActivities')">
                    <span>活性记录数</span>
                    <SortIcon :active="sortKey === 'numOfActivities'" :dir="sortDir" />
                  </button>
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-if="loading">
                <td colspan="8" class="p-6 text-sm text-slate-500 text-center">加载中...</td>
              </tr>
              <tr v-else-if="sortedTargets.length === 0">
                <td colspan="8" class="p-6 text-sm text-slate-400 text-center">暂无匹配记录</td>
              </tr>
              <tr
                v-else
                v-for="(target, idx) in sortedTargets"
                :key="target.targetId"
                :class="[idx % 2 === 0 ? 'bg-white' : 'bg-slate-50/30', 'hover:bg-slate-50 transition-colors']"
              >
                <td class="p-3 text-sm">
                  <RouterLink :to="`/targets/${target.targetId}`" class="text-[#3B82F6] hover:underline font-medium">
                    {{ target.targetId }}
                  </RouterLink>
                </td>
                <td class="p-3 text-sm text-slate-800 font-medium">{{ target.targetName || '—' }}</td>
                <td class="p-3 text-sm text-slate-600">{{ target.geneName || '—' }}</td>
                <td class="p-3 text-sm text-slate-600">{{ target.targetType || '—' }}</td>
                <td class="p-3 text-sm text-slate-600">{{ target.targetOrganism || '—' }}</td>
                <td class="p-3 text-sm text-slate-600">{{ target.uniprotId || '—' }}</td>
                <td class="p-3 text-sm text-slate-600">{{ formatCount(target.numOfNaturalProducts) }}</td>
                <td class="p-3 text-sm text-slate-600">{{ formatCount(target.numOfActivities) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="p-4 border-t border-[#E2E8F0] flex items-center justify-between">
          <span class="text-xs text-slate-500">第 {{ page }} / {{ totalPages }} 页</span>
          <div class="flex items-center space-x-1">
            <button
              class="px-2 py-1 text-sm border rounded"
              :class="page === 1 ? 'text-slate-400 border-gray-100 cursor-not-allowed' : 'text-slate-600 hover:bg-gray-50'"
              :disabled="page === 1"
              @click="goToPage(page - 1)"
            >
              上一页
            </button>
            <template v-for="item in pageItems" :key="`page-${item}`">
              <span v-if="item === '...'" class="text-sm text-slate-400 px-1">...</span>
              <button
                v-else
                class="px-3 py-1 text-sm rounded"
                :class="item === page ? 'bg-[#10B981] text-white' : 'text-slate-600 hover:bg-gray-50'"
                @click="goToPage(Number(item))"
              >
                {{ item }}
              </button>
            </template>
            <button
              class="px-2 py-1 text-sm border rounded"
              :class="page === totalPages ? 'text-slate-400 border-gray-100 cursor-not-allowed' : 'text-[#10B981] border-[#10B981]/20 hover:bg-[#10B981]/5'"
              :disabled="page === totalPages"
              @click="goToPage(page + 1)"
            >
              下一页
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import SortIcon from '@/components/SortIcon.vue';
import { fetchTargets } from '@/api/targets';
import type { TargetApi } from '@/api/types';
import { formatCount } from '@/utils/format';

interface TargetRow {
  targetId: string;
  targetName?: string;
  geneName?: string;
  targetType?: string;
  targetOrganism?: string;
  uniprotId?: string;
  numOfNaturalProducts?: number | null;
  numOfActivities?: number | null;
}

type SortKey = 'targetId' | 'targetName' | 'numOfNaturalProducts' | 'numOfActivities';

type PageItem = number | '...';

const route = useRoute();
const router = useRouter();

const searchQuery = ref(String(route.query.q ?? ''));
const page = ref(1);
const pageSize = ref(20);
const total = ref(0);
const rows = ref<TargetRow[]>([]);
const loading = ref(false);
const error = ref('');

const sortKey = ref<SortKey>('numOfActivities');
const sortDir = ref<'asc' | 'desc'>('desc');

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize.value)));

const pageItems = computed<PageItem[]>(() => {
  const totalPageCount = totalPages.value;
  if (totalPageCount <= 7) {
    return Array.from({ length: totalPageCount }, (_, idx) => idx + 1);
  }
  const current = page.value;
  const items: PageItem[] = [1];
  const start = Math.max(2, current - 1);
  const end = Math.min(totalPageCount - 1, current + 1);
  if (start > 2) items.push('...');
  for (let i = start; i <= end; i += 1) items.push(i);
  if (end < totalPageCount - 1) items.push('...');
  items.push(totalPageCount);
  return items;
});

const compareValues = (a: unknown, b: unknown) => {
  if (a === null || a === undefined || a === '') return 1;
  if (b === null || b === undefined || b === '') return -1;
  if (typeof a === 'string' || typeof b === 'string') {
    return String(a).localeCompare(String(b), 'zh-Hans-CN', { numeric: true });
  }
  return Number(a) > Number(b) ? 1 : -1;
};

const sortedTargets = computed(() => {
  const data = [...rows.value];
  const key = sortKey.value;
  const dir = sortDir.value;
  return data.sort((a, b) => {
    const result = compareValues(a[key], b[key]);
    return dir === 'asc' ? result : -result;
  });
});

const mapRow = (item: TargetApi): TargetRow => ({
  targetId: item.targetId || '-',
  targetName: item.targetName || '',
  geneName: item.geneName || '',
  targetType: item.targetType || '',
  targetOrganism: item.targetOrganism || '',
  uniprotId: item.uniprotId || '',
  numOfNaturalProducts: item.numOfNaturalProducts ?? item.numOfCompounds ?? null,
  numOfActivities: item.numOfActivities ?? null,
});

let requestId = 0;
const fetchList = async (options?: { resetPage?: boolean }) => {
  if (options?.resetPage) {
    page.value = 1;
  }
  const currentId = (requestId += 1);
  loading.value = true;
  error.value = '';
  try {
    const response = await fetchTargets({
      page: page.value,
      pageSize: pageSize.value,
      q: searchQuery.value.trim() || undefined,
    });
    if (currentId !== requestId) return;
    rows.value = response.records.map(mapRow);
    total.value = response.total;
    page.value = response.page;
    pageSize.value = response.pageSize;
  } catch (err) {
    if (currentId !== requestId) return;
    error.value = err instanceof Error ? err.message : '数据加载失败';
  } finally {
    if (currentId === requestId) {
      loading.value = false;
    }
  }
};

let searchTimer: ReturnType<typeof setTimeout> | null = null;
const scheduleSearch = () => {
  if (searchTimer) {
    clearTimeout(searchTimer);
  }
  searchTimer = setTimeout(() => {
    fetchList({ resetPage: true });
  }, 300);
};

const syncQueryToRoute = () => {
  const q = searchQuery.value.trim();
  const nextQuery = { ...route.query, q: q || undefined };
  router.replace({ query: nextQuery });
};

const toggleSort = (key: SortKey) => {
  if (sortKey.value === key) {
    sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc';
    return;
  }
  sortKey.value = key;
  sortDir.value = 'desc';
};

const goToPage = (target: number) => {
  const safe = Math.min(Math.max(target, 1), totalPages.value);
  if (safe !== page.value) {
    page.value = safe;
    fetchList();
  }
};

watch(searchQuery, () => {
  syncQueryToRoute();
  scheduleSearch();
});

watch(pageSize, () => {
  fetchList({ resetPage: true });
});

onMounted(() => {
  fetchList();
});
</script>
