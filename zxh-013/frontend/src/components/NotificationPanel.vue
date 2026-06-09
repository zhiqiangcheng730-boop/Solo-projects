<template>
  <div class="panel">
    <h3>站内通知</h3>
    <button class="btn-primary" @click="load">刷新通知</button>
    <ul class="notif-list" v-if="notifications.length">
      <li v-for="n in notifications" :key="n.id" class="notif-item">
        <strong>[{{ n.marker_category }}]</strong> {{ n.marker_title }}
        <br><small>{{ formatTime(n.created_at) }}</small>
      </li>
    </ul>
    <p v-else class="hint">暂无新通知。订阅区域后会收到该区域的新标记通知。</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { api } from '../services/api.js'

const notifications = ref([])

function formatTime(ts) {
  return new Date(ts).toLocaleString('zh-CN')
}

async function load() {
  try { notifications.value = await api.getNotifications() }
  catch (e) { console.error(e) }
}

load()
</script>

<style scoped>
.notif-list { list-style: none; padding: 0; }
.notif-item { padding: 8px 0; border-bottom: 1px solid #eee; font-size: 13px; }
.notif-item small { color: #999; }
</style>
