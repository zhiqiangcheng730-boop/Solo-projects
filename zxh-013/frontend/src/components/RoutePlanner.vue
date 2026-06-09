<template>
  <div class="panel">
    <h3>路线优化</h3>
    <div class="field">
      <label>起点 (lat, lng)</label>
      <input v-model="startStr" placeholder="39.9042, 116.4074" />
    </div>
    <div class="field">
      <label>终点 (lat, lng)</label>
      <input v-model="endStr" placeholder="39.9142, 116.4274" />
    </div>
    <button class="btn-primary" @click="search">计算路线</button>
    <p v-if="error" class="error">{{ error }}</p>
    <div v-if="result" class="result">
      <p>绕开了 <strong>{{ result.avoided_markers }}</strong> 个高频堵车/事故/交警点</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { api } from '../services/api.js'

const startStr = ref('39.9042, 116.4074')
const endStr = ref('39.9142, 116.4274')
const result = ref(null)
const error = ref('')

function parseCoord(s) {
  const parts = s.split(',').map(Number)
  if (parts.length !== 2 || parts.some(isNaN)) throw new Error('格式: lat, lng')
  return { lat: parts[0], lng: parts[1] }
}

async function search() {
  error.value = ''
  result.value = null
  try {
    const start = parseCoord(startStr.value)
    const end = parseCoord(endStr.value)
    result.value = await api.optimizeRoute(start, end)
  } catch (e) { error.value = e.message }
}
</script>
