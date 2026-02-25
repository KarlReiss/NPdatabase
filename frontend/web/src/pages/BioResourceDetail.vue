<template>
  <div
    class="max-w-[1200px] mx-auto px-6 py-8"
    :style="{ '--theme': '#2F6F5E', '--theme-soft': '#DDEBE6', '--theme-bg': '#EFF6F2' }"
  >
    <nav class="text-xs text-slate-500 mb-6 flex items-center space-x-2">
      <RouterLink to="/" class="hover:text-[#10B981]">首页</RouterLink>
      <span>/</span>
      <RouterLink to="/resources" class="hover:text-[#10B981]">生物资源列表</RouterLink>
      <span>/</span>
      <span class="text-slate-700 font-medium">{{ resource?.resourceId || '—' }}</span>
    </nav>

    <div v-if="loading" class="text-sm text-slate-500 mb-4">加载中...</div>
    <div v-if="error" class="text-sm text-red-500 mb-4">{{ error }}</div>

    <section v-if="resource" class="bg-white rounded-lg border border-[#E2E8F0] shadow-sm p-8 mb-8">
      <div class="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6">
        <div class="space-y-4">
          <div>
            <div class="flex items-center gap-3 flex-wrap">
              <h1 class="text-2xl font-bold text-slate-800">{{ resource.chineseName }}</h1>
              <span class="px-2.5 py-0.5 rounded-full text-[11px] font-semibold" style="background: var(--theme-soft); color: var(--theme);">
                生物资源
              </span>
            </div>
            <div class="mt-2 text-base text-slate-500 flex flex-wrap gap-x-4 gap-y-1">
              <span>编号：{{ resource.resourceId }}</span>
              <span>拉丁名：{{ resource.latinName ?? '—' }}</span>
            </div>
          </div>

        </div>

        <div class="grid grid-cols-2 gap-3 rounded-lg p-4 min-w-[240px]" style="background: var(--theme-bg); border: 1px solid var(--theme-soft);">
          <div class="text-center">
            <div class="text-xs text-slate-500">天然产物</div>
            <div class="text-xl font-semibold text-slate-800">{{ resource.numOfNaturalProducts }}</div>
          </div>
          <div class="text-center">
            <div class="text-xs text-slate-500">相关处方</div>
            <div class="text-xl font-semibold text-slate-800">{{ resource.numOfPrescriptions }}</div>
          </div>
        </div>
      </div>

      <div class="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-4 text-sm text-slate-600">
        <div class="rounded-lg p-4" style="background: #fff; border: 1px solid #E2E8F0;">
          <div class="text-xs text-slate-400 uppercase tracking-wider">基本信息</div>
          <div class="mt-3 grid grid-cols-1 md:grid-cols-2 gap-3">
            <div>资源类型：{{ resource.resourceType ?? '—' }}</div>
            <div>中文名来源：{{ resource.translationSource ?? '—' }}</div>
            <div>拉丁名：{{ resource.latinName ?? '—' }}</div>
            <div>Taxonomy ID：{{ resource.taxonomyId ?? '—' }}</div>
          </div>
        </div>

        <div class="rounded-lg p-4" style="background: var(--theme-bg); border: 1px solid var(--theme-soft);">
          <div class="text-xs text-slate-400 uppercase tracking-wider">分类学信息</div>
          <div class="mt-2 space-y-1 text-sm text-slate-600">
            <div>界：{{ resource.taxonomyKingdom ?? '—' }}</div>
            <div>科/属/种：{{ resource.taxonomyFamily ?? '—' }} / {{ resource.taxonomyGenus ?? '—' }} / {{ resource.taxonomySpecies ?? '—' }}</div>
            <div>Family/Genus/Species Tax ID：{{ resource.familyTaxId ?? '—' }} / {{ resource.genusTaxId ?? '—' }} / {{ resource.speciesTaxId ?? '—' }}</div>
          </div>
        </div>

        <div class="rounded-lg p-4" style="background: #fff; border: 1px solid #E2E8F0;">
          <div class="text-xs text-slate-400 uppercase tracking-wider">标识信息</div>
          <div class="mt-2 space-y-1 text-sm text-slate-600">
            <div>CMAUP ID：{{ resource.cmaupId ?? '—' }}</div>
            <div>TCMID：{{ resource.tcmidId ?? '—' }}</div>
            <div>资源编号：{{ resource.resourceId ?? '—' }}</div>
          </div>
        </div>

        <div class="rounded-lg p-4" style="background: var(--theme-bg); border: 1px solid var(--theme-soft);">
          <div class="text-xs text-slate-400 uppercase tracking-wider">统计信息</div>
          <div class="mt-2 space-y-1 text-sm text-slate-600">
            <div>天然产物数：{{ resource.numOfNaturalProducts ?? 0 }}</div>
            <div>相关处方数：{{ resource.numOfPrescriptions ?? 0 }}</div>
          </div>
        </div>
      </div>

    </section>

    <section v-if="resource" class="bg-white rounded-md border border-[#E2E8F0] shadow-sm overflow-hidden">
      <div class="flex border-b border-[#E2E8F0] px-4">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="onTabChange(tab.id as 'compounds' | 'prescriptions')"
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
        <div v-if="activeTab === 'compounds'">
          <div v-if="compoundsLoading" class="text-sm text-slate-400 py-4">加载中...</div>
          <table v-else class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-50/50">
                <th class="p-3 text-sm font-bold text-slate-700 border-b">编号</th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">名称</th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">分子量</th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">数据来源</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50">
              <tr v-for="cmp in compounds" :key="cmp.npId" class="hover:bg-slate-50/50">
                <td class="p-3 text-sm">
                  <RouterLink :to="`/natural-products/${cmp.npId}`" class="text-[#3B82F6] hover:underline font-medium">
                    {{ cmp.npId }}
                  </RouterLink>
                </td>
                <td class="p-3 text-sm text-slate-700">
                  <div class="font-medium">{{ cmp.prefName || cmp.iupacName || cmp.npId }}</div>
                </td>
                <td class="p-3 text-sm text-slate-600">{{ formatDecimal(cmp.molecularWeight) }}</td>
                <td class="p-3 text-sm text-slate-600">{{ formatSource(cmp) }}</td>
              </tr>
            </tbody>
          </table>
          <div class="flex items-center justify-between mt-4 text-sm text-slate-500">
            <span>第 {{ compoundsPage }} / {{ Math.ceil(compoundsTotal / 20) || 1 }} 页，共 {{ compoundsTotal }} 条</span>
            <div class="flex gap-2">
              <button :disabled="compoundsPage <= 1" @click="loadCompounds(compoundsPage - 1)"
                class="px-3 py-1 rounded border text-xs disabled:opacity-40 hover:bg-slate-50">上一页</button>
              <button :disabled="compoundsPage >= Math.ceil(compoundsTotal / 20)" @click="loadCompounds(compoundsPage + 1)"
                class="px-3 py-1 rounded border text-xs disabled:opacity-40 hover:bg-slate-50">下一页</button>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'prescriptions'">
          <div v-if="presLoading" class="text-sm text-slate-400 py-4">加载中...</div>
          <table v-else class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-50/50">
                <th class="p-3 text-sm font-bold text-slate-700 border-b">编号</th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">处方名称</th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">主治</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50">
              <tr v-for="pres in prescriptions" :key="pres.prescriptionId" class="hover:bg-slate-50/50">
                <td class="p-3 text-sm">
                  <RouterLink :to="`/prescriptions/${pres.prescriptionId}`" class="text-[#3B82F6] hover:underline font-medium">
                    {{ pres.prescriptionId }}
                  </RouterLink>
                </td>
                <td class="p-3 text-sm text-slate-700">{{ pres.chineseName }}</td>
                <td class="p-3 text-sm text-slate-600">{{ pres.indications || '—' }}</td>
              </tr>
            </tbody>
          </table>
          <div class="flex items-center justify-between mt-4 text-sm text-slate-500">
            <span>第 {{ presPage }} / {{ Math.ceil(presTotal / 20) || 1 }} 页，共 {{ presTotal }} 条</span>
            <div class="flex gap-2">
              <button :disabled="presPage <= 1" @click="loadPrescriptions(presPage - 1)"
                class="px-3 py-1 rounded border text-xs disabled:opacity-40 hover:bg-slate-50">上一页</button>
              <button :disabled="presPage >= Math.ceil(presTotal / 20)" @click="loadPrescriptions(presPage + 1)"
                class="px-3 py-1 rounded border text-xs disabled:opacity-40 hover:bg-slate-50">下一页</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <div v-else-if="!loading" class="bg-white border border-[#E2E8F0] rounded-md p-6 text-sm text-slate-400">
      未找到对应生物资源记录。
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { fetchBioResourceDetail, fetchBioResourceNaturalProducts, fetchBioResourcePrescriptions } from '@/api/bioResources';
import type { BioResource, BioResourceNaturalProductItem, Prescription } from '@/api/types';
import { formatDecimal } from '@/utils/format';

