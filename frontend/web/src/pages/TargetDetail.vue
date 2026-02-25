<template>
  <div
    class="max-w-[1200px] mx-auto px-6 py-8"
    :style="{ '--theme': '#6B4C9A', '--theme-soft': '#E9E1F3', '--theme-bg': '#F5F0FA' }"
  >
    <nav class="text-xs text-slate-500 mb-6 flex items-center space-x-2">
      <RouterLink to="/" class="hover:text-[#10B981]">首页</RouterLink>
      <span>/</span>
      <RouterLink to="/targets" class="hover:text-[#10B981]">靶点列表</RouterLink>
      <span>/</span>
      <span class="text-slate-700 font-medium">{{ targetId }}</span>
    </nav>

    <div v-if="loading" class="text-sm text-slate-500 mb-4">加载中...</div>
    <div v-if="error" class="text-sm text-red-500 mb-4">{{ error }}</div>

    <template v-if="target">
      <section class="bg-white rounded-lg border border-[#E2E8F0] shadow-sm p-8 mb-8">
        <div class="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6">
          <div class="space-y-4">
            <div>
              <div class="flex items-center gap-3 flex-wrap">
                <h1 class="text-2xl font-bold text-slate-800">{{ target.targetName || target.targetId }}</h1>
              <span class="px-2.5 py-0.5 rounded-full text-[11px] font-semibold" style="background: var(--theme-soft); color: var(--theme);">
                靶点
              </span>
            </div>
            <div class="mt-2 text-base text-slate-500">
              <span>编号：{{ target.targetId || '—' }}</span>
            </div>
          </div>

          <div class="flex flex-wrap gap-2">
            <span class="px-3 py-1 rounded-full text-sm bg-slate-100 text-slate-600">
              类型：{{ target.targetType || '—' }}
            </span>
            <span class="px-3 py-1 rounded-full text-sm bg-slate-100 text-slate-600">
              物种：{{ target.targetOrganism || '—' }}
            </span>
          </div>
        </div>

        <div class="grid grid-cols-3 gap-3 rounded-lg p-4 min-w-[260px]" style="background: var(--theme-bg); border: 1px solid var(--theme-soft);">
          <div class="text-center">
            <div class="text-xs text-slate-500">关联天然产物</div>
            <div class="text-xl font-semibold text-slate-800">{{ formatCount(target.naturalProductCount) }}</div>
          </div>
          <div class="text-center">
            <div class="text-xs text-slate-500">活性记录</div>
            <div class="text-xl font-semibold text-slate-800">{{ formatCount(target.bioactivityCount) }}</div>
          </div>
          <div class="text-center">
            <div class="text-xs text-slate-500">最佳活性</div>
            <div class="text-xl font-semibold text-slate-800">{{ formatActivityValue(target.bestActivityValue) }}</div>
          </div>
        </div>
      </div>

        <div class="mt-6 space-y-4 text-base text-slate-600">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="rounded-lg p-4" style="background: var(--theme-bg); border: 1px solid var(--theme-soft);">
              <div class="text-xs text-slate-400 uppercase tracking-wider">基础信息</div>
              <div class="mt-2 space-y-1 text-sm text-slate-600">
                <div>基因名：{{ target.geneName || '—' }}</div>
                <div class="flex flex-wrap gap-1 items-center">
                  <span>TTD ID：</span>
                  <span v-if="ttdIds.length === 0">—</span>
                  <template v-else>
                    <a
                      v-for="(id, idx) in ttdIds"
                      :key="idx"
                      :href="`https://db.idrblab.net/ttd/data/target/details/${id}`"
                      target="_blank"
                      rel="noopener noreferrer"
                      class="text-[#3B82F6] hover:underline"
                    >{{ id }}</a>
                    <span v-if="idx < ttdIds.length - 1">,</span>
                  </template>
                </div>
                <div>EC 编号：{{ target.ecNumber || '—' }}</div>
                <div class="flex flex-wrap gap-1 items-center">
                  <span>PDB 结构：</span>
                  <span v-if="pdbIds.length === 0">—</span>
                  <template v-else>
                    <a
                      v-for="(id, idx) in pdbIds"
                      :key="idx"
                      :href="`https://www.rcsb.org/structure/${id}`"
                      target="_blank"
                      rel="noopener noreferrer"
                      class="text-[#3B82F6] hover:underline"
                    >{{ id }}</a>
                    <span v-if="idx < pdbIds.length - 1">,</span>
                  </template>
                </div>
                <div>生物分类：{{ target.bioclass || '—' }}</div>
                <div>物种 Tax ID：{{ target.targetOrganismTaxId || '—' }}</div>
                <div class="flex flex-wrap gap-1 items-center">
                  <span>UniProt ID：</span>
                  <span v-if="uniprotIds.length === 0">—</span>
                  <template v-else>
                    <a
                      v-for="(id, idx) in uniprotIds"
                      :key="idx"
                      :href="`https://www.uniprot.org/uniprotkb/${id}/entry`"
                      target="_blank"
                      rel="noopener noreferrer"
                      class="text-[#3B82F6] hover:underline"
                    >{{ id }}</a>
                    <span v-if="idx < uniprotIds.length - 1">,</span>
                  </template>
                </div>
              </div>
            </div>
          </div>

          <div class="rounded-lg p-4" style="background: var(--theme-bg); border: 1px solid var(--theme-soft);">
            <div class="text-xs text-slate-400 uppercase tracking-wider">同义词</div>
            <div class="mt-2 text-sm text-slate-600 leading-relaxed">
              {{ target.synonyms || '—' }}
            </div>
          </div>

          <div class="rounded-lg p-4" style="background: var(--theme-bg); border: 1px solid var(--theme-soft);">
            <div class="text-xs text-slate-400 uppercase tracking-wider">功能</div>
            <div class="mt-2 text-sm text-slate-600 leading-relaxed">
              {{ target.function || '—' }}
            </div>
          </div>

          <div class="rounded-lg p-4" style="background: var(--theme-bg); border: 1px solid var(--theme-soft);">
            <div class="text-xs text-slate-400 uppercase tracking-wider">序列</div>
            <div class="mt-2 text-sm text-slate-600 break-all font-mono">
              {{ target.sequence || '—' }}
            </div>
          </div>
        </div>
      </section>

      <section class="bg-white rounded-md border border-[#E2E8F0] shadow-sm overflow-hidden">
        <div class="flex border-b border-[#E2E8F0] px-4">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="onTabChange(tab.id as 'compounds' | 'bio')"
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
          <!-- 相关天然产物 -->
          <div v-if="activeTab === 'compounds'">
            <div v-if="compoundsLoading" class="text-sm text-slate-400 text-center py-8">加载中...</div>
            <template v-else>
              <table class="w-full text-left border-collapse">
                <thead>
                  <tr class="bg-slate-50/50">
                    <th class="p-3 text-sm font-bold text-slate-700 border-b">编号</th>
                    <th class="p-3 text-sm font-bold text-slate-700 border-b">名称</th>
                    <th class="p-3 text-sm font-bold text-slate-700 border-b">分子量（MW）</th>
                    <th class="p-3 text-sm font-bold text-slate-700 border-b">最强活性</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-50">
                  <tr v-if="compoundRows.length === 0">
                    <td colspan="4" class="p-6 text-sm text-slate-400 text-center">暂无关联化合物</td>
                  </tr>
                  <tr v-else v-for="cmp in compoundRows" :key="cmp.id" class="hover:bg-slate-50/50">
                    <td class="p-3 text-sm">
                      <RouterLink :to="`/compounds/${cmp.id}`" class="text-[#3B82F6] hover:underline font-medium">
                        {{ cmp.id }}
                      </RouterLink>
                    </td>
                    <td class="p-3 text-sm text-slate-700">{{ cmp.name }}</td>
                    <td class="p-3 text-sm text-slate-600">{{ formatDecimal(cmp.molecularWeight) }}</td>
                    <td class="p-3 text-sm text-slate-700 font-medium">{{ formatActivityValue(cmp.bestActivityValue) }}</td>
                  </tr>
                </tbody>
              </table>
              <div v-if="compoundsTotalPages > 1" class="flex items-center justify-between mt-4 text-sm text-slate-500">
                <span>第 {{ compoundsPage }} / {{ compoundsTotalPages }} 页，共 {{ compoundsTotal }} 条</span>
                <div class="flex gap-2">
                  <button
                    :disabled="compoundsPage <= 1"
                    @click="loadCompounds(compoundsPage - 1)"
                    class="px-3 py-1 rounded border border-slate-200 disabled:opacity-40 hover:bg-slate-50"
                  >上一页</button>
                  <button
                    :disabled="compoundsPage >= compoundsTotalPages"
                    @click="loadCompounds(compoundsPage + 1)"
                    class="px-3 py-1 rounded border border-slate-200 disabled:opacity-40 hover:bg-slate-50"
                  >下一页</button>
                </div>
              </div>
            </template>
          </div>

          <!-- 活性记录 -->
          <div v-if="activeTab === 'bio'">
            <div v-if="bioLoading" class="text-sm text-slate-400 text-center py-8">加载中...</div>
            <template v-else>
              <table class="w-full text-left border-collapse">
                <thead>
                  <tr class="bg-slate-50/50">
                    <th class="p-3 text-sm font-bold text-slate-700 border-b">活性类型</th>
                    <th class="p-3 text-sm font-bold text-slate-700 border-b">关系</th>
                    <th class="p-3 text-sm font-bold text-slate-700 border-b">值</th>
                    <th class="p-3 text-sm font-bold text-slate-700 border-b">单位</th>
                    <th class="p-3 text-sm font-bold text-slate-700 border-b">标准值</th>
                    <th class="p-3 text-sm font-bold text-slate-700 border-b">标准单位</th>
                    <th class="p-3 text-sm font-bold text-slate-700 border-b">天然产物</th>
                    <th class="p-3 text-sm font-bold text-slate-700 border-b">参考文献</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-50">
                  <tr v-if="bioactivities.length === 0">
                    <td colspan="8" class="p-6 text-sm text-slate-400 text-center">暂无活性记录</td>
                  </tr>
                  <tr v-else v-for="row in bioactivities" :key="row.id" class="hover:bg-slate-50/50">
                    <td class="p-3 text-sm text-slate-700">{{ row.activityType || '—' }}</td>
                    <td class="p-3 text-sm text-slate-600">{{ row.activityRelation || '—' }}</td>
                    <td class="p-3 text-sm text-slate-600">{{ row.activityValue ?? '—' }}</td>
                    <td class="p-3 text-sm text-slate-600">{{ row.activityUnits || '—' }}</td>
                    <td class="p-3 text-sm text-slate-600">{{ row.activityValueStd ?? '—' }}</td>
                    <td class="p-3 text-sm text-slate-600">{{ row.activityUnitsStd || '—' }}</td>
                    <td class="p-3 text-sm">
                      <RouterLink v-if="row.npId" :to="`/compounds/${row.npId}`" class="text-[#3B82F6] hover:underline">
                        {{ row.npId }}
                      </RouterLink>
                      <span v-else>—</span>
                    </td>
                    <td class="p-3 text-sm text-slate-600">{{ row.refId || '—' }}</td>
                  </tr>
                </tbody>
              </table>
              <div v-if="bioTotalPages > 1" class="flex items-center justify-between mt-4 text-sm text-slate-500">
                <span>第 {{ bioPage }} / {{ bioTotalPages }} 页，共 {{ bioTotal }} 条</span>
                <div class="flex gap-2">
                  <button
                    :disabled="bioPage <= 1"
                    @click="loadBio(bioPage - 1)"
                    class="px-3 py-1 rounded border border-slate-200 disabled:opacity-40 hover:bg-slate-50"
                  >上一页</button>
                  <button
                    :disabled="bioPage >= bioTotalPages"
                    @click="loadBio(bioPage + 1)"
                    class="px-3 py-1 rounded border border-slate-200 disabled:opacity-40 hover:bg-slate-50"
                  >下一页</button>
                </div>
              </div>
            </template>
          </div>
        </div>
      </section>
    </template>

    <div v-else-if="!loading" class="bg-white border border-[#E2E8F0] rounded-md p-6 text-sm text-slate-400">
      未找到对应靶点记录。
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { fetchTargetBioactivities, fetchTargetDetail, fetchTargetNaturalProducts } from '@/api/targets';
import type { BioactivityApi, NaturalProductApi, TargetDetailApi } from '@/api/types';
import { formatActivityValue, formatCount, formatDecimal, toNumber } from '@/utils/format';

