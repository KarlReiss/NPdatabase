<style lang="less" scoped>
.cusSeacrh {
  .el-input_wrapper {
    box-shadow: 0 0 0 0 var(--el-input-border-color, var(--el-border-color)) inset !important;
  }
}
</style>
<template>
  <div class="max-w-[1440px] mx-auto px-6 py-6">
    <section class="mt-20 flex flex-col items-center px-6">
      <h1 class="text-3xl md:text-4xl font-bold text-[#212121] dark:color-white mb-10 text-center">
        探索天然产物与活性数据
      </h1>

      <div
        class="w-full max-w-[900px]"
        :style="{
          '--el-border-color': '#0071BC',
          '--el-border-color-hover': '#0071BC'
        }"
      >
        <form @submit="handleSearch" class="relative group">
          <el-input
            v-model="searchValue"
            type="text"
            :placeholder="
              searchTab === 'keyword' ? '输入名称、CAS号、编号...' : '输入SMILES序列...'
            "
            @keyup.enter="handleSearch"
            class="header-search w-full h-11 bg-white dark:bg-[var(--el-bg-color)] border rounded-md text-sm focus:outline-none focus:ring-0"
          >
            <template #prepend>
              <el-select
                v-model="searchTab"
                placeholder="关键词搜索"
                class="!w-[150px] cursor-pointer"
                @change="onSearchTabChange"
                :style="{
                  '--el-text-color-regular': '#212121',
                  '--el-text-color-placeholder': '#212121'
                }"
              >
                <el-option label="关键词搜索" value="keyword" />
                <el-option label="SMILES结构搜索" value="smiles" />
              </el-select>
            </template>
            <template #append>
              <el-icon color="#fff" size="24px" class="font-bold" @click="handleSearch">
                <Search color="#fff" />
              </el-icon>
            </template>
          </el-input>
        </form>

        <div class="mt-4 flex flex-wrap gap-1 text-slate-500 text-xs">
          <el-button
            v-for="(item, idx) in shiliList"
            :key="`_${idx}`"
            type="primary"
            class="bg-[#0071BC] hover:shadow-md hover:-translate-y-1 duration-300"
            :title="item.label"
            @click="applyExample(item.value as string)"
            >{{ item.label }}</el-button
          >
        </div>
      </div>
    </section>

    <div class="h-1 bg-gray-300 my-14"></div>
    <section class="max-w-[1440px] mx-auto">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-3xl font-bold text-[#212121] dark:color-white w-1/2">数据库概览</h2>
        <el-alert
          v-if="statsError"
          :title="statsError"
          type="error"
          class="text-xs text-red-500 w-1/2"
        />
      </div>
      <div class="grid grid-cols-2 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="(menu, idx) in menuList"
          :key="`__${idx}`"
          class="bg-[#E1F3F8] border border-[#E2E8F0] overflow-hidden rounded-[8px] px-9 py-8 bg-[#E1F3F8] hover:shadow-md hover:-translate-y-1 duration-300 group transition-all relative cursor-pointer"
        >
          <div class="absolute top-0 bottom-0 left-0 w-2 bg-[#02BFE7]"></div>
          <div class="text-2xl text-[#212121] font-bold">{{ menu.label }}</div>
          <div class="text-3xl leading-12 font-bold text-[var(--el-color-primary)] font-400">{{
            menu.value
          }}</div>
        </div>
      </div>
    </section>

    <section class="w-full mx-auto mt-3xl grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-xl">
      <div
        v-for="(topic, idx) in topicList"
        :key="`__${idx}`"
        :class="[
          'bg-[#EBEBEB] pl-7.5 py-7.5 pr-26 rounded-md overflow-hidden border border-gray-100',
          'shadow-sm hover:shadow-md hover:-translate-y-1 duration-300 group',
          'relative cursor-pointer transition-all'
        ]"
        @click="onOtherClick(topic)"
      >
        <div
          class="absolute top-9 right-7.5 w-13.5 h-13.5 rounded-lg flex items-center justify-center"
        >
          <Icon :icon="topic.icon" :size="54" class="mr-10px" />
        </div>
        <h3 class="text-6 leading-7 text-[#212121] font-bold mb-1">{{ topic.label }}</h3>
        <p class="text-sm leading-7 text-[#0033BD] font-bold mb-2">{{ topic.value }}</p>
        <p class="text-xs leading-7 text-[#212121]">{{ topic.bref }}</p>

        <div class="absolute bottom-0 left-0 right-0 h-2 bg-[var(--el-color-primary)]"></div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { fetchSearch, fetchStats } from '@/app/api/cms/common'
import { Search } from '@element-plus/icons-vue'
import { formatCount } from '@/app/utils/index'
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const { push } = useRouter()
const stats = ref<any>(null)
const statsError = ref('')

