<template>
  <div
    class="bg-white dark:bg-[var(--el-bg-color)]"
    :style="{
      '--theme-white': '#fff',
      '--theme': '#2E5E9E',
      '--theme-soft': '#DDE7F5',
      '--theme-bg': '#EEF3FA'
    }"
  >
    <div class="max-w-[1440px] mx-auto px-6 py-6 flex space-x-4">
      <aside class="w-[300px] flex-shrink-0">
        <div class="bg-white rounded-md border dark:bg-[var(--el-bg-color)] border-[#E2E8F0] p-4">
          <div
            class="flex items-center justify-between pb-3 border-b border-b-solid border-b-[var(--theme-soft)]"
          >
            <h2 class="font-bold text-slate-800 dark:color-white text-lg">筛选</h2>
          </div>

          <el-collapse v-model="activeNames" @change="handleChange">
            <el-collapse-item title="理化属性（Properties）" name="1">
              <template #icon="{ isActive }">
                <Icon
                  class="icon-ele"
                  :icon="`svg-icon:${isActive ? 'menu-up' : 'menu-down'}`"
                  :size="20"
                />
              </template>
              <div class="py-1 space-y-2">
                <div class="space-y-2">
                  <label class="text-sm text-slate-500">分子量（MW）</label>
                  <div class="grid grid-cols-2 gap-2.5 py-1">
                    <el-input
                      v-model="filters.mwMin"
                      type="number"
                      clearable
                      placeholder="最小"
                      class="w-full border rounded"
                    />
                    <el-input
                      v-model="filters.mwMax"
                      type="number"
                      clearable
                      placeholder="最大"
                      class="w-full border rounded"
                    />
                  </div>
                </div>
                <div class="space-y-2">
                  <label class="text-sm text-slate-500">脂水分配系数（XLogP）</label>
                  <div class="grid grid-cols-2 gap-2.5 py-1">
                    <el-input
                      v-model="filters.xlogpMin"
                      type="number"
                      clearable
                      placeholder="最小"
                      class="w-full border rounded"
                    />
                    <el-input
                      v-model="filters.xlogpMax"
                      type="number"
                      clearable
                      placeholder="最大"
                      class="w-full border rounded"
                    />
                  </div>
                </div>
                <div class="space-y-2">
                  <label class="text-sm text-slate-500">极性表面积（PSA）</label>
                  <div class="grid grid-cols-2 gap-2.5 py-1">
                    <el-input
                      v-model="filters.psaMin"
                      type="number"
                      clearable
                      placeholder="最小"
                      class="w-full border rounded"
                    />
                    <el-input
                      v-model="filters.psaMax"
                      type="number"
                      clearable
                      placeholder="最大"
                      class="w-full border rounded"
                    />
                  </div>
                </div>
              </div>
            </el-collapse-item>
            <el-collapse-item title="活性筛选（Activity）" name="2">
              <template #icon="{ isActive }">
                <Icon
                  class="icon-ele"
                  :icon="`svg-icon:${isActive ? 'menu-up' : 'menu-down'}`"
                  :size="20"
                />
              </template>
              <div class="grid grid-cols-2 gap-2.5 py-1">
                <el-select
                  v-model="filters.activityType"
                  class="w-full border rounded"
                  clearable
                  @change="onSearchList"
                >
                  <el-option value="">全部类型</el-option>
                  <el-option value="IC50">IC50</el-option>
                  <el-option value="EC50">EC50</el-option>
                  <el-option value="Ki">Ki</el-option>
                  <el-option value="Kd">Kd</el-option>
                </el-select>
                <el-input
                  v-model="filters.activityMaxNm"
                  type="number"
                  clearable
                  placeholder="活性阈值（nM）"
                  class="w-full border rounded"
                />
              </div>
            </el-collapse-item>
            <el-collapse-item title="靶点筛选（Target）" name="3">
              <template #icon="{ isActive }">
                <Icon
                  class="icon-ele"
                  :icon="`svg-icon:${isActive ? 'menu-up' : 'menu-down'}`"
                  :size="20"
                />
              </template>
              <div class="py-1">
                <el-input
                  v-model="filters.targetType"
                  type="text"
                  clearable
                  placeholder="输入靶点类型..."
                  class="w-full text-sm"
                />
              </div>
            </el-collapse-item>
            <el-collapse-item title="毒性筛选（Toxicity）" name="4">
              <template #icon="{ isActive }">
                <Icon
                  class="icon-ele"
                  :icon="`svg-icon:${isActive ? 'menu-up' : 'menu-down'}`"
                  :size="20"
                />
              </template>
              <div class="py-1">
                <el-select
                  v-model="filters.toxicity"
                  class="w-full text-sm"
                  clearable
                  @change="onSearchList"
                >
                  <el-option label="全部记录" value="all" />
                  <el-option label="仅有毒记录" value="toxic" />
                  <el-option label="仅无毒记录" value="non-toxic" />
                </el-select>
              </div>
            </el-collapse-item>
          </el-collapse>

          <div>
            <el-button
              type="primary"
              class="w-full mt-7 hover:shadow-md hover:-translate-y-0.5 duration-300"
              @click="onSearchList"
            >
              应用筛选
            </el-button>
            <el-button
              type="default"
              class="w-full mt-3 !ml-0 hover:shadow-md hover:-translate-y-0.5 duration-300"
              @click="onResetList"
            >
              重置筛选
            </el-button>
          </div>
        </div>
      </aside>

      <main class="flex-1 min-w-0">
        <div
          class="bg-white rounded-md border dark:bg-[var(--el-bg-color)] border-[#E2E8F0] overflow-hidden"
        >
          <div
            class="py-4 border-b border-[#E2E8F0] flex flex-wrap items-center justify-between gap-4"
          >
            <el-input
              v-model="filters.keyword"
              type="text"
              placeholder="在本列表中搜索..."
              @keyup.enter="onSearchList"
              class="header-search w-full h-10 bg-white dark:bg-[var(--el-bg-color)] border border-[#E2E8F0] rounded-md text-sm text-slate-700 focus:outline-none focus:ring-0"
            >
              <template #append>
                <el-icon color="#fff" class="font-bold" @click="onSearchList">
                  <Search color="#fff" />
                </el-icon>
              </template>
            </el-input>
          </div>

          <el-alert v-if="error" :title="error" type="error" class="mb-4" />
          <div class="overflow-x-auto">
            <el-skeleton v-if="pager.fristLoading && pager.isLoading" :rows="17" animated />
            <el-table
              v-show="!pager.fristLoading"
              ref="tableRef"
              v-table-height="{ diffValue: 15 }"
              v-loading="pager.isLoading"
              :data="pager.dataList"
              size="small"
              :border="false"
              stripe
              highlight-current-row
              scrollbar-always-on
              :sort-orders="['ascending', 'descending']"
              :header-cell-style="{ background: '#f5f7fa', color: '#606266' }"
              class="w-full min-w-[900px]"
            >
              <!-- show-overflow-tooltip -->
              <el-table-column
                prop="id"
                label="编号"
                width="120px"
                align="center"
                header-align="center"
              >
                <template #default="{ row }">
                  <RouterLink
                    :to="`/compounds/${row.id}`"
                    class="text-[var(--el-color-primary)] hover:underline font-medium"
                  >
                    {{ row.id }}
                  </RouterLink>
                </template>
              </el-table-column>
              <!-- <el-table-column
                prop="structureUrl"
                label="结构"
                width="100px"
                align="center"
                header-align="center"
              >
                <template #default="{ row }">
                  <div
                    class="w-10 h-10 border border-gray-100 bg-white dark:bg-[var(--el-bg-color)] rounded p-0.5 flex items-center justify-center overflow-hidden hover:scale-150 transition-transform origin-left z-10"
                  >
                    <Image
                      v-if="row.structureUrl"
                      :src="row.structureUrl"
                      class="max-w-full max-h-full object-contain"
                      :alt="row.name"
                    />
                    <div v-else class="text-[10px] text-slate-300">无结构</div>
                  </div>
                </template>
              </el-table-column> -->
              <el-table-column prop="chineseName" label="名称" align="center" header-align="center">
                <template #default="{ row }">
                  <div class="flex flex-col">
                    <span class="text-sm font-bold text-slate-800">{{ row.name }}</span>
                    <span class="text-xs text-slate-400">{{ row.subtitle || '—' }}</span>
                    <span
                      v-if="row.hasToxicity"
                      class="mt-1 inline-flex w-fit px-2 py-0.5 text-[10px] font-semibold rounded-full bg-red-50 text-red-600"
                    >
                      含毒性记录
                    </span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column
                prop="molecularWeight"
                label="分子量（MW）"
                align="center"
                header-align="center"
              >
                <template #default="{ row }">
                  {{ formatDecimal(row.molecularWeight) }}
                </template>
              </el-table-column>
              <el-table-column
                prop="activityCount"
                label="活性记录"
                align="center"
                header-align="center"
              >
                <template #default="{ row }">
                  {{ formatCount(row.activityCount) }}
                </template>
              </el-table-column>
              <!-- <el-table-column
                prop="chineseName"
                label="理化属性"
                align="center"
                header-align="center"
              >
                <template #default="{ row }">
                  分子式：{{ row.formula || '—' }}<br />
                  分子量（MW）：{{ formatDecimal(row.molecularWeight) }}<br />
                  脂水分配系数（XLogP）：{{ formatDecimal(row.xlogp) }}<br />
                  极性表面积（PSA）：{{ formatDecimal(row.psa) }}
                </template>
              </el-table-column> -->
              <!-- <el-table-column
                prop="chineseName"
                label="统计"
                width="140px"
                align="center"
                header-align="center"
              >
                <template #default="{ row }">
                  活性记录：{{ formatCount(row.activityCount) }}<br />
                  靶点数：{{ formatCount(row.targetCount) }}<br />
                  来源资源：{{ formatCount(row.organismCount) }}
                </template>
              </el-table-column>
              <el-table-column
                prop="chineseName"
                label="最强活性"
                width="140px"
                align="center"
                header-align="center"
              >
                <template #default="{ row }">
                  <span class="text-sm font-bold text-[var(--el-color-primary)]">{{
                    formatActivityValue(row.bestActivityValue)
                  }}</span>
                  <div class="text-xs text-slate-400">标准化值（nM）</div>
                </template>
              </el-table-column> -->
            </el-table>
          </div>
          <div
            class="p-4 border-t border-[#E2E8F0] flex items-center justify-between"
            v-if="pager.totalCount > 0"
          >
            <span class="text-xs text-slate-500">
              第 {{ pager.currentPage }} 页 / {{ Math.ceil(pager.totalCount / pager.pageSize) }} 页
            </span>
            <!-- layout="prev, pager, next, ->, total, jumper" -->
            <Pagination
              :page="pager.currentPage"
              :total="pager.totalCount"
              :limit="pager.pageSize"
              @change-page="currentChange"
              @change-size="sizeChange"
            />
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { fetchNaturalProducts } from '@/app/api/cms/naturalProducts'
import type { NaturalProductApi } from '@/app/api/cms/types'
import { Search } from '@element-plus/icons-vue'
import { onMounted, reactive, ref } from 'vue'

