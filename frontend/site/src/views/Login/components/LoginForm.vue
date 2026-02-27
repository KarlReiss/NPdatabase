<script setup lang="ts">
import type { RouteLocationNormalizedLoaded, RouteRecordRaw } from 'vue-router'
import { usePermissionStoreWithOut } from '@/store/modules/permission'
import { computed, onMounted, reactive, ref, unref, watch } from 'vue'
import { ElButton, ElLoading, ElMessage } from 'element-plus'
import { useUserStoreWithOut } from '@/store/modules/user'
import { EventsConfigs } from '@/app/hooks/event/event'
import { useStorage } from '@/app/hooks/web/useStorage'
import { useI18n } from '@/app/hooks/web/useI18n'
import { ImgCode } from '@/components/ImgCode'
import { useRouter } from 'vue-router'

const wsStorage = useStorage()
const permissionStore = usePermissionStoreWithOut() as any
const userStore = useUserStoreWithOut() as any
const { currentRoute, addRoute, push } = useRouter() as any
const { t } = useI18n() as any

const rules = {
  mobile: [],
  pwdCode: [],
  smsCode: []
}

const tempForm = reactive<any>({
  loginType: 'platform',
  mobile: '',
  pwdCode: '',
  smsCode: '',
  code: '',
  imgCode1: '',
  imgCode2: ''
})

const remember = ref(false)
const loading = ref(false)
const redirect = ref<string>('')
watch(
  () => currentRoute.value,
  (route: RouteLocationNormalizedLoaded) => {
    redirect.value = route?.query?.redirect as string
  },
  {
    immediate: true
  }
)

const imgCode1 = ref<{ code: string; type: 'expression' | 'image_code' }>({
  code: '',
  type: 'expression'
})

const changeCode1 = (event: { code: string; type: 'expression' | 'image_code' }) => {
  imgCode1.value = event
  if (['base', 'dev', 'test'].includes(import.meta.env.MODE)) {
    tempForm.imgCode1 = event.code
  }
}
const loginType = ref(1)

const getCookie = () => {
  const loginInfo = wsStorage.getStorage(EventsConfigs.wsStorage.user.userInfo)
  const userType = wsStorage.getStorage(EventsConfigs.wsStorage.user.userType)

  const localUser = loginInfo
    ? loginInfo
    : {
        mobile: undefined,
        pwdCode: undefined,
        remember: undefined
      }

  const loginType = userType ? userType : 'platform'

  const mobile = localUser.mobile
  remember.value = localUser.remember
  let pwdCode = localUser.pwdCode
  pwdCode = pwdCode === undefined ? tempForm.pwdCode : pwdCode

  return {
    loginType: loginType === undefined ? tempForm.loginType : loginType,
    mobile: mobile === undefined ? tempForm.mobile : mobile,
    pwdCode: pwdCode
  }
}

const signIn = async () => {
  const form = { ...tempForm }
  if (!form.mobile || form.mobile == null) {
    ElMessage.warning('请输入登录账号')
    return
  }
  if (loginType.value == 1) {
    if (!form.pwdCode || form.pwdCode == null) {
      ElMessage.warning('请输入账号密码')
      return
    }
  } else {
    if (!form.smsCode || form.smsCode == null) {
      ElMessage.warning('请输入短信验证码')
      return
    }
  }
  const value = imgCode1.value.type == 'image_code' ? form.imgCode1.toUpperCase() : form.imgCode1
  if (!value) {
    ElMessage.warning('请输入图形验证码值')
    return
  }
  const val =
    imgCode1.value.type == 'image_code' ? imgCode1.value.code.toUpperCase() : imgCode1.value.code
  if (val != value) {
    ElMessage.warning('输入的图形验证码值不正确')
    return
  }
  loading.value = true
  const loadingInstance = ElLoading.service({
    text: '账号' + form.mobile + '登录中，请耐心等待...',
    background: 'rgba(0, 0, 0, 0.6)'
  })

  onRouter(loadingInstance)
  loading.value = false
  loadingInstance.close()
}

const onRouter = async (loadingInstance: any) => {
  if (unref(remember)) {
    userStore.setLoginInfo({
      username: tempForm.mobile,
      password: tempForm.password
    })
  } else {
    userStore.setLoginInfo(undefined)
  }
  userStore.setRememberMe(unref(remember))
  userStore.setUserInfo({ username: tempForm.mobile, password: tempForm.password })
  await permissionStore.generateRoutes('static').catch(() => {})
  permissionStore.getAddRouters.forEach((route) => {
    addRoute(route as RouteRecordRaw)
  })
  setTimeout(() => {
    loading.value = false
    loadingInstance.close()
    push({ name: 'Home' }).catch((_err: any) => {
      location.reload()
    })
  }, 580)
}

