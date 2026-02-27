<script setup lang="ts">
import { ElDropdown, ElDropdownMenu, ElDropdownItem } from 'element-plus'
import { useDesign } from '@/app/hooks/web/useDesign'
import LockDialog from './components/LockDialog.vue'
import { useLockStore } from '@/store/modules/lock'
import { useUserStore } from '@/store/modules/user'
import { useI18n } from '@/app/hooks/web/useI18n'
import LockPage from './components/LockPage.vue'
import { ref, computed } from 'vue'

const userStore = useUserStore()
const lockStore = useLockStore()
const getIsLock = computed(() => lockStore.getLockInfo?.isLock ?? false)
const { getPrefixCls } = useDesign()
const prefixCls = getPrefixCls('user-info')
const { t } = useI18n()
// const loginOut = () => {
//   userStore.logoutConfirm()
// }

const dialogVisible = ref<boolean>(false)
// 锁定屏幕
const lockScreen = () => {
  dialogVisible.value = true
}
</script>

<template>
  <ElDropdown class="custom-hover" :class="prefixCls" trigger="click">
    <div class="flex items-center color-black dark:color-white">
      <img
        :src="'https://picsum.photos/64/64' || '@/assets/imgs/avatar.jpg'"
        alt=""
        class="w-[calc(var(--logo-height)-25px)] rounded-[50%]"
      />
      <span class="<lg:hidden text-14px pl-[5px] color-black dark:color-white">
        {{ 'Dr. Research' || userStore.getUserInfo?.username }}
      </span>
    </div>
    <template #dropdown>
      <ElDropdownMenu>
        <ElDropdownItem
          ><div @click="lockScreen">{{ t('lock.lockScreen') }}</div></ElDropdownItem
        >
        <!-- <ElDropdownItem><div @click="loginOut">{{ t('common.loginOut') }}</div></ElDropdownItem> -->
      </ElDropdownMenu>
    </template>
  </ElDropdown>

  <LockDialog v-if="dialogVisible" v-model="dialogVisible" />
  <teleport to="body">
    <transition name="fade-bottom" mode="out-in">
      <LockPage v-if="getIsLock" />
    </transition>
  </teleport>
</template>

<style scoped lang="less">
.fade-bottom-enter-active,
.fade-bottom-leave-active {
  transition:
    opacity 0.25s,
    transform 0.3s;
}

.fade-bottom-enter-from {
  opacity: 0;
  transform: translateY(-10%);
}

.fade-bottom-leave-to {
  opacity: 0;
  transform: translateY(10%);
}
</style>
