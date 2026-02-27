<template>
  <div class="img-verify" @click="handleDraw">
    <canvas ref="verifyRef" :id="defaultId" :width="width" :height="height"></canvas>
  </div>
</template>

<script setup lang="ts">
import { toAnyString, getRandomString } from '@/app/utils'
import { ElMessage } from 'element-plus'
import { computed, onMounted, ref, reactive } from 'vue'

const defaultId = computed(() => {
  return `vue-canvas-${getRandomString(8)}-${toAnyString()}`
})

const width = ref(150)
const height = ref(40)
const verifyRef = ref()
const emit = defineEmits(['change'])
const checkCode = ref<any>('') // 图片验证码的值
const expressValue = ref<any>('') // 表达式的值
// canvas各种设置
const cvs = reactive<any>({
  w: 150, // 给出默认宽度  宽度会在图片绘制时根据长度更改
  h: 40, // 高 与input保持一致
  fontSize: 20, // 字体大小
  str: '+-*', // 符号生成范围
  line: 3 // 噪音线个数
})

onMounted(() => {
  handleDraw()
})
// 点击图片重新绘制
const handleDraw = () => {
  // verifyRef.value = ref<any>();
  const boo = Boolean(Math.round(Math.random()))
  if (boo) {
    drawImageCode()
  } else {
    drawExpression()
  }
}
// 随机整数生成器，范围[0, max)
const rInt = (max) => {
  return Math.floor((Math.random() * 100000) % max)
}
// 生成随机表达式
const rCode = () => {
  const a = rInt(118)
  const b = rInt(18)
  const op = cvs.str.charAt(rInt(cvs.str.length))
  // 表达式
  const code = `${a}${op}${b}=`
  checkCode.value = code
  // 表达式的值
  expressValue.value = eval(code.slice(0, code.length - 1))
  emit('change', { code: expressValue.value, type: 'expression' })

  return code
}
// 生成随机颜色 rgba格式
const rColor = () => {
  const a = ((Math.random() * 5 + 5) / 10).toFixed(2)
  return `rgba(${rInt(256)}, ${rInt(256)}, ${rInt(256)}, ${a})`
}
// 验证码图片绘制
const drawExpression = () => {
  const domCvs = verifyRef.value
  // 随机表达式
  const checkCode = rCode()
  // 宽设置
  cvs.w = 10 + cvs.fontSize * checkCode.length

  // 判断是否支持canvas
  if (domCvs !== null && domCvs.getContext && domCvs.getContext('2d')) {
    // 设置显示区域大小
    domCvs.style.width = cvs.w
    // 设置画板宽高
    domCvs.setAttribute('width', cvs.w)
    domCvs.setAttribute('height', cvs.h + 20)
    // 画笔
    const ctx = domCvs.getContext('2d')
    // 背景: 颜色  区域
    ctx.fillStyle = '#eee'
    ctx.fillRect(0, 0, cvs.w, cvs.h + 20)
    // 水平线位置
    ctx.textBaseline = 'middle' // top middle bottom
    // 内容
    for (let i = 0; i < checkCode.length; i++) {
      ctx.fillStyle = rColor() // 随机颜色
      ctx.font = `bold ${cvs.fontSize}px 微软雅黑` // 字体设置
      // 字符绘制: (字符, X坐标, Y坐标)
      ctx.fillText(checkCode.charAt(i), 5 + cvs.fontSize * i, 30 + rInt(10))
    }
    // 噪音线
    for (let i = 0; i < cvs.line; i++) {
      // 起点
      ctx.moveTo(rInt(cvs.w), rInt(cvs.h) + 10)
      // 终点
      ctx.lineTo(rInt(cvs.w), rInt(cvs.h) + 10)
      // 颜色
      ctx.strokeStyle = rColor()
      // 粗细
      ctx.lineWidth = '1'
      // 绘制
      ctx.stroke()
    }
  } else {
    ElMessage.error('不支持验证码格式，请升级或更换浏览器重试')
  }
}

