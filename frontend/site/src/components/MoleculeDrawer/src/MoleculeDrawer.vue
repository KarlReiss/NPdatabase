<template>
  <div class="molecule-drawer" :class="{ 'has-error': hasError }">
    <!-- 错误状态 -->
    <div v-if="hasError" class="error-container">
      <div class="error-message">
        <i class="error-icon">⚠️</i>
        <p>{{ errorMessage }}</p>
      </div>
      <div class="error-actions">
        <button @click="retryDrawing" class="retry-btn"> <i>🔄</i> 重试 </button>
        <button v-if="lastValidImage" @click="downloadImage" class="download-btn">
          <i>💾</i> 下载上次成功结构
        </button>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-else-if="isLoading" class="loading-container">
      <div class="spinner"></div>
      <p>正在渲染分子结构...</p>
    </div>

    <!-- 渲染区域 -->
    <div v-show="!hasError && !isLoading" class="render-container">
      <div class="canvas-wrapper">
        <div :id="canvasId" ref="canvasRef" class="canvas-container">
          <!-- <canvas
            :id="`${canvasId}-canvas`"
            :canvas-id="`${canvasId}-canvas`"
            :width="props.width"
            :height="props.height"
          ></canvas> -->
        </div>

        <!-- 下载按钮 -->
        <div v-if="isRendered && showBtn" class="action-buttons">
          <button @click="downloadImage" class="action-btn download-action">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 16v1a2 2 0 002 2h12a2 2 0 002-2v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
              />
            </svg>
            下载结构
          </button>
          <!-- <button @click="copyImage" class="action-btn copy-action"> <i>📋</i> 复制结构 </button> -->
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import html2canvas from 'html2canvas'
import { ElMessage } from 'element-plus'

// 组件属性（保持不变）
interface Props {
  smiles?: string
  name?: string
  width?: number
  height?: number
  theme?: 'light' | 'dark'
  backgroundColor?: string
  bondThickness?: number
  showBtn?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  smiles: 'O=C(C=CC1=CC=CC=C1O)C1=CC=CC=C1',
  width: 300,
  height: 300,
  theme: 'light',
  backgroundColor: '#ffffff',
  bondThickness: 1.6,
  showBtn: true
})

// 事件定义（保持不变）
const emit = defineEmits<{
  rendered: [success: boolean]
  download: [imageData: string]
  error: [error: Error]
}>()

// const { isLoading, error, load, cleanup } = useRDKit()

const rdkit = ref<any>(null)

// 响应式数据
const hasError = ref(false)
const isLoading = ref(false)
const isRendered = ref(false)
const errorMessage = ref('')
const lastValidImage = ref<string>('')
const canvasId = ref(`smiles-canvas-${Math.random().toString(36).substr(2, 9)}`)
const canvasRef = ref<HTMLCanvasElement | null>(null)
const canvasEle = ref<HTMLCanvasElement | null>()

// Vue3 组件内实现
const convertWithHtml2Canvas = async (element) => {
  try {
    // 配置选项
    const options = {
      backgroundColor: '#ffffff',
      scale: 1, // 提高清晰度
      useCORS: true, // 处理跨域图片
      logging: false, // 关闭日志
      allowTaint: true, // 允许污染画布
      width: element.offsetWidth,
      height: element.offsetHeight
    }

    // 转换为 canvas
    const canvas = await html2canvas(element, options)

    // 获取 Base64 数据
    const base64Data = canvas.toDataURL('image/png')

    // 下载为 PNG
    const downloadPNG = (
      filename = `SMILES-${new Date()
        .toISOString()
        .replace(/[:.TZ]/g, '-')
        .trim()}.png`
    ) => {
      const link = document.createElement('a')
      link.href = base64Data
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }

    // 转换为 Blob 对象
    const getBlobFromBase64 = (base64Data) => {
      const byteString = atob(base64Data.split(',')[1])
      const mimeString = base64Data.split(',')[0].split(':')[1].split(';')[0]
      const ab = new ArrayBuffer(byteString.length)
      const ia = new Uint8Array(ab)

      for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i)
      }

      return new Blob([ab], { type: mimeString })
    }

    return {
      base64: base64Data,
      canvas: canvas,
      blob: getBlobFromBase64(base64Data),
      download: downloadPNG
    }
  } catch (error) {
    console.error('html2canvas 转换失败:', error)
    throw error
  }
}
// 修复后的绘制函数
const drawSmiles = async () => {
  if (!props.smiles || props.smiles.trim() === '') {
    console.warn('No SMILES string provided')
    isLoading.value = false
    return
  }

  try {
    // 清除之前的状态
    hasError.value = false
    errorMessage.value = ''
    isLoading.value = true
    isRendered.value = false

    // 等待 DOM 更新
    await nextTick()

    if (!rdkit.value) {
      loadRDKit()
      return
    }

    if (canvasRef.value) {
      const mol = rdkit.value.get_mol(props.smiles)
      // const svg = mol.get_svg()
      // if (canvasRef.value) {
      //   canvasRef.value.innerHTML = svg
      // }
      canvasRef.value.innerHTML = ''
      // 创建 canvas 元素
      const canvas = document.createElement('canvas')
      canvas.id = `${canvasId.value}-canvas`
      canvas.width = props.width
      canvas.height = props.height
      canvas.style.backgroundColor = props.backgroundColor
      canvas.style.borderRadius = '4px'
      canvas.style.boxShadow =
        props.theme === 'dark' ? '0 2px 8px rgba(0,0,0,0.3)' : '0 2px 8px rgba(0,0,0,0.1)'

      const mdetails = {
        atoms: [0, 0, 0],
        bondIndices: true,
        explicitMethyl: true,
        addAtomIndices: true,
        addStereoAnnotation: true,
        bondLineWidth: 1,
        legend: props.name
      }
      mol.draw_to_canvas_with_highlights(canvas, JSON.stringify(mdetails))
      canvasEle.value = canvas
      canvasRef.value.appendChild(canvas)

      mol.delete()
    }
    isLoading.value = false
    isRendered.value = true
  } catch (error: any) {
    console.error('SMILES 渲染失败:', error)
    hasError.value = true
    errorMessage.value = error.message || '无法渲染分子结构'
    isLoading.value = false
    isRendered.value = false
    emit('rendered', false)
    emit('error', error)

    // 添加更详细的错误信息
    if (error.message.includes('determineDimensions')) {
      errorMessage.value = '分子结构过于复杂或存在无效的化学键'
    }
  }
}

