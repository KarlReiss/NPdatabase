<template>
  <div
    class="bg-white dark:bg-[var(--el-bg-color)]"
    :style="{
      '--theme-white': '#fff',
      '--theme': '#2F6F5E',
      '--theme-soft': '#DDEBE6',
      '--theme-bg': '#EFF6F2'
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
                v-model="filters.resourceType"
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
            <!-- <el-collapse-item title="分类（科/属）" name="2">
              <template #icon="{ isActive }">
                <Icon class="icon-ele" :icon="`svg-icon:${isActive ? 'menu-up' : 'menu-down'}`" :size="20" />
              </template>
              <el-cascader
                v-model="filters.taxonomy" :options="cateList"
                :props="{ checkStrictly: true }" placeholder="请选择分类（科/属）"
                clearable filterable class="w-full text-sm"
              />
            </el-collapse-item> -->
            <el-collapse-item title="分类（科）" name="2">
              <template #icon="{ isActive }">
                <Icon
                  class="icon-ele"
                  :icon="`svg-icon:${isActive ? 'menu-up' : 'menu-down'}`"
                  :size="20"
                />
              </template>
              <el-select
                v-model="filters.taxonomyFamily"
                class="w-full text-sm"
                placeholder="请输入/选择分类（科）"
                clearable
                filterable
                @change="onFamilyChange"
              >
                <el-option
                  v-for="(item, idx) in cateList"
                  :key="idx"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-collapse-item>
            <el-collapse-item v-if="subCateList.length > 0" title="分类（属）" name="3">
              <template #icon="{ isActive }">
                <Icon
                  class="icon-ele"
                  :icon="`svg-icon:${isActive ? 'menu-up' : 'menu-down'}`"
                  :size="20"
                />
              </template>
              <el-select
                v-model="filters.taxonomyGenus"
                class="w-full text-sm"
                placeholder="请输入/选择分类（属）"
                clearable
                filterable
                @change="onSearch"
              >
                <el-option
                  v-for="(item, idx) in subCateList"
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
              :default-sort="{ prop: 'resourceId', order: 'descending' }"
              @sort-change="onSortChange"
            >
              <!-- show-overflow-tooltip
              @cell-click="onCellClick" @sort-change="onSortChange"
              @selection-change="handleSelectionChange" -->
              <el-table-column
                prop="resourceId"
                label="编号"
                sortable
                align="center"
                header-align="center"
              >
                <template #default="{ row }">
                  <RouterLink
                    :to="`/resources/${row.resourceId}`"
                    class="text-[var(--el-color-primary)] hover:underline font-medium"
                  >
                    {{ row.resourceId }}
                  </RouterLink>
                </template>
              </el-table-column>
              <el-table-column
                prop="standardChineseName"
                label="名称"
                sortable
                align="center"
                header-align="center"
              >
                <template #default="{ row }">
                  {{
                    row.standardChineseName ||
                    row.officialChineseName ||
                    row.chineseName ||
                    row.latinName ||
                    row.resourceId
                  }}
                </template>
              </el-table-column>
              <el-table-column
                prop="resourceType"
                label="拉丁名"
                align="center"
                header-align="center"
              >
                <template #default="{ row }">
                  {{ row.latinName || '—' }}
                </template>
              </el-table-column>
              <el-table-column
                prop="resourceType"
                label="资源类型"
                align="center"
                header-align="center"
              >
                <template #default="{ row }">
                  {{ toTypeLabel(row.resourceType) }}
                </template>
              </el-table-column>
              <el-table-column
                prop="taxonomyFamily"
                label="分类（科/属）"
                align="center"
                header-align="center"
              >
                <template #default="{ row }">
                  {{ row.taxonomyFamily || '—' }} / {{ row.taxonomyGenus || '—' }}
                </template>
              </el-table-column>
              <el-table-column
                prop="numOfNaturalProducts"
                label="天然产物数"
                sortable
                align="center"
                header-align="center"
              />
              <el-table-column
                prop="numOfPrescriptions"
                label="相关处方数"
                sortable
                align="center"
                header-align="center"
              />
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
  fetchBioResources,
  fetchBioResourceResourceType,
  fetchBioResourceCategories
} from '@/app/api/cms/bioResources'
import type { BioResource } from '@/app/api/cms/types'
import { onMounted, reactive, ref, watch } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { useRoute } from 'vue-router'
import { set } from 'lodash-es'

