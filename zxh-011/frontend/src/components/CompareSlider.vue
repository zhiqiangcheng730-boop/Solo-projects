<template>
  <div class="compare-slider" ref="containerRef" @mousemove="onMouseMove" @touchmove="onTouchMove">
    <div class="compare-before" :style="{ backgroundImage: `url(${before})` }" />
    <div class="compare-after" :style="{ backgroundImage: `url(${after})`, clipPath: `inset(0 ${100 - slidePos}% 0 0)` }" />
    <div class="compare-handle" :style="{ left: slidePos + '%' }">
      <div class="handle-line" />
      <span class="handle-arrow">◀ ▶</span>
    </div>
    <div class="compare-labels">
      <span class="label-before">改造前</span>
      <span class="label-after">改造后</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  before: { type: String, required: true },
  after: { type: String, required: true },
})

const slidePos = ref(50)
const containerRef = ref(null)

function getPercent(e) {
  const rect = containerRef.value?.getBoundingClientRect()
  if (!rect) return 50
  const x = e.touches ? e.touches[0].clientX : e.clientX
  return Math.max(0, Math.min(100, ((x - rect.left) / rect.width) * 100))
}

function onMouseMove(e) { slidePos.value = getPercent(e) }
function onTouchMove(e) { e.preventDefault(); slidePos.value = getPercent(e) }
</script>

<style scoped>
.compare-slider {
  position: relative; width: 100%; height: 400px; overflow: hidden; cursor: col-resize;
  border-radius: 8px; user-select: none;
}
.compare-before, .compare-after {
  position: absolute; inset: 0; background-size: cover; background-position: center;
}
.compare-after { z-index: 1; }
.compare-handle {
  position: absolute; top: 0; bottom: 0; width: 4px; z-index: 2; transform: translateX(-50%);
  display: flex; align-items: center; justify-content: center;
}
.handle-line { width: 4px; height: 100%; background: #fff; box-shadow: 0 0 8px rgba(0,0,0,.5); }
.handle-arrow {
  position: absolute; color: #fff; font-size: 12px; background: rgba(0,0,0,.4);
  padding: 4px 8px; border-radius: 4px; white-space: nowrap;
}
.compare-labels {
  position: absolute; bottom: 12px; left: 0; right: 0; display: flex; justify-content: space-between;
  z-index: 3; padding: 0 20px;
}
.label-before, .label-after {
  background: rgba(0,0,0,.5); color: #fff; padding: 4px 12px; border-radius: 4px; font-size: 13px;
}
</style>
