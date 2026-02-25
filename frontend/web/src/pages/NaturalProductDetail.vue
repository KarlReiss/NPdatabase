<template>
  <div
    class="max-w-[1200px] mx-auto px-6 py-8"
    :style="{ '--theme': '#2E5E9E', '--theme-soft': '#DDE7F5', '--theme-bg': '#EEF3FA' }"
  >
    <nav class="text-xs text-slate-500 mb-6 flex items-center space-x-2">
      <RouterLink to="/" class="hover:text-[#10B981]">首页</RouterLink>
      <span>/</span>
      <RouterLink to="/compounds" class="hover:text-[#10B981]">化合物列表</RouterLink>
      <span>/</span>
      <span class="text-slate-700 font-medium">{{ compoundId }}</span>
    </nav>

    <div v-if="loading" class="text-sm text-slate-500 mb-4">加载中...</div>
    <div v-if="error" class="text-sm text-red-500 mb-4">{{ error }}</div>

    <template v-if="compound">
      <section class="bg-white rounded-md border border-[#E2E8F0] shadow-sm overflow-hidden flex flex-col md:flex-row mb-8">
        <div class="flex-1 p-8">
          <div class="flex items-start justify-between mb-6">
            <div>
              <h1 class="text-2xl font-bold text-slate-800">
                {{ compoundName }}
              </h1>
              <div class="text-sm text-slate-500 mt-1">
                {{ compoundSubtitle || '—' }}
              </div>
              <div class="flex items-center space-x-3 mt-3">
                <span
                  class="px-2 py-0.5 text-[11px] font-bold rounded"
                  style="background: var(--theme-soft); color: var(--theme);"
                >
                  天然产物
                </span>
                <span class="text-[12px] text-slate-400 font-mono select-all cursor-pointer">ID: {{ compound.npId }}</span>
              </div>
            </div>
            <button class="w-9 h-9 flex items-center justify-center rounded-full border border-gray-200 hover:border-[#10B981] hover:text-[#10B981] transition-all">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </button>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-y-4 gap-x-8">
            <div v-for="item in metadata" :key="item.label">
              <div class="text-xs text-slate-400 uppercase tracking-wider mb-0.5">{{ item.label }}</div>
              <div :class="['text-sm font-medium', item.highlight ? 'text-[#10B981]' : 'text-slate-700']">
                {{ item.value }}
              </div>
            </div>
          </div>

          <div class="mt-8">
            <div class="text-xs text-slate-400 uppercase tracking-wider mb-2">简介</div>
            <p class="text-sm text-slate-600 leading-relaxed max-w-2xl">
              暂无结构化简介信息，可从文献和外部数据库补充。
            </p>
          </div>
        </div>

        <div
          class="md:w-[260px] p-6 border-t md:border-t-0 md:border-l border-[#E2E8F0] bg-white flex flex-col items-center justify-start"
        >
          <div class="grid grid-cols-3 gap-2 rounded-lg p-3 w-full mb-4" style="background: var(--theme-bg); border: 1px solid var(--theme-soft);">
            <div class="text-center">
              <div class="text-[11px] text-slate-500">活性记录</div>
              <div class="text-lg font-semibold text-slate-800">{{ formatCount(compound.numOfActivity ?? compound.bioactivityCount ?? 0) }}</div>
            </div>
            <div class="text-center">
              <div class="text-[11px] text-slate-500">靶点数量</div>
              <div class="text-lg font-semibold text-slate-800">{{ formatCount(compound.numOfTarget ?? compound.targetCount ?? 0) }}</div>
            </div>
            <div class="text-center">
              <div class="text-[11px] text-slate-500">生物资源</div>
              <div class="text-lg font-semibold text-slate-800">{{ formatCount(compound.numOfOrganism ?? compound.bioResourceCount ?? 0) }}</div>
            </div>
          </div>
          <img v-if="structureUrl"
            :src="structureUrl"
            :alt="compoundName"
            class="w-[200px] h-[200px] object-contain mb-3"
          />
          <button v-if="structureUrl" class="flex items-center space-x-2 px-3 py-2 bg-slate-50 border border-slate-200 rounded-md text-xs text-slate-600 hover:bg-slate-100 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a2 2 0 002 2h12a2 2 0 002-2v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            <span>下载结构</span>
          </button>
        </div>
      </section>

      <section class="bg-white rounded-md border border-[#E2E8F0] shadow-sm overflow-hidden">
        <div class="flex border-b border-[#E2E8F0] px-4">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              'px-6 py-4 text-sm font-medium transition-all relative',
              activeTab === tab.id ? 'text-[#10B981]' : 'text-slate-500 hover:text-slate-700'
            ]"
          >
            {{ tab.name }} <span class="text-[11px] opacity-60">({{ tab.count }})</span>
            <div v-if="activeTab === tab.id" class="absolute bottom-0 left-0 right-0 h-0.5 bg-[#10B981]"></div>
          </button>
        </div>

        <div class="p-6">
          <div v-if="activeTab === 'targets'">
            <div class="mb-4 flex items-center justify-between">
              <h3 class="text-sm font-bold text-slate-800">关联靶点列表</h3>
              <div class="text-xs text-slate-500">共 {{ formatCount(targetSummaries.length) }} 个靶点</div>
            </div>
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-slate-50/50">
                  <th class="p-3 text-sm font-bold text-slate-700 border-b">靶点</th>
                  <th class="p-3 text-sm font-bold text-slate-700 border-b">类型</th>
                  <th class="p-3 text-sm font-bold text-slate-700 border-b">物种</th>
                  <th class="p-3 text-sm font-bold text-slate-700 border-b">活性记录数</th>
                  <th class="p-3 text-sm font-bold text-slate-700 border-b">最佳活性(nM)</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-50">
                <tr v-if="targetSummaries.length === 0">
                  <td colspan="5" class="p-6 text-sm text-slate-400 text-center">暂无靶点记录</td>
                </tr>
                <tr v-else v-for="t in targetSummaries" :key="t.targetDbId" class="hover:bg-slate-50/50">
                  <td class="p-3">
                    <RouterLink
                      v-if="t.targetId"
                      :to="`/targets/${t.targetId}`"
                      class="text-sm text-[#3B82F6] font-medium hover:underline"
                    >{{ t.targetName || t.targetId }}</RouterLink>
                    <span v-else class="text-sm text-slate-800 font-medium">{{ t.targetName || '—' }}</span>
                    <div class="text-[11px] text-slate-400">编号：{{ t.targetId || '—' }}</div>
                  </td>
                  <td class="p-3 text-sm text-slate-600">{{ t.targetType || '—' }}</td>
                  <td class="p-3 text-sm text-slate-600">{{ t.targetOrganism || '—' }}</td>
                  <td class="p-3 text-sm text-slate-600">{{ formatCount(t.bioactivityCount ?? 0) }}</td>
                  <td class="p-3 text-sm font-bold text-slate-800">{{ formatDecimal(t.bestActivityValue, 2) }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-if="activeTab === 'bioactivity'">
            <div class="mb-4 flex items-center justify-between">
              <h3 class="text-sm font-bold text-slate-800">活性数据列表</h3>
              <div class="text-xs text-slate-500">共 {{ formatCount(bioactivityTotal) }} 条记录</div>
            </div>
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-slate-50/50">
                  <th class="p-3 text-sm font-bold text-slate-700 border-b">靶点</th>
                  <th class="p-3 text-sm font-bold text-slate-700 border-b">靶点类型</th>
                  <th class="p-3 text-sm font-bold text-slate-700 border-b">实验类型</th>
                  <th class="p-3 text-sm font-bold text-slate-700 border-b">标准化值</th>
                  <th class="p-3 text-sm font-bold text-slate-700 border-b">参考文献</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-50">
                <tr v-if="bioactivityLoading">
                  <td colspan="5" class="p-6 text-sm text-slate-400 text-center">加载中…</td>
                </tr>
                <tr v-else-if="bioactivityRows.length === 0">
                  <td colspan="5" class="p-6 text-sm text-slate-400 text-center">暂无活性记录</td>
                </tr>
                <tr v-else v-for="act in bioactivityRows" :key="act.id" class="hover:bg-slate-50/50">
                  <td class="p-3 text-sm font-medium">
                    <RouterLink
                      v-if="act.targetRouteId"
                      :to="`/targets/${act.targetRouteId}`"
                      class="text-[#3B82F6] hover:underline"
                    >{{ act.targetLabel }}</RouterLink>
                    <span v-else class="text-slate-800">{{ act.targetLabel }}</span>
                    <div class="text-[11px] text-slate-400">{{ act.targetIdLabel }}</div>
                  </td>
                  <td class="p-3 text-sm text-slate-600">{{ act.targetType }}</td>
                  <td class="p-3 text-sm text-slate-600">{{ act.type }}</td>
                  <td class="p-3 text-sm text-slate-600">{{ act.stdValue }}</td>
                  <td class="p-3 text-sm">
                    <div class="flex flex-col gap-1">
                      <a
                        v-if="act.refLink"
                        :href="act.refLink"
                        target="_blank"
                        rel="noreferrer"
                        class="text-xs text-[#3B82F6] hover:underline flex items-center space-x-1"
                      >
                        <span>{{ act.refLabel }}</span>
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                        </svg>
                      </a>
                      <span v-else class="text-xs text-slate-400">{{ act.refLabel }}</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
            <div v-if="bioactivityTotalPages > 1" class="mt-4 flex items-center justify-center gap-2">
              <button
                class="px-3 py-1 text-xs rounded border border-[#E2E8F0] text-slate-600 disabled:opacity-40"
                :disabled="bioactivityPage <= 1"
                @click="loadBioactivity(bioactivityPage - 1)"
              >上一页</button>
              <span class="text-xs text-slate-500">{{ bioactivityPage }} / {{ bioactivityTotalPages }}</span>
              <button
                class="px-3 py-1 text-xs rounded border border-[#E2E8F0] text-slate-600 disabled:opacity-40"
                :disabled="bioactivityPage >= bioactivityTotalPages"
                @click="loadBioactivity(bioactivityPage + 1)"
              >下一页</button>
            </div>
          </div>

          <div v-if="activeTab === 'herb'" class="space-y-4">
            <div class="flex items-center justify-between">
              <div class="text-sm font-bold text-slate-800">生物资源</div>
              <div class="text-xs text-slate-500">共 {{ formatCount(resourcesTotal) }} 条记录</div>
            </div>
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-slate-50/50">
                  <th class="p-3 text-sm font-bold text-slate-700 border-b">名称</th>
                  <th class="p-3 text-sm font-bold text-slate-700 border-b">类型</th>
                  <th class="p-3 text-sm font-bold text-slate-700 border-b">分类</th>
                  <th class="p-3 text-sm font-bold text-slate-700 border-b">关联天然产物数</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-50">
                <tr v-if="resourcesLoading">
                  <td colspan="4" class="p-6 text-sm text-slate-400 text-center">加载中…</td>
                </tr>
                <tr v-else-if="resources.length === 0">
                  <td colspan="4" class="p-6 text-sm text-slate-400 text-center">暂无来源记录</td>
                </tr>
                <tr v-else v-for="res in resources" :key="res.id" class="hover:bg-slate-50/50">
                  <td class="p-3 text-sm text-slate-700">
                    <RouterLink
                      v-if="res.resourceId"
                      :to="`/bio-resources/${res.resourceId}`"
                      class="text-[#3B82F6] hover:underline"
                    >{{ res.chineseName || res.latinName || res.resourceId }}</RouterLink>
                    <span v-else>—</span>
                  </td>
                  <td class="p-3 text-sm text-slate-600">{{ res.resourceType || '—' }}</td>
                  <td class="p-3 text-sm text-slate-600">{{ res.taxonomyFamily || res.taxonomyGenus || '—' }}</td>
                  <td class="p-3 text-sm text-slate-600">{{ formatCount(res.numOfNaturalProducts) }}</td>
                </tr>
              </tbody>
            </table>
            <div v-if="resourcesTotalPages > 1" class="flex items-center justify-center gap-2">
              <button
                class="px-3 py-1 text-xs rounded border border-[#E2E8F0] text-slate-600 disabled:opacity-40"
                :disabled="resourcesPage <= 1"
                @click="loadResources(resourcesPage - 1)"
              >上一页</button>
              <span class="text-xs text-slate-500">{{ resourcesPage }} / {{ resourcesTotalPages }}</span>
              <button
                class="px-3 py-1 text-xs rounded border border-[#E2E8F0] text-slate-600 disabled:opacity-40"
                :disabled="resourcesPage >= resourcesTotalPages"
                @click="loadResources(resourcesPage + 1)"
              >下一页</button>
            </div>
          </div>

          <div v-if="activeTab === 'trial'" class="py-20 flex flex-col items-center justify-center text-slate-400">
            <svg class="w-12 h-12 mb-4 opacity-20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
              />
            </svg>
            <span class="text-sm">更多专题数据即将上线。</span>
          </div>
        </div>
      </section>
    </template>

    <div v-else-if="!loading" class="bg-white border border-[#E2E8F0] rounded-md p-6 text-sm text-slate-400">
      未找到对应化合物记录。
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import {
  fetchNaturalProductBioactivity,
  fetchNaturalProductBioactivityTargets,
  fetchNaturalProductDetail,
  fetchNaturalProductResources,
} from '@/api/naturalProducts';
import type {
  BioactivityApi,
  BioactivityTargetSummaryApi,
  BioResourceApi,
  NaturalProductApi,
} from '@/api/types';
import { buildPubchemImage, formatCount, formatDecimal, toNumber } from '@/utils/format';

const PAGE_SIZE = 20;

const route = useRoute();
const activeTab = ref<'targets' | 'bioactivity' | 'herb' | 'trial'>('targets');
const compound = ref<NaturalProductApi | null>(null);

const bioactivity = ref<BioactivityApi[]>([]);
const bioactivityTotal = ref(0);
const bioactivityPage = ref(1);
const bioactivityLoading = ref(false);

const targetSummaries = ref<BioactivityTargetSummaryApi[]>([]);

const resources = ref<BioResourceApi[]>([]);
const resourcesTotal = ref(0);
const resourcesPage = ref(1);
const resourcesLoading = ref(false);

const loading = ref(false);
const error = ref('');

const compoundId = computed(() => String(route.params.id || ''));
const compoundName = computed(() => compound.value?.prefName || compound.value?.npId || '');
const compoundSubtitle = computed(() => compound.value?.iupacName || '');
const structureUrl = computed(() => buildPubchemImage(compound.value?.pubchemId));

const bioactivityTotalPages = computed(() => Math.ceil(bioactivityTotal.value / PAGE_SIZE));
const resourcesTotalPages = computed(() => Math.ceil(resourcesTotal.value / PAGE_SIZE));

const metadata = computed(() => [
  { label: '分子式（Formula）', value: compound.value?.formula || '—' },
  { label: '分子量（MW）', value: formatDecimal(compound.value?.molecularWeight) },
  { label: '脂水分配系数（XLogP）', value: formatDecimal(compound.value?.xlogp) },
  { label: '极性表面积（PSA）', value: formatDecimal(compound.value?.psa) },
  { label: '水溶性（LogS）', value: formatDecimal(compound.value?.logS) },
  { label: '分配系数（LogD, pH7.4）', value: formatDecimal(compound.value?.logD) },
  { label: '脂水分配系数（LogP）', value: formatDecimal(compound.value?.logP) },
  { label: '拓扑极性表面积（tPSA）', value: formatDecimal(compound.value?.tpsa) },
  { label: '氢键供体数', value: compound.value?.hBondDonors ?? '—' },
  { label: '氢键受体数', value: compound.value?.hBondAcceptors ?? '—' },
  { label: '可旋转键数', value: compound.value?.rotatableBonds ?? '—' },
  { label: '环数量', value: compound.value?.ringCount ?? '—' },
  {
    label: '活性记录数',
    value: formatCount(compound.value?.numOfActivity ?? compound.value?.bioactivityCount ?? 0),
  },
  {
    label: '靶点数',
    value: formatCount(compound.value?.numOfTarget ?? compound.value?.targetCount ?? 0),
  },
  {
    label: '来源生物资源数',
    value: formatCount(compound.value?.numOfOrganism ?? compound.value?.bioResourceCount ?? 0),
  },
  { label: '是否量化', value: compound.value?.ifQuantity ? '是' : '否' },
  { label: 'InChI', value: compound.value?.inchi || '—' },
  { label: 'SMILES', value: compound.value?.smiles || '—' },
  { label: 'PubChem CID', value: compound.value?.pubchemId || '—' },
  { label: 'ChEMBL ID', value: compound.value?.chemblId || '—' },
  { label: 'InChIKey', value: compound.value?.inchikey || '—' },
  { label: '创建时间', value: compound.value?.createdAt || '—' },
  { label: '更新时间', value: compound.value?.updatedAt || '—' },
]);

const tabs = computed(() => [
  { id: 'targets', name: '关联靶点', count: compound.value?.numOfTarget ?? compound.value?.targetCount ?? targetSummaries.value.length },
  { id: 'bioactivity', name: '活性记录', count: compound.value?.numOfActivity ?? compound.value?.bioactivityCount ?? bioactivityTotal.value },
  { id: 'herb', name: '生物资源', count: compound.value?.numOfOrganism ?? compound.value?.bioResourceCount ?? resourcesTotal.value },
  { id: 'trial', name: '临床试验', count: 0 },
]);

const targetMap = computed(() => {
  const map = new Map<number, BioactivityTargetSummaryApi>();
  targetSummaries.value.forEach((target) => {
    if (typeof target.targetDbId === 'number') {
      map.set(target.targetDbId, target);
    }
  });
  return map;
});

const formatActivityRecord = (value: unknown, unit?: string | null, relation?: string | null) => {
  const numeric = toNumber(value);
  if (numeric === null) return '—';
  const prefix = relation ? `${relation} ` : '';
  const suffix = unit ? ` ${unit}` : '';
  return `${prefix}${formatDecimal(numeric, 2)}${suffix}`.trim();
};

const bioactivityRows = computed(() =>
  bioactivity.value.map((act) => {
    const target = typeof act.targetId === 'number' ? targetMap.value.get(act.targetId) : undefined;
    const targetLabel = target?.targetName || target?.targetId || (act.targetId ? `靶点 ${act.targetId}` : '—');
    const targetIdLabel = target?.targetId || '—';
    const type = act.activityType || '—';
    const rawValue = formatActivityRecord(act.activityValue, act.activityUnits, act.activityRelation);
    const stdValue = formatActivityRecord(
      act.activityValueStd ?? act.activityValue,
      act.activityUnitsStd ?? act.activityUnits,
      act.activityRelation,
    );
    const refType = act.refIdType || '';
    const refId = act.refId || '—';
    const refLabel = refType ? `${refType}: ${refId}` : refId;
    const refLink = refType.toUpperCase() === 'PMID' && act.refId ? `https://pubmed.ncbi.nlm.nih.gov/${act.refId}/` : '';

    return {
      id: act.id ?? `${act.targetId}-${act.activityType}`,
      targetRouteId: target?.targetId || null,
      targetLabel,
      targetIdLabel,
      targetType: target?.targetType || '—',
      type,
      stdValue,
      refLabel,
      refLink,
    };
  })
);

const loadBioactivity = async (page: number) => {
  if (!compoundId.value) return;
  bioactivityLoading.value = true;
  try {
    const res = await fetchNaturalProductBioactivity(compoundId.value, { page, pageSize: PAGE_SIZE });
    bioactivity.value = res.records;
    bioactivityTotal.value = res.total;
    bioactivityPage.value = page;
  } catch {
    bioactivity.value = [];
    bioactivityTotal.value = 0;
  } finally {
    bioactivityLoading.value = false;
  }
};

const loadResources = async (page: number) => {
  if (!compoundId.value) return;
  resourcesLoading.value = true;
  try {
    const res = await fetchNaturalProductResources(compoundId.value, { page, pageSize: PAGE_SIZE });
    resources.value = res.records;
    resourcesTotal.value = res.total;
    resourcesPage.value = page;
  } catch {
    resources.value = [];
    resourcesTotal.value = 0;
  } finally {
    resourcesLoading.value = false;
  }
};

const fetchAll = async () => {
  if (!compoundId.value) return;
  loading.value = true;
  error.value = '';
  bioactivityPage.value = 1;
  resourcesPage.value = 1;
  try {
    const [detailResult, bioResult, targetResult, resourceResult] = await Promise.allSettled([
      fetchNaturalProductDetail(compoundId.value),
      fetchNaturalProductBioactivity(compoundId.value, { page: 1, pageSize: PAGE_SIZE }),
      fetchNaturalProductBioactivityTargets(compoundId.value),
      fetchNaturalProductResources(compoundId.value, { page: 1, pageSize: PAGE_SIZE }),
    ]);

    if (detailResult.status === 'fulfilled') {
      compound.value = detailResult.value;
    } else {
      throw detailResult.reason;
    }

    if (bioResult.status === 'fulfilled') {
      bioactivity.value = bioResult.value.records;
      bioactivityTotal.value = bioResult.value.total;
    } else {
      bioactivity.value = [];
      bioactivityTotal.value = 0;
    }

    targetSummaries.value = targetResult.status === 'fulfilled' ? targetResult.value : [];

    if (resourceResult.status === 'fulfilled') {
      resources.value = resourceResult.value.records;
      resourcesTotal.value = resourceResult.value.total;
    } else {
      resources.value = [];
      resourcesTotal.value = 0;
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : '数据加载失败';
    compound.value = null;
    bioactivity.value = [];
    targetSummaries.value = [];
    resources.value = [];
  } finally {
    loading.value = false;
  }
};

watch(compoundId, () => {
  fetchAll();
}, { immediate: true });
</script>
