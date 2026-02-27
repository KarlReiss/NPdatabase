<template>
  <div
    class="max-w-[1440px] mx-auto px-6 py-6"
    :style="{ '--theme': '#2E5E9E', '--theme-soft': '#DDE7F5', '--theme-bg': '#EEF3FA' }"
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
        to="/compounds"
        class="color-[#212121] dark:color-white hover:color-[var(--el-color-primary)] select-none no-underline hover:no-underline"
        >天然产物列表</RouterLink
      >
      <span class="dark:color-white">></span>
      <span class="text-slate-700 font-medium select-none">{{ compoundId }}</span>
    </nav>

    <div v-if="loading" class="text-sm text-slate-500 mb-4">加载中...</div>
    <el-skeleton v-if="!infoItem && loading" :rows="15" animated />
    <el-alert v-if="error" :title="error" type="error" class="text-sm text-red-500 mb-4" />
    <template v-if="infoItem">
      <section class="bg-white rounded-lg border border-[#E2E8F0] shadow-sm mb-4">
        <div
          class="flex items-center justify-between gap-3 flex-wrap bg-[var(--el-color-primary)] p-4 rounded-[4px_4px_0_4px]"
        >
          <div class="flex items-center">
            <h1 class="text-2xl font-400 color-white">
              {{ compoundName }}
            </h1>
            <span
              class="px-2.5 py-0.5 text-sm color-white border border-solid border-white rounded-full"
            >
              天然产物
            </span>
          </div>
          <span
            class="w-9 h-9 flex items-center justify-center rounded-full border border-gray-200 hover:border-[var(--el-color-primary)] hover:text-white text-white transition-all"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
              />
            </svg>
          </span>
        </div>
        <div class="flex flex-col md:flex-row">
          <div class="flex-1 p-8">
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-y-2 gap-x-4">
              <div v-for="item in metadata" :key="item.label" class="pl-[160px] relative w-full">
                <div
                  class="text-xs text-slate-400 uppercase tracking-wider absolute top-0.5 left-0"
                  >{{ item.label }}</div
                >
                <div
                  :class="[
                    'text-sm font-medium',
                    item?.highlight ? 'text-[var(--el-color-primary)]' : 'text-slate-700'
                  ]"
                >
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
            class="md:w-[360px] border-b md:border-b-0 md:border-r border-[#E2E8F0] bg-white dark:bg-[var(--el-bg-color)] flex flex-col items-center justify-center"
            style="
              border-inline: 2px solid var(--el-color-primary);
              border-bottom: 2px solid var(--el-color-primary);
            "
          >
            <MoleculeDrawer :smiles="infoItem?.smiles" :width="356" :heiht="356" :showBtn="true" />
            <!-- <MoleculeDrawer :smiles="infoItem.inchi" :width="356" :heiht="356" :showBtn="true" /> -->
          </div> </div
        ><div
          class="md:w-[260px] p-6 border-t md:border-t-0 md:border-l border-[#E2E8F0] bg-white flex flex-col items-center justify-start"
        >
          <div
            class="grid grid-cols-3 gap-2 rounded-lg p-3 w-full mb-4"
            style="background: var(--theme-bg); border: 1px solid var(--theme-soft)"
          >
            <div class="text-center">
              <div class="text-[11px] text-slate-500">活性记录</div>
              <div class="text-lg font-semibold text-slate-800">{{
                formatCount(infoItem.numOfActivity ?? infoItem.bioactivityCount ?? 0)
              }}</div>
            </div>
            <div class="text-center">
              <div class="text-[11px] text-slate-500">靶点数量</div>
              <div class="text-lg font-semibold text-slate-800">{{
                formatCount(infoItem.numOfTarget ?? infoItem.targetCount ?? 0)
              }}</div>
            </div>
            <div class="text-center">
              <div class="text-[11px] text-slate-500">生物资源</div>
              <div class="text-lg font-semibold text-slate-800">{{
                formatCount(infoItem.numOfOrganism ?? infoItem.bioResourceCount ?? 0)
              }}</div>
            </div>
          </div>
          <img
            v-if="structureUrl"
            :src="structureUrl"
            :alt="compoundName"
            class="w-[200px] h-[200px] object-contain mb-3"
          />
          <button
            v-if="structureUrl"
            class="flex items-center space-x-2 px-3 py-2 bg-slate-50 border border-slate-200 rounded-md text-xs text-slate-600 hover:bg-slate-100 transition-colors"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 16v1a2 2 0 002 2h12a2 2 0 002-2v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
              />
            </svg>
            <span>下载结构</span>
          </button>
        </div>
      </section>

      <section
        class="bg-white rounded-md border dark:bg-[var(--el-bg-color)] border-[#E2E8F0] shadow-sm overflow-hidden"
      >
        <CusTabMenu v-model="activeTab" :tabs="tabs" />

        <div class="p-4 min-h-100">
          <div v-show="activeTab === 'targets'" class="space-y-4">
            <div class="bg-[#EFF6FF] border-l-4 border-[#3B82F6] p-4 text-[13px] text-[#1E40AF]">
              <strong>Disease inference note:</strong> Disease association is inferred through
              target links and is provided for research reference only, not clinical evidence.
            </div>
            <CommonTable
              rowKey="id"
              emptyText="暂无关联靶点记录。"
              :listById="compoundId"
              :apiFetch="fetchNaturalProductBioactivityTargets"
              :columns="[
                {
                  prop: 'targetName',
                  label: '靶点',
                  renderer: (row, val, idx) => {
                    return h('div', {}, [
                      h(
                        'div',
                        {
                          class: 'text-sm text-slate-800 font-medium'
                        },
                        row.targetId || row.targetId || '—'
                      ),
                      h(
                        'div',
                        {
                          class: 'text-[11px] text-slate-400'
                        },
                        `编号：${row.targetId || '—'}`
                      ),
                      h(
                        RouterLink,
                        {
                          to: `/targets/${row.targetId}`,
                          class:
                            'text-[var(--el-color-primary)] hover:underline font-medium select-none no-underline hover:no-underline  mt-1'
                        },
                        '查看靶点详情'
                      )
                    ])
                  }
                },
                {
                  prop: 'targetType',
                  label: '类型',
                  renderer: (row, val, idx) => {
                    return row.targetType || '—'
                  }
                },
                {
                  prop: 'targetOrganism',
                  label: '物种',
                  func: (row, val, idx) => {
                    return row.targetOrganism || '-'
                  }
                },
                {
                  prop: 'taxonomyFamily',
                  label: '活性记录数',
                  func: (row, val, idx) => {
                    return formatCount(row.bioactivityCount || 0)
                  }
                },
                {
                  prop: 'bestActivityValue',
                  label: '最佳活性(nM)',
                  func: (row, val, idx) => {
                    return formatDecimal(row.bestActivityValue, 2)
                  }
                }
              ]"
              @update:count="onUpdatedCount($event, 'targets')"
            />
          </div>
          <div v-show="activeTab === 'bioactivity'">
            <div class="mb-4 flex items-center justify-between">
              <h3 class="text-sm font-bold text-slate-800">实验与活性证据</h3>
              <div class="text-xs text-slate-500">展示前 {{ menuState.bio }} 条记录</div>
            </div>
            <CommonTable
              rowKey="id"
              emptyText="暂无关联生物资源"
              :listById="compoundId"
              :checkList="checkBioactivityList"
              :apiFetch="fetchNaturalProductBioactivity"
              :columns="[
                {
                  prop: 'targetRouteId',
                  label: '靶点',
                  renderer: (row, val, idx) => {
                    return h('div', {}, [
                      row?.targetRouteId
                        ? h(
                            RouterLink,
                            {
                              to: `/web/targets/${row.targetRouteId}`,
                              class:
                                'text-[var(--el-color-primary)] hover:underline font-medium select-none no-underline hover:no-underline'
                            },
                            row.targetRouteId
                          )
                        : row?.targetLabel,
                      h('div', { class: 'text-[11px] text-slate-400' }, row.targetIdLabel)
                    ])
                  }
                },
                {
                  prop: 'targetType',
                  label: '靶点类型',
                  func: (row, val, idx) => {
                    return row.targetType
                  }
                },
                {
                  prop: 'type',
                  label: '实验类型',
                  func: (row, val, idx) => {
                    return row.type
                  }
                },
                {
                  prop: 'stdValue',
                  label: '标准化值',
                  func: (row, val, idx) => {
                    return row.stdValue
                  }
                },
                {
                  prop: 'numOfNaturalProducts',
                  label: '参考文献',
                  renderer: (row, val, idx) => {
                    return h('div', { class: 'flex flex-col gap-1' }, [
                      row.refLink
                        ? h(
                            'a',
                            {
                              href: 'row.refLink',
                              target: '_blank',
                              rel: 'noreferrer',
                              class:
                                'text-xs text-[var(--el-color-primary)] hover:underline flex items-center space-x-1'
                            },
                            [
                              h('span', {}, row.refLabel),
                              h(
                                'svg',
                                {
                                  class: 'w-3 h-3',
                                  fill: 'none',
                                  stroke: 'currentColor',
                                  viewBox: '0 0 24 24'
                                },
                                h('path', {
                                  'stroke-linecap': 'round',
                                  'stroke-linejoin': 'round',
                                  'stroke-width': '2',
                                  d: 'M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14'
                                })
                              )
                            ]
                          )
                        : h('span', { class: 'text-xs text-slate-400' }, row.refLabel)
                    ])
                  }
                }
              ]"
              @update:count="onUpdatedCount($event, 'bioactivity')"
            />
          </div>

          <div v-show="activeTab === 'herb'" class="space-y-4">
            <div class="text-sm font-bold text-slate-800">来源生物资源</div>
            <CommonTable
              rowKey="id"
              emptyText="暂无关联天然产物"
              :listById="compoundId"
              :apiFetch="fetchNaturalProductResources"
              :columns="[
                {
                  prop: 'chineseName',
                  label: '名称',
                  renderer: (row, val, idx) => {
                    return h('div', {}, [
                      row?.resourceId
                        ? h(
                            RouterLink,
                            {
                              to: `/web/bio-resources/${row.resourceId}`,
                              class:
                                'text-[var(--el-color-primary)] hover:underline font-medium select-none no-underline hover:no-underline'
                            },
                            row.chineseName || row.latinName || row.resourceId || '—'
                          )
                        : '-'
                    ])
                  }
                },
                {
                  prop: 'resourceType',
                  label: '类型',
                  func: (row, val, idx) => {
                    return row.resourceType
                  }
                },
                {
                  prop: 'taxonomyFamily',
                  label: '分类',
                  func: (row, val, idx) => {
                    return row.taxonomyFamily || row.taxonomyGenus || '—'
                  }
                },
                {
                  prop: 'numOfNaturalProducts',
                  label: '关联天然产物数',
                  func: (row, val, idx) => {
                    return formatCount(row.numOfNaturalProducts)
                  }
                }
              ]"
              @update:count="onUpdatedCount($event, 'herb')"
            />
          </div>

          <div
            v-show="activeTab === 'trial'"
            class="py-20 flex flex-col items-center justify-center text-slate-400"
          >
            <svg
              class="w-12 h-12 mb-4 opacity-20"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
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

    <div
      v-else-if="!loading"
      class="bg-white border border-[#E2E8F0] rounded-md p-6 text-sm text-slate-400"
    >
      未找到对应化合物记录。
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  fetchNaturalProductDetail,
  fetchNaturalProductBioactivity,
  fetchNaturalProductBioactivityTargets,
  fetchNaturalProductResources,
  fetchNaturalProductToxicity
} from '@/app/api/cms/naturalProducts'
import type { NaturalProductApi, TargetApi } from '@/app/api/cms/types'
import { buildPubchemImage, formatCount, formatDecimal, toNumber } from '@/app/utils/index'
import { MoleculeDrawer } from '@/components/MoleculeDrawer'
import CommonTable from './components/CommonTable.vue'
import CusTabMenu from './components/CusTabMenu.vue'
import { computed, ref, watch, h, reactive } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()
const activeTab = ref<any>('targets')
const menuState = reactive<any>({ targets: 0, bioactivity: 0, herb: 0, trial: 0 })
const onUpdatedCount = (val, key) => {
  menuState[key] = val
}
const tabs = computed(() => [
  { value: 'targets', label: '关联靶点', count: infoItem.value?.targetCount ?? menuState.target },
  {
    value: 'bioactivity',
    label: '活性数据',
    count: infoItem.value?.bioactivityCount ?? menuState.bioactivity
  },
  {
    value: 'herb',
    label: '来源药材',
    count: infoItem.value?.bioResourceCount ?? menuState.herb
  },
  { value: 'trial', label: '临床试验', count: 0 }
])

