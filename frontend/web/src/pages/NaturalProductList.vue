<template>
  <div
    class="min-h-screen bg-[#F8FAFC]"
    :style="{ '--theme': '#2E5E9E', '--theme-soft': '#DDE7F5', '--theme-bg': '#EEF3FA' }"
  >
    <div class="max-w-[1440px] mx-auto px-6 py-6 flex gap-6">
      <aside class="w-[300px] flex-shrink-0">
        <div class="bg-white rounded-md border border-[#E2E8F0] p-4">
          <div class="flex items-center justify-between mb-6">
            <h2 class="font-bold text-slate-800 text-base">筛选</h2>
            <button class="text-xs text-[#10B981] hover:underline" @click="resetFilters">清空</button>
          </div>

          <div class="space-y-4">
            <div>
              <button class="flex items-center justify-between w-full py-2 border-b border-gray-50 mb-2">
                <span class="text-sm font-semibold text-slate-700">理化属性（Properties）</span>
                <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div class="py-2 space-y-4">
                <div class="space-y-2">
                  <label class="text-sm text-slate-500">分子量（MW）</label>
                  <div class="grid grid-cols-2 gap-2">
                    <input
                      v-model="filters.mwMin"
                      type="number"
                      placeholder="最小"
                      class="w-full text-sm px-2 py-1.5 border rounded"
                    />
                    <input
                      v-model="filters.mwMax"
                      type="number"
                      placeholder="最大"
                      class="w-full text-sm px-2 py-1.5 border rounded"
                    />
                  </div>
                </div>
                <div class="space-y-2">
                  <label class="text-sm text-slate-500">脂水分配系数（XLogP）</label>
                  <div class="grid grid-cols-2 gap-2">
                    <input
                      v-model="filters.xlogpMin"
                      type="number"
                      placeholder="最小"
                      class="w-full text-sm px-2 py-1.5 border rounded"
                    />
                    <input
                      v-model="filters.xlogpMax"
                      type="number"
                      placeholder="最大"
                      class="w-full text-sm px-2 py-1.5 border rounded"
                    />
                  </div>
                </div>
                <div class="space-y-2">
                  <label class="text-sm text-slate-500">极性表面积（PSA）</label>
                  <div class="grid grid-cols-2 gap-2">
                    <input
                      v-model="filters.psaMin"
                      type="number"
                      placeholder="最小"
                      class="w-full text-sm px-2 py-1.5 border rounded"
                    />
                    <input
                      v-model="filters.psaMax"
                      type="number"
                      placeholder="最大"
                      class="w-full text-sm px-2 py-1.5 border rounded"
                    />
                  </div>
                </div>
              </div>
            </div>

            <div>
              <button class="flex items-center justify-between w-full py-2 border-b border-gray-50 mb-2">
                <span class="text-sm font-semibold text-slate-700">活性筛选（Activity）</span>
                <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div class="py-2 space-y-3">
                <select v-model="filters.activityType" class="w-full text-sm px-2 py-1.5 border rounded">
                  <option value="">全部类型</option>
                  <option value="IC50">IC50</option>
                  <option value="EC50">EC50</option>
                  <option value="Ki">Ki</option>
                  <option value="Kd">Kd</option>
                </select>
                <input
                  v-model="filters.activityMaxNm"
                  type="number"
                  placeholder="活性阈值（nM）"
                  class="w-full text-sm px-2 py-1.5 border rounded"
                />
              </div>
            </div>

            <div>
              <button class="flex items-center justify-between w-full py-2 border-b border-gray-50 mb-2">
                <span class="text-sm font-semibold text-slate-700">靶点筛选（Target）</span>
                <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div class="py-2">
                <input
                  v-model="filters.targetType"
                  type="text"
                  placeholder="输入靶点类型..."
                  class="w-full text-sm px-2 py-1.5 border rounded"
                />
              </div>
            </div>

            <div>
              <button class="flex items-center justify-between w-full py-2 border-b border-gray-50 mb-2">
                <span class="text-sm font-semibold text-slate-700">毒性筛选（Toxicity）</span>
                <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div class="py-2">
                <select v-model="filters.toxicity" class="w-full text-sm px-2 py-1.5 border rounded">
                  <option value="all">全部记录</option>
                  <option value="toxic">仅有毒记录</option>
                  <option value="non-toxic">仅无毒记录</option>
                </select>
              </div>
            </div>
          </div>

          <button
            class="w-full mt-6 py-2.5 bg-[#10B981] text-white rounded-md text-base font-medium hover:bg-[#059669] transition-colors"
            @click="applyFilters"
          >
            应用筛选
          </button>
        </div>
      </aside>

      <main class="flex-1 min-w-0">
        <nav class="text-xs text-slate-500 mb-4 flex items-center space-x-2">
          <RouterLink to="/" class="hover:text-[#10B981]">首页</RouterLink>
          <span>/</span>
          <span class="text-slate-700 font-medium">化合物列表</span>
        </nav>

        <div class="bg-white rounded-md border border-[#E2E8F0] overflow-hidden">
          <div
            class="p-4 border-b border-[#E2E8F0] flex flex-wrap items-center justify-between gap-4"
            style="background: var(--theme-soft);"
          >
            <div class="flex items-center space-x-3">
              <span class="text-sm text-slate-600">
                总记录数：
                <span class="font-bold">{{ total > 0 ? formatCount(total) : '未统计' }}</span>
              </span>
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
              <div class="flex items-center space-x-2 text-sm">
                <span class="text-slate-500">排序：</span>
                <span class="text-slate-600">点击表头排序</span>
              </div>
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
            <table class="w-full text-left border-collapse min-w-[760px]">
              <thead>
                <tr style="background: var(--theme-bg);">
                  <th class="p-3 text-sm font-bold text-slate-700 border-b w-32">编号</th>
                  <th class="p-3 text-sm font-bold text-slate-700 border-b w-[360px]">名称</th>
                  <th class="p-3 text-sm font-bold text-slate-700 border-b w-36">分子量（MW）</th>
                  <th class="p-3 text-sm font-bold text-slate-700 border-b w-28">活性记录</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-if="loading">
                  <td colspan="4" class="p-6 text-sm text-slate-500 text-center">加载中...</td>
                </tr>
                <tr v-else-if="rows.length === 0">
                  <td colspan="4" class="p-6 text-sm text-slate-400 text-center">暂无匹配记录</td>
                </tr>
                <tr
                  v-else
                  v-for="(cmp, idx) in rows"
                  :key="cmp.id"
                  :class="[
                    idx % 2 === 0 ? 'bg-white' : 'bg-slate-50/30',
                    'hover:bg-slate-50 transition-colors'
                  ]"
                >
                  <td class="p-3 text-sm">
                    <RouterLink :to="`/compounds/${cmp.id}`" class="text-[#3B82F6] hover:underline font-medium">
                      {{ cmp.id }}
                    </RouterLink>
                  </td>
                  <td class="p-3">
                    <div class="flex flex-col">
                      <span class="text-sm font-bold text-slate-800">{{ cmp.name }}</span>
                      <span
                        v-if="cmp.hasToxicity"
                        class="mt-1 inline-flex w-fit px-2 py-0.5 text-[10px] font-semibold rounded-full bg-red-50 text-red-600"
                      >
                        含毒性记录
                      </span>
                    </div>
                  </td>
                  <td class="p-3 text-sm text-slate-600">{{ formatDecimal(cmp.molecularWeight) }}</td>
                  <td class="p-3 text-sm text-slate-600">{{ formatCount(cmp.activityCount) }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="p-4 border-t border-[#E2E8F0] flex items-center justify-between">
            <span class="text-xs text-slate-500">
              第 {{ page }} 页<span v-if="total > 0"> / {{ totalPages }} 页</span>
              <span v-else>（为提升性能暂不统计总数）</span>
            </span>
            <div class="flex items-center space-x-1">
              <button
                class="px-2 py-1 text-sm border rounded"
                :class="page === 1 ? 'text-slate-400 border-gray-100 cursor-not-allowed' : 'text-slate-600 hover:bg-gray-50'"
                :disabled="page === 1"
                @click="goToPage(page - 1)"
              >
                上一页
              </button>
              <template v-if="total > 0">
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
              </template>
              <button
                class="px-2 py-1 text-sm border rounded"
                :class="canGoNext ? 'text-[#10B981] border-[#10B981]/20 hover:bg-[#10B981]/5' : 'text-slate-400 border-gray-100 cursor-not-allowed'"
                :disabled="!canGoNext"
                @click="goToPage(page + 1)"
              >
                下一页
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { fetchNaturalProducts } from '@/api/naturalProducts';
import type { NaturalProductApi } from '@/api/types';
import { buildPubchemImage, formatCount, formatDecimal, toNumber } from '@/utils/format';

interface CompoundRow {
  id: string;
  name: string;
  subtitle?: string;
  structureUrl?: string;
  formula?: string | null;
  molecularWeight?: number | null;
  xlogp?: number | null;
  psa?: number | null;
  activityCount?: number | null;
  bestActivityValue?: number | null;
  targetCount?: number | null;
  organismCount?: number | null;
  hasToxicity?: boolean;
}

type PageItem = number | '...';

const route = useRoute();
const router = useRouter();

const searchQuery = ref(String(route.query.q ?? ''));
const filters = reactive({
  mwMin: '',
  mwMax: '',
  xlogpMin: '',
  xlogpMax: '',
  psaMin: '',
  psaMax: '',
  activityType: '',
  activityMaxNm: '',
  targetType: '',
  toxicity: 'all',
});

const page = ref(1);
const pageSize = ref(20);
const total = ref(0);
const rows = ref<CompoundRow[]>([]);
const loading = ref(false);
const error = ref('');

const SAFE_LITERAL = /^[A-Za-z0-9_. -]+$/;

const totalPages = computed(() => {
  if (total.value <= 0) return 1;
  return Math.max(1, Math.ceil(total.value / pageSize.value));
});

const canGoNext = computed(() => {
  if (total.value > 0) {
    return page.value < totalPages.value;
  }
  return rows.value.length === pageSize.value;
});

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

const mapRow = (item: NaturalProductApi): CompoundRow => {
  const molecularWeight = toNumber(item.molecularWeight);
  const xlogp = toNumber(item.xlogp);
  const psa = toNumber(item.psa);
  const bestActivityValue = toNumber(item.bestActivityValue);
  const activityCount = (item.numOfActivity ?? item.bioactivityCount ?? null) as number | null;
  const targetCount = (item.numOfTarget ?? item.targetCount ?? null) as number | null;
  const organismCount = (item.numOfOrganism ?? item.bioResourceCount ?? null) as number | null;
  const name = item.prefName || item.iupacName || item.npId || '未命名';

  return {
    id: item.npId || '-',
    name,
    subtitle: item.iupacName || item.npId || '',
    structureUrl: buildPubchemImage(item.pubchemId),
    formula: item.formula ?? null,
    molecularWeight,
    xlogp,
    psa,
    activityCount,
    bestActivityValue,
    targetCount,
    organismCount,
    hasToxicity: item.hasToxicity ?? false,
  };
};

const buildParams = () => {
  const mwMin = toNumber(filters.mwMin);
  const mwMax = toNumber(filters.mwMax);
  const xlogpMin = toNumber(filters.xlogpMin);
  const xlogpMax = toNumber(filters.xlogpMax);
  const psaMin = toNumber(filters.psaMin);
  const psaMax = toNumber(filters.psaMax);
  const activityMaxNm = toNumber(filters.activityMaxNm);
  const rawTargetType = filters.targetType.trim();
  const targetType = rawTargetType && SAFE_LITERAL.test(rawTargetType) ? rawTargetType : undefined;

  const toxicityValue =
    filters.toxicity === 'toxic' ? true : filters.toxicity === 'non-toxic' ? false : undefined;

  return {
    page: page.value,
    pageSize: pageSize.value,
    q: searchQuery.value.trim() || undefined,
    mwMin: mwMin ?? undefined,
    mwMax: mwMax ?? undefined,
    xlogpMin: xlogpMin ?? undefined,
    xlogpMax: xlogpMax ?? undefined,
    psaMin: psaMin ?? undefined,
    psaMax: psaMax ?? undefined,
    activityType: filters.activityType.trim() || undefined,
    activityMaxNm: activityMaxNm ?? undefined,
    targetType,
    hasToxicity: toxicityValue,
  };
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
    const response = await fetchNaturalProducts(buildParams());
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

const applyFilters = () => {
  fetchList({ resetPage: true });
};

const resetFilters = () => {
  filters.mwMin = '';
  filters.mwMax = '';
  filters.xlogpMin = '';
  filters.xlogpMax = '';
  filters.psaMin = '';
  filters.psaMax = '';
  filters.activityType = '';
  filters.activityMaxNm = '';
  filters.targetType = '';
  filters.toxicity = 'all';
  fetchList({ resetPage: true });
};

const goToPage = (target: number) => {
  const safe = Math.max(target, 1);
  if (total.value > 0 && safe > totalPages.value) {
    return;
  }
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
