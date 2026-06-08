<template>
  <div class="font-list">
    <h2 class="section-title">推荐字体</h2>
    <div v-if="loading" class="loading-hint">字体加载中...</div>
    <div v-else-if="fonts.length === 0" class="empty-hint">请先选择心情</div>
    <ul v-else class="font-items">
      <li v-for="font in fonts" :key="font.family" class="font-item">
        <div class="font-info">
          <span class="font-name">{{ font.label }}</span>
          <span class="font-tag">{{ font.tag }}</span>
        </div>
        <button
          :class="['copy-btn', { copied: copiedId === font.family }]"
          @click="$emit('copy-css', font)"
        >
          {{ copiedId === font.family ? '已复制 ✓' : '复制 CSS' }}
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  fonts: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  copiedId: { type: String, default: null },
})

defineEmits(['copy-css'])
</script>

<style scoped>
.section-title {
  font-size: 1rem;
  color: #555;
  margin: 0 0 12px;
  font-weight: 600;
}
.loading-hint, .empty-hint {
  color: #999;
  font-size: 0.85rem;
  padding: 8px 0;
}
.font-items {
  list-style: none;
  margin: 0;
  padding: 0;
}
.font-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  border-radius: 8px;
  background: #fafafa;
  margin-bottom: 8px;
}
.font-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.font-name {
  font-weight: 600;
  font-size: 0.9rem;
}
.font-tag {
  font-size: 0.75rem;
  color: #888;
}
.copy-btn {
  padding: 5px 12px;
  border: 1px solid #d0d0d0;
  border-radius: 6px;
  background: #fff;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.2s;
  white-space: nowrap;
}
.copy-btn:hover { border-color: #4361ee; color: #4361ee; }
.copy-btn.copied { border-color: #2ecc71; color: #2ecc71; background: #f0faf4; }
</style>
