<template>
  <div class="footer-wrapper">
    <div class="footer-content">
      <div class="copyright text-base leading-[30px] color-white">
        © 2026 云南天然产物活性数据库
        <span class="h-4 w-px bg-gray-300 mx-2"></span>
        保留所有权利。
      </div>
      <div class="flex flex-row items-center justify-around">
        <el-link
          type="info"
          :underline="true"
          href="#/web/article-detail/user-guide"
          class="text-[12px] leading-[30px] !color-white"
          >使用指南</el-link
        >
        <span class="h-4 w-px bg-gray-300 mx-2"></span>
        <el-link
          type="info"
          :underline="true"
          href="#/web/article-detail/data-source"
          class="text-[12px] leading-[30px] !color-white"
          >数据来源</el-link
        >
        <span class="h-4 w-px bg-gray-300 mx-2"></span>
        <el-link
          type="info"
          :underline="true"
          href="#/web/article-detail/regarding-project"
          class="text-[12px] leading-[30px] !color-white"
          >关于项目</el-link
        >
        <span class="h-4 w-px bg-gray-300 mx-2"></span>
        <el-link
          type="info"
          :underline="true"
          href="#/web/article-detail/contact-us"
          class="text-[12px] leading-[30px] !color-white"
          >联系我们</el-link
        >
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 页脚组件
</script>

<style scoped>
.footer-wrapper {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--header-footer-color-primary);
}

.footer-content {
  /* width: 100%; */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.footer-link {
  font-size: 12px;
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
    gap: 5px;
    text-align: center;
  }
}
</style>