const infoItem = ref<NaturalProductApi | null>(null)
const targets = ref<any>([])
const toxicity = ref<any[]>([])

const loading = ref(false)
const error = ref('')
const currentSmiles = ref('')

const compoundId = computed(() => String(route.params.id || ''))
const compoundName = computed(() => infoItem.value?.prefName || infoItem.value?.npId || '')
const compoundSubtitle = computed(() => infoItem.value?.iupacName || '')
const structureUrl = computed(() => buildPubchemImage(infoItem.value?.pubchemId))

const metadata = computed(() => [
  { label: '分子式（Formula）', value: infoItem.value?.formula || '—' },
  { label: '分子量（MW）', value: formatDecimal(infoItem.value?.molecularWeight) },
  { label: '脂水分配系数（XLogP）', value: formatDecimal(infoItem.value?.xlogp) },
  { label: '极性表面积（PSA）', value: formatDecimal(infoItem.value?.psa) },
  { label: '水溶性（LogS）', value: formatDecimal(infoItem.value?.logS) },
  { label: '分配系数（LogD, pH7.4）', value: formatDecimal(infoItem.value?.logD) },
  { label: '脂水分配系数（LogP）', value: formatDecimal(infoItem.value?.logP) },
  { label: '拓扑极性表面积（tPSA）', value: formatDecimal(infoItem.value?.tpsa) },
  { label: '氢键供体数', value: infoItem.value?.hBondDonors ?? '—' },
  { label: '氢键受体数', value: infoItem.value?.hBondAcceptors ?? '—' },
  { label: '可旋转键数', value: infoItem.value?.rotatableBonds ?? '—' },
  { label: '环数量', value: infoItem.value?.ringCount ?? '—' },
  {
    label: '活性记录数',
    value: formatCount(infoItem.value?.numOfActivity ?? infoItem.value?.bioactivityCount ?? 0)
  },
  {
    label: '靶点数',
    value: formatCount(infoItem.value?.numOfTarget ?? infoItem.value?.targetCount ?? 0)
  },
  {
    label: '来源生物资源数',
    value: formatCount(infoItem.value?.numOfOrganism ?? infoItem.value?.bioResourceCount ?? 0)
  },
  { label: '是否量化', value: infoItem.value?.ifQuantity ? '是' : '否' },
  { label: 'InChI', value: infoItem.value?.inchi || '—' },
  { label: 'SMILES', value: infoItem.value?.smiles || '—' },
  { label: 'PubChem CID', value: infoItem.value?.pubchemId || '—' },
  { label: 'ChEMBL ID', value: infoItem.value?.chemblId || '—' },
  { label: 'InChIKey', value: infoItem.value?.inchikey || '—' },
  { label: '创建时间', value: infoItem.value?.createdAt || '—' },
  { label: '更新时间', value: infoItem.value?.updatedAt || '—' }
]) as any

