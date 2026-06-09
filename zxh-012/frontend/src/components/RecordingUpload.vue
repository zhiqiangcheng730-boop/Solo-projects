<template>
  <div class="max-w-2xl mx-auto">
    <div class="bg-white rounded-2xl shadow-lg p-6">
      <h2 class="text-xl font-semibold text-gray-800 mb-4">上传方言录音</h2>
      <form @submit.prevent="submit" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-600 mb-1">方言名称</label>
            <input v-model="form.dialect_name" placeholder="如: 四川成都话"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-400 focus:border-transparent outline-none" required />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-600 mb-1">省份</label>
            <input v-model="form.province" placeholder="如: 四川"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-400 focus:border-transparent outline-none" required />
          </div>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-600 mb-1">城市 (可选)</label>
            <input v-model="form.city" placeholder="如: 成都"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-400 focus:border-transparent outline-none" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-600 mb-1">上传者位置 (可选)</label>
            <input v-model="form.uploader_location" placeholder="如: 四川成都"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-400 focus:border-transparent outline-none" />
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-600 mb-1">朗读文本</label>
          <div class="flex gap-2 mb-2">
            <button type="button" v-for="p in presets" :key="p"
              @click="form.preset_text = p; form.is_preset = true"
              :class="['px-3 py-1 text-xs rounded-full border transition',
                form.preset_text === p ? 'bg-orange-100 border-orange-400 text-orange-700' : 'border-gray-200 text-gray-500 hover:border-orange-300']">
              {{ p.slice(0, 10) }}...
            </button>
          </div>
          <textarea v-model="form.preset_text" rows="2"
            placeholder="或输入自由文本"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-400 focus:border-transparent outline-none resize-none"
            required></textarea>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-600 mb-1">录音</label>
          <div class="flex items-center gap-4">
            <button type="button" @click="toggleRecord"
              :class="['px-4 py-2 rounded-lg text-sm font-medium transition',
                isRecording ? 'bg-red-500 text-white animate-pulse' : 'bg-orange-600 text-white hover:bg-orange-700']">
              {{ isRecording ? '停止录音' : '开始录音' }}
            </button>
            <span v-if="audioBlob" class="text-sm text-green-600">录音完成 ({{ (audioBlob.size / 1024).toFixed(1) }} KB)</span>
            <span v-else-if="!isRecording" class="text-sm text-gray-400">点击开始录音</span>
          </div>
        </div>
        <button type="submit" :disabled="!audioBlob || submitting"
          class="w-full py-3 bg-orange-600 text-white rounded-lg font-medium hover:bg-orange-700 disabled:opacity-50 disabled:cursor-not-allowed transition">
          {{ submitting ? '上传中...' : '提交录音' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useApi } from '../composables/useApi'

const emit = defineEmits(['uploaded'])
const { postForm } = useApi()

const presets = [
  '从前有座山，山里有座庙，庙里有个老和尚在给小和尚讲故事。',
  '今天天气真好，我们去公园散步吧。',
  '吃了吗您？这天儿可真够热的。',
  '老板，这个多少钱一斤？能便宜点不？',
]

const form = reactive({
  dialect_name: '',
  province: '',
  city: '',
  uploader_location: '',
  preset_text: '',
  is_preset: false,
})

const isRecording = ref(false)
const audioBlob = ref(null)
const submitting = ref(false)
let mediaRecorder = null
let chunks = []

async function toggleRecord() {
  if (isRecording.value) {
    mediaRecorder.stop()
    isRecording.value = false
    return
  }
  chunks = []
  audioBlob.value = null
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' })
    mediaRecorder.ondataavailable = (e) => { if (e.data.size > 0) chunks.push(e.data) }
    mediaRecorder.onstop = () => {
      audioBlob.value = new Blob(chunks, { type: 'audio/webm' })
      stream.getTracks().forEach(t => t.stop())
    }
    mediaRecorder.start()
    isRecording.value = true
  } catch {
    alert('无法访问麦克风，请确保已授予权限。')
  }
}

async function submit() {
  if (!audioBlob.value) return
  submitting.value = true
  const fd = new FormData()
  Object.entries(form).forEach(([k, v]) => fd.append(k, String(v ?? '')))
  fd.append('audio', audioBlob.value, 'recording.webm')
  await postForm('/recordings/', fd)
  submitting.value = false
  Object.keys(form).forEach(k => form[k] = k === 'is_preset' ? false : '')
  audioBlob.value = null
  emit('uploaded')
}
</script>
