<script setup>
import { ref, watch } from 'vue'
import { useImageProcessor } from '../composables/useImageProcessor.js'
import { useShadowStore } from '../composables/useShadowStore.js'

const emit = defineEmits(['added'])

const { originalBase64, silhouetteBase64, processing, error, loadOriginal, processSilhouette, reset } =
  useImageProcessor()
const { add } = useShadowStore()

const threshold = ref(128)
const imgRef = ref(null)
const fileInput = ref(null)

watch(threshold, (val) => {
  if (imgRef.value) {
    processSilhouette(imgRef.value, val)
  }
})

async function handleFileSelect(e) {
  const file = e.target.files[0]
  if (!file) return

  const img = await loadOriginal(file)
  if (img) {
    imgRef.value = img
    await processSilhouette(img, threshold.value)
  }
}

function handleAdd() {
  if (!silhouetteBase64.value) return
  add(originalBase64.value, silhouetteBase64.value, threshold.value)
  emit('added')
  reset()
  threshold.value = 128
  if (fileInput.value) fileInput.value.value = ''
  imgRef.value = null
}

function triggerUpload() {
  fileInput.value?.click()
}
</script>

<template>
  <div class="creator">
    <div class="creator-left">
      <input
        ref="fileInput"
        type="file"
        accept="image/*"
        class="file-input"
        @change="handleFileSelect"
      />
      <button class="btn upload-btn" @click="triggerUpload">选择照片</button>

      <div v-if="processing" class="status">处理中...</div>
      <div v-if="error" class="status error">{{ error }}</div>

      <div v-if="originalBase64" class="preview-box">
        <h3>原图</h3>
        <img :src="originalBase64" alt="原图" class="preview-img" />
      </div>
    </div>

    <div class="creator-right">
      <div v-if="silhouetteBase64" class="preview-box">
        <h3>剪影预览</h3>
        <img :src="silhouetteBase64" alt="剪影预览" class="preview-img" />
      </div>

      <div v-if="originalBase64" class="controls">
        <label class="slider-label">
          剪影阈值：<strong>{{ threshold }}</strong>
        </label>
        <input
          type="range"
          min="0"
          max="255"
          v-model.number="threshold"
          class="slider"
        />

        <button class="btn add-btn" :disabled="!silhouetteBase64" @click="handleAdd">
          添加到影子墙
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.creator {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
  justify-content: center;
}
.creator-left,
.creator-right {
  flex: 1;
  min-width: 280px;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}
.file-input {
  display: none;
}
.preview-box {
  width: 100%;
  text-align: center;
}
.preview-box h3 {
  margin: 0 0 8px;
  font-weight: 400;
  font-size: 14px;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 2px;
}
.preview-img {
  width: 100%;
  max-height: 320px;
  object-fit: contain;
  border: 1px solid #333;
  border-radius: 4px;
  background: #1a1a1a;
}
.controls {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}
.slider-label {
  font-size: 14px;
  color: #aaa;
}
.slider {
  width: 100%;
  -webkit-appearance: none;
  appearance: none;
  height: 4px;
  background: #444;
  border-radius: 2px;
  outline: none;
}
.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #fff;
  cursor: pointer;
  border: 2px solid #333;
}
.slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #fff;
  cursor: pointer;
  border: 2px solid #333;
}
.btn {
  padding: 10px 28px;
  border: 1px solid #555;
  border-radius: 4px;
  background: transparent;
  color: #ddd;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
}
.btn:hover {
  background: #2a2a2a;
  border-color: #888;
}
.btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}
.add-btn {
  border-color: #888;
  font-weight: 600;
}
.status {
  font-size: 13px;
  color: #888;
}
.status.error {
  color: #c44;
}
</style>