// 重试绘制
const retryDrawing = () => {
  hasError.value = false
  errorMessage.value = ''
  drawSmiles()
}

// 下载结构
const downloadImage = async () => {
  try {
    const { base64, download } = await convertWithHtml2Canvas(canvasRef.value)
    emit('download', base64)
    download()
  } catch (error) {
    console.error('Download failed:', error)
    ElMessage.error('下载失败')
  }
}

// 复制结构到剪贴板
const copyImage = async () => {
  const canvas = canvasRef.value
  if (!canvas) {
    ElMessage.error('画布不可用')
    return
  }

  try {
    // 转换为 blob
    const { blob } = await convertWithHtml2Canvas(canvas)
    if (!blob) {
      throw new Error('无法创建结构数据')
    }
    try {
      await navigator.clipboard.write([new ClipboardItem({ 'image/png': blob })])
      ElMessage.error('结构已复制到剪贴板')
    } catch (clipboardError) {
      console.error(`Clipboard write failed: ${clipboardError}`)
      // 备用方案：使用 canvas.toDataURL 提示用户手动保存
      ElMessage.error('自动复制失败，请使用下载功能')
    }
  } catch (error: any) {
    console.error('Copy failed:', error)
    ElMessage.error(`复制失败: ${error.message}`)
  }
}

let count = 0
const loadRDKit = () => {
  const { initRDKitModule, RDKit } = window as any
  if (RDKit) {
    rdkit.value = RDKit
    if (props.smiles) {
      drawSmiles()
    }
  } else {
    if (initRDKitModule) {
      initRDKitModule()
        .then(function (_RDKit) {
          console.log('_RDKit version: ' + _RDKit.version())
          rdkit.value = _RDKit
          if (props.smiles) {
            drawSmiles()
          }
        })
        .catch(() => {
          // handle loading errors here...
        })
    } else {
      if (count >= 30) {
        setTimeout(loadRDKit, 2000)
      }
      count++
    }
  }
}

// 监听 SMILES 变化
watch(
  () => props.smiles,
  (newSmiles) => {
    if (newSmiles && newSmiles.trim() !== '') {
      drawSmiles()
    } else {
      // 清除 canvas
      const container = canvasRef.value
      if (container) {
        container.innerHTML = ''
      }
      isRendered.value = false
      lastValidImage.value = ''
      canvasRef.value = null
    }
  },
  { immediate: true }
)

// 监听主题变化
watch(
  () => props.theme,
  () => {
    if (props.smiles && !hasError.value) {
      drawSmiles()
    }
  }
)

// 监听尺寸变化
watch(
  () => [props.width, props.height],
  () => {
    if (props.smiles && !hasError.value) {
      drawSmiles()
    }
  }
)

// 暴露方法给父组件
defineExpose({
  retryDrawing,
  downloadImage,
  copyImage
})
</script>

<style scoped>
.molecule-drawer {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  margin: 1rem 0;
}

.render-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.canvas-wrapper {
  position: relative;
  display: inline-block;
  overflow: hidden;
  width: fit-content;
  border-radius: 4px;
}

.canvas-container {
  display: block;
  transition: transform 0.3s ease;
}

.action-buttons {
  /*
  position: absolute;
  bottom: 12px;
  right: 12px;
  */
  display: flex;
  justify-content: center;
  /*
  justify-content: space-between;
  */
  gap: 8px;
  opacity: 0.7;
  transition: opacity 0.3s ease;
  padding: 8px 8px 12px;
}

.canvas-wrapper:hover .action-buttons {
  opacity: 1;
}

.action-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(4px);
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: all 0.2s ease;
}

.action-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.25);
}

.download-action {
  color: #2196f3;
}

.copy-action {
  color: #4caf50;
}

.smiles-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f5f5f5;
  border-radius: 4px;
  font-size: 14px;
  gap: 1rem;
}

.smiles-display {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.smiles-display code {
  background: #fff;
  padding: 6px 12px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  flex: 1;
  overflow-x: auto;
  white-space: nowrap;
  border: 1px solid #ddd;
}

.controls {
  display: flex;
  gap: 4px;
}

.control-btn {
  padding: 4px 8px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  min-width: 32px;
}

.control-btn:hover {
  background: #f0f0f0;
}

.error-container {
  padding: 2rem;
  text-align: center;
  background: #fff5f5;
  border: 1px solid #fed7d7;
  border-radius: 8px;
}

.error-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-bottom: 1.5rem;
  color: #c53030;
}

.error-icon {
  font-size: 2rem;
}

.error-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.retry-btn,
.download-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
}

.retry-btn {
  background: #4299e1;
  color: white;
}

.download-btn {
  background: #48bb78;
  color: white;
}

.retry-btn:hover {
  background: #3182ce;
}

.download-btn:hover {
  background: #38a169;
}

.loading-container {
  padding: 3rem;
  text-align: center;
  color: #718096;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e2e8f0;
  border-top-color: #4299e1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.has-error .canvas-container {
  opacity: 0.5;
  filter: grayscale(50%);
}
</style>
