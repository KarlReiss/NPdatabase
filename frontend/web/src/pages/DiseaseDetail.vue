<template>
  <div
    class="max-w-[1200px] mx-auto px-6 py-8"
    :style="{ '--theme': '#8A3D3D', '--theme-soft': '#F1DDDD', '--theme-bg': '#F7EEEE' }"
  >
    <nav class="text-xs text-slate-500 mb-6 flex items-center space-x-2">
      <RouterLink to="/" class="hover:text-[#10B981]">首页</RouterLink>
      <span>/</span>
      <RouterLink to="/diseases" class="hover:text-[#10B981]">疾病列表</RouterLink>
      <span>/</span>
      <span class="text-slate-700 font-medium">{{ disease?.diseaseNameZh || disease?.diseaseName || '—' }}</span>
    </nav>

    <div v-if="loading" class="text-sm text-slate-500 mb-4">加载中...</div>
    <div v-if="error" class="text-sm text-red-500 mb-4">{{ error }}</div>

    <section v-if="disease" class="bg-white rounded-lg border border-[#E2E8F0] shadow-sm p-8 mb-8">
      <div class="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6">
        <div class="space-y-4">
          <div>
            <div class="flex items-center gap-3 flex-wrap">
              <h1 class="text-2xl font-bold text-slate-800">{{ disease.diseaseNameZh || disease.diseaseName }}</h1>
              <span class="px-2.5 py-0.5 rounded-full text-[11px] font-semibold" style="background: var(--theme-soft); color: var(--theme);">
                疾病
              </span>
            </div>
            <div class="mt-2 text-base text-slate-500 flex flex-wrap gap-x-4 gap-y-1">
              <span>编号：{{ disease.id }}</span>
              <span>ICD-11：{{ disease.icd11Code }}</span>
              <span>分类：{{ disease.diseaseCategory ?? '—' }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section v-if="disease" class="bg-white rounded-md border border-[#E2E8F0] shadow-sm overflow-hidden">
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
        <div v-if="activeTab === 'resources'">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-50/50">
                <th class="p-3 text-sm font-bold text-slate-700 border-b">编号</th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">资源名称</th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">类型</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50">
              <tr v-if="relatedResources.length === 0">
                <td colspan="3" class="p-6 text-sm text-slate-400 text-center">暂无关联生物资源</td>
              </tr>
              <tr v-else v-for="res in relatedResources" :key="res.resourceId" class="hover:bg-slate-50/50">
                <td class="p-3 text-sm">
                  <RouterLink :to="`/resources/${res.resourceId}`" class="text-[#3B82F6] hover:underline font-medium">
                    {{ res.resourceId }}
                  </RouterLink>
                </td>
                <td class="p-3 text-sm text-slate-700">{{ res.chineseName || res.latinName || res.resourceId }}</td>
                <td class="p-3 text-sm text-slate-600">{{ toTypeLabel(res.resourceType) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="activeTab === 'compounds'">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-50/50">
                <th class="p-3 text-sm font-bold text-slate-700 border-b">编号</th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">名称</th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">分子量（MW）</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50">
              <tr v-if="relatedCompounds.length === 0">
                <td colspan="3" class="p-6 text-sm text-slate-400 text-center">暂无关联天然产物</td>
              </tr>
              <tr v-else v-for="cmp in relatedCompounds" :key="cmp.npId" class="hover:bg-slate-50/50">
                <td class="p-3 text-sm">
                  <RouterLink :to="`/compounds/${cmp.npId}`" class="text-[#3B82F6] hover:underline font-medium">
                    {{ cmp.npId }}
                  </RouterLink>
                </td>
                <td class="p-3 text-sm text-slate-700">{{ cmp.prefName || cmp.iupacName || cmp.npId }}</td>
                <td class="p-3 text-sm text-slate-600">{{ formatDecimal(cmp.molecularWeight) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <div v-else-if="!loading" class="bg-white border border-[#E2E8F0] rounded-md p-6 text-sm text-slate-400">
      未找到对应疾病记录。
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { fetchDiseaseBioResources, fetchDiseaseDetail, fetchDiseaseNaturalProducts } from '@/api/diseases';
import type { BioResource, Disease, NaturalProductApi } from '@/api/types';
import { formatDecimal } from '@/utils/format';

const route = useRoute();
const activeTab = ref<'resources' | 'compounds'>('resources');

const disease = ref<Disease | null>(null);
const relatedResources = ref<BioResource[]>([]);
const relatedCompounds = ref<NaturalProductApi[]>([]);
const loading = ref(false);
const error = ref('');

const diseaseId = computed(() => String(route.params.id || ''));

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

const tabs = computed(() => [
  { id: 'resources', name: '关联生物资源', count: relatedResources.value.length },
  { id: 'compounds', name: '关联天然产物', count: relatedCompounds.value.length },
]);

const fetchAll = async () => {
  if (!diseaseId.value) return;
  loading.value = true;
  error.value = '';
  try {
    const detailPromise = fetchDiseaseDetail(diseaseId.value);
    const resourcesPromise = fetchDiseaseBioResources(diseaseId.value);
    const compoundsPromise = fetchDiseaseNaturalProducts(diseaseId.value);
    const [detailResult, resourcesResult, compoundsResult] = await Promise.allSettled([
      detailPromise,
      resourcesPromise,
      compoundsPromise,
    ]);

    if (detailResult.status === 'fulfilled') {
      disease.value = detailResult.value;
    } else {
      throw detailResult.reason;
    }

    relatedResources.value = resourcesResult.status === 'fulfilled' ? resourcesResult.value : [];
    relatedCompounds.value = compoundsResult.status === 'fulfilled' ? compoundsResult.value : [];
  } catch (err) {
    error.value = err instanceof Error ? err.message : '数据加载失败';
    disease.value = null;
    relatedResources.value = [];
    relatedCompounds.value = [];
  } finally {
    loading.value = false;
  }
};

watch(diseaseId, () => {
  activeTab.value = 'resources';
  fetchAll();
}, { immediate: true });
</script>
