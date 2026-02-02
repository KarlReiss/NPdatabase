<template>
  <span class="inline-flex flex-col text-[10px] leading-none">
    <span :class="[active && dir === 'asc' ? 'text-[#10B981]' : 'text-slate-300']">▲</span>
    <span :class="[active && dir === 'desc' ? 'text-[#10B981]' : 'text-slate-300']">▼</span>
  </span>
</template>

<script setup lang="ts">
defineProps<{ active?: boolean; dir?: 'asc' | 'desc' }>();
</script>