// 1.随机数
const randomNum = (min: number = 0, max: number = 255) => {
  const Range = Math.abs(max - min)
  const Rand = Math.random()
  return min + Math.round(Rand * Range)
}
// 2.随机颜色
const randomColor = (min: number, max: number) => {
  const r = randomNum(min, max)
  const g = randomNum(min, max)
  const b = randomNum(min, max)
  return `rgb(${r},${g},${b})`
}
// 绘制图片
const drawImageCode = () => {
  const domCvs = verifyRef.value
  // 随机表达式
  // let checkCode = rCode();
  // 宽设置
  // cvs.w = cvs.fontSize * checkCode.length;

  // 判断是否支持canvas
  if (domCvs !== null && domCvs.getContext && domCvs.getContext('2d')) {
    // 画笔
    const ctx = domCvs.getContext('2d')
    // 水平线位置
    ctx.textBaseline = 'middle' // top middle bottom
    // 背景: 颜色  区域
    ctx.fillStyle = randomColor(180, 230)
    // 填充的位置
    ctx.fillRect(0, 0, cvs.w, cvs.h)
    // ctx.fillRect(0, 0, width, height)
    // ctx.clearRect(0, 0, verifyRef.value.width, verifyRef.value.height);
    // 定义paramText
    let imgCode = ''
    // 4.随机产生字符串，并且随机旋转
    for (let i = 0; i < 4; i++) {
      // 随机的四个字
      const text = getRandomString(1)
      imgCode += text
      // 随机的字体大小
      const fontSize = randomNum(24, 30)
      // 字体随机的旋转角度
      const deg = randomNum(-30, 30)
      /*
       * 绘制文字并让四个文字在不同的位置显示的思路 :
       * 1、定义字体
       * 2、定义对齐方式
       * 3、填充不同的颜色
       * 4、保存当前的状态（以防止以上的状态受影响）
       * 5、平移translate()
       * 6、旋转 rotate()
       * 7、填充文字
       * 8、restore出栈
       * */
      ctx.font = `bold ${fontSize}px 微软雅黑` // 字体设置
      ctx.textBaseline = 'top'
      ctx.fillStyle = randomColor(80, 150) // 随机颜色
      /*
       * save() 方法把当前状态的一份拷贝压入到一个保存图像状态的栈中。
       * 这就允许您临时地改变图像状态，
       * 然后，通过调用 restore() 来恢复以前的值。
       * save是入栈，restore是出栈。
       * 用来保存Canvas的状态。save之后，可以调用Canvas的平移、放缩、旋转、错切、裁剪等操作。 restore：用来恢复Canvas之前保存的状态。防止save后对Canvas执行的操作对后续的绘制有影响。
       *
       * */
      ctx.save()
      ctx.translate(30 * i + 15, 15)
      ctx.rotate((deg * Math.PI) / 180)
      // fillText() 方法在画布上绘制填色的文本。文本的默认颜色是黑色。
      // 请使用 font 属性来定义字体和字号，并使用 fillStyle 属性以另一种颜色/渐变来渲染文本。
      // ctx.fillText(text,x,y,maxWidth);
      ctx.fillText(text, 5, -5)
      ctx.restore()
    }
    // 5.随机产生5条干扰线,干扰线的颜色要浅一点
    for (let i = 0; i < 5; i++) {
      ctx.beginPath()
      ctx.moveTo(randomNum(0, width.value), randomNum(0, height.value))
      ctx.lineTo(randomNum(0, width.value), randomNum(0, height.value))
      ctx.strokeStyle = randomColor(180, 230)
      ctx.closePath()
      ctx.stroke()
    }
    // 6.随机产生40个干扰的小点
    for (let i = 0; i < 55; i++) {
      ctx.beginPath()
      ctx.arc(randomNum(0, width.value), randomNum(0, height.value), 1, 0, 2 * Math.PI)
      ctx.closePath()
      ctx.fillStyle = randomColor(150, 200)
      // ctx.fillStyle = rColor();
      ctx.fill()
    }
    // 将生成的四个字传递给父组件
    emit('change', { code: imgCode.toUpperCase(), type: 'image_code' })
  } else {
    ElMessage.error('不支持验证码格式，请升级或更换浏览器重试')
  }
}

defineExpose({
  handleDraw
})
</script>
<style lang="less">
.img-verify {
  width: 100px;
  height: 40px;
  margin-left: 20px;
  border-radius: 5px;

  canvas {
    width: 100px;
    height: 40px;
    cursor: pointer;
    // border:1px solid #f5f5f5cc;
    border-radius: 5px;
  }
}
</style>
