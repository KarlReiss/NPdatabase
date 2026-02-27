<template>
  <div
    class="bg-white dark:bg-[var(--el-bg-color)]"
    :style="{
      '--theme-white': '#fff',
      '--theme': '#7A5A2E',
      '--theme-soft': '#EFE6D8',
      '--theme-bg': '#F7F1E6'
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
            <!-- <el-collapse-item title="分类" name="1">
              <template #icon="{ isActive }">
                <Icon class="icon-ele" :icon="`svg-icon:${isActive ? 'menu-up' : 'menu-down'}`" :size="20" />
              </template>
              <el-select v-model="filters.category" class="w-full text-sm">
                <el-option label="全部分类" value="" />
                <el-option v-for="(item, idx) in cateList" :key="idx" :label="item.label" :value="item.value" />
              </el-select>
            </el-collapse-item> -->
            <el-collapse-item title="功效/主治" name="2">
              <template #icon="{ isActive }">
                <Icon
                  class="icon-ele"
                  :icon="`svg-icon:${isActive ? 'menu-up' : 'menu-down'}`"
                  :size="20"
                />
              </template>
              <el-input
                v-model="filters.functions"
                placeholder="请输入功效/主治"
                class="w-full text-sm"
                clearable
              />
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
              :default-sort="{ prop: 'prescriptionId', order: 'descending' }"
              @sort-change="onSortChange"
            >
              <!-- show-overflow-tooltip -->
              <el-table-column
                prop="prescriptionId"
                label="处方编号"
                sortable
                align="center"
                header-align="center"
              >
                <template #default="{ row }">
                  <RouterLink
                    :to="`/web/prescriptions/${row.prescriptionId}`"
                    class="text-[var(--el-color-primary)] hover:underline font-medium"
                  >
                    {{ row.prescriptionId }}
                  </RouterLink>
                </template>
              </el-table-column>
              <el-table-column
                prop="chineseName"
                label="处方名称"
                align="center"
                header-align="center"
              >
                <template #default="{ row }">
                  {{ row.chineseName || '—' }}
                </template>
              </el-table-column>
              <!-- <el-table-column prop="pinyinName" label="拼音" align="center" header-align="center">
                <template #default="{ row }">
                  {{ row.pinyinName || '—' }}
                </template>
              </el-table-column>
              <el-table-column prop="category" label="分类" align="center" header-align="center">
                <template #default="{ row }">
                  {{ row.category || '—' }} / {{ row.subcategory || '—' }}
                </template>
              </el-table-column> -->
              <el-table-column prop="functions" label="功效" align="center" header-align="center">
                <template #default="{ row }">
                  {{ row.functions || '—' }}
                </template>
              </el-table-column>
              <el-table-column
                prop="diseaseIcd11Category"
                label="疾病编号"
                align="center"
                header-align="center"
              >
                <template #default="{ row }">
                  {{ row.diseaseIcd11Category || '—' }}
                </template>
              </el-table-column>
              <el-table-column
                prop="bioResourceCount"
                label="生物资源数量"
                align="center"
                header-align="center"
              >
                <template #default="{ row }">
                  {{ row.bioResourceCount || '—' }}
                </template>
              </el-table-column>
              <!-- <el-table-column
                prop="numOfHerbs"
                label="药材数"
                sortable
                align="center"
                header-align="center"
              >
                <template #default="{ row }">
                  {{ row.numOfHerbs || '—' }}
                </template>
              </el-table-column>
              <el-table-column
                prop="numOfNaturalProducts"
                label="天然产物数"
                sortable
                align="center"
                header-align="center"
              >
                <template #default="{ row }">
                  {{ row.numOfNaturalProducts || '—' }}
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
import { fetchPrescriptions } from '@/app/api/cms/prescriptions'
import type { Prescription } from '@/app/api/cms/types'
import { Search } from '@element-plus/icons-vue'
import { onMounted, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute()

const prescriptions = ref<Prescription[]>([])
const error = ref('')

const sortKey = ref<'prescriptionId' | 'chineseName' | 'numOfHerbs' | 'numOfNaturalProducts' | any>(
  'numOfNaturalProducts'
)
const sortDir = ref<'asc' | 'desc'>('desc')

// const cateList = ref<any>([])
// const functionList = ref<any>([])

const filters = reactive({
  keyword: '',
  category: '',
  functions: ''
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

const onSortChange = (row: any) => {
  let sort = 0
  let orderBy
  switch (row.prop) {
    case 'rowcriptionId':
      sort = 1
      if (!row.order) orderBy = ''
      if (row.order == 'ascending') orderBy = 'asc'
      if (row.order == 'descending') orderBy = 'desc'
      break
    case 'numOfHerbs':
      sort = 2
      if (!row.order) orderBy = ''
      if (row.order == 'ascending') orderBy = 'asc'
      if (row.order == 'descending') orderBy = 'desc'
      break
    case 'numOfNaturalProducts':
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

const buildParams = () => {
  return {
    page: pager.currentPage,
    pageSize: pager.pageSize,
    q: String(filters.keyword ?? '') || undefined,
    functions: filters.functions
  }
}

const onQueryList = async () => {
  pager.isLoading = true
  error.value = ''
  try {
    const result = (await fetchPrescriptions(buildParams())) as any
    pager.dataList = result.records ?? []
    pager.totalCount = result.total ?? 0
  } catch (err) {
    error.value = err instanceof Error ? err.message : '数据加载失败'
    prescriptions.value = []
  } finally {
    pager.fristLoading = false
    pager.isLoading = false
  }
  tableRef.value?.doLayout()
}

const onResetList = () => {
  pager.currentPage = 1
  filters.keyword = ''
  filters.category = ''
  filters.functions = ''
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
