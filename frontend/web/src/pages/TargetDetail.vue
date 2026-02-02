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
            <div class="mt-2 text-base text-slate-500 flex flex-wrap gap-x-4 gap-y-1">
              <span>编号：{{ target.targetId || '—' }}</span>
              <span>UniProt：{{ target.uniprotId || '—' }}</span>
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

      <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4 text-base text-slate-600">
        <div class="rounded-lg p-4" style="background: var(--theme-bg); border: 1px solid var(--theme-soft);">
          <div class="text-xs text-slate-400 uppercase tracking-wider">基础信息</div>
          <div class="mt-2 space-y-1 text-sm text-slate-600">
            <div>基因名：{{ target.geneName || '—' }}</div>
            <div>TTD ID：{{ target.ttdId || '—' }}</div>
            <div>EC 编号：{{ target.ecNumber || '—' }}</div>
            <div>PDB 结构：{{ target.pdbStructure || '—' }}</div>
            <div>生物分类：{{ target.bioclass || '—' }}</div>
            <div>物种 Tax ID：{{ target.targetOrganismTaxId || '—' }}</div>
          </div>
        </div>
        <div class="rounded-lg p-4" style="background: var(--theme-bg); border: 1px solid var(--theme-soft);">
          <div class="text-xs text-slate-400 uppercase tracking-wider">功能与同义词</div>
          <div class="mt-2 text-sm text-slate-600 leading-relaxed">
            <div>同义词：{{ target.synonyms || '—' }}</div>
            <div class="mt-2">功能：{{ target.function || '—' }}</div>
          </div>
        </div>
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
          <div v-if="activeTab === 'compounds'">
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
          </div>

          <div v-if="activeTab === 'bio'" class="py-10 text-sm text-slate-400 text-center">
            当前接口暂未提供靶点级活性明细，后续补充。
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
import { fetchTargetDetail, fetchTargetNaturalProducts } from '@/api/targets';
import type { NaturalProductApi, TargetDetailApi } from '@/api/types';
import { formatActivityValue, formatCount, formatDecimal, toNumber } from '@/utils/format';

const route = useRoute();
const activeTab = ref<'compounds' | 'bio'>('compounds');

const target = ref<TargetDetailApi | null>(null);
const relatedCompounds = ref<NaturalProductApi[]>([]);
const loading = ref(false);
const error = ref('');

const targetId = computed(() => String(route.params.id || ''));

const compoundRows = computed(() =>
  relatedCompounds.value.map((item) => ({
    id: item.npId || '-',
    name: item.prefName || item.iupacName || item.npId || '—',
    molecularWeight: toNumber(item.molecularWeight),
    bestActivityValue: toNumber(item.bestActivityValue),
  }))
);

const tabs = computed(() => [
  { id: 'compounds', name: '相关天然产物', count: relatedCompounds.value.length },
  { id: 'bio', name: '活性记录', count: target.value?.bioactivityCount ?? 0 },
]);

const fetchAll = async () => {
  if (!targetId.value) return;
  loading.value = true;
  error.value = '';
  try {
    const detailPromise = fetchTargetDetail(targetId.value);
    const compoundsPromise = fetchTargetNaturalProducts(targetId.value);
    const [detailResult, compoundResult] = await Promise.allSettled([detailPromise, compoundsPromise]);

    if (detailResult.status === 'fulfilled') {
      target.value = detailResult.value;
    } else {
      throw detailResult.reason;
    }

    relatedCompounds.value = compoundResult.status === 'fulfilled' ? compoundResult.value : [];
  } catch (err) {
    error.value = err instanceof Error ? err.message : '数据加载失败';
    target.value = null;
    relatedCompounds.value = [];
  } finally {
    loading.value = false;
  }
};

watch(targetId, () => {
  activeTab.value = 'compounds';
  fetchAll();
}, { immediate: true });
</script>