const PAGE_SIZE = 20;

const route = useRoute();
const activeTab = ref<'compounds' | 'bio'>('compounds');

const target = ref<TargetDetailApi | null>(null);
const loading = ref(false);
const error = ref('');

// compounds tab
const compounds = ref<NaturalProductApi[]>([]);
const compoundsPage = ref(1);
const compoundsTotal = ref(0);
const compoundsLoading = ref(false);

// bio tab
const bioactivities = ref<BioactivityApi[]>([]);
const bioPage = ref(1);
const bioTotal = ref(0);
const bioLoading = ref(false);

const targetId = computed(() => String(route.params.id || ''));

const uniprotIds = computed(() => {
  if (!target.value?.uniprotId) return [];
  return target.value.uniprotId.split(/[,;]\s*/).filter(id => id.trim());
});

const ttdIds = computed(() => {
  if (!target.value?.ttdId) return [];
  return target.value.ttdId.split(/[,;]\s*/).filter(id => id.trim());
});

const pdbIds = computed(() => {
  if (!target.value?.pdbStructure) return [];
  return target.value.pdbStructure.split(/[,;]\s*/).filter(id => id.trim());
});

const compoundRows = computed(() =>
  compounds.value.map((item) => ({
    id: item.npId || '-',
    name: item.prefName || item.iupacName || item.npId || '—',
    molecularWeight: toNumber(item.molecularWeight),
    bestActivityValue: toNumber(item.bestActivityValue),
  }))
);

