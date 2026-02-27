<template>
  <div
    class="bg-white dark:bg-[var(--el-bg-color)]"
    :style="{
      '--theme-white': '#fff',
      '--theme': '#6B4C9A',
      '--theme-soft': '#E9E1F3',
      '--theme-bg': '#F5F0FA'
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
            <el-collapse-item title="类型" name="1">
              <template #icon="{ isActive }">
                <Icon
                  class="icon-ele"
                  :icon="`svg-icon:${isActive ? 'menu-up' : 'menu-down'}`"
                  :size="20"
                />
              </template>
              <el-select
                v-model="filters.targetType"
                class="w-full text-sm"
                placeholder="请输入/选择类型"
                clearable
                filterable
                @change="onSearch"
              >
                <el-option
                  v-for="(item, idx) in typeList"
                  :key="idx"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-collapse-item>
            <el-collapse-item title="物种" name="2">
              <template #icon="{ isActive }">
                <Icon
                  class="icon-ele"
                  :icon="`svg-icon:${isActive ? 'menu-up' : 'menu-down'}`"
                  :size="20"
                />
              </template>
              <el-select
                v-model="filters.bioclass"
                class="w-full text-sm"
                placeholder="请输入/选择物种"
                clearable
                filterable
                @change="onSearch"
              >
                <el-option
                  v-for="(item, idx) in bioclassList"
                  :key="idx"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
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
              clearable
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
              :default-sort="{ prop: 'targetId', order: 'descending' }"
              @sort-change="onSortChange"
            >
              <!-- show-overflow-tooltip -->
              <el-table-column
                prop="targetId"
                label="编号"
                sortable
                align="center"
                header-align="center"
              >
                <template #default="{ row }">
                  <RouterLink
                    :to="`/web/targets/${row.targetId}`"
                    class="text-[var(--el-color-primary)] hover:underline font-medium"
                  >
                    {{ row.targetId }}
                  </RouterLink>
                </template>
              </el-table-column>
              <el-table-column
                prop="targetName"
                label="靶点名称"
                align="center"
                header-align="center"
              >
                <template #default="{ row }">
                  {{ row.targetName || '—' }}
                </template>
              </el-table-column>
              <!-- <el-table-column prop="geneName" label="基因名" align="center" header-align="center">
                <template #default="{ row }">
                  {{ row.geneName || '—' }}
                </template>
              </el-table-column> -->
              <el-table-column prop="UniProt" label="UniProt" align="center" header-align="center">
                <template #default="{ row }">
                  {{ formatUniprot(row.uniprotId) }}
                </template>
              </el-table-column>
              <el-table-column prop="targetType" label="类型" align="center" header-align="center">
                <template #default="{ row }">
                  {{ row.targetType || '—' }}
                </template>
              </el-table-column>
              <!-- <el-table-column prop="bioclass" label="物种" align="center" header-align="center">
                <template #default="{ row }">
                  {{ row.bioclass || '—' }}
                </template>
              </el-table-column> -->
              <el-table-column
                prop="numOfNaturalProducts"
                label="关联天然产物数"
                sortable
                align="center"
                header-align="center"
              >
                <template #default="{ row }">
                  {{ formatCount(row.numOfNaturalProducts) }}
                </template>
              </el-table-column>
              <el-table-column
                prop="numOfHerbs"
                label="活性记录数"
                sortable
                align="center"
                header-align="center"
              >
                <template #default="{ row }">
                  {{ formatCount(row.numOfActivities) }}
                </template>
              </el-table-column>
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
import {
  fetchTargets,
  fetchTargetsTargetTypes,
  fetchTargetsBioclasses
} from '@/app/api/cms/targets'
import type { TargetApi } from '@/app/api/cms/types'
import { Search } from '@element-plus/icons-vue'
import { onMounted, reactive, ref } from 'vue'
import { formatCount } from '@/app/utils'
import { useRoute } from 'vue-router'

interface TargetRow {
  targetId: string
  targetName?: string
  geneName?: string
  targetType?: string
  bioclass?: string
  uniprotId?: string
  numOfNaturalProducts?: number | null
  numOfActivities?: number | null
}

