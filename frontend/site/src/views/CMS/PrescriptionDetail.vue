<template>
  <div
    class="max-w-[1440px] mx-auto px-6 py-6"
    :style="{ '--theme': '#7A5A2E', '--theme-soft': '#EFE6D8', '--theme-bg': '#F7F1E6' }"
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
        to="/web/prescriptions"
        class="color-[#212121] dark:color-white hover:color-[var(--el-color-primary)] select-none no-underline hover:no-underline"
        >处方列表</RouterLink
      >
      <span class="dark:color-white">></span>
      <span class="text-slate-700 font-medium select-none">
        {{ infoItem?.prescriptionId || '—' }}
      </span>
    </nav>

    <div v-if="loading" class="text-sm text-slate-500 mb-4">加载中...</div>
    <el-skeleton v-if="!infoItem && loading" :rows="15" animated />
    <el-alert v-if="error" :title="error" type="error" class="text-sm text-red-500 mb-4" />

    <section v-if="infoItem" class="bg-white rounded-lg border border-[#E2E8F0] shadow-sm mb-4">
      <div class="flex items-center gap-3 flex-wrap bg-[var(--el-color-primary)] p-4 rounded-1">
        <h1 class="text-2xl font-400 color-white">{{ infoItem.chineseName }}</h1>
        <span
          class="px-2.5 py-0.5 color-white text-sm border border-solid border-white rounded-full"
        >
          处方
        </span>
      </div>
      <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4 text-base text-slate-600">
        <div class="p-5 rounded-2 border border-solid border-[var(--theme-soft)] max-h-[104px]">
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[78px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">编号</span>
            {{ infoItem.prescriptionId || '—' }}
          </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[78px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">拼音</span>
            {{ infoItem.pinyinName || '—' }}
          </div>
        </div>
        <!-- <div class="p-5 rounded-2 border border-solid border-[var(--theme-soft)] max-h-[104px]">
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[78px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0"
              >分类</span
            >
            {{ infoItem.category || '—' }} / {{ infoItem.subcategory || '—' }}
          </div>
        </div> -->
        <!-- <div
          class="grid grid-cols-1 md:grid-cols-2 gap-4 p-5 overflow-hidden bg-[#FCF1E1] relative"
        >
          <div class="absolute top-0 bottom-0 left-0 w-1.5 bg-[#E59317]"></div>
          <div class="text-center">
            <div class="text-xl color-[#212121]">药材数</div>
            <div class="text-xl font-500 color-[#E59317]">
              {{ infoItem.numOfHerbs || '—' }}
            </div>
          </div>
          <div class="text—center">
            <div class="text-xl color-[#212121]">天然产物</div>
            <div class="text-xl font-500 color-[#E59317]">
              {{ infoItem.numOfNaturalProducts || '—' }}
            </div>
          </div>
        </div> -->
      </div>

      <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4 text-slate-600">
        <div class="pt-2 px-2 bg-[#E1F3F8] rounded-2 min-h-[100px]">
          <span
            class="px-2.5 py-1 color-white bg-[var(--el-color-primary)] text-sm rounded-1 select-none"
          >
            功效
          </span>
          <div class="p-4 text-sm leading-7 min-h-7 color-slate-600 font-400 w-full">
            {{ infoItem.functions || '—' }}
          </div>
        </div>
        <div class="pt-2 px-2 bg-[#E1F3F8] rounded-2 min-h-[100px]">
          <span
            class="px-2.5 py-1 color-white bg-[var(--el-color-primary)] text-sm rounded-1 select-none"
          >
            主治
          </span>
          <div class="p-4 text-sm leading-7 min-h-7 color-slate-600 font-400 w-full">
            {{ infoItem.indications || '—' }}
          </div>
        </div>
      </div>

      <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4 text-base text-slate-600">
        <div class="p-5 rounded-2 border border-solid border-[var(--theme-soft)] min-h-[168px]">
          <div class="color-[#212121] rounded-1 text-2xl leading-9 font-500 mb-2"> 来源消息 </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">来源书籍</span>
            {{ infoItem.sourceBook || '—' }}
          </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">朝代/作者</span>
            {{ infoItem.sourceDynasty || '—' }}
          </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">别名</span>
            {{ infoItem.alias || '—' }}
          </div>
        </div>
        <div class="p-5 rounded-2 border border-solid border-[var(--theme-soft)] min-h-[168px]">
          <div class="color-[#212121] rounded-1 text-2xl leading-9 font-500 mb-2"> 用法与剂型 </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">剂型</span>
            {{ infoItem.dosageForm || '—' }}
          </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">用法</span>
            {{ infoItem.usageMethod || '—' }}
          </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">用量</span>
            {{ infoItem.dosage || '—' }}
          </div>
        </div>
      </div>

      <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4 text-base text-slate-600">
        <div class="p-5 rounded-2 border border-solid border-[var(--theme-soft)] min-h-[168px]">
          <div class="color-[#212121] rounded-1 text-2xl leading-9 font-500 mb-2"> 组成与制备 </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">组成</span>
            {{ infoItem.compositionText || '—' }}
          </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">制备方法</span>
            {{ infoItem.preparationMethod || '—' }}
          </div>
        </div>
        <div class="p-5 rounded-2 border border-solid border-[var(--theme-soft)] min-h-[168px]">
          <div class="color-[#212121] rounded-1 text-2xl leading-9 font-500 mb-2"> 注意事项 </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">禁忌</span>
            {{ infoItem.contraindications || '—' }}
          </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">注意事项</span>
            {{ infoItem.precautions || '—' }}
          </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">不良反应</span>
            {{ infoItem.adverseReactions || '—' }}
          </div>
        </div>
      </div>

      <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4 text-base text-slate-600">
        <div class="p-5 rounded-2 border border-solid border-[var(--theme-soft)] min-h-[198px]">
          <div class="color-[#212121] rounded-1 text-2xl leading-9 font-500 mb-2"> 现代消息 </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">现代主治</span>
            {{ infoItem.indicationsModern || '—' }}
          </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">证型</span>
            {{ infoItem.syndrome || '—' }}
          </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">药理</span>
            {{ infoItem.pharmacology || '—' }}
          </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">临床应用</span>
            {{ infoItem.clinicalApplication || '—' }}
          </div>
        </div>
        <div class="p-5 rounded-2 border border-solid border-[var(--theme-soft)] min-h-[198px]">
          <div class="color-[#212121] rounded-1 text-2xl leading-9 font-500 mb-2"> 疾病与组织 </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">相关疾病</span>
            {{ infoItem.relatedDiseases || '—' }}
          </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">ICD-11分类</span>
            {{ infoItem.diseaseIcd11Category || '—' }}
          </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">人体组织</span>
            {{ infoItem.humanTissues || '—' }}
          </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[90px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">靶向组织</span>
            {{ infoItem.targetTissues || '—' }}
          </div>
        </div>
      </div>

      <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4 text-base text-slate-600">
        <div class="p-5 rounded-2 border border-solid border-[var(--theme-soft)] min-h-[108px]">
          <div class="color-[#212121] rounded-1 text-2xl leading-9 font-500 mb-2"> 外部标识 </div>
          <!-- <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[194px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0"
              >TCMID/TCMSP/SymMap</span
            >
            {{ infoItem.tcmidId || '—' }} / {{ infoItem.tcmspId || '—' }} /
            {{ infoItem.symmapId || '—' }}
          </div> -->
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[100px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">TCMID</span>
            {{ infoItem.tcmidId || '—' }}
          </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[100px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">ICD-11 分类</span>
            {{ infoItem.diseaseIcd11Category || '—' }}
          </div>
          <!-- <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[100px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0"
              >TCMSP</span
            >
            {{ infoItem.tcmspId || '—' }}
          </div> -->
          <!-- <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[100px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0"
              >SymMap</span
            >
            {{ infoItem.symmapId || '—' }}
          </div> -->
        </div>
        <div class="p-5 rounded-2 border border-solid border-[var(--theme-soft)] min-h-[108px]">
          <div class="color-[#212121] rounded-1 text-2xl leading-9 font-500 mb-2"> 参考信息 </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[100px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0">参考文献</span>
            {{ infoItem.reference || '—' }}
          </div>
          <!-- <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[100px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0"
              >参考书籍</span
            >
            {{ infoItem.pharmacopoeiaRef || '—' }}
          </div>
          <div
            class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[100px] relative w-full"
          >
            <span class="color-[#212121] font-500 absolute top-0 left-0"
              >药典/文献</span
            >
            {{ infoItem.pharmacopoeiaRef || '—' }} /
            {{ infoItem.literatureRef || '—' }}
          </div> -->
        </div>
      </div>
    </section>

    <div
      v-else-if="!loading"
      class="bg-white border border-[#E2E8F0] rounded-md p-6 text-sm text-slate-400"
    >
      未找到对应处方记录。
    </div>

    <section
      v-if="infoItem"
      class="bg-white rounded-md border dark:bg-[var(--el-bg-color)] border-[#E2E8F0] shadow-sm overflow-hidden"
    >
      <!-- <CusTabMenu v-model="activeTab" :tabs="tabs" /> -->
      <div class="p-4 min-h-100">
        <div v-show="activeTab === 'resources'">
          <CommonTable
            rowKey="id"
            emptyText="暂无组成药材"
            :listById="prescriptionId"
            :apiFetch="fetchPrescriptionBioResources"
            :columns="[
              {
                prop: 'resourceId',
                label: '药材编号',
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
                prop: 'standardChineseName',
                label: '药材（生物资源）',
                func: (row, val, idx) => {
                  return h(
                    RouterLink,
                    {
                      to: `/resources/${row.resourceId}`,
                      class:
                        'text-[var(--el-color-primary)] hover:underline font-medium select-none no-underline hover:no-underline'
                    },
                    row.standardChineseName ||
                      row.officialChineseName ||
                      row.chineseName ||
                      row.latinName ||
                      row.resourceId
                  )
                }
              },
              {
                prop: 'resourceType',
                label: '资源类型',
                func: (row, val, idx) => {
                  return toTypeLabel(row.resourceType)
                }
              },
              {
                prop: '',
                label: '分类（科/属）',
                func: (row, val, idx) => {
                  return `${row.taxonomyFamily || '—'} / ${row.taxonomyGenus || '—'}`
                }
              },
              {
                prop: 'numOfNaturalProducts',
                label: '天然产物数',
                func: (row, val, idx) => {
                  return row.numOfNaturalProducts ?? 0
                }
              }
            ]"
            @update:count="onUpdatedCount($event, 'resources')"
          />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import CommonTable from './components/CommonTable.vue'
import CusTabMenu from './components/CusTabMenu.vue'
import { computed, ref, watch, h, reactive } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { fetchPrescriptionDetail, fetchPrescriptionBioResources } from '@/app/api/cms/prescriptions'

const route = useRoute()
const activeTab = ref<any>('resources')
const menuState = reactive<any>({ resources: 0, compounds: 0 })
const onUpdatedCount = (val, key) => {
  menuState[key] = val
}
const tabs = computed(() => [
  { value: 'resources', label: '组成药材', count: menuState.resources }
  // { value: 'compounds', label: '关联天然产物', count: menuState.compounds }
])

const infoItem = ref<any>(null)
const relatedResources = ref<any>([])
const relatedCompounds = ref<any>([])
const loading = ref(false)
const error = ref('')

const prescriptionId = computed(() => String(route.params.id || ''))

const fetchAll = async () => {
  if (!prescriptionId.value) return
  loading.value = true
  error.value = ''
  try {
    const detailPromise = fetchPrescriptionDetail(prescriptionId.value)
    const [detailResult] = await Promise.allSettled([detailPromise])

    if (detailResult.status === 'fulfilled') {
      infoItem.value = detailResult.value
    } else {
      throw detailResult.reason
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : '数据加载失败'
    infoItem.value = null
    relatedResources.value = []
    relatedCompounds.value = []
  } finally {
    loading.value = false
  }
}

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

watch(
  prescriptionId,
  () => {
    activeTab.value = 'resources'
    fetchAll()
  },
  { immediate: true }
)
</script>
