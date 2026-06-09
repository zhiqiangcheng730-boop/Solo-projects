<template>
  <Teleport to="body">
    <div class="fixed inset-0 bg-black/40 flex items-center justify-center z-50" @click.self="$emit('close')">
      <div class="bg-white rounded-2xl p-6 w-[480px] max-h-[80vh] overflow-y-auto shadow-2xl">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-800">方言词汇注解</h3>
          <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 text-xl leading-none">&times;</button>
        </div>

        <form @submit.prevent="addAnnotation" class="flex gap-2 mb-4">
          <input v-model="newWord" placeholder="方言词汇"
            class="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm outline-none focus:ring-2 focus:ring-orange-400" required />
          <input v-model="newStandard" placeholder="标准含义"
            class="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm outline-none focus:ring-2 focus:ring-orange-400" required />
          <button type="submit" class="px-4 py-2 bg-orange-600 text-white rounded-lg text-sm font-medium hover:bg-orange-700 transition">
            添加
          </button>
        </form>

        <div v-if="loading" class="text-center py-6 text-gray-400">加载中...</div>
        <div v-else-if="annotations.length === 0" class="text-center py-6 text-gray-400">暂无词汇注解</div>
        <ul v-else class="space-y-2">
          <li v-for="a in annotations" :key="a.id" class="flex items-center justify-between px-3 py-2 bg-gray-50 rounded-lg">
            <span><span class="font-medium text-orange-700">{{ a.dialect_word }}</span> <span class="text-gray-400 mx-1">=</span> <span class="text-gray-600">{{ a.standard_word }}</span></span>
            <button @click="removeAnnotation(a.id)" class="text-gray-400 hover:text-red-500 text-sm transition">删除</button>
          </li>
        </ul>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useApi } from '../composables/useApi'

const props = defineProps({ recordingId: Number })
defineEmits(['close'])
const { get, post, del } = useApi()

const annotations = ref([])
const loading = ref(false)
const newWord = ref('')
const newStandard = ref('')

async function fetchAnnotations() {
  if (!props.recordingId) return
  loading.value = true
  const data = await get(`/vocabulary/${props.recordingId}`)
  annotations.value = Array.isArray(data) ? data : []
  loading.value = false
}

async function addAnnotation() {
  if (!newWord.value || !newStandard.value) return
  await post('/vocabulary/', {
    recording_id: props.recordingId,
    dialect_word: newWord.value,
    standard_word: newStandard.value,
  })
  newWord.value = ''
  newStandard.value = ''
  fetchAnnotations()
}

async function removeAnnotation(id) {
  await del(`/vocabulary/${id}`)
  fetchAnnotations()
}

watch(() => props.recordingId, fetchAnnotations)
onMounted(fetchAnnotations)
</script>
