<script setup lang="ts">
import { LoginForm, RegisterForm } from './components'
import { useDesign } from '@/app/hooks/web/useDesign'
import { useAppStore } from '@/store/modules/app'
import { underlineToHump } from '@/app/utils'
import { ElScrollbar } from 'element-plus'
import { ref } from 'vue'

const { getPrefixCls } = useDesign()
const prefixCls = getPrefixCls('login')
const appStore = useAppStore()
const isLogin = ref(true)
const toRegister = () => {
  isLogin.value = false
}
const toLogin = () => {
  isLogin.value = true
}
</script>

<template>
  <div :class="prefixCls" class="h-[100%] relative">
    <ElScrollbar class="h-full">
      <div
        class="relative flex mx-auto min-h-100vh"
        :class="`${prefixCls} flex-1 bg-gray-500 bg-opacity-20 relative p-30px`"
      >
        <div class="flex-1 p-30px lt-sm:p-10px relative">
          <div class="flex items-center relative text-[#000]">
            <img src="@/assets/imgs/logo.png" alt="" class="w-48px h-48px mr-10px" />
            <span class="text-20px font-bold">{{ underlineToHump(appStore.getTitle) }}</span>
          </div>
          <Transition appear enter-active-class="animate__animated animate__bounceInRight">
            <div
              class="h-full flex items-center m-auto w-[100%] at-2xl:max-w-500px at-xl:max-w-500px at-md:max-w-500px at-lg:max-w-500px"
            >
              <LoginForm
                v-if="isLogin"
                class="p-20px h-auto m-auto lt-xl:rounded-3xl lt-xl:light:bg-white"
                @to-register="toRegister"
              />
              <RegisterForm
                v-else
                class="p-20px h-auto m-auto lt-xl:rounded-3xl lt-xl:light:bg-white"
                @to-login="toLogin"
              />
            </div>
          </Transition>
        </div>
      </div>
    </ElScrollbar>
  </div>
</template>

<style lang="less" scoped>
@prefix-cls: ~'@{adminNamespace}-login';

.@{prefix-cls} {
  overflow: auto;

  &__left {
    &::before {
      position: absolute;
      top: 0;
      left: 0;
      z-index: -1;
      width: 100%;
      height: 100%;
      background-image: url('@/assets/svgs/login-bg.svg');
      background-position: center;
      background-repeat: no-repeat;
      content: '';
    }
  }
}
</style>