const PAGE_SIZE = 20;

const route = useRoute();
const activeTab = ref<'compounds' | 'prescriptions'>('compounds');

const resource = ref<BioResource | null>(null);
const loading = ref(false);
const error = ref('');

// compounds tab state
const compounds = ref<BioResourceNaturalProductItem[]>([]);
const compoundsPage = ref(1);
const compoundsTotal = ref(0);
const compoundsLoading = ref(false);

// prescriptions tab state
const prescriptions = ref<Prescription[]>([]);
const presPage = ref(1);
const presTotal = ref(0);
const presLoading = ref(false);

const resourceId = computed(() => String(route.params.id || ''));

const tabs = computed(() => [
  { id: 'compounds', name: '相关天然产物', count: resource.value?.numOfNaturalProducts || compoundsTotal.value },
  { id: 'prescriptions', name: '相关处方', count: resource.value?.numOfPrescriptions || presTotal.value },
]);

const loadCompounds = async (page: number) => {
  compoundsLoading.value = true;
  try {
    const res = await fetchBioResourceNaturalProducts(resourceId.value, { page, pageSize: PAGE_SIZE });
    compounds.value = res.records;
    compoundsTotal.value = res.total;
    compoundsPage.value = page;
  } finally {
    compoundsLoading.value = false;
  }
};