const formatUniprot = (value?: string) => {
  if (!value) return '—'
  const cleaned = value.replace(/\s+/g, '')
  if (!cleaned || cleaned === 'n.a.' || cleaned === 'n.a' || cleaned === 'na' || cleaned === '-') {
    return '—'
  }
  const parts = cleaned.split(/[|;]+/).filter(Boolean)
  if (parts.length <= 1) {
    return parts[0] || '—'
  }
  return `${parts[0]} (+${parts.length - 1})`
}

const route = useRoute()
const error = ref('')

const sortKey = ref<'targetId' | 'targetName' | 'numOfNaturalProducts' | 'numOfActivities' | any>(
  'numOfActivities'
)
const sortDir = ref<'asc' | 'desc'>('desc')

const mapRow = (item: TargetApi): TargetRow => ({
  targetId: item.targetId || '-',
  targetName: item.targetName || '',
  geneName: item.geneName || '',
  targetType: item.targetType || '',
  bioclass: item.bioclass || '',
  uniprotId: item.uniprotId || '',
  numOfNaturalProducts: item.numOfNaturalProducts ?? item.numOfCompounds ?? null,
  numOfActivities: item.numOfActivities ?? null
})

const typeList = ref<any>([])
const bioclassList = ref<any>([])
const fetchAll = async () => {
  try {
    const targetTypesPromise = fetchTargetsTargetTypes()
    const bioclassesPromise = fetchTargetsBioclasses()
    const [targetTypesResult, bioclassesResult] = await Promise.allSettled([
      targetTypesPromise,
      bioclassesPromise
    ])

    if (targetTypesResult.status === 'fulfilled') {
      typeList.value = (targetTypesResult.value as any).map((txt: any) => {
        return { value: txt, label: txt }
      })
    }

    if (bioclassesResult.status === 'fulfilled') {
      bioclassList.value = (bioclassesResult.value as any).map((txt: any) => {
        return { value: txt, label: txt }
      })
    }
  } catch (err) {
    console.error(err)
    typeList.value = []
    bioclassList.value = []
  }
}
const tableRef = ref()
const pager = reactive<any>({
  currentPage: 1,
  pageSize: 10,
  totalCount: 0,
  fristLoading: true,
  isLoading: true,
  dataList: []
})

const filters = reactive({
  keyword: '',
  targetType: '',
  bioclass: ''
})

const activeNames = ref(['1', '2'])
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

const buildParams = () => {
  return {
    page: pager.currentPage,
    pageSize: pager.pageSize,
    q: String(filters.keyword ?? '') || undefined,
    targetType: String(filters.targetType ?? '') || undefined,
    bioclass: String(filters.bioclass ?? '') || undefined
  }
}

let requestId = 0
const onQueryList = async () => {
  const currentId = (requestId += 1)
  pager.isLoading = true
  error.value = ''
  try {
    const result = (await fetchTargets(buildParams())) as any
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

const onSortChange = (row: any) => {
  let sort = 0
  let orderBy
  switch (row.prop) {
    case 'targetId':
      sort = 1
      if (!row.order) orderBy = ''
      if (row.order == 'ascending') orderBy = 'asc'
      if (row.order == 'descending') orderBy = 'desc'
      break
    case 'numOfNaturalProducts':
      sort = 2
      if (!row.order) orderBy = ''
      if (row.order == 'ascending') orderBy = 'asc'
      if (row.order == 'descending') orderBy = 'desc'
      break
    case 'numOfHerbs':
      sort = 3
      if (!row.order) orderBy = ''
      if (row.order == 'ascending') orderBy = 'asc'
      if (row.order == 'descending') orderBy = 'desc'
      break
  }
  pager.currentPage = 1
  sortKey.value = `${sort}`
  sortDir.value = orderBy
  onQueryList()
}

const onResetList = () => {
  pager.currentPage = 1
  filters.keyword = ''
  filters.targetType = ''
  filters.bioclass = ''
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
  fetchAll()
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
