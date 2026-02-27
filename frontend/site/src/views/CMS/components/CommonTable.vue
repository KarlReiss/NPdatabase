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
    <el-skeleton v-if="pager.fristLoading && pager.isLoading" :rows="8" animated />
    <el-table
      ref="tableRef"
      v-loading="pager.isLoading"
      :data="pager.dataList"
      size="small"
      :border="false"
      stripe
      :row-key="rowKey"
      :empty-text="emptyText"
      highlight-current-row
      scrollbar-always-on
      :header-cell-style="{ background: '#f5f7fa', color: '#606266' }"
      class="w-full"
    >
      <!-- show-overflow-tooltip -->
      <el-table-column
        v-for="(columnItem, idx) in columns"
        :key="idx"
        :prop="columnItem?.prop ?? 'prop'"
        :label="columnItem?.label ?? 'label'"
        :align="columnItem?.align ?? 'center'"
        :headerAlign="columnItem?.align ?? 'center'"
        :min-width="columnItem?.minWidth ?? 'auto'"
        :width="columnItem?.width ?? 'auto'"
        :fixed="columnItem?.fixed ?? ''"
        :formatter="columnItem?.formatter ?? defaultFormatter"
      >
        <template
          v-if="typeof columnItem?.renderer == 'symbol' || typeof columnItem?.func == 'object'"
          #default="{ row, $index }"
        >
          <component
            v-if="typeof columnItem?.renderer == 'symbol'"
            :is="columnItem?.renderer(row, row[columnItem?.prop], $index)"
          />
          <template v-if="typeof columnItem?.func == 'object'">
            {{ columnItem?.func(row, row[columnItem?.prop], $index) }}
          </template>
        </template>
      </el-table-column>
    </el-table>
    <Pagination
      v-if="pager.totalCount > 0"
      :page="pager.currentPage"
      :total="pager.totalCount"
      :limit="pager.pageSize"
      @change-page="currentChange"
      @change-size="sizeChange"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
// 组件属性（保持不变）
interface Props {
  rowKey?: string
  emptyText?: string
  listById?: string
  checkList?: any
  params?: any
  apiFetch: any
  columns: any
}
const props = withDefaults(defineProps<Props>(), {
  rowKey: 'id',
  emptyText: '暂无数据',
  listById: '',
  checkList: () => {},
  params: {},
  apiFetch: () => {},
  columns: []
})

const defaultFormatter = (row, column, cellValue, index) => {
  return cellValue
}

const error = ref('')

const sortKey = ref<string>('')
const sortDir = ref<'asc' | 'desc'>('desc')
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

const emit = defineEmits(['update:count'])
const onQueryList = async () => {
  const { listById, checkList, params, apiFetch } = props
  pager.isLoading = true
  error.value = ''
  try {
    const result = await apiFetch(listById, {
      page: pager.currentPage,
      pageSize: pager.pageSize,
      ...params
    })
    pager.dataList = result.records
      ? typeof checkList != 'undefined'
        ? checkList(result.records)
        : result.records
      : (result.records ?? [])
    pager.totalCount = result.total ?? 0
    emit('update:count', pager.totalCount)
  } catch (err) {
    error.value = err instanceof Error ? err.message : '数据加载失败'
    pager.dataList.value = []
  } finally {
    pager.fristLoading = false
    pager.isLoading = false
  }
  tableRef.value.doLayout()
}

const onResetList = () => {
  pager.currentPage = 1
  onQueryList()
}

const onSearchList = () => {
  pager.currentPage = 1
  onQueryList()
}

onMounted(onSearchList)
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
