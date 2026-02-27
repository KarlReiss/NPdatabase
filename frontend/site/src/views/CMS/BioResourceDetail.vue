<template>
  <div
    class="max-w-[1440px] mx-auto px-6 py-6"
    :style="{ '--theme': '#2F6F5E', '--theme-soft': '#DDEBE6', '--theme-bg': '#EFF6F2' }"
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
        to="/resources"
        class="color-[#212121] dark:color-white hover:color-[var(--el-color-primary)] select-none no-underline hover:no-underline"
        >生物资源列表</RouterLink
      >
      <span class="dark:color-white">></span>
      <span class="color-[var(--el-color-primary)] font-medium select-none">
        {{ infoItem?.resourceId || '—' }}
      </span>
    </nav>

    <div v-if="loading" class="text-sm text-slate-500 mb-4">加载中...</div>
    <el-skeleton v-if="!infoItem && loading" :rows="15" animated />
    <el-alert v-if="error" :title="error" type="error" class="text-sm text-red-500 mb-4" />

    <section v-if="infoItem" class="bg-white rounded-lg border border-[#E2E8F0] shadow-sm p-0 mb-8">
      <div class="flex items-center gap-3 flex-wrap bg-[var(--el-color-primary)] p-4 rounded-1">
        <h1 class="text-2xl font-400 color-white">{{ infoItem.chineseName }}</h1>
        <span
          class="px-2.5 py-1 text-sm color-white text-sm border border-solid border-white rounded-full"
        >
          生物资源
        </span>
      </div>
      <div class="flex flex-col lg:flex-row lg:items-start lg:justify-between space-x-6 mt-5">
        <div class="bg-[#EBEBEB] p-5 rounded-2 w-7/10">
          <div class="text-xl color-[#212121] font-400 pl-[78px] relative">
            <span class="color-[#212121] font-500 absolute top-0 left-0">类型</span>
            {{ toTypeLabel(infoItem.resourceType) }}
          </div>
          <div class="text-xl color-[#212121] font-400 pl-[78px] relative">
            <span class="color-[#212121] font-500 absolute top-0 left-0">分类</span>
            {{ infoItem.taxonomyFamily || '—' }} / {{ infoItem.taxonomyGenus || '—' }}
          </div>
        </div>
        <div
          class="grid grid-cols-1 md:grid-cols-2 gap-4 p-5 w-3/10 rounded-lg overflow-hidden bg-[#FCF1E1] relative"
        >
          <div class="absolute top-0 bottom-0 left-0 w-1.5 bg-[#E59317]"></div>
          <div class="text-center">
            <div class="text-xl color-[#212121]">天然产物</div>
            <div class="text-xl font-500 color-[#E59317]">
              {{ infoItem.numOfNaturalProducts || '—' }}
            </div>
          </div>
          <div class="text-center">
            <div class="text-xl color-[#212121]">相关处方</div>
            <div class="text-xl font-500 color-[#E59317]">
              {{ infoItem.numOfPrescriptions || '—' }}
            </div>
          </div>
        </div>
      </div>

      <div class="pt-2 px-1 bg-[#E1F3F8] rounded-2 mt-4">
        <span class="px-2.5 py-1 text-sm color-white bg-[var(--el-color-primary)] rounded-1">
          基本信息
        </span>
        <div class="flex flex-row space-x-4">
          <div class="p-4 w-1/2 text-left">
            <div
              class="text-base leading-7 min-h-7 color-slate-500 font-400 pl-[94px] relative w-full"
            >
              <span class="color-[#212121] font-500 absolute top-0 left-0">资源类型</span>
              {{ toTypeLabel(infoItem.resourceType) || '—' }}
            </div>
            <div
              class="text-base leading-7 min-h-7 color-slate-500 font-400 pl-[94px] relative w-full"
            >
              <span class="color-[#212121] font-500 absolute top-0 left-0">中文名来源 </span>
              {{ infoItem.translationSource || '—' }}
            </div>
          </div>
          <div class="p-4 w-1/2 text-left">
            <div
              class="text-base leading-7 min-h-7 color-slate-500 font-400 pl-[94px] relative w-full"
            >
              <span class="color-[#212121] font-500 absolute top-0 left-0">拉丁名</span>
              {{ infoItem.latinName || '—' }}
            </div>
          </div>
        </div>
      </div>

      <div class="flex flex-col lg:flex-row lg:items-start lg:justify-between space-x-6 mt-5">
        <div
          class="p-1 rounded-2 w-1/3 relative border border-solid border-[var(--theme-soft)] min-h-[230px]"
        >
          <span
            class="px-2.5 py-1 color-white bg-[var(--el-color-primary)] rounded-1 absolute top-1 left-1 z-10 text-sm"
          >
            示例图片
          </span>
          <img :src="infoItem.imageUrl" alt="示例图片" class="h-full w-full object-contain" />
        </div>
        <div
          class="p-5 rounded-2 w-2/3 border border-solid border-[var(--theme-soft)] min-h-[230px]"
        >
          <div class="color-[#212121] rounded-1 text-2xl leading-9 font-500 mb-2"> 分类学信息 </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[257px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">界</span>
            {{ infoItem.taxonomyKingdom || '—' }}
          </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[257px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">科/属/种</span>
            {{ infoItem.taxonomyFamily || '—' }} / {{ infoItem.taxonomyGenus || '—' }} /
            {{ infoItem.taxonomySpecies || '—' }}
          </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[257px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">TaxonomyID</span>
            {{ infoItem.taxonomyId || '—' }}
          </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[257px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0"
              >Family/Genus/Species Tax ID</span
            >
            {{ infoItem.familyTaxId || '—' }} / {{ infoItem.genusTaxId || '—' }} /
            {{ infoItem.speciesTaxId || '—' }}
          </div>
        </div>
      </div>
      <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4 text-base text-slate-600">
        <div class="p-5 rounded-2 border border-solid border-[var(--theme-soft)] min-h-[180px]">
          <div class="color-[#212121] rounded-1 text-2xl leading-9 font-500 mb-2"> 标识信息 </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">CMAUP ID</span>
            {{ infoItem.cmaupId || '—' }}
          </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">TCMID</span>
            <!-- {{ infoItem.tcmidId || '—' }} -->
            <template v-if="infoItem.tcmidId && infoItem.tcmidId.indexOf(',')">
              <div v-for="txt in infoItem.tcmidId.split(',')" :key="txt">{{ txt }}</div>
            </template>
            <div v-else>{{ infoItem.tcmidId || '-' }}</div>
          </div>
          <!-- <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0"
              >TCMSP</span
            >
            {{ infoItem.tcmspId || '—' }}
          </div> -->
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">资源编号 </span>
            {{ infoItem.resourceId || '—' }}
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
        <div v-show="activeTab === 'compounds'">
          <CommonTable
            rowKey="id"
            emptyText="暂无关联天然产物"
            :listById="resourceId"
            :apiFetch="fetchBioResourceNaturalProducts"
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
              },
              {
                prop: '',
                label: '数据来源',
                func: (row, val, idx) => {
                  return formatSource(row)
                }
              }
            ]"
            @update:count="onUpdatedCount($event, 'compounds')"
          />
        </div>

        <div v-show="activeTab === 'prescriptions'">
          <CommonTable
            rowKey="id"
            emptyText="暂无关联生物资源"
            :listById="resourceId"
            :apiFetch="fetchBioResourcePrescriptions"
            :columns="[
              {
                prop: 'prescriptionId',
                label: '编号',
                renderer: (row, val, idx) => {
                  return h(
                    RouterLink,
                    {
                      to: `/prescriptions/${row.prescriptionId}`,
                      class:
                        'text-[var(--el-color-primary)] hover:underline font-medium select-none no-underline hover:no-underline'
                    },
                    row.prescriptionId
                  )
                }
              },
              {
                prop: 'chineseName',
                label: '处方名称',
                func: (row, val, idx) => {
                  return row.chineseName
                }
              },
              {
                prop: 'indications',
                label: '主治',
                func: (row, val, idx) => {
                  return row.indications || '—'
                }
              }
            ]"
            @update:count="onUpdatedCount($event, 'prescriptions')"
          />
        </div>
      </div>
    </section>

    <div
      v-else-if="!loading"
      class="bg-white border border-[#E2E8F0] rounded-md p-6 text-sm text-slate-400"
    >
      未找到对应生物资源记录。
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  fetchBioResourceDetail,
  fetchBioResourceNaturalProducts,
  fetchBioResourcePrescriptions
} from '@/app/api/cms/bioResources'
import type { NaturalProductApi, Prescription } from '@/app/api/cms/types'
import { computed, ref, watch, h, reactive } from 'vue'
import CommonTable from './components/CommonTable.vue'
import CusTabMenu from './components/CusTabMenu.vue'
import { RouterLink, useRoute } from 'vue-router'
import { formatDecimal } from '@/app/utils/index'

