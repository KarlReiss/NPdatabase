import { dateUtil } from '@/app/utils/dateUtil'
import { reactive, toRefs } from 'vue'
import { tryOnMounted, tryOnUnmounted } from '@vueuse/core'

export const useNow = (immediate = true) => {
  let timer: IntervalHandle

  const state = reactive({
    year: 0,
    month: '',
    day: '',
    week: '',
    hour: '',
    minute: '',
    second: '',
    meridiem: ''
  })

  const update = () => {
    const now = dateUtil()

    const h = now.format('HH')
    const m = now.format('mm')
    const s = now.get('s').toString()

    state.year = now.get('y')
    state.month = Number(now.get('M') + 1) < 10 ? `0${now.get('M') + 1}` : `${now.get('M') + 1}`
    state.day = Number(now.get('date')) < 10 ? `0${now.get('date')}` : `${now.get('date')}`
    state.week = '星期' + ['日', '一', '二', '三', '四', '五', '六'][now.day()]
    state.hour = Number(h) < 10 ? `0${Number(h)}` : h
    state.minute = Number(m) < 10 ? `0${Number(m)}` : m
    state.second = Number(s) < 10 ? `0${Number(s)}` : s

    state.meridiem = now.format('A')
  }

  function start() {
    update()
    clearInterval(timer)
    timer = setInterval(() => update(), 1000)
  }

  function stop() {
    clearInterval(timer)
  }

  tryOnMounted(() => {
    immediate && start()
  })

  tryOnUnmounted(() => {
    stop()
  })

  return {
    ...toRefs(state),
    start,
    stop
  }
}
