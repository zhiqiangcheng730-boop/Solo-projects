<template>
  <div class="profile-page">
    <el-card>
      <template #header><h2>个人中心</h2></template>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="用户ID">{{ userId }}</el-descriptions-item>
        <el-descriptions-item label="用户名">灵感改造家</el-descriptions-item>
        <el-descriptions-item label="贡献方案">暂未统计</el-descriptions-item>
        <el-descriptions-item label="获赞总数">暂未统计</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card style="margin-top:16px">
      <template #header><h3>改造统计</h3></template>
      <div ref="chartRef" style="width:100%;height:300px"></div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { useUserStore } from '../stores'

const userStore = useUserStore()
const userId = ref(userStore.userId)
const chartRef = ref(null)

onMounted(() => {
  if (!chartRef.value) return
  const chart = echarts.init(chartRef.value)
  chart.setOption({
    tooltip: { trigger: 'item' },
    legend: { top: 'bottom' },
    series: [{
      name: '旧物分类统计',
      type: 'pie',
      radius: ['40%', '70%'],
      data: [
        { value: 40, name: '衣物' },
        { value: 30, name: '家具' },
        { value: 20, name: '电子' },
        { value: 10, name: '包装' },
      ],
      emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0,0,0,0.5)' } },
    }],
  })
})
</script>

<style scoped>
.profile-page { max-width: 800px; margin: 0 auto; }
</style>