const shiliList = ref([
  { label: 'Curcumin', value: 'Curcumin' },
  { label: 'Panax ginseng', value: 'Panax ginseng' },
  { label: 'EGFR', value: 'EGFR' },
  { label: 'CAS 458-37-7', value: 'CAS 458-37-7' }
])

const menuList = computed(() => {
  return [
    { label: '生物资源', value: formatCount(stats.value?.bioResources) },
    { label: '天然产物', value: formatCount(stats.value?.naturalProducts) },
    { label: '处方', value: formatCount(stats.value?.prescriptions) },
    { label: '靶点', value: formatCount(stats.value?.targets) },
    { label: '活性记录', value: formatCount(stats.value?.bioactivity) },
    { label: '毒性记录', value: formatCount(stats.value?.toxicity) }
  ]
})

const topicList = computed(() => {
  return [
    {
      id: 'anti-tumor',
      icon: 'svg-icon:anti-tumor',
      label: '抗肿瘤（Anti-tumor）',
      value: '1,245+ 个化合物',
      bref: '浏览具有抗肿瘤活性的天然产物集合。'
    },
    {
      id: 'cardiovascular',
      icon: 'svg-icon:cardiovascular',
      label: '心脑血管（Cardiovascular）',
      value: '892+ 个化合物',
      bref: '探索心脑血管相关靶点的活性天然产物。'
    },
    {
      id: 'toxic-herbs',
      icon: 'svg-icon:toxic-herbs',
      label: '有毒药材（Toxic Herbs）',
      value: '310+ 条记录',
      bref: '传统用药的毒性与安全性信息汇总。'
    },
    {
      id: 'anti-inflammatory',
      icon: 'svg-icon:anti-tumor',
      label: '抗炎免疫（Anti-inflammatory）',
      value: '176+ 条记录',
      bref: '炎症相关靶点与活性数据'
    }
  ]
})

import { ElLoading } from 'element-plus'
const searchTab = ref<'keyword' | 'smiles'>('keyword')
const searchValue = ref('')
import { useEventBus } from '@/app/hooks/event/useEventBus'
import { EventsConfigs } from '@/app/hooks/event/event'

const { emit } = useEventBus()
function onSearchTabChange(value) {
  emit(EventsConfigs.eventBus.searchTab, value)
}

useEventBus({
  name: EventsConfigs.eventBus.searchTab,
  callback: (value: 'keyword' | 'smiles') => {
    searchTab.value = value
  }
})
const handleSearch = async (event: Event) => {
  event.preventDefault()
  const loading = ElLoading.service({
    lock: true,
    text: 'Loading...',
    background: 'rgba(255, 255, 255, 0.7)'
  })
  const q = searchValue.value?.trim()
  if (!q) return
  if (searchTab.value === 'smiles') {
    push({ path: '/compounds', query: { q } })
    return
  }
  try {
    const result = (await fetchSearch(q, 'all')) as any
    const keyword = q.toLowerCase()
    const exactNp = result.naturalProducts.find(
      (item) => (item.npId || '').toLowerCase() === keyword
    )
    if (exactNp?.npId) {
      push({ path: `/compounds/${exactNp.npId}` })
      return
    }
    const exactTarget = result.targets.find(
      (item) => (item.targetId || '').toLowerCase() === keyword
    )
    if (exactTarget?.targetId) {
      push({ path: `/web/targets/${exactTarget.targetId}` })
      return
    }
    if (result.targets.length > 0 && result.naturalProducts.length === 0) {
      push({ path: '/web/targets', query: { q } })
      return
    }
  } catch (err) {
    // ignore and fallback
  } finally {
    setTimeout(() => {
      loading.close()
    }, 2000)
  }
  push({ path: '/compounds', query: { q } })
}

const applyExample = (value: string) => {
  searchValue.value = value
  push({ path: '/compounds', query: { q: value } })
}

const loadStats = async () => {
  try {
    stats.value = await fetchStats()
  } catch (err) {
    statsError.value = err instanceof Error ? err.message : '统计数据加载失败'
  }
}

const onOtherClick = (item: any) => {
  push({ path: `topics/${item.id}` })
}

onMounted(() => {
  loadStats()
})
</script>
<style scoped lang="less">
.header-search {
  :deep(.el-input-group__prepend) {
    padding: 0;
    .el-select {
      margin: 0;
      height: 100%;
      .el-select__wrapper {
        line-height: 24px;
        min-height: 100%;
      }
    }
  }
  :deep(.el-input-group__append) {
    background-color: var(--el-color-primary);
    width: 100px;
    cursor: pointer;
  }
}
.cusSearch {
  :deep(.el-input__wrapper) {
    box-shadow: 0 0 0 0 var(--el-input-border-color, var(--el-border-color)) inset !important;
  }
}
</style>
