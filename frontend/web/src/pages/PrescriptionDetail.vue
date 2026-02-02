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

          <div class="flex flex-wrap gap-2">
            <span class="px-3 py-1 rounded-full text-sm bg-slate-100 text-slate-600">
              分类：{{ prescription.category ?? '—' }} / {{ prescription.subcategory ?? '—' }}
            </span>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3 rounded-lg p-4 min-w-[240px]" style="background: var(--theme-bg); border: 1px solid var(--theme-soft);">
          <div class="text-center">
            <div class="text-xs text-slate-500">药材数</div>
            <div class="text-xl font-semibold text-slate-800">{{ prescription.numOfHerbs }}</div>
          </div>
          <div class="text-center">
            <div class="text-xs text-slate-500">天然产物</div>
            <div class="text-xl font-semibold text-slate-800">{{ prescription.numOfNaturalProducts }}</div>
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
          <div class="text-xs text-slate-400 uppercase tracking-wider">来源信息</div>
          <div class="mt-2 space-y-1">
            <div>来源书籍：{{ prescription.sourceBook ?? '—' }}</div>
            <div>朝代/作者：{{ prescription.sourceDynasty ?? '—' }} / {{ prescription.sourceAuthor ?? '—' }}</div>
            <div>别名：{{ prescription.alias ?? '—' }}</div>
          </div>
        </div>
        <div class="rounded-lg p-4" style="background: #fff; border: 1px solid #E2E8F0;">
          <div class="text-xs text-slate-400 uppercase tracking-wider">用法与剂型</div>
          <div class="mt-2 space-y-1">
            <div>剂型：{{ prescription.dosageForm ?? '—' }}</div>
            <div>用法：{{ prescription.usageMethod ?? '—' }}</div>
            <div>用量：{{ prescription.dosage ?? '—' }}</div>
          </div>
        </div>
      </div>

      <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-slate-600">
        <div class="rounded-lg p-4" style="background: #fff; border: 1px solid #E2E8F0;">
          <div class="text-xs text-slate-400 uppercase tracking-wider">组成与制备</div>
          <div class="mt-2 space-y-2">
            <div>组成：{{ prescription.compositionText ?? '—' }}</div>
            <div>制备方法：{{ prescription.preparationMethod ?? '—' }}</div>
          </div>
        </div>
        <div class="rounded-lg p-4" style="background: #fff; border: 1px solid #E2E8F0;">
          <div class="text-xs text-slate-400 uppercase tracking-wider">注意事项</div>
          <div class="mt-2 space-y-2">
            <div>禁忌：{{ prescription.contraindications ?? '—' }}</div>
            <div>注意事项：{{ prescription.precautions ?? '—' }}</div>
            <div>不良反应：{{ prescription.adverseReactions ?? '—' }}</div>
          </div>
        </div>
      </div>

      <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-slate-600">
        <div class="rounded-lg p-4" style="background: #fff; border: 1px solid #E2E8F0;">
          <div class="text-xs text-slate-400 uppercase tracking-wider">现代信息</div>
          <div class="mt-2 space-y-2">
            <div>现代主治：{{ prescription.indicationsModern ?? '—' }}</div>
            <div>证型：{{ prescription.syndrome ?? '—' }}</div>
            <div>药理：{{ prescription.pharmacology ?? '—' }}</div>
            <div>临床应用：{{ prescription.clinicalApplication ?? '—' }}</div>
          </div>
        </div>
        <div class="rounded-lg p-4" style="background: #fff; border: 1px solid #E2E8F0;">
          <div class="text-xs text-slate-400 uppercase tracking-wider">疾病与组织</div>
          <div class="mt-2 space-y-2">
            <div>相关疾病：{{ prescription.relatedDiseases ?? '—' }}</div>
            <div>ICD-11 分类：{{ prescription.diseaseIcd11Category ?? '—' }}</div>
            <div>人体组织：{{ prescription.humanTissues ?? '—' }}</div>
            <div>靶向组织：{{ prescription.targetTissues ?? '—' }}</div>
          </div>
        </div>
      </div>

      <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-slate-600">
        <div class="rounded-lg p-4" style="background: #fff; border: 1px solid #E2E8F0;">
          <div class="text-xs text-slate-400 uppercase tracking-wider">外部标识</div>
          <div class="mt-2 space-y-1">
            <div>TCMID/TCMSP/SymMap：{{ prescription.tcmidId ?? '—' }} / {{ prescription.tcmspId ?? '—' }} / {{ prescription.symmapId ?? '—' }}</div>
          </div>
        </div>
        <div class="rounded-lg p-4" style="background: #fff; border: 1px solid #E2E8F0;">
          <div class="text-xs text-slate-400 uppercase tracking-wider">参考信息</div>
          <div class="mt-2 space-y-1">
            <div>参考文献：{{ prescription.reference ?? '—' }}</div>
            <div>参考书籍：{{ prescription.referenceBook ?? '—' }}</div>
            <div>药典/文献：{{ prescription.pharmacopoeiaRef ?? '—' }} / {{ prescription.literatureRef ?? '—' }}</div>
          </div>
        </div>
      </div>
    </section>

    <section v-if="prescription" class="bg-white rounded-md border border-[#E2E8F0] shadow-sm overflow-hidden">
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
                <th class="p-3 text-sm font-bold text-slate-700 border-b">药材编号</th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">药材名称</th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">角色</th>
                <th class="p-3 text-sm font-bold text-slate-700 border-b">用量</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50">
              <tr v-for="resource in relatedResources" :key="resource.resourceId" class="hover:bg-slate-50/50">
                <td class="p-3 text-sm">
                  <RouterLink :to="`/resources/${resource.resourceId}`" class="text-[#3B82F6] hover:underline font-medium">
                    {{ resource.resourceId }}
                  </RouterLink>
                </td>
                <td class="p-3 text-sm text-slate-700">{{ resource.chineseName }}</td>
                <td class="p-3 text-sm text-slate-600">—</td>
                <td class="p-3 text-sm text-slate-600">—</td>
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
                <th class="p-3 text-sm font-bold text-slate-700 border-b">来源药材</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50">
              <tr v-for="cmp in relatedCompounds" :key="cmp.npId" class="hover:bg-slate-50/50">
                <td class="p-3 text-sm">
                  <RouterLink :to="`/compounds/${cmp.npId}`" class="text-[#3B82F6] hover:underline font-medium">
                    {{ cmp.npId }}
                  </RouterLink>
                </td>
                <td class="p-3 text-sm text-slate-700">{{ cmp.prefName || cmp.iupacName || cmp.npId }}</td>
                <td class="p-3 text-sm text-slate-600">{{ relatedResources[0]?.chineseName ?? '—' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
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
import { fetchPrescriptionBioResources, fetchPrescriptionDetail, fetchPrescriptionNaturalProducts } from '@/api/prescriptions';
import type { BioResource, NaturalProductApi, Prescription } from '@/api/types';

const route = useRoute();
const activeTab = ref<'resources' | 'compounds'>('resources');

const prescription = ref<Prescription | null>(null);
const relatedResources = ref<BioResource[]>([]);
const relatedCompounds = ref<NaturalProductApi[]>([]);
const loading = ref(false);
const error = ref('');

const prescriptionId = computed(() => String(route.params.id || ''));

const tabs = computed(() => [
  { id: 'resources', name: '组成药材', count: relatedResources.value.length },
  { id: 'compounds', name: '关联天然产物', count: relatedCompounds.value.length },
]);

const fetchAll = async () => {
  if (!prescriptionId.value) return;
  loading.value = true;
  error.value = '';
  try {
    const detailPromise = fetchPrescriptionDetail(prescriptionId.value);
    const resourcesPromise = fetchPrescriptionBioResources(prescriptionId.value);
    const compoundsPromise = fetchPrescriptionNaturalProducts(prescriptionId.value);
    const [detailResult, resourcesResult, compoundsResult] = await Promise.allSettled([
      detailPromise,
      resourcesPromise,
      compoundsPromise,
    ]);

    if (detailResult.status === 'fulfilled') {
      prescription.value = detailResult.value;
    } else {
      throw detailResult.reason;
    }

    relatedResources.value = resourcesResult.status === 'fulfilled' ? resourcesResult.value : [];
    relatedCompounds.value = compoundsResult.status === 'fulfilled' ? compoundsResult.value : [];
  } catch (err) {
    error.value = err instanceof Error ? err.message : '数据加载失败';
    prescription.value = null;
    relatedResources.value = [];
    relatedCompounds.value = [];
  } finally {
    loading.value = false;
  }
};

watch(prescriptionId, () => {
  activeTab.value = 'resources';
  fetchAll();
}, { immediate: true });
</script>
