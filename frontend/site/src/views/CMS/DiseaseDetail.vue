<template>
  <div
    class="max-w-[1440px] mx-auto px-6 py-6"
    :style="{ '--theme': '#8A3D3D', '--theme-soft': '#F1DDDD', '--theme-bg': '#F7EEEE' }"
  >
    <nav
      class="text-xs text-slate-500 mb-5 flex items-center space-x-2 bg-[#f1f1f1] dark:bg-[var(--el-bg-color)] p-4 rounded-1"
    >
      <RouterLink
        to="/"
        class="color-[#212121] dark:color-white hover:color-[var(--el-color-primary)] select-none no-underline hover:no-underline"
        >首页</RouterLink
      >
      <span class="dark:color-white">></span>
      <RouterLink
        to="/web/diseases"
        class="color-[#212121] dark:color-white hover:color-[var(--el-color-primary)] select-none no-underline hover:no-underline"
        >疾病列表</RouterLink
      >
      <span class="dark:color-white">></span>
      <span class="text-slate-700 font-medium select-none">
        {{ infoItem?.diseaseNameZh || infoItem?.diseaseName || '—' }}
      </span>
    </nav>

    <div v-if="loading" class="text-sm text-slate-500 mb-4">加载中...</div>
    <el-skeleton v-if="!infoItem && loading" :rows="15" animated />
    <el-alert v-if="error" :title="error" type="error" class="text-sm text-red-500 mb-4" />

    <section v-if="infoItem" class="bg-white rounded-lg border border-[#E2E8F0] shadow-sm mb-4">
      <div class="flex items-center gap-3 flex-wrap bg-[var(--el-color-primary)] p-4 rounded-1">
        <h1 class="text-2xl font-400 color-white">{{
          infoItem.diseaseNameZh || infoItem.diseaseName
        }}</h1>
        <span
          class="px-2.5 py-0.5 color-white text-sm border border-solid border-white rounded-full"
        >
          疾病
        </span>
      </div>
      <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4 text-base text-slate-600">
        <div class="p-5 rounded-2 border border-solid border-[var(--theme-soft)] max-h-[104px]">
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[108px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">ICD-11</span>
            {{ infoItem.icd11Code || '—' }}
          </div>
          <div
            v-if="infoItem.diseaseName"
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[108px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">英文名</span>
            {{ infoItem.diseaseName || '—' }}
          </div>
        </div>
        <div class="p-5 rounded-2 border border-solid border-[var(--theme-soft)] max-h-[104px]">
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[108px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">疾病分类</span>
            {{ infoItem.diseaseCategory || '—' }}
          </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[108px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">CMAUP 名称</span>
            {{ infoItem.diseaseNameCmaup || '—' }}
          </div>
        </div>
        <!-- <div
          class="grid grid-cols-2 md:grid-cols-2 gap-4 rounded-lg p-5 overflow-hidden bg-[#FCF1E1] relative"
        >
          <div class="absolute top-0 bottom-0 left-0 w-1.5 bg-[#E59317]"></div>
          <div class="text-center">
            <div class="text-base color-[#212121]">关联靶点</div>
            <div class="text-xl font-500 color-[#E59317]">
              {{ infoItem.numOfRelatedTargets || '—' }}
            </div>
          </div>
          <div class="text-center">
            <div class="text-base color-[#212121]">关联植物</div>
            <div class="text-xl font-500 color-[#E59317]">
              {{ infoItem.numOfRelatedPlants || '—' }}
            </div>
          </div>
        </div> -->
      </div>

      <div class="mt-6 grid grid-cols-1 md:grid-cols-1 gap-4 text-base text-slate-600">
        <div class="rounded-lg px-4 py-6 bg-[#E1F3F8] relative">
          <div
            class="px-2.5 py-0.5 text-xs color-white bg-[var(--el-color-primary)] rounded-1 absolute top-1 left-1 z-10"
            >简介</div
          >
          <div class="pt-5 rounded-2 min-h-[80px]">
            <p class="text-sm text-slate-600 leading-7 color-slate-500 font-400">{{
              infoItem.description || '疾病信息待补充。'
            }}</p>
          </div>
        </div>
      </div>
    </section>

    <section
      v-if="infoItem"
      class="bg-white rounded-md border dark:bg-[var(--el-bg-color)] border-[#E2E8F0] shadow-sm overflow-hidden"
    >
      <CusTabMenu v-model="activeTab" :tabs="tabs" />

      <div class="p-4 min-h-100">
        <div v-show="activeTab === 'resources'">
          <CommonTable
            rowKey="id"
            emptyText="暂无关联生物资源"
            :listById="diseaseId"
            :apiFetch="fetchDiseaseBioResources"
            :columns="[
              {
                prop: 'resourceId',
                label: '编号',
                renderer: (row, val, idx) => {
                  return h(
                    RouterLink,
                    {
                      to: `/resources/${row.resourceId}`,
                      class:
                        'text-[var(--el-color-primary)] hover:underline font-medium select-none no-underline hover:no-underline'
                    },
                    row.resourceId
                  )
                }
              },
              {
                prop: 'chineseName',
                label: '资源名称',
                func: (row, val, idx) => {
                  return row.chineseName || row.latinName || row.resourceId
                }
              },
              {
                prop: 'resourceType',
                label: '类型',
                func: (row, val, idx) => {
                  return toTypeLabel(row.resourceType)
                }
              }
            ]"
            @update:count="onUpdatedCount($event, 'resources')"
          />
        </div>

        <div v-show="activeTab === 'compounds'">
          <CommonTable
            rowKey="id"
            emptyText="暂无关联天然产物"
            :listById="diseaseId"
            :apiFetch="fetchDiseaseNaturalProducts"
            :columns="[
              {
                prop: 'npId',
                label: '编号',
                renderer: (row, val, idx) => {
                  return h(
                    RouterLink,
                    {
                      to: `/compounds/${row.npId}`,
                      class:
                        'text-[var(--el-color-primary)] hover:underline font-medium select-none no-underline hover:no-underline'
                    },
                    row.npId
                  )
                }
              },
              {
                prop: 'prefName',
                label: '名称',
                func: (row, val, idx) => {
                  return row.prefName || row.iupacName || row.npId
                }
              },
              {
                prop: 'molecularWeight',
                label: '分子量（MW）',
                func: (row, val, idx) => {
                  return formatDecimal(row.molecularWeight)
                }
              }
            ]"
            @update:count="onUpdatedCount($event, 'compounds')"
          />
        </div>
      </div>
    </section>

    <div
      v-else-if="!loading"
      class="bg-white border border-[#E2E8F0] rounded-md p-6 text-sm text-slate-400"
    >
      未找到对应疾病记录。
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  fetchDiseaseBioResources,
  fetchDiseaseDetail,
  fetchDiseaseNaturalProducts
} from '@/app/api/cms/diseases'
import { computed, ref, watch, h, reactive } from 'vue'
import CommonTable from './components/CommonTable.vue'
import CusTabMenu from './components/CusTabMenu.vue'
import { RouterLink, useRoute } from 'vue-router'
import { formatDecimal } from '@/app/utils/index'

const route = useRoute()
const activeTab = ref<any>('resources')
const menuState = reactive<any>({ resources: 0, compounds: 0 })
const onUpdatedCount = (val, key) => {
  menuState[key] = val
}
const tabs = computed(() => [
  { value: 'resources', label: '关联生物资源', count: menuState.resources },
  { value: 'compounds', label: '关联天然产物', count: menuState.compounds }
])

const infoItem = ref<any>(null)
const loading = ref(false)
const error = ref('')

const diseaseId = computed(() => String(route.params.id || ''))

const toTypeLabel = (value?: string) => {
  if (!value) return '—'
  const key = value.trim().toLowerCase()
  if (key === 'plant') return '植物'
  if (key === 'animal') return '动物'
  if (key === 'mineral') return '矿物'
  if (key === 'fungi' || key === 'fungus') return '真菌'
  if (key === 'microbe' || key === 'microorganism') return '微生物'
  if (key === 'bacteria') return '细菌'
  if (key === 'virus') return '病毒'
  if (key === 'algae') return '藻类'
  if (key === 'unknown' || key === 'unclassified') return '未知'
  if (key === 'other') return '其他'
  return value
}

const fetchAll = async () => {
  if (!diseaseId.value) return
  loading.value = true
  error.value = ''
  try {
    const detailPromise = fetchDiseaseDetail(diseaseId.value)
    const [detailResult] = await Promise.allSettled([detailPromise])

    if (detailResult.status === 'fulfilled') {
      infoItem.value = detailResult.value as any
    } else {
      throw detailResult.reason
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : '数据加载失败'
    infoItem.value = null
  } finally {
    loading.value = false
  }
}

watch(
  diseaseId,
  () => {
    activeTab.value = 'resources'
    fetchAll()
  },
  { immediate: true }
)
</script>