const targetMap = computed(() => {
  const map = new Map<number, TargetApi>()
  targets.value.forEach((target) => {
    if (typeof target.id === 'number') {
      map.set(target.id, target)
    }
  })
  return map
})

const formatActivityRecord = (value: unknown, unit?: string | null, relation?: string | null) => {
  const numeric = toNumber(value)
  if (numeric === null) return '—'
  const prefix = relation ? `${relation} ` : ''
  const suffix = unit ? ` ${unit}` : ''
  return `${prefix}${formatDecimal(numeric, 2)}${suffix}`.trim()
}

const checkBioactivityList = (list) => {
  return list.map((act) => {
    const target = typeof act.targetId === 'number' ? targetMap.value.get(act.targetId) : undefined
    const targetLabel =
      target?.targetName || target?.targetId || (act.targetId ? `靶点 ${act.targetId}` : '—')
    const targetIdLabel = target?.targetId || '—'
    const type = act.activityType || '—'
    const rawValue = formatActivityRecord(
      act.activityValue,
      act.activityUnits,
      act.activityRelation
    )
    const stdValue = formatActivityRecord(
      act.activityValueStd,
      act.activityUnitsStd,
      act.activityRelation
    )
    const refType = act.refIdType || ''
    const refId = act.refId || '—'
    const refLabel = refType ? `${refType}: ${refId}` : refId
    const refLink =
      refType.toUpperCase() === 'PMID' && act.refId
        ? `https://pubmed.ncbi.nlm.nih.gov/${act.refId}/`
        : ''

    return {
      id: act.id ?? `${act.targetId}-${act.activityType}`,
      targetLabel,
      targetIdLabel,
      type,
      rawValue,
      stdValue,
      refLabel,
      refLink
    }
  })
}

const fetchAll = async () => {
  if (!compoundId.value) return
  loading.value = true
  error.value = ''
  try {
    const detailPromise = fetchNaturalProductDetail(compoundId.value)
    // const toxicityPromise = fetchNaturalProductToxicity(compoundId.value, { page: 1, pageSize: 50 })

    const results = await Promise.allSettled([detailPromise])

    const [detailResult] = results

    if (detailResult.status === 'fulfilled') {
      infoItem.value = detailResult.value as any
      currentSmiles.value = infoItem.value?.smiles as any
    } else {
      throw detailResult.reason
    }

    // toxicity.value = toxicityResult.status === 'fulfilled' ? (toxicityResult.value as any) : []
  } catch (err) {
    error.value = err instanceof Error ? err.message : '数据加载失败'
    infoItem.value = null
    toxicity.value = []
  } finally {
    loading.value = false
  }
}

watch(
  compoundId,
  () => {
    activeTab.value = 'targets'
    fetchAll()
  },
  { immediate: true }
)
</script>
