import { verifyEmail, verifyIPAddress, verifyPhone, verifyIntegerNumber } from './toolsValidate'
import { useI18n } from '@/app/hooks/web/useI18n'
const { t } = useI18n()

// 必填项
export const required = {
  required: true,
  message: t('common.required'),
  trigger: ['blur', 'change']
}

// 必填项手机号
export const checkVerifyPhone = {
  required: true,
  validator: (_rule: any, value: any, callback: any) => {
    if (!value) {
      callback(new Error('请输入手机号！'))
      return
    }
    if (!verifyPhone(value)) {
      callback(new Error('手机号格式不正确！'))
      return
    }
    callback()
  },
  trigger: ['blur', 'change']
}

// 必填项 邮箱
export const checkVerifyEmail = {
  required: true,
  validator: (_rule: any, value: any, callback: any) => {
    if (!value) {
      callback(new Error('请输入邮箱'))
      return
    }
    if (!verifyEmail(value)) {
      callback(new Error('邮箱格式不正确！'))
      return
    }
    callback()
  },
  trigger: ['blur', 'change']
}

/**
 * 强密码校验
 * @param rule
 * @param value
 * @param callback
 * @returns
 */
export const passwordValidator = {
  required: true,
  validator: (_rule: any, value: any, callback: any) => {
    if (!value) {
      callback('请输入密码！')
      return
    }

    if (!value) {
      callback(new Error('密码需包含大、小写字母及符号、数字！'))
      return
    }
    if (value.length < 6) {
      callback(new Error('长度不能小于6位！'))
      return
    }
    if (value.length > 20) {
      callback(new Error('长度不能大于20位！'))
      return
    }
    let reg = /\d+/
    if (!reg.test(value)) {
      callback(new Error('密码需要数字！'))
      return
    }
    reg = /[a-z]+/
    if (!reg.test(value)) {
      callback(new Error('密码需要小写字母！'))
      return
    }
    reg = /[A-Z]+/
    if (!reg.test(value)) {
      callback(new Error('密码需要大写字母！'))
      return
    }
    reg = /\W+/
    if (!reg.test(value)) {
      callback(new Error('密码需要特殊字符！'))
      return
    }
    callback()
  },
  trigger: ['blur', 'change']
}

// 必填项 IP地址
export const checkVerifyIPAddress = {
  required: true,
  validator: (_rule: any, value: any, callback: any) => {
    if (!value) {
      callback(new Error('请输入IP地址！'))
      return
    }
    if (!verifyIPAddress(value)) {
      callback(new Error('IP地址格式不正确！'))
      return
    }
    callback()
  },
  trigger: ['blur', 'change']
}
/**
 * 必填项 正整数
 */
export const checkVerifyIntegerNumber = {
  required: true,
  validator: (rule: any, value: any, callback: any) => {
    if (['', null, undefined].includes(value)) {
      callback(new Error('该项为必填项'))
      return
    }
    if (verifyIntegerNumber(value)) {
      callback(new Error('请输入正整数'))
      return
    }
    callback()
  },
  trigger: ['blur', 'focus']
}

/**
 * 必填项 保留两位小数的金额
 */
export const checkVerifyDecimalAmount = {
  required: true,
  validator: (rule: any, value: any, callback: any) => {
    if (['', null, undefined].includes(value)) {
      callback(new Error('该项为必填项'))
      return
    }

    // 金额,只允许2位小数
    if (Number(value) > 0 && !/^[0-9]\d*(,\d{3})*(\.\d{1,2})?$|^0\.\d{1,2}$/.test(value)) {
      callback(new Error('请输入金额,只允许2位小数'))
      return
    }
    callback()
  },
  trigger: ['blur', 'focus']
}
