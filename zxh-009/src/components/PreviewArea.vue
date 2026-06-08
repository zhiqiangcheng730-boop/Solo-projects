<template>
  <div class="preview-area">
    <div class="preview-header">
      <h2 class="section-title">实时预览</h2>
      <button
        v-if="fonts.length > 0 && text"
        class="fav-btn"
        @click="$emit('save-favorite')"
      >
        ⭐ 收藏这个搭配
      </button>
    </div>
    <textarea
      v-model="localText"
      placeholder="输入自定义文字，实时预览字体效果..."
      class="text-input"
      rows="3"
    />
    <div v-if="!fonts.length" class="empty-hint">
      选择心情后，在此输入文字查看效果
    </div>
    <div
      v-for="font in fonts"
      :key="font.family"
      class="preview-card"
      :style="{ fontFamily: `'${font.family}', ${font.fallback}` }"
    >
      <div class="preview-meta">
        <span class="preview-font-name">{{ font.label }}</span>
        <span class="preview-font-css">font-family: '{{ font.family }}', {{ font.fallback }};</span>
      </div>
      <div class="preview-text">
        {{ text || '你好，Hello World!' }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  text: { type: String, default: '' },
  fonts: { type: Array, default: () => [] },
})

const emit = defineEmits(['update:text', 'save-favorite'])

const localText = ref(props.text)

watch(localText, (val) => emit('update:text', val))
watch(() => props.text, (val) => { localText.value = val })
</script>

<style scoped>
.section-title {
  font-size: 1rem;
  color: #555;
  margin: 0;
  font-weight: 600;
}
.preview-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}
.fav-btn {
  padding: 6px 14px;
  border: 1px solid #f0c040;
  border-radius: 8px;
  background: #fffdf0;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s;
}
.fav-btn:hover { background: #fff8d0; border-color: #e0b030; }
.text-input {
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 1rem;
  resize: vertical;
  box-sizing: border-box;
  outline: none;
  transition: border-color 0.2s;
  margin-bottom: 12px;
}
.text-input:focus { border-color: #4361ee; }
.empty-hint {
  color: #bbb;
  text-align: center;
  padding: 40px 0;
  font-size: 0.9rem;
}
.preview-card {
  background: #fff;
  border: 1px solid #eee;
  border-radius: 10px;
  padding: 14px 16px;
  margin-bottom: 10px;
}
.preview-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-family: system-ui, sans-serif;
}
.preview-font-name {
  font-weight: 600;
  font-size: 0.8rem;
  color: #4361ee;
}
.preview-font-css {
  font-size: 0.7rem;
  color: #aaa;
  max-width: 60%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.preview-text {
  font-size: 1.8rem;
  line-height: 1.5;
  word-break: break-all;
}
</style>
