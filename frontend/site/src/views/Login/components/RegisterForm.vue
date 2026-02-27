<script setup lang="ts">
import { ElButton, ElInput, ElMessage, FormRules } from 'element-plus'
import { required, checkVerifyPhone } from '@/app/utils/formRules'
import type { RouteLocationNormalizedLoaded } from 'vue-router'
import { useUserStoreWithOut } from '@/store/modules/user'
import { verifyPhone } from '@/app/utils/toolsValidate'
import { useI18n } from '@/app/hooks/web/useI18n'
import { watch, ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const userStore = useUserStoreWithOut() as any
const { currentRoute } = useRouter() as any
const emit = defineEmits(['to-login'])
const toLogin = () => {
  emit('to-login')
}

const { t } = useI18n()
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

const showRegister = ref<boolean>(true)
const tempForm = ref<any>({ name: '', mobile: '', password: '', smsCode: '' })
const seconds = ref(0)
const sendCount = ref(0)
const smsTip = ref('获取验证码')
const onCountDown = (num = 60) => {
  if (seconds.value > 0) return
  const mobile = tempForm.value.mobile
  if (!mobile || mobile == null) {
    ElMessage.error(`请输入手机号！`)
    return
  }

  if (!verifyPhone(mobile)) {
    ElMessage.error(`手机号格式不正确！`)
    return
  }

  seconds.value = num
  sendCount.value++
  const timer = setInterval(() => {
    if (seconds.value < 1) {
      if (sendCount.value > 0) smsTip.value = '重新获取验证码'
      else smsTip.value = '获取验证码'
      clearInterval(timer)
    } else {
      seconds.value--
      smsTip.value = `${seconds.value} 秒`
    }
  }, 1000)
}

const rules: FormRules = {
  name: [required],
  mobile: [required, checkVerifyPhone],
  password: [required],
  smsCode: [required]
}

const loading = ref(false)
const elFormRef = ref()
const loginRegister = async () => {
  try {
    const { name, mobile, password, smsCode } = tempForm.value
    if (!name || name == null) {
      ElMessage.error(`请输入用户名称`)
      return
    }
    if (!mobile || mobile == null) {
      ElMessage.error(`请输入手机号！`)
      return
    }
    if (!verifyPhone(mobile)) {
      ElMessage.error(`手机号格式不正确！`)
      return
    }
    if (!smsCode || smsCode == null) {
      ElMessage.error('请输入验证码！')
      return
    }
    if (!password || password == null) {
      ElMessage.error('请输入密码！')
      return
    }
    if (password.length < 6) {
      ElMessage.error('长度不能小于6位！')
      return
    }
    if (password.length > 20) {
      ElMessage.error('长度不能大于20位！')
      return
    }
    loading.value = true
    userStore.setRegister(tempForm.value).then((res: any) => {
      if (res) {
        ElMessage.success(`注册成功！`)
        showRegister.value = false
      }
    })
  } finally {
    loading.value = false
  }
}

import { EventsConfigs } from '@/app/hooks/event/event'
import { useStorage } from '@/app/hooks/web/useStorage'
const wsStorage = useStorage()
const platInfo = computed(() => {
  let _platInfo = wsStorage.getStorage(EventsConfigs.wsStorage.user.platform)
  if (!!_platInfo && _platInfo != null) {
    userStore.setPlatInfo()
    _platInfo = wsStorage.getStorage(EventsConfigs.wsStorage.user.platform)
  }
  return _platInfo
})
</script>

<template>
  <div class="w-[100%">
    <el-form
      v-if="showRegister"
      ref="elFormRef"
      v-model="tempForm"
      label-position="top"
      hide-required-asterisk
      size="large"
      :rules="rules"
      class="dark:(border-1 border-[var(--el-border-color)] border-solid) w-[100%] rounded-lg bg-white dark:bg-[var(--el-bg-color)]"
    >
      <el-form-item label-width="8px">
        <h2 class="text-4xl font-bold text-center w-[100%]">{{ t('login.register') }}</h2>
      </el-form-item>
      <el-form-item label="用户名称">
        <el-input
          v-model="tempForm.name"
          type="text"
          placeholder="请输入用户名称"
          :maxlength="50"
          @keyup.enter="loginRegister()"
        />
      </el-form-item>
      <el-form-item label="手机号">
        <el-input
          v-model="tempForm.mobile"
          placeholder="请输入手机号"
          :maxlength="20"
          @keyup.enter="loginRegister()"
        />
      </el-form-item>
      <el-form-item :label="t('login.code')">
        <div class="codeArea">
          <el-input
            v-model="tempForm.smsCode"
            :loading="loading"
            :maxlength="4"
            :placeholder="t('login.codePlaceholder')"
            auto-complete="off"
            @keyup.enter="loginRegister()"
          />
          <ElButton :disabled="sendCount > 0" class="img-verify" @click="onCountDown()">
            {{ smsTip }}
          </ElButton>
        </div>
      </el-form-item>
      <el-form-item :label="t('login.password')">
        <el-input
          v-model="tempForm.password"
          type="password"
          show-password
          :placeholder="t('login.passwordPlaceholder')"
          :maxlength="20"
          @keyup.enter="loginRegister()"
        />
      </el-form-item>
      <el-form-item prop="register" label-width="0">
        <div class="w-[100%]">
          <ElButton type="primary" class="w-[100%]" :loading="loading" @click="loginRegister">
            {{ t('login.register') }}
          </ElButton>
        </div>
        <div class="w-[100%] mt-15px">
          <ElButton class="w-[100%]" @click="toLogin"> {{ t('login.hasUser') }} </ElButton>
        </div>
      </el-form-item>
    </el-form>
    <div v-else class="dark:(border-1 border-[var(--el-border-color)] border-solid) w-[100%]">
      <el-result
        icon="success"
        :title="`${
          !!tempForm.name && tempForm.name != null && !!tempForm.mobile && tempForm.mobile != null
            ? `${tempForm.name}的${tempForm.mobile}，`
            : ''
        }注册成功！`"
        sub-title="请等待平台人员联系"
      >
        <template #extra>
          <div v-if="platInfo" class="mb-20px">
            <div style="font-size: 14px; font-weight: bold" class="mb-10px">平台客服</div>
            <p v-for="(service, idx) in platInfo.serviceJson" :key="idx">
              {{ service.phone }}
              &emsp;&emsp;
              {{ service.name }}
            </p>
          </div>
          <el-button type="primary" @click="toLogin()">返回</el-button>
        </template>
      </el-result>
    </div>
  </div>
</template>

<style lang="less" scoped>
:deep(.anticon) {
  &:hover {
    color: var(--el-color-primary) !important;
  }
}

.codeArea {
  display: inline-flex;
  width: 100%;

  .el-input {
    width: calc(100% - 120px);
  }

  .img-verify {
    width: 140px;
  }
}
</style>
