<template>
  <div class="mood-selector">
    <h2 class="section-title">选择你的心情</h2>
    <div class="mood-grid">
      <button
        v-for="mood in moods"
        :key="mood.id"
        :class="['mood-btn', { active: mood.id === selectedMood }]"
        @click="$emit('select', mood.id)"
      >
        <span class="mood-emoji">{{ mood.emoji }}</span>
        <span class="mood-label">{{ mood.label }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  moods: { type: Array, required: true },
  selectedMood: { type: String, default: null },
})

defineEmits(['select'])
</script>

<style scoped>
.section-title {
  font-size: 1rem;
  color: #555;
  margin: 0 0 12px;
  font-weight: 600;
}
.mood-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}
.mood-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 14px 8px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  background: #fff;
  cursor: pointer;
  transition: all 0.2s;
}
.mood-btn:hover { border-color: #a0c4ff; background: #f5f9ff; }
.mood-btn.active {
  border-color: #4361ee;
  background: #eef2ff;
  box-shadow: 0 2px 8px rgba(67, 97, 238, 0.2);
}
.mood-emoji { font-size: 1.8rem; }
.mood-label { font-size: 0.85rem; color: #666; }
</style>