import { useRoute } from 'vue-router'
const route = useRoute()

import {
  buildPubchemImage,
  formatActivityValue,
  formatCount,
  formatDecimal,
  toNumber
} from '@/app/utils'

interface CompoundRow {
  id: string
  name: string
  subtitle?: string
  structureUrl?: string
  formula?: string | null
  molecularWeight?: number | null
  xlogp?: number | null
  psa?: number | null
  activityCount?: number | null
  bestActivityValue?: number | null
  targetCount?: number | null
  organismCount?: number | null
  hasToxicity?: boolean
}

const error = ref('')
const SAFE_LITERAL = /^[A-Za-z0-9_. -]+$/

const filters = reactive({
  keyword: '',
  mwMin: '',
  mwMax: '',
  xlogpMin: '',
  xlogpMax: '',
  psaMin: '',
  psaMax: '',
  activityType: '',
  activityMaxNm: '',
  targetType: '',
  toxicity: 'all'
})

const tableRef = ref()
const pager = reactive<any>({
  currentPage: 1,
  pageSize: 10,
  totalCount: 0,
  fristLoading: true,
  isLoading: true,
  dataList: []
})

const activeNames = ref(['1', '2', '3', '4'])
const handleChange = (val: any) => {
  activeNames.value = val
}

const currentChange = (page: number) => {
  pager.currentPage = page
  onQueryList()
}

