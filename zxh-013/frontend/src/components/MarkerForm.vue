<template>
  <div class="panel">
    <h3>添加标记</h3>
    <div v-if="!position" class="hint">在地图上点击选择位置</div>
    <template v-else>
      <div class="field">
        <label>坐标</label>
        <span>{{ position.lat.toFixed(5) }}, {{ position.lng.toFixed(5) }}</span>
      </div>
      <div class="field">
        <label>类别</label>
        <select v-model="form.category">
          <option value="traffic_jam">经常堵车点</option>
          <option value="accident">事故高发点</option>
          <option value="hot_zone">乘客叫车热区</option>
          <option value="police">交警常驻点</option>
          <option value="toilet">厕所位置</option>
          <option value="gas_station">便宜加油站</option>
          <option value="other">其他</option>
        </select>
      </div>
      <div class="field">
        <label>标题</label>
        <input v-model="form.title" maxlength="128" placeholder="简短描述" />
      </div>
      <div class="field">
        <label>描述</label>
        <textarea v-model="form.description" maxlength="512" rows="3" placeholder="补充说明（可选）"></textarea>
      </div>
      <button class="btn-primary" @click="submit" :disabled="!form.title">提交标记</button>
      <p v-if="error" class="error">{{ error }}</p>
    </template>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { api } from '../services/api.js'

const props = defineProps({ position: Object })
const emit = defineEmits(['created'])

const form = reactive({ category: 'traffic_jam', title: '', description: '' })
const error = ref('')

async function submit() {
  error.value = ''
  try {
    await api.createMarker({
      category: form.category,
      title: form.title,
      description: form.description,
      latitude: props.position.lat,
      longitude: props.position.lng,
    })
    form.title = ''
    form.description = ''
    emit('created')
  } catch (e) { error.value = e.message }
}
</script>
