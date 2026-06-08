<script setup>
const props = defineProps({
  item: { type: Object, required: true },
})

const emit = defineEmits(['close', 'delete'])
</script>

<template>
  <div class="overlay" @click.self="emit('close')">
    <div class="viewer">
      <button class="close-btn" @click="emit('close')" title="关闭">×</button>
      <div class="compare">
        <div class="compare-pane">
          <h3 class="pane-title">原图</h3>
          <img :src="item.original" alt="原图" class="compare-img" />
        </div>
        <div class="compare-pane">
          <h3 class="pane-title">剪影</h3>
          <img :src="item.shadow" alt="剪影" class="compare-img" />
        </div>
      </div>
      <div class="viewer-meta">
        <span>阈值：{{ item.threshold }}</span>
        <button class="btn delete-btn-lg" @click="emit('delete', item.id)">删除此影子</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.viewer {
  position: relative;
  background: #111;
  border: 1px solid #333;
  border-radius: 8px;
  padding: 32px;
  max-width: 90vw;
  max-height: 90vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.close-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 32px;
  height: 32px;
  border: none;
  background: none;
  color: #999;
  font-size: 24px;
  cursor: pointer;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.close-btn:hover {
  color: #fff;
  background: #333;
}
.compare {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
  justify-content: center;
}
.compare-pane {
  flex: 1;
  min-width: 200px;
  max-width: 420px;
  text-align: center;
}
.pane-title {
  margin: 0 0 8px;
  font-weight: 400;
  font-size: 13px;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 2px;
}
.compare-img {
  width: 100%;
  max-height: 50vh;
  object-fit: contain;
  border: 1px solid #333;
  border-radius: 4px;
  background: #1a1a1a;
}
.viewer-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  color: #888;
  font-size: 13px;
}
.btn {
  padding: 8px 20px;
  border: 1px solid #555;
  border-radius: 4px;
  background: transparent;
  color: #ddd;
  font-size: 13px;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
}
.btn:hover {
  background: #2a2a2a;
  border-color: #888;
}
.delete-btn-lg {
  border-color: #844;
  color: #d88;
}
.delete-btn-lg:hover {
  background: #3a1a1a;
  border-color: #a44;
}
</style>
