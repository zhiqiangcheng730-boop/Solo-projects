<template>
  <div class="panel">
    <h3>排行榜 - 城市雷达</h3>
    <button class="btn-primary" @click="load">刷新</button>
    <ul class="lb-list" v-if="list.length">
      <li v-for="item in list" :key="item.user_id" class="lb-item">
        <span class="rank">#{{ item.rank }}</span>
        <span class="name">{{ item.nickname || '司机' + item.user_id }}</span>
        <span class="stats">{{ item.score }} 分 / {{ item.marker_count }} 标记</span>
      </li>
    </ul>
    <p v-else class="hint">暂无数据</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { api } from '../services/api.js'

const list = ref([])

async function load() {
  try { list.value = await api.getLeaderboard() }
  catch (e) { console.error(e) }
}

load()
</script>

<style scoped>
.lb-list { list-style: none; padding: 0; }
.lb-item { display: flex; align-items: center; padding: 8px 0; border-bottom: 1px solid #eee; gap: 8px; font-size: 13px; }
.rank { font-weight: bold; color: #e94560; min-width: 30px; }
.name { flex: 1; }
.stats { color: #888; font-size: 12px; }
</style>
