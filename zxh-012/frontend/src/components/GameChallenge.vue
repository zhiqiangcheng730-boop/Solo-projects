<template>
  <div class="max-w-2xl mx-auto space-y-4">
    <!-- Start screen -->
    <div v-if="!started" class="bg-white rounded-2xl shadow-lg p-10 text-center">
      <h2 class="text-2xl font-bold text-gray-800 mb-2">方言挑战</h2>
      <p class="text-gray-500 mb-6">播放一段方言录音，选择正确的含义选项</p>
      <button @click="startGame" class="px-8 py-3 bg-orange-600 text-white rounded-xl font-medium text-lg hover:bg-orange-700 transition shadow-lg">
        开始挑战
      </button>
    </div>

    <!-- Game -->
    <div v-else-if="questions.length > 0 && currentIdx < questions.length" class="bg-white rounded-2xl shadow-lg p-6">
      <div class="flex items-center justify-between mb-4">
        <span class="text-sm font-medium text-gray-500">第 {{ currentIdx + 1 }} / {{ questions.length }} 题</span>
        <span class="text-xs text-orange-600 bg-orange-50 px-2 py-0.5 rounded-full">得分: {{ score }}</span>
      </div>
      <div class="mb-4">
        <p class="text-sm text-gray-500 mb-1">方言: {{ currentQuestion.dialect_name }} ({{ currentQuestion.province }})</p>
        <p class="text-gray-700 mb-3">"{{ currentQuestion.preset_text?.slice(0, 50) }}..."</p>
        <audio v-if="currentQuestion.audio_file_path" :src="currentQuestion.audio_file_path"
          controls class="w-full"></audio>
      </div>
      <p class="font-medium text-gray-700 mb-3">这段话的意思是？</p>
      <div class="space-y-2">
        <button v-for="(opt, i) in currentOptions" :key="i"
          @click="answer(opt)"
          :disabled="answered"
          :class="['w-full text-left px-4 py-3 rounded-xl border-2 transition text-sm',
            answered
              ? (opt === currentQuestion.correct_meaning ? 'border-green-400 bg-green-50 text-green-800' : answeredOption === opt ? 'border-red-400 bg-red-50 text-red-800' : 'border-gray-100 bg-gray-50 text-gray-400')
              : 'border-gray-200 hover:border-orange-300 hover:bg-orange-50']">
          {{ opt }}
        </button>
      </div>
      <div v-if="answered" class="mt-4 text-center">
        <p v-if="isCorrect" class="text-green-600 font-medium">正确!</p>
        <p v-else class="text-red-600 font-medium">错误! 正确答案: {{ currentQuestion.correct_meaning }}</p>
        <button @click="nextQuestion" class="mt-3 px-6 py-2 bg-orange-600 text-white rounded-lg text-sm hover:bg-orange-700 transition">
          {{ currentIdx + 1 < questions.length ? '下一题' : '查看结果' }}
        </button>
      </div>
    </div>

    <!-- Result -->
    <div v-else-if="started" class="bg-white rounded-2xl shadow-lg p-10 text-center">
      <h2 class="text-2xl font-bold text-gray-800 mb-2">挑战结束!</h2>
      <p class="text-6xl font-bold text-orange-600 my-4">{{ score }} / {{ questions.length }}</p>
      <p class="text-gray-500 mb-6">{{ resultMessage }}</p>
      <button @click="startGame" class="px-8 py-3 bg-orange-600 text-white rounded-xl font-medium hover:bg-orange-700 transition">
        再来一局
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useApi } from '../composables/useApi'

const { get } = useApi()
const started = ref(false)
const questions = ref([])
const currentIdx = ref(0)
const score = ref(0)
const answered = ref(false)
const answeredOption = ref('')
const isCorrect = ref(false)

const currentQuestion = computed(() => questions.value[currentIdx.value] || {})
const currentOptions = computed(() => {
  if (!currentQuestion.value.correct_meaning) return []
  let wrong = []
  try { wrong = JSON.parse(currentQuestion.value.wrong_options) } catch { wrong = [] }
  const opts = [currentQuestion.value.correct_meaning, ...(wrong || [])]
  return opts.sort(() => Math.random() - 0.5)
})

const resultMessage = computed(() => {
  const rate = score.value / questions.value.length
  if (rate >= 0.8) return '方言达人，太厉害了!'
  if (rate >= 0.5) return '不错，继续加油!'
  return '方言博大精深，多听听吧!'
})

async function startGame() {
  started.value = true
  currentIdx.value = 0
  score.value = 0
  answered.value = false
  const data = await get('/game/challenge?limit=5')
  questions.value = Array.isArray(data) ? data : []
}

function answer(opt) {
  if (answered.value) return
  answered.value = true
  answeredOption.value = opt
  isCorrect.value = opt === currentQuestion.value.correct_meaning
  if (isCorrect.value) score.value++
}

function nextQuestion() {
  answered.value = false
  currentIdx.value++
}
</script>
