<template>
  <header
    class="h-14 bg-#F1F1F1 dark:bg-[var(--el-bg-color)] border-b border-[#E2E8F0] z-50 overflow-hidden shadow-md duration-300"
    :style="[cusStyle]"
  >
    <div class="max-w-[1440px] mx-auto h-full px-6 flex items-center gap-6">
      <div class="flex items-center space-x-2">
        <div
          class="w-8 h-8 bg-[var(--header-footer-color-primary)] rounded-md flex items-center justify-center"
        >
          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
            />
          </svg>
        </div>
        <span class="color-[#1E293B] dark:color-white text-lg leading-5 font-bold tracking-tight"
          >云南天然产物活性数据库</span
        >
      </div>

      <nav class="inline-flex lg:flex items-center space-x-1 text-sm mr-auto">
        <RouterLink
          v-for="item in navItems"
          :key="item.name"
          :to="item.to"
          :class="[
            'hover:color-[var(--header-footer-color-primary)] px-2 leading-15 h-15 text-center transition-colors duration-200 relative select-none no-underline hover:no-underline',
            isActive(item)
              ? 'color-[var(--header-footer-color-primary)] font-bold bg-white dark:bg-[var(--el-bg-color)]'
              : 'color-[#334155] dark:color-white',
            `${['生物资源', '天然产物'].includes(item.name) ? '!min-w-[81px]' : '!min-w-[50px]'}`
          ]"
        >
          {{ item.name }}
          <div
            v-if="isActive(item)"
            class="absolute bottom-0.75 left-0 right-0 h-0.75 rounded-2 bg-[var(--header-footer-color-primary)]"
          ></div>
        </RouterLink>
      </nav>

      <div class="lg:flex flex-0.3 justify-center ml-auto sm:hidden md:hidden lg:hidden md:hidden">
        <div class="relative w-full max-w-[680px]">
          <el-input
            type="text"
            :placeholder="
              searchTab === 'keyword' ? '输入名称、CAS号、编号...' : '输入SMILES序列...'
            "
            v-model="searchValue"
            @keyup.enter="handleSearch"
            class="header-search w-full h-10 bg-white dark:bg-[var(--el-bg-color)] border border-[#E2E8F0] rounded-md text-sm text-slate-700 focus:outline-none focus:ring-0"
          >
            <template #prepend>
              <el-select
                v-model="searchTab"
                placeholder="关键词搜索"
                class="!w-[120px] cursor-pointer"
                @change="onSearchTabChange"
              >
                <el-option label="关键词搜索" value="keyword" />
                <el-option label="SMILES结构搜索" value="smiles" />
              </el-select>
            </template>
            <template #append>
              <el-icon color="#fff" class="font-bold" @click="handleSearch">
                <Search color="#fff" />
              </el-icon>
            </template>
          </el-input>
        </div>
      </div>
      <div class="h-4 w-px bg-gray-300 mx-2 sm:hidden md:hidden lg:hidden"></div>
      <div class="flex items-center space-x-2 cursor-pointer group">
        <UserInfo />
        <!-- <ThemeSwitch /> -->
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
// import { ThemeSwitch } from '@/components/ThemeSwitch'
import { Search } from '@element-plus/icons-vue'
import { UserInfo } from '@/components/UserInfo'
import { useRouter, useRoute } from 'vue-router'
import { computed, ref } from 'vue'

const route = useRoute()
const router = useRouter()
const searchTab = ref<'keyword' | 'smiles'>('keyword')
const searchValue = ref('')
const navItems = [
  { name: '首页', to: { path: '/web/home' } },
  { name: '生物资源', to: { path: '/web/bio-resources' } },
  { name: '天然产物', to: { path: '/web/natural-products' } },
  { name: '处方', to: { path: '/web/prescriptions' } },
  { name: '靶点', to: { path: '/web/targets' } },
  { name: '疾病', to: { path: '/web/diseases' } }
]

const isActive = (item: (typeof navItems)[number]) => {
  if (item.to.path === '/') return route.path === '/'
  return route.path.startsWith(item.to.path)
}

const appStore = useAppStore()
// const isDark = computed(() => appStore.getIsDark)
const cusStyle = computed(() => {
  let cs = 'background-size: 3px 3px; backdrop-filter: saturate(50%) blur(4px);'
  cs += 'background-image: radial-gradient(transparent 1px, --bg-color 1px);'
  cs += 'border-bottom:1px solid --border-color;'
  if (appStore.getIsDark) {
    cs = cs.replace(/--bg-color/g, '#141414').replace(/--border-color/g, '#4c4d4f')
  } else {
    cs = cs.replace(/--bg-color/g, '#ffffff').replace(/--border-color/g, '#dcdfe6')
  }
  return cs
})

import { fetchSearch } from '@/app/api/cms/common'
import { ElLoading } from 'element-plus'
import { useEventBus } from '@/app/hooks/event/useEventBus'
import { EventsConfigs } from '@/app/hooks/event/event'
import { useAppStore } from '@/store/modules/app'

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
  const q = searchValue.value.trim()

  if (!q) return
  if (searchTab.value === 'smiles') {
    router.push({ path: '/compounds', query: { q } })
    return
  }
  try {
    const result = (await fetchSearch(q, 'all')) as any
    const keyword = q.toLowerCase()
    const exactNp = result.naturalProducts.find(
      (item) => (item.npId || '').toLowerCase() === keyword
    )
    if (exactNp?.npId) {
      router.push({ path: `/compounds/${exactNp.npId}` })
      return
    }
    const exactTarget = result.targets.find(
      (item) => (item.targetId || '').toLowerCase() === keyword
    )
    if (exactTarget?.targetId) {
      router.push({ path: `/web/targets/${exactTarget.targetId}` })
      return
    }
    if (result.targets.length > 0 && result.naturalProducts.length === 0) {
      router.push({ path: '/web/targets', query: { q } })
      return
    }
  } catch (err) {
    // ignore and fallback
  } finally {
    setTimeout(() => {
      loading.close()
    }, 2000)
  }
  router.push({ path: '/compounds', query: { q } })
}
</script>
<style lang="less" scoped>
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
    background-color: var(--header-footer-color-primary);
    width: 50px;
    cursor: pointer;
  }
}
</style>
