<template>
  <div
    class="min-h-screen bg-[#F8FAFC]"
    :style="{ '--theme': '#2F6F5E', '--theme-soft': '#DDEBE6', '--theme-bg': '#EFF6F2' }"
  >
    <div class="max-w-[1200px] mx-auto px-6 py-6">
      <nav class="text-xs text-slate-500 mb-4 flex items-center space-x-2">
        <RouterLink to="/" class="hover:text-[#10B981]">首页</RouterLink>
        <span>/</span>
        <span class="text-slate-700 font-medium">生物资源列表</span>
      </nav>

      <div class="bg-white rounded-md border border-[#E2E8F0] overflow-hidden">
        <div
          class="p-4 border-b border-[#E2E8F0] flex flex-wrap items-center justify-between gap-4"
          style="background: var(--theme-soft);"
        >
          <div class="flex items-center space-x-3">
            <span class="text-sm text-slate-600">总记录数：<span class="font-bold">{{ total }}</span></span>
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
          <table class="w-full text-left border-collapse min-w-[1200px]">
            <thead>
              <tr style="background: var(--theme-bg);">
                <th class="p-3 text-sm font-bold text-slate-700 border-b w-35">
                  <button class="flex items-center space-x-1" @click="toggleSort('resourceId')">
                    <span>编号</span>
                    <SortIcon :active="sortKey === 'resourceId'" :dir="sortDir" />
                  </button>
                </th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b w-42">
                  <button class="flex items-center space-x-1" @click="toggleSort('chineseName')">
                    <span>名称</span>
                    <SortIcon :active="sortKey === 'chineseName'" :dir="sortDir" />
                  </button>
                </th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b w-42">拉丁名</th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b w-22">资源类型</th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b w-22">
                  <button class="flex items-center space-x-1" @click="toggleSort('numOfNaturalProducts')">
                    <span>天然产物数</span>
                    <SortIcon :active="sortKey === 'numOfNaturalProducts'" :dir="sortDir" />
                  </button>
                </th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b w-22">
                  <button class="flex items-center space-x-1" @click="toggleSort('numOfPrescriptions')">
                    <span>相关处方数</span>
                    <SortIcon :active="sortKey === 'numOfPrescriptions'" :dir="sortDir" />
                  </button>
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-if="loading">
                <td colspan="6" class="p-6 text-sm text-slate-500 text-center">加载中...</td>
              </tr>
              <tr v-else-if="rows.length === 0">
                <td colspan="6" class="p-6 text-sm text-slate-400 text-center">暂无匹配记录</td>
              </tr>
              <tr
                v-else
                v-for="(resource, idx) in rows"
                :key="resource.resourceId"
                :class="[idx % 2 === 0 ? 'bg-white' : 'bg-slate-50/30', 'hover:bg-slate-50 transition-colors']"
              >
                <td class="p-3 text-sm">
                  <RouterLink :to="`/resources/${resource.resourceId}`" class="text-[#3B82F6] hover:underline font-medium">
                    {{ resource.resourceId }}
                  </RouterLink>
                </td>
                <td class="p-3 text-sm text-slate-800 font-medium">
                  {{
                    resource.chineseName
                      ?? resource.latinName
                      ?? resource.resourceId
                  }}
                </td>
                <td class="p-3 text-sm text-slate-600 max-w-[160px] truncate" :title="resource.latinName ?? ''">{{ resource.latinName ?? '—' }}</td>
                <td class="p-3 text-sm text-slate-600">{{ toTypeLabel(resource.resourceType) }}</td>
                <td class="p-3 text-sm text-slate-600">{{ resource.numOfNaturalProducts }}</td>
                <td class="p-3 text-sm text-slate-600">{{ resource.numOfPrescriptions ?? 0 }}</td>
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
import { fetchBioResources } from '@/api/bioResources';
import type { BioResource } from '@/api/types';

type SortKey = 'resourceId' | 'chineseName' | 'numOfNaturalProducts' | 'numOfPrescriptions';
type PageItem = number | '...';

const route = useRoute();
const router = useRouter();

const searchQuery = ref(String(route.query.q ?? ''));
const page = ref(1);
const pageSize = ref(20);
const total = ref(0);
const rows = ref<BioResource[]>([]);
const loading = ref(false);
const error = ref('');

const sortKey = ref<SortKey>('numOfNaturalProducts');
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

const toTypeLabel = (value?: string) => {
  if (!value) return '—';
  const key = value.trim().toLowerCase();
  if (key === 'plant') return '植物';
  if (key === 'animal') return '动物';
  if (key === 'mineral') return '矿物';
  if (key === 'fungi' || key === 'fungus') return '真菌';
  if (key === 'microbe' || key === 'microorganism') return '微生物';
  if (key === 'bacteria') return '细菌';
  if (key === 'virus') return '病毒';
  if (key === 'algae') return '藻类';
  if (key === 'unknown' || key === 'unclassified') return '未知';
  if (key === 'other') return '其他';
  return value;
};

let requestId = 0;
const fetchList = async (options?: { resetPage?: boolean }) => {
  if (options?.resetPage) {
    page.value = 1;
  }
  const currentId = (requestId += 1);
  loading.value = true;
  error.value = '';
  try {
    const response = await fetchBioResources({
      page: page.value,
      pageSize: pageSize.value,
      q: searchQuery.value.trim() || undefined,
      sortBy: sortKey.value,
      sortOrder: sortDir.value,
    });
    if (currentId !== requestId) return;
    rows.value = response.records ?? [];
    total.value = response.total ?? 0;
    page.value = response.page ?? page.value;
    pageSize.value = response.pageSize ?? pageSize.value;
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
  } else {
    sortKey.value = key;
    sortDir.value = 'desc';
  }
  fetchList({ resetPage: true });
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