const compoundsTotalPages = computed(() => Math.ceil(compoundsTotal.value / PAGE_SIZE));
const bioTotalPages = computed(() => Math.ceil(bioTotal.value / PAGE_SIZE));

const tabs = computed(() => [
  { id: 'compounds', name: '相关天然产物', count: target.value?.naturalProductCount ?? compoundsTotal.value },
  { id: 'bio', name: '活性记录', count: target.value?.bioactivityCount ?? bioTotal.value },
]);

const loadCompounds = async (page: number) => {
  if (!targetId.value) return;
  compoundsLoading.value = true;
  try {
    const res = await fetchTargetNaturalProducts(targetId.value, { page, pageSize: PAGE_SIZE });
    compounds.value = res.records ?? [];
    compoundsTotal.value = res.total ?? 0;
    compoundsPage.value = page;
  } finally {
    compoundsLoading.value = false;
  }
};

const loadBio = async (page: number) => {
  if (!targetId.value) return;
  bioLoading.value = true;
  try {
    const res = await fetchTargetBioactivities(targetId.value, { page, pageSize: PAGE_SIZE });
    bioactivities.value = res.records ?? [];
    bioTotal.value = res.total ?? 0;
    bioPage.value = page;
  } finally {
    bioLoading.value = false;
  }
};

const onTabChange = (tab: 'compounds' | 'bio') => {
  activeTab.value = tab;
  if (tab === 'compounds' && compounds.value.length === 0) loadCompounds(1);
  if (tab === 'bio' && bioactivities.value.length === 0) loadBio(1);
};

const init = async () => {
  if (!targetId.value) return;
  loading.value = true;
  error.value = '';
  compounds.value = [];
  bioactivities.value = [];
  compoundsPage.value = 1;
  bioPage.value = 1;
  compoundsTotal.value = 0;
  bioTotal.value = 0;
  try {
    target.value = await fetchTargetDetail(targetId.value);
    await loadCompounds(1);
  } catch (err) {
    error.value = err instanceof Error ? err.message : '数据加载失败';
    target.value = null;
  } finally {
    loading.value = false;
  }
};

watch(targetId, () => {
  activeTab.value = 'compounds';
  init();
}, { immediate: true });
</script>
