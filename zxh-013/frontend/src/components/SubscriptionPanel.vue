<template>
  <div class="panel">
    <h3>区域订阅</h3>
    <div class="field">
      <label>订阅名称</label>
      <input v-model="form.name" placeholder="如：国贸片区" />
    </div>
    <div class="field">
      <label>中心点 (lat, lng)</label>
      <input v-model="centerStr" placeholder="39.9042, 116.4074" />
    </div>
    <div class="field">
      <label>半径 (km)</label>
      <input v-model.number="form.radius_km" type="number" min="0.1" max="100" step="0.5" />
    </div>
    <button class="btn-primary" @click="subscribe">添加订阅</button>
    <p v-if="error" class="error">{{ error }}</p>
    <hr />
    <h4>我的订阅</h4>
    <ul class="sub-list" v-if="subs.length">
      <li v-for="s in subs" :key="s.id" class="sub-item">
        <span>{{ s.name || '未命名' }} ({{ s.radius_km }}km)</span>
        <button class="btn-sm" @click="$emit('focusRegion', { lat: s.center_lat, lng: s.center_lng }, s.radius_km)">定位</button>
        <button class="btn-sm btn-danger" @click="remove(s.id)">删除</button>
      </li>
    </ul>
    <p v-else class="hint">暂无订阅</p>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { api } from '../services/api.js'

defineEmits(['focusRegion'])

const subs = ref([])
const centerStr = ref('')
const error = ref('')
const form = reactive({ name: '', center_lat: 0, center_lng: 0, radius_km: 5 })

async function loadSubs() {
  try { subs.value = await api.getSubscriptions() }
  catch (e) { console.error(e) }
}

function parseCoord(s) {
  const parts = s.split(',').map(Number)
  if (parts.length !== 2 || parts.some(isNaN)) throw new Error('格式: lat, lng')
  return { lat: parts[0], lng: parts[1] }
}

async function subscribe() {
  error.value = ''
  try {
    const center = parseCoord(centerStr.value)
    form.center_lat = center.lat
    form.center_lng = center.lng
    await api.createSubscription({ ...form })
    form.name = ''
    centerStr.value = ''
    await loadSubs()
  } catch (e) { error.value = e.message }
}

async function remove(id) {
  await api.deleteSubscription(id)
  await loadSubs()
}

onMounted(loadSubs)
</script>

<style scoped>
.sub-list { list-style: none; padding: 0; }
.sub-item { display: flex; align-items: center; gap: 6px; padding: 6px 0; border-bottom: 1px solid #eee; font-size: 13px; }
.sub-item span { flex: 1; }
.btn-sm { padding: 2px 8px; font-size: 12px; border: none; border-radius: 3px; cursor: pointer; background: #3498db; color: #fff; }
.btn-danger { background: #e74c3c; }
</style>