const sizeChange = (size: number) => {
  pager.currentPage = 1
  pager.pageSize = size
  onQueryList()
}

const mapRow = (item: NaturalProductApi): CompoundRow => {
  const molecularWeight = toNumber(item.molecularWeight)
  const xlogp = toNumber(item.xlogp)
  const psa = toNumber(item.psa)
  const bestActivityValue = toNumber(item.bestActivityValue)
  const activityCount = (item.numOfActivity ?? item.bioactivityCount ?? null) as number | null
  const targetCount = (item.numOfTarget ?? item.targetCount ?? null) as number | null
  const organismCount = (item.numOfOrganism ?? item.bioResourceCount ?? null) as number | null
  const name = item.prefName || item.iupacName || item.npId || '未命名'

  return {
    id: item.npId || '-',
    name,
    subtitle: item.iupacName || item.npId || '',
    structureUrl: buildPubchemImage(item.pubchemId),
    formula: item.formula ?? null,
    molecularWeight,
    xlogp,
    psa,
    activityCount,
    bestActivityValue,
    targetCount,
    organismCount,
    hasToxicity: item.hasToxicity ?? false
  }
}

const buildParams = () => {
  const mwMin = toNumber(filters.mwMin)
  const mwMax = toNumber(filters.mwMax)
  const xlogpMin = toNumber(filters.xlogpMin)
  const xlogpMax = toNumber(filters.xlogpMax)
  const psaMin = toNumber(filters.psaMin)
  const psaMax = toNumber(filters.psaMax)
  const activityMaxNm = toNumber(filters.activityMaxNm)
  const rawTargetType = filters.targetType?.trim()
  const targetType = rawTargetType && SAFE_LITERAL.test(rawTargetType) ? rawTargetType : undefined

  const toxicityValue =
    filters.toxicity === 'toxic' ? true : filters.toxicity === 'non-toxic' ? false : undefined

  return {
    page: pager.currentPage,
    pageSize: pager.pageSize,
    q: String(filters.keyword ?? '') || undefined,
    mwMin: mwMin ?? '',
    mwMax: mwMax ?? '',
    xlogpMin: xlogpMin ?? '',
    xlogpMax: xlogpMax ?? '',
    psaMin: psaMin ?? '',
    psaMax: psaMax ?? '',
    activityType: filters.activityType?.trim() || undefined,
    activityMaxNm: activityMaxNm ?? '',
    targetType,
    hasToxicity: toxicityValue
  }
}