const route = useRoute()

const resources = ref<BioResource[]>([])
const error = ref('')

const sortKey = ref<
  'resourceId' | 'chineseName' | 'numOfNaturalProducts' | 'numOfPrescriptions' | any
>('numOfNaturalProducts')
const sortDir = ref<'asc' | 'desc'>('desc')
const typeList = ref<any>([])
const cateList = ref<any>([])
const subCateList = ref<any>([])

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
  try {
    const resourceTypePromise = fetchBioResourceResourceType()
    const categoriesPromise = fetchBioResourceCategories()
    const [resourceTypeResult, categoriesResult] = await Promise.allSettled([
      resourceTypePromise,
      categoriesPromise
    ])

    if (resourceTypeResult.status === 'fulfilled') {
      typeList.value = (resourceTypeResult.value as any).map((txt: any) => {
        return { value: txt, label: txt }
      })
    }

    if (categoriesResult.status === 'fulfilled') {
      const keys = Object.keys(categoriesResult.value as any)
      const tree: any = []
      keys.forEach((txt) => {
        const values = txt.split(' ')
        const some = tree.find((row) => row.value == values[0])
        if (some) {
          set(some, 'children', [
            ...some.children,
            {
              label: values[1],
              value: values[1]
            }
          ])
        } else {
          tree.push({
            label: values[0],
            value: values[0],
            children: [
              {
                label: values[1],
                value: values[1]
              }
            ]
          })
        }
      })
      cateList.value = tree
    }
  } catch (err) {
    console.error(err)
    typeList.value = []
    cateList.value = []
  }
}

const onFamilyChange = (val: any) => {
  const some = cateList.value.find((row) => row.value == val)
  filters.taxonomyGenus = ''
  if (some) {
    subCateList.value = some.children
  } else {
    subCateList.value = []
  }
}

const filters = reactive<any>({
  keyword: '',
  resourceType: '',
  taxonomy: [],
  taxonomyFamily: '',
  taxonomyGenus: ''
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

watch(
  () => filters.taxonomy,
  (vals: any) => {
    if (vals.length > 0) {
      if (vals.length > 1) {
        filters.taxonomyFamily = vals[0]
        filters.taxonomyGenus = vals[1]
      } else {
        filters.taxonomyFamily = vals[0]
        filters.taxonomyGenus = ''
      }
    }
  },
  {
    // deep: true,
    immediate: true
  }
)

const activeNames = ref(['1', '2', '3'])
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
    case 'resourceId':
      sort = 1
      if (!row.order) orderBy = ''
      if (row.order == 'ascending') orderBy = 'asc'
      if (row.order == 'descending') orderBy = 'desc'
      break
    case 'chineseName':
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
    case 'numOfPrescriptions':
      sort = 4
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
    resourceType: String(filters.resourceType ?? '') || undefined,
    taxonomyFamily: String(filters.taxonomyFamily ?? '') || undefined,
    taxonomyGenus: String(filters.taxonomyGenus ?? '') || undefined
  }
}

const onQueryList = async () => {
  pager.isLoading = true
  error.value = ''
  // const loadingInstance = ElLoading.service({
  //   target: document.querySelector('.el-table__body'),
  //   lock: false, spinner: '',
  //   background: '', // 遮罩背景色
  //   svg: '' // 元素覆盖默认加载器
  // })

  try {
    const result = (await fetchBioResources(buildParams())) as any
    pager.dataList = result.records ?? []
    pager.totalCount = result.total ?? 0
  } catch (err) {
    error.value = err instanceof Error ? err.message : '数据加载失败'
    resources.value = []
  } finally {
    pager.fristLoading = false
    pager.isLoading = false
    // loadingInstance.close()
  }
  tableRef.value?.doLayout()
}

const onResetList = () => {
  pager.currentPage = 1
  filters.keyword = ''
  filters.resourceType = ''
  filters.taxonomy = []
  filters.taxonomyFamily = ''
  filters.taxonomyGenus = ''
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
