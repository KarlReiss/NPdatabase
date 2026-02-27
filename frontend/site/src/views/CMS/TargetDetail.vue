<template>
  <div
    class="max-w-[1440px] mx-auto px-6 py-6"
    :style="{ '--theme': '#6B4C9A', '--theme-soft': '#E9E1F3', '--theme-bg': '#F5F0FA' }"
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
        to="/web/targets"
        class="color-[#212121] dark:color-white hover:color-[var(--el-color-primary)] select-none no-underline hover:no-underline"
        >靶点列表</RouterLink
      >
      <span class="dark:color-white">></span>
      <span class="text-slate-700 font-medium select-none">{{ targetId }}</span>
    </nav>

    <div v-if="loading" class="text-sm text-slate-500 mb-4">加载中...</div>
    <el-skeleton v-if="!infoItem && loading" :rows="15" animated />
    <el-alert v-if="error" :title="error" type="error" class="text-sm text-red-500 mb-4" />

    <template v-if="infoItem">
      <section class="bg-white rounded-lg border border-[#E2E8F0] shadow-sm mb-4">
        <div class="flex items-center gap-3 flex-wrap bg-[var(--el-color-primary)] p-4 rounded-1">
          <h1 class="text-2xl font-400 color-white">{{
            infoItem.targetName || infoItem.targetId
          }}</h1>
          <span
            class="px-2.5 py-0.5 color-white text-sm border border-solid border-white rounded-full"
          >
            靶点
          </span>
        </div>
        <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4 text-base text-slate-600">
          <div class="p-5 rounded-2 border border-solid border-[var(--theme-soft)] max-h-[104px]">
            <div
              class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[78px] relative w-full"
            >
              <span class="color-[#212121] font-500 absolute top-0 left-0">编号</span>
              {{ infoItem.targetId || '—' }}
            </div>
            <div
              class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[78px] relative w-full"
            >
              <span class="color-[#212121] font-500 absolute top-0 left-0">UniProt</span>
              <span v-if="uniprotIds.length === 0">—</span>
              <template v-else>
                <block v-for="(id, idx) in uniprotIds" :key="idx">
                  <a
                    :href="`https://www.uniprot.org/uniprotkb/${id}/entry`"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="text-[#3B82F6] hover:underline"
                    >{{ id }}</a
                  >
                  <span v-if="idx < uniprotIds.length - 1">,</span>
                </block>
              </template>
            </div>
          </div>
          <div class="p-5 rounded-2 border border-solid border-[var(--theme-soft)] max-h-[104px]">
            <div
              class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[78px] relative w-full"
            >
              <span class="color-[#212121] font-500 absolute top-0 left-0">分类</span>
              {{ infoItem.targetType || '—' }}
            </div>
            <div
              class="text-base leading-7 min-h-7 color-slate-400 font-400 pl-[78px] relative w-full"
            >
              <span class="color-[#212121] font-500 absolute top-0 left-0">物种</span>
              {{ infoItem.targetOrganism || '—' }}
            </div>
          </div>
          <div
            class="grid grid-cols-3 md:grid-cols-3 gap-1 rounded-lg py-5 pl-3 pr-3 overflow-hidden bg-[#FCF1E1] relative"
          >
            <div class="absolute top-0 bottom-0 left-0 w-1.5 bg-[#E59317]"></div>
            <div class="text-center">
              <div class="text-base color-[#212121]">关联天然产物</div>
              <div class="text-xl font-500 color-[#E59317]">
                {{ formatCount(infoItem.naturalProductCount) }}
              </div>
            </div>
            <div class="text-center">
              <div class="text-base color-[#212121]">活性记录</div>
              <div class="text-xl font-500 color-[#E59317]">
                {{ formatCount(infoItem.bioactivityCount) }}
              </div>
            </div>
            <div class="text-center">
              <div class="text-base color-[#212121]">最佳活性</div>
              <div class="text-xl font-500 color-[#E59317]">
                {{ formatActivityValue(infoItem.bestActivityValue) }}
              </div>
            </div>
          </div>
        </div>

        <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4 text-base text-slate-600">
          <div
            class="rounded-lg px-2 pt-2 bg-[#E1F3F8] border border-solid border-[var(--theme-soft)]"
          >
            <span
              class="px-2.5 py-1 color-white bg-[var(--el-color-primary)] text-sm rounded-1 select-none"
              >基础信息</span
            >
            <div class="p-4 text-sm leading-7 color-slate-600 font-400 w-full min-h-[190px]">
              <div
                class="text-sm text-slate-600 leading-7 h-7 color-slate-500 font-400 pl-[100px] relative w-full"
                ><span class="color-[#212121] font-500 absolute top-0 left-0">基因名</span
                >{{ infoItem.geneName || '—' }}</div
              >
              <div
                class="text-sm text-slate-600 leading-7 h-7 color-slate-500 font-400 pl-[100px] relative w-full"
                ><span class="color-[#212121] font-500 absolute top-0 left-0">TTD ID</span>
                <span v-if="ttdIds.length === 0">—</span>
                <template v-else>
                  <block v-for="(id, idx) in ttdIds" :key="idx">
                    <a
                      :href="`https://db.idrblab.net/ttd/data/target/details/${id}`"
                      target="_blank"
                      rel="noopener noreferrer"
                      class="text-[#3B82F6] hover:underline"
                      >{{ id }}</a
                    >
                    <span v-if="idx < ttdIds.length - 1">,</span>
                  </block>
                </template>
              </div>
              <div
                class="text-sm text-slate-600 leading-7 h-7 color-slate-500 font-400 pl-[100px] relative w-full"
                ><span class="color-[#212121] font-500 absolute top-0 left-0">EC 编号</span
                >{{ infoItem.ecNumber || '—' }}</div
              >
              <div
                class="text-sm text-slate-600 leading-7 h-7 color-slate-500 font-400 pl-[100px] relative w-full"
                ><span class="color-[#212121] font-500 absolute top-0 left-0">PDB 结构</span>
                <span v-if="pdbIds.length === 0">—</span>
                <template v-else>
                  <block v-for="(id, idx) in pdbIds" :key="idx">
                    <a
                      :href="`https://www.rcsb.org/structure/${id}`"
                      target="_blank"
                      rel="noopener noreferrer"
                      class="text-[#3B82F6] hover:underline"
                      >{{ id }}</a
                    >
                    <span v-if="idx < pdbIds.length - 1">,</span>
                  </block>
                </template>
              </div>
              <div
                class="text-sm text-slate-600 leading-7 h-7 color-slate-500 font-400 pl-[100px] relative w-full"
                ><span class="color-[#212121] font-500 absolute top-0 left-0">生物分类</span
                >{{ infoItem.bioclass || '—' }}</div
              >
              <div
                class="text-sm text-slate-600 leading-7 h-7 color-slate-500 font-400 pl-[100px] relative w-full"
                ><span class="color-[#212121] font-500 absolute top-0 left-0">物种 Tax ID</span
                >{{ infoItem.targetOrganismTaxId || '—' }}</div
              >
            </div>
          </div>
          <div
            class="rounded-lg px-2 pt-2 bg-[#E1F3F8] border border-solid border-[var(--theme-soft)]"
          >
            <span
              class="px-2.5 py-1 color-white bg-[var(--el-color-primary)] text-sm rounded-1 select-none"
              >功能与同义词</span
            >
            <div class="p-4 text-sm leading-7 color-slate-600 font-400 w-full min-h-[190px]">
              <div
                class="text-sm text-slate-600 leading-7 h-7 color-slate-500 font-400 pl-[100px] relative w-full"
                ><span class="color-[#212121] font-500 absolute top-0 left-0">功能</span
                >{{ infoItem.function || '—' }}</div
              >
              <div
                class="text-sm text-slate-600 leading-7 h-7 color-slate-500 font-400 pl-[100px] relative w-full"
                ><span class="color-[#212121] font-500 absolute top-0 left-0">同义词</span
                >{{ infoItem.synonyms || '—' }}</div
              >
            </div>
          </div>

          <div
            class="rounded-lg px-2 pt-2 bg-[#E1F3F8] border border-solid border-[var(--theme-soft)]"
          >
            <span
              class="px-2.5 py-1 color-white bg-[var(--el-color-primary)] text-sm rounded-1 select-none"
              >序列</span
            >
            <div class="p-4 text-sm leading-7 color-slate-600 font-400 w-full min-h-[90px]">
              {{ infoItem.sequence || '—' }}
            </div>
          </div>
        </div>
      </section>

      <section
        class="bg-white rounded-md border dark:bg-[var(--el-bg-color)] border-[#E2E8F0] shadow-sm overflow-hidden"
      >
        <CusTabMenu v-model="activeTab" :tabs="tabs" />

        <div class="p-4 min-h-100">
          <div v-show="activeTab === 'compounds'">
            <CommonTable
              rowKey="id"
              emptyText="暂无关联天然产物"
              :listById="targetId"
              :apiFetch="fetchTargetNaturalProducts"
              :columns="[
                {
                  prop: 'id',
                  label: '编号',
                  renderer: (row, val, idx) => {
                    return h(
                      RouterLink,
                      {
                        to: `/compounds/${row.id}`,
                        class:
                          'text-[var(--el-color-primary)] hover:underline font-medium select-none no-underline hover:no-underline'
                      },
                      row.id
                    )
                  }
                },
                {
                  prop: 'name',
                  label: '名称',
                  func: (row, val, idx) => {
                    return row.name
                  }
                },
                {
                  prop: 'molecularWeight',
                  label: '分子量（MW）',
                  func: (row, val, idx) => {
                    return formatDecimal(toNumber(row.molecularWeight))
                  }
                },
                {
                  prop: 'bestActivityValue',
                  label: '最强活性',
                  func: (row, val, idx) => {
                    return formatActivityValue(toNumber(row.bestActivityValue))
                  }
                }
              ]"
              @update:count="onUpdatedCount($event, 'compounds')"
            />
          </div>

          <div v-show="activeTab === 'bio'" class="py-10 text-sm text-slate-400 text-center">
            当前接口暂未提供靶点级活性明细，后续补充。
          </div>
        </div>
      </section>
    </template>

    <div
      v-else-if="!loading"
      class="bg-white border border-[#E2E8F0] rounded-md p-6 text-sm text-slate-400"
    >
      未找到对应靶点记录。
    </div>
  </div>