let requestId = 0
const onQueryList = async () => {
  const currentId = (requestId += 1)
  pager.isLoading = true
  error.value = ''
  try {
    const result = (await fetchNaturalProducts(buildParams())) as any
    if (currentId !== requestId) return
    pager.dataList = result.records.map(mapRow)
    pager.totalCount = result.total ?? 0
  } catch (err) {
    if (currentId !== requestId) return
    error.value = err instanceof Error ? err.message : '数据加载失败'
  } finally {
    pager.fristLoading = false
    if (currentId === requestId) {
      pager.isLoading = false
    }
  }
  tableRef.value?.doLayout()
}

const onResetList = () => {
  pager.currentPage = 1
  filters.mwMin = ''
  filters.mwMax = ''
  filters.xlogpMin = ''
  filters.xlogpMax = ''
  filters.psaMin = ''
  filters.psaMax = ''
  filters.activityType = ''
  filters.activityMaxNm = ''
  filters.targetType = ''
  filters.toxicity = 'all'
  onQueryList()
}

const onSearch = () => {
  pager.currentPage = 1
  onQueryList()
}

const onSearchList = () => {
  pager.currentPage = 1
  onQueryList()
}

onMounted(() => {
  filters.keyword = String(route.query.q ?? '')
  onQueryList()
})
</script>

<style lang="less" scoped>
.header-search {
  :deep(.el-input-group__append),
  :deep(.el-input-group__prepend) {
    background-color: var(--el-color-primary);
    cursor: pointer;
  }
}
:deep(.el-collapse) {
  border-top-width: 0;
  border-bottom-width: 0;
}
:deep(.el-collapse-item__wrap) {
  border-bottom-width: 0;
}
:deep(.el-collapse-item__header) {
  font-size: 16px;
  font-weight: bold;
  border-bottom-width: 0;
  justify-content: space-between;
}
:deep(.el-collapse-item__content) {
  padding-bottom: 0;
}
</style>