const loadPrescriptions = async (page: number) => {
  presLoading.value = true;
  try {
    const res = await fetchBioResourcePrescriptions(resourceId.value, { page, pageSize: PAGE_SIZE });
    prescriptions.value = res.records;
    presTotal.value = res.total;
    presPage.value = page;
  } finally {
    presLoading.value = false;
  }
};

const onTabChange = (tab: 'compounds' | 'prescriptions') => {
  activeTab.value = tab;
  if (tab === 'compounds' && compounds.value.length === 0) loadCompounds(1);
  if (tab === 'prescriptions' && prescriptions.value.length === 0) loadPrescriptions(1);
};

const init = async () => {
  if (!resourceId.value) return;
  loading.value = true;
  error.value = '';
  compounds.value = [];
  prescriptions.value = [];
  compoundsPage.value = 1;
  presPage.value = 1;
  try {
    resource.value = await fetchBioResourceDetail(resourceId.value);
    await loadCompounds(1);
  } catch (err) {
    error.value = err instanceof Error ? err.message : '数据加载失败';
    resource.value = null;
  } finally {
    loading.value = false;
  }
};

watch(resourceId, () => {
  activeTab.value = 'compounds';
  init();
}, { immediate: true });

const formatSource = (item: BioResourceNaturalProductItem) => {
  const rawParts = [item.refType, item.refIdType, item.refId]
    .filter((value) => value != null && value !== '')
    .map((value) => String(value).trim())
    .filter((value) => value !== '' && value.toLowerCase() !== 'database');
  const parts: string[] = [];
  for (const value of rawParts) {
    if (parts.length === 0 || parts[parts.length - 1] !== value) {
      parts.push(value);
    }
  }
  return parts.length ? parts.join(' / ') : '—';
};
</script>
