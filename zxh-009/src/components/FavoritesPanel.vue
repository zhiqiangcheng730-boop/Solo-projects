<template>
  <div class="favorites-panel">
    <h2 class="section-title">我的收藏 ({{ favorites.length }})</h2>
    <div v-if="favorites.length === 0" class="empty-hint">还没有收藏，快去搭配吧</div>
    <div v-for="item in favorites" :key="item.id" class="fav-card">
      <div class="fav-header">
        <span class="fav-mood">{{ item.moodEmoji }} {{ item.moodLabel }}</span>
        <button class="del-btn" @click="$emit('remove', item.id)">✕</button>
      </div>
      <div class="fav-text">{{ item.text }}</div>
      <div class="fav-fonts">
        <span v-for="font in item.fonts" :key="font.family" class="fav-font-tag">
          {{ font.label }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  favorites: { type: Array, default: () => [] },
})

defineEmits(['remove'])
</script>

<style scoped>
.section-title {
  font-size: 1rem;
  color: #555;
  margin: 0 0 12px;
  font-weight: 600;
}
.empty-hint {
  color: #bbb;
  font-size: 0.85rem;
  padding: 8px 0;
}
.fav-card {
  background: #fafafa;
  border: 1px solid #eee;
  border-radius: 10px;
  padding: 12px;
  margin-bottom: 10px;
}
.fav-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
}
.fav-mood { font-weight: 600; font-size: 0.9rem; }
.del-btn {
  border: none;
  background: none;
  cursor: pointer;
  color: #ccc;
  font-size: 0.9rem;
  padding: 2px 6px;
  border-radius: 4px;
  transition: all 0.2s;
}
.del-btn:hover { color: #e74c3c; background: #fdeaea; }
.fav-text {
  font-size: 0.95rem;
  color: #444;
  margin-bottom: 8px;
  padding: 8px;
  background: #fff;
  border-radius: 6px;
}
.fav-fonts { display: flex; gap: 6px; flex-wrap: wrap; }
.fav-font-tag {
  font-size: 0.7rem;
  padding: 2px 8px;
  background: #eef2ff;
  color: #4361ee;
  border-radius: 10px;
}
</style>
