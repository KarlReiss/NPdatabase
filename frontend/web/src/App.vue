<template>
  <div class="min-h-screen flex flex-col bg-[#F8FAFC] selection:bg-[#10B981]/10 selection:text-[#10B981]">
    <AppHeader />
    <main class="flex-grow">
      <RouterView />
    </main>
    <footer class="bg-white border-t border-[#E2E8F0] py-8 text-center">
      <div class="max-w-[1440px] mx-auto px-6">
        <p class="text-slate-400 text-xs">
          © 2024 云南天然产物活性数据库。保留所有权利。
        </p>
        <div class="mt-2 space-x-4 text-xs">
          <a href="#" class="text-slate-500 hover:text-[#10B981]">隐私政策</a>
          <a href="#" class="text-slate-500 hover:text-[#10B981]">联系我们</a>
          <a href="#" class="text-slate-500 hover:text-[#10B981]">文档</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import AppHeader from '@/components/AppHeader.vue';
</script>
