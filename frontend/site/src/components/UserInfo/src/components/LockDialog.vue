<script setup lang="ts">
import { useValidator } from '@/app/hooks/web/useValidator'
import { useDesign } from '@/app/hooks/web/useDesign'
import { useLockStore } from '@/store/modules/lock'
import { useUserStore } from '@/store/modules/user'
import { useI18n } from '@/app/hooks/web/useI18n'
import { Dialog } from '@/components/Dialog'
import { reactive, computed } from 'vue'
import { ref, watch } from 'vue'

const { getPrefixCls } = useDesign()
const prefixCls = getPrefixCls('lock-dialog')

const { required } = useValidator()

const { t } = useI18n()

const lockStore = useLockStore()
const userStore = useUserStore()

const props = defineProps({
  modelValue: {
    type: Boolean
  }
})

const emit = defineEmits(['update:modelValue'])

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (val) => {
    emit('update:modelValue', val)
  }
})

const tempForm = reactive<any>({
  password: ''
})

const elFormRef = ref()
const apasswordRef = ref()

//  自动聚焦输入框
watch(
  dialogVisible,
  async (val) => {
    if (val) {
      const formExposeInput = apasswordRef.value
      setTimeout(() => {
        formExposeInput?.focus()
      }, 10)
    }
  },
  { immediate: true }
)

const dialogTitle = ref(t('lock.lockScreen'))

const rules = reactive({
  password: [required()]
})

const handleLock = async () => {
  const formExpose = elFormRef.value
  await formExpose?.validate((valid) => {
    if (valid) {
      dialogVisible.value = false
      lockStore.setLockInfo({
        isLock: true,
        ...tempForm
      })
    }
  })
}
</script>

<template>
  <Dialog
    v-model="dialogVisible"
    width="500px"
    max-height="220px"
    :class="prefixCls"
    :title="dialogTitle"
    append-to-body
  >
    <div class="flex flex-col items-center">
      <img
        :src="'https://picsum.photos/64/64' || '@/assets/imgs/avatar.jpg'"
        alt=""
        class="w-70px h-70px rounded-[50%]"
      />
      <span class="text-14px my-10px text-[var(--top-header-text-color)]">
        {{ 'Dr. Research' || userStore.getUserInfo?.username }}
      </span>
    </div>
    <el-form
      ref="elFormRef"
      :rules="rules"
      label-position="top"
      :model="tempForm"
      hide-required-asterisk
      size="large"
      class="dark:(border-1 border-[var(--el-border-color)] border-solid) w-[100%] rounded-lg bg-white dark:bg-[var(--el-bg-color)]"
    >
      <el-form-item :label="t('lock.lockPassword')">
        <!-- show-password -->
        <el-input
          ref="passwordRef"
          type="text"
          name="password"
          autofocus
          maxlength="20"
          placeholder="请输入密码"
          v-model="tempForm.password"
          @keyup.enter="handleLock()"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <BaseButton type="primary" @click="handleLock">{{ t('lock.lock') }}</BaseButton>
    </template>
  </Dialog>
</template>

<style lang="less" scoped>
:global(.v-lock-dialog) {
  @media (width <= 767px) {
    max-width: calc(100vw - 16px);
  }
}
</style>
