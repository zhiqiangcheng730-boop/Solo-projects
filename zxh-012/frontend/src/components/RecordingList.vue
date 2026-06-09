<template>
  <div class="space-y-4">
    <DialectFilter v-model:province="province" v-model:dialect="dialect" @filter="fetchRecordings" />

    <div v-if="loading" class="text-center py-20 text-gray-400">加载中...</div>
    <div v-else-if="recordings.length === 0" class="text-center py-20 text-gray-400">暂无录音记录</div>
    <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <div v-for="r in recordings" :key="r.id"
        class="bg-white rounded-xl shadow-md hover:shadow-lg transition p-5 cursor-pointer"
        @click="$emit('select', r.id)">
        <div class="flex items-start justify-between mb-2">
          <span class="text-sm font-semibold text-orange-700 bg-orange-50 px-2 py-0.5 rounded">{{ r.dialect_name }}</span>
          <span class="text-xs text-gray-400">{{ r.province }}{{ r.city ? ' · ' + r.city : '' }}</span>
        </div>
        <p class="text-sm text-gray-600 line-clamp-2 mb-3">{{ r.preset_text }}</p>
        <audio v-if="r.audio_file_path" :src="r.audio_file_path" controls
          class="w-full h-8 mt-2" @click.stop></audio>
        <div class="flex items-center justify-between mt-3 pt-3 border-t border-gray-100">
          <span class="text-xs text-gray-400">{{ formatDate(r.recorded_at) }}</span>
          <button @click.stop="$emit('select', r.id)"
            class="text-xs text-orange-600 hover:text-orange-800 font-medium">词汇注解</button>
        </div>
      </div>
    </div>

    <div v-if="total > size" class="flex justify-center gap-2 pt-4">
      <button v-for="p in totalPages" :key="p"
        @click="page = p; fetchRecordings()"
        :class="['px-3 py-1 rounded text-sm', p === page ? 'bg-orange-600 text-white' : 'bg-white text-gray-600 hover:bg-orange-50 border']">
        {{ p }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useApi } from '../composables/useApi'
import DialectFilter from './DialectFilter.vue'

defineEmits(['select'])
const { get } = useApi()

const recordings = ref([])
const loading = ref(false)
const page = ref(1)
const size = 12
const total = ref(0)
const province = ref('')
const dialect = ref('')

const totalPages = computed(() => Math.ceil(total.value / size.value))

function formatDate(d) { return d ? new Date(d).toLocaleDateString('zh-CN') : '' }

async function fetchRecordings() {
  loading.value = true
  const data = await get('/recordings/', { province: province.value, dialect: dialect.value, page: page.value, size: size.value })
  if (data && data.items) {
    recordings.value = data.items
    total.value = data.total
  }
  loading.value = false
}

onMounted(fetchRecordings)
</script>