const emit = defineEmits(['to-register', 'to-forget'])

onMounted(() => {
  const { mobile, pwdCode, loginType } = getCookie()
  tempForm.loginType = loginType ? loginType : tempForm.loginType
  tempForm.mobile = mobile ? mobile : tempForm.mobile
  tempForm.pwdCode = pwdCode ? pwdCode : tempForm.pwdCode
  if (['base', 'dev', 'test'].includes(import.meta.env.MODE)) {
    if (!tempForm.mobile || tempForm.mobile == null) {
      tempForm.mobile = 'admin'
      tempForm.pwdCode = '1q2w3E*'
    }
  }
})

const isFormValid = computed(() => {
  const { mobile, pwdCode } = tempForm
  return !!mobile && mobile != null && !!pwdCode && pwdCode != null
})
</script>

<template>
  <el-form
    ref="elFormRef"
    :rules="rules"
    label-position="top"
    v-model="tempForm"
    hide-required-asterisk
    size="large"
    class="dark:(border-1 border-[var(--el-border-color)] border-solid) w-[100%] rounded-lg bg-white dark:bg-[var(--el-bg-color)]"
  >
    <el-form-item label-width="8px">
      <h2 class="text-4xl font-bold text-center w-[100%]">{{ t('login.login') }}</h2>
    </el-form-item>
    <el-form-item label="登录账号" prop="mobile">
      <el-input
        ref="mobileRef"
        :loading="loading"
        placeholder="请输入登录账号"
        maxlength="20"
        name="mobile"
        v-model="tempForm.mobile"
        @keyup.enter="signIn()"
      />
    </el-form-item>
    <el-form-item label="账号密码" prop="password">
      <el-input
        ref="passwordRef"
        :loading="loading"
        type="password"
        name="password"
        show-password
        placeholder="请输入账号密码"
        maxlength="20"
        v-model="tempForm.pwdCode"
        @keyup.enter="signIn()"
      />
    </el-form-item>
    <el-form-item label="图形验证" prop="imgCode">
      <div class="codeArea">
        <el-input
          :loading="loading"
          v-model="tempForm.imgCode1"
          maxlength="4"
          placeholder="请输入图形验证码值"
          auto-complete="off"
          @keyup.enter="signIn()"
        />
        <ImgCode @change="changeCode1" ref="imgVerifyRef1" />
      </div>
    </el-form-item>
    <el-form-item label-width="8px">
      <div class="flex justify-between items-center w-[100%]">
        <el-checkbox v-model="remember" :label="t('login.remember')" size="default" />
        <!-- <el-link type="primary" :underline="false" @click="toForget">{{
          t('login.forgetPassword')
        }}</el-link> -->
      </div>
    </el-form-item>
    <el-form-item label-width="8px">
      <div class="w-[100%]">
        <el-button
          ref="loginBtnRef"
          :disabled="!isFormValid"
          :loading="loading"
          type="primary"
          class="w-[100%] loginBtn"
          @click="signIn"
        >
          {{ t('login.login') }}
        </el-button>
      </div>
    </el-form-item>
  </el-form>
</template>

<style lang="less" scoped>
:deep(.el-tabs__item) {
  &.is-active {
    font-size: 22px;
    font-weight: bold;
    color: var(--el-color-primary);
  }
}

.el-select__popper {
  width: 400px;
}

:deep(.anticon) {
  &:hover {
    color: var(--el-color-primary) !important;
  }
}

:deep(.el-select) {
  width: 100%;
}

:deep(.el-select-dropdown) {
  max-width: 243px;
}

:deep(.el-radio-group) {
  width: 100% !important;
  .el-radio-button {
    width: 33% !important;
    transition: transform 0.3s ease-in-out; /* 平滑过渡效果 */
    &:hover {
      transform: scale(1); /* 鼠标悬停时放大按钮 */
    }
    &.is-active {
      transform: scale(1); /* 选中状态时也应用放大效果 */
    }
  }
}

:deep(.el-radio-button__inner) {
  width: 100% !important;
}

:deep(.el-select-dropdown) {
  min-width: 100% !important;
}

.codeArea {
  display: inline-flex;
  width: 100%;

  .el-input {
    width: calc(100% - 100px);
  }

  .img-verify {
    // width:120px
  }
}
</style>