const route = useRoute()
const activeTab = ref<any>('compounds')
const menuState = reactive<any>({ compounds: 0, prescriptions: 0 })
const onUpdatedCount = (val, key) => {
  menuState[key] = val
}
const tabs = computed(() => [
  { value: 'compounds', label: '相关天然产物', count: menuState.compounds },
  { value: 'prescriptions', label: '相关处方', count: menuState.prescriptions }
])

const infoItem = ref<any>(null)
const relatedCompounds = ref<NaturalProductApi[]>([])
const relatedPrescriptions = ref<Prescription[]>([])
const loading = ref(false)
const error = ref('')

const resourceId = computed(() => String(route.params.id || ''))

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
  if (!resourceId.value) return
  loading.value = true
  error.value = ''
  try {
    const detailPromise = fetchBioResourceDetail(resourceId.value)
    const [detailResult] = await Promise.allSettled([detailPromise])

    if (detailResult.status === 'fulfilled') {
      infoItem.value = detailResult.value as any
    } else {
      throw detailResult.reason
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : '数据加载失败'
    infoItem.value = null
    relatedCompounds.value = []
    relatedPrescriptions.value = []
  } finally {
    loading.value = false
  }
}

watch(
  resourceId,
  () => {
    activeTab.value = 'compounds'
    fetchAll()
  },
  { immediate: true }
)

const formatSource = (item: any) => {
  const rawParts = [item.refType, item.refIdType, item.refId]
    .filter((value) => value != null && value !== '')
    .map((value) => String(value).trim())
    .filter((value) => value !== '' && value.toLowerCase() !== 'database')
  const parts: string[] = []
  for (const value of rawParts) {
    if (parts.length === 0 || parts[parts.length - 1] !== value) {
      parts.push(value)
    }
  }
  return parts.length ? parts.join(' / ') : '—'
}
</script>