</template>

<script setup lang="ts">
import { formatActivityValue, formatCount, formatDecimal, toNumber } from '@/app/utils/index'
import { fetchTargetDetail, fetchTargetNaturalProducts } from '@/app/api/cms/targets'
import type { TargetDetailApi } from '@/app/api/cms/types'
import { computed, ref, watch, h, reactive } from 'vue'
import CommonTable from './components/CommonTable.vue'
import CusTabMenu from './components/CusTabMenu.vue'
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()
const activeTab = ref<any>('compounds')
const menuState = reactive<any>({ compounds: 0, bio: 0 })
const onUpdatedCount = (val, key) => {
  menuState[key] = val
}
const tabs = computed(() => [
  { value: 'compounds', label: '相关天然产物', count: menuState.compounds },
  { value: 'bio', label: '活性记录', count: infoItem.value?.bioactivityCount ?? 0 }
])

const infoItem = ref<TargetDetailApi | null>(null)
const loading = ref(false)
const error = ref('')

const targetId = computed(() => String(route.params.id || ''))

const fetchAll = async () => {
  if (!targetId.value) return
  loading.value = true
  error.value = ''
  try {
    const detailPromise = fetchTargetDetail(targetId.value)
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
const uniprotIds = computed(() => {
  if (!infoItem.value?.uniprotId) return []
  return infoItem.value.uniprotId.split(/[,;]\s*/).filter((id) => id.trim())
})

const ttdIds = computed(() => {
  if (!infoItem.value?.ttdId) return []
  return infoItem.value.ttdId.split(/[,;]\s*/).filter((id) => id.trim())
})

const pdbIds = computed(() => {
  if (!infoItem.value?.pdbStructure) return []
  return infoItem.value.pdbStructure.split(/[,;]\s*/).filter((id) => id.trim())
})

watch(
  targetId,
  () => {
    activeTab.value = 'compounds'
    fetchAll()
  },
  { immediate: true }
)
</script>
