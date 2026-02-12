<template>
  <div
    class="max-w-[1200px] mx-auto px-6 py-8"
    :style="{ '--theme': '#7A5A2E', '--theme-soft': '#EFE6D8', '--theme-bg': '#F7F1E6' }"
  >
    <nav class="text-xs text-slate-500 mb-6 flex items-center space-x-2">
      <RouterLink to="/" class="hover:text-[#10B981]">首页</RouterLink>
      <span>/</span>
      <RouterLink to="/prescriptions" class="hover:text-[#10B981]">处方列表</RouterLink>
      <span>/</span>
      <span class="text-slate-700 font-medium">{{ prescription?.prescriptionId || '—' }}</span>
    </nav>

    <div v-if="loading" class="text-sm text-slate-500 mb-4">加载中...</div>
    <div v-if="error" class="text-sm text-red-500 mb-4">{{ error }}</div>

    <section v-if="prescription" class="bg-white rounded-lg border border-[#E2E8F0] shadow-sm p-8 mb-8">
      <div class="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6">
        <div class="space-y-4">
          <div>
            <div class="flex items-center gap-3 flex-wrap">
              <h1 class="text-2xl font-bold text-slate-800">{{ prescription.chineseName }}</h1>
              <span class="px-2.5 py-0.5 rounded-full text-[11px] font-semibold" style="background: var(--theme-soft); color: var(--theme);">
                处方
              </span>
            </div>
            <div class="mt-2 text-base text-slate-500 flex flex-wrap gap-x-4 gap-y-1">
              <span>编号：{{ prescription.prescriptionId }}</span>
              <span>拼音：{{ prescription.pinyinName ?? '—' }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4 text-base text-slate-600">
        <div class="rounded-lg p-4" style="background: var(--theme-bg); border: 1px solid var(--theme-soft);">
          <div class="text-xs text-slate-400 uppercase tracking-wider">功效</div>
          <div class="mt-1">{{ prescription.functions ?? '—' }}</div>
        </div>
        <div class="rounded-lg p-4" style="background: var(--theme-bg); border: 1px solid var(--theme-soft);">
          <div class="text-xs text-slate-400 uppercase tracking-wider">主治</div>
          <div class="mt-1">{{ prescription.indications ?? '—' }}</div>
        </div>
      </div>

      <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-slate-600">
        <div class="rounded-lg p-4" style="background: #fff; border: 1px solid #E2E8F0;">
          <div class="text-xs text-slate-400 uppercase tracking-wider">外部标识</div>
          <div class="mt-2 space-y-1">
            <div>TCMID：{{ prescription.tcmidId ?? '—' }}</div>
            <div>ICD-11 分类：{{ prescription.diseaseIcd11Category ?? '—' }}</div>
          </div>
        </div>
        <div class="rounded-lg p-4" style="background: #fff; border: 1px solid #E2E8F0;">
          <div class="text-xs text-slate-400 uppercase tracking-wider">参考信息</div>
          <div class="mt-2 space-y-1">
            <div>参考文献：{{ prescription.reference ?? '—' }}</div>
          </div>
        </div>
      </div>
    </section>

    <section v-if="prescription" class="bg-white rounded-md border border-[#E2E8F0] shadow-sm overflow-hidden">
      <div class="p-6">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-slate-50/50">
              <th class="p-3 text-sm font-bold text-slate-700 border-b">编号</th>
              <th class="p-3 text-sm font-bold text-slate-700 border-b">药材（生物资源）</th>
              <th class="p-3 text-sm font-bold text-slate-700 border-b">资源类型</th>
              <th class="p-3 text-sm font-bold text-slate-700 border-b">分类（科/属）</th>
              <th class="p-3 text-sm font-bold text-slate-700 border-b">天然产物数</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50">
            <tr v-for="resource in relatedResources" :key="resource.resourceId" class="hover:bg-slate-50/50">
              <td class="p-3 text-sm">
                <RouterLink :to="`/resources/${resource.resourceId}`" class="text-[#3B82F6] hover:underline font-medium">
                  {{ resource.resourceId }}
                </RouterLink>
              </td>
              <td class="p-3 text-sm">
                <RouterLink :to="`/resources/${resource.resourceId}`" class="text-[#3B82F6] hover:underline font-medium">
                  {{
                    resource.standardChineseName
                      ?? resource.officialChineseName
                      ?? resource.chineseName
                      ?? resource.latinName
                      ?? resource.resourceId
                  }}
                </RouterLink>
              </td>
              <td class="p-3 text-sm text-slate-600">{{ toTypeLabel(resource.resourceType) }}</td>
              <td class="p-3 text-sm text-slate-600">
                {{ resource.taxonomyFamily ?? '—' }} / {{ resource.taxonomyGenus ?? '—' }}
              </td>
              <td class="p-3 text-sm text-slate-600">{{ resource.numOfNaturalProducts ?? 0 }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <div v-else-if="!loading" class="bg-white border border-[#E2E8F0] rounded-md p-6 text-sm text-slate-400">
      未找到对应处方记录。
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { fetchPrescriptionBioResources, fetchPrescriptionDetail } from '@/api/prescriptions';
import type { BioResource, Prescription } from '@/api/types';

const route = useRoute();
const prescription = ref<Prescription | null>(null);
const relatedResources = ref<BioResource[]>([]);
const loading = ref(false);
const error = ref('');

const prescriptionId = computed(() => String(route.params.id || ''));

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

const fetchAll = async () => {
  if (!prescriptionId.value) return;
  loading.value = true;
  error.value = '';
  try {
    const detailPromise = fetchPrescriptionDetail(prescriptionId.value);
    const resourcesPromise = fetchPrescriptionBioResources(prescriptionId.value);
    const [detailResult, resourcesResult] = await Promise.allSettled([
      detailPromise,
      resourcesPromise,
    ]);

    if (detailResult.status === 'fulfilled') {
      prescription.value = detailResult.value;
    } else {
      throw detailResult.reason;
    }

    relatedResources.value = resourcesResult.status === 'fulfilled' ? resourcesResult.value : [];
  } catch (err) {
    error.value = err instanceof Error ? err.message : '数据加载失败';
    prescription.value = null;
    relatedResources.value = [];
  } finally {
    loading.value = false;
  }
};

watch(prescriptionId, () => {
  fetchAll();
}, { immediate: true });
</script>
