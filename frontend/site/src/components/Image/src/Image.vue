<script lang="tsx">
import { defineComponent, PropType, ref, computed, unref, withModifiers } from 'vue'
import { propTypes } from '@/app/utils/propTypes'
import { isNumber } from '@/app/utils/is'
import { ElMessage, ElImage } from 'element-plus'
import { Picture as IconPicture } from '@element-plus/icons-vue'
import { isStringArray } from '@/app/utils/is'
export default defineComponent({
  name: 'Image',
  props: {
    width: propTypes.oneOfType([Number, String]).def('30px'),
    height: propTypes.oneOfType([Number, String]).def('30px'),
    isError: propTypes.bool.def(false),
    isPreview: propTypes.bool.def(true),
    src: propTypes.any.def('')
  },
  setup(props) {
    const imageStyle = computed(() => {
      return `
        width: ${
          isNumber(props.width)
            ? `${props.width}px`
            : props.width.indexOf('px') > -1
              ? props.width
              : `${props.width}px`
        };
        height: ${
          isNumber(props.height)
            ? `${props.height}px`
            : props.height.indexOf('px') > -1
              ? props.height
              : `${props.height}px`
        }
      `
    })

    const imgs = computed(() => {
      const modelValue = props.src
      switch (typeof modelValue) {
        case 'string':
          if (modelValue.indexOf('http') == -1) {
            return []
          } else {
            if (isStringArray(modelValue)) {
              return JSON.parse(modelValue).map((ysr: any) => ysr.url || ysr.path || ysr.src || ysr)
            } else if (modelValue.indexOf(',') > -1) {
              return modelValue.split(',').map((img: any) => img)
            } else {
              return [modelValue]
            }
          }
        case 'object':
          return modelValue.map((ysr: any) => ysr.url || ysr.path || ysr.src || ysr)
        case 'number':
        case 'boolean':
        case 'undefined':
        case 'function':
          return []
        default:
          return []
      }
    })

    return () =>
      unref(imgs).length > 0 ? (
        props.isPreview ? (
          unref(imgs).map((img: any) => {
            return (
              <ElImage
                src={img}
                style={unref(imageStyle)}
                class={unref(imgs).length > 1 ? 'mr-6px mt-6px' : ''}
                preview-src-list={unref(imgs)}
                preview-teleported
                fit="cover"
                onClick={withModifiers(() => {
                  console.log('点击了图片')
                }, ['stop'])}
              />
            )
          })
        ) : (
          unref(imgs).map((img: any) => {
            return (
              <ElImage
                src={img}
                style={unref(imageStyle)}
                class={unref(imgs).length > 1 ? 'mr-6px mt-6px' : ''}
                fit="cover"
              />
            )
          })
        )
      ) : props.isError ? (
        <div class="flex items-center justify-center h-full">
          <el-icon size="30" class="text-gray-300">
            <icon-picture />
          </el-icon>
        </div>
      ) : (
        ''
      )
  }
})
</script>
