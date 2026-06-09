<template>
  <div class="space-y-4">
    <div class="bg-white rounded-2xl shadow-lg p-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-semibold text-gray-800">听懂区域分布热力图</h2>
        <button @click="markUnderstood" :disabled="!props.recordingId"
          class="px-4 py-2 bg-green-600 text-white rounded-lg text-sm font-medium hover:bg-green-700 disabled:opacity-50 transition">
          标记我听懂了
        </button>
      </div>
      <div ref="chartRef" class="w-full" style="height: 520px"></div>
    </div>

    <!-- Mark dialog -->
    <Teleport to="body">
      <div v-if="showMarkDialog" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50" @click.self="showMarkDialog = false">
        <div class="bg-white rounded-xl p-6 w-96 shadow-2xl">
          <h3 class="text-lg font-semibold mb-4">标记听懂状态</h3>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-600 mb-1">你所在的省份</label>
            <select v-model="markProvince" class="w-full px-3 py-2 border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-orange-400">
              <option value="">请选择</option>
              <option v-for="p in provinces" :key="p" :value="p">{{ p }}</option>
            </select>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-600 mb-1">听懂程度</label>
            <div class="flex gap-3">
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="radio" v-model="markUnderstoodValue" :value="true" class="text-green-600" />
                <span class="text-sm">听懂了</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="radio" v-model="markUnderstoodValue" :value="false" class="text-red-600" />
                <span class="text-sm">没听懂</span>
              </label>
            </div>
          </div>
          <div class="flex gap-3">
            <button @click="submitMark" :disabled="!markProvince"
              class="flex-1 py-2 bg-orange-600 text-white rounded-lg text-sm font-medium hover:bg-orange-700 disabled:opacity-50">
              提交
            </button>
            <button @click="showMarkDialog = false" class="px-4 py-2 border border-gray-300 rounded-lg text-sm">
              取消
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick, onUnmounted } from 'vue'
import { useApi } from '../composables/useApi'
import { useMap } from '../composables/useMap'

const props = defineProps({ recordingId: { type: Number, default: 0 } })
const { get, post } = useApi()
const { buildHeatmapData, CHINA_PROVINCE_COORDS } = useMap()

const chartRef = ref(null)
let chartInstance = null
const provinces = Object.keys(CHINA_PROVINCE_COORDS)
const showMarkDialog = ref(false)
const markProvince = ref('')
const markUnderstoodValue = ref(true)

function markUnderstood() {
  showMarkDialog.value = true
  markProvince.value = ''
}

async function submitMark() {
  if (!props.recordingId || !markProvince.value) return
  await post('/understanding/', {
    recording_id: props.recordingId,
    province: markProvince.value,
    understood: markUnderstoodValue.value,
  })
  showMarkDialog.value = false
  fetchHeatmap()
}

async function fetchHeatmap() {
  const path = props.recordingId ? `/understanding/heatmap?recording_id=${props.recordingId}` : '/statistics/heatmap'
  const data = await get(path.startsWith('/api') ? path.replace('/api', '') : path)
  const stats = Array.isArray(data) ? data : []
  renderChart(stats)
}

function renderChart(stats) {
  if (!chartRef.value) return
  if (!chartInstance) {
    chartInstance = echarts.init(chartRef.value)
  }
  const scattered = buildHeatmapData(stats)

  const option = {
    tooltip: {
      formatter: (p) => {
        if (!p.data || !p.data.name) return ''
        const d = p.data
        return `<b>${d.name}</b><br/>总标记: ${d.total ?? 0}<br/>听懂: ${d.understood ?? 0}<br/>听懂率: ${((d.ratio ?? 0) * 100).toFixed(0)}%`
      },
    },
    grid: { top: 20, right: 20, bottom: 20, left: 20 },
    xAxis: { show: false, min: 73, max: 136 },
    yAxis: { show: false, min: 17, max: 54 },
    series: [
      {
        type: 'scatter',
        data: Object.entries(CHINA_PROVINCE_COORDS).map(([name, coord]) => {
          const hit = stats.find(s => s.province && s.province.includes(name)) || stats.find(s => name.includes(s.province))
          return {
            name,
            value: coord,
            symbolSize: hit ? Math.max(hit.total * 3, 12) : 8,
            itemStyle: {
              color: hit ? `rgba(220, 38, 38, ${Math.max(hit.ratio, 0.15)})` : 'rgba(180,180,180,0.4)',
              borderColor: hit && hit.ratio > 0.5 ? '#dc2626' : '#ccc',
              borderWidth: 1,
            },
            total: hit?.total ?? 0,
            understood: hit?.understood ?? 0,
            ratio: hit?.ratio ?? 0,
          }
        }),
        emphasis: { scale: 1.5 },
      },
    ],
  }
  chartInstance.setOption(option)
}

watch(() => props.recordingId, fetchHeatmap)

function handleResize() { chartInstance?.resize() }

onMounted(async () => {
  await nextTick()
  fetchHeatmap()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
})
</script>
