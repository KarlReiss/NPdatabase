<template>
  <el-container :class="`${prefixCls}-content`" class="layout-container">
    <!-- 主内容区 -->
    <el-container>
      <!-- 顶部导航栏 -->
      <el-header height="60px" class="layout-header shadow-lg">
        <Header />
      </el-header>
      <!-- 内容区域 -->
      <el-main class="layout-main bg-white dark:bg-[var(--el-bg-color)]" :loading="pageLoading">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
        <!-- <el-footer height="90px" class="layout-footer !p-0"><Footer /></el-footer> -->
      </el-main>
      <!-- 页脚 -->
      <el-footer height="90px" class="layout-footer !p-0">
        <Footer />
      </el-footer>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
import { useAppStore } from '@/store/modules/app'
import { useDesign } from '@/app/hooks/web/useDesign'

import { computed } from 'vue'

const { getPrefixCls } = useDesign()
const prefixCls = getPrefixCls('cus-layout')
const appStore = useAppStore()

const pageLoading = computed(() => appStore.getPageLoading)
</script>

<style scoped>
.layout-container {
  height: 100vh;
  overflow: hidden;
}

.layout-sidebar {
  background-color: #001529;
  color: #fff;
  overflow-y: auto;
}

.layout-header {
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 0;
}

.layout-main {
  padding: 0;
  overflow-y: auto;
  /* background-color: #f0f2f5; */
}

.layout-footer {
  background-color: #fff;
  text-align: center;
  line-height: 40px;
  font-size: 12px;
  color: #999;
  border-top: 1px solid #e8e8e8;
}

.content-card {
  margin-bottom: 20px;
  border-radius: 4px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
