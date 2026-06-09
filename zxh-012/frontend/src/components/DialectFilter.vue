<template>
  <div class="flex flex-wrap gap-3 items-center bg-white rounded-xl shadow p-4">
    <select v-model="localProvince" @change="emitFilter"
      class="px-3 py-2 border border-gray-300 rounded-lg text-sm outline-none focus:ring-2 focus:ring-orange-400">
      <option value="">全部省份</option>
      <option v-for="p in provinces" :key="p" :value="p">{{ p }}</option>
    </select>
    <input v-model="localDialect" @input="emitFilter" placeholder="搜索方言名称..."
      class="px-3 py-2 border border-gray-300 rounded-lg text-sm outline-none focus:ring-2 focus:ring-orange-400 flex-1 min-w-[200px]" />
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useApi } from '../composables/useApi'

const props = defineProps({ province: String, dialect: String })
const emit = defineEmits(['update:province', 'update:dialect', 'filter'])
const { get } = useApi()

const localProvince = ref(props.province || '')
const localDialect = ref(props.dialect || '')
const provinces = ref([])

watch(() => props.province, v => localProvince.value = v || '')
watch(() => props.dialect, v => localDialect.value = v || '')

function emitFilter() {
  emit('update:province', localProvince.value)
  emit('update:dialect', localDialect.value)
  emit('filter', { province: localProvince.value, dialect: localDialect.value })
}

onMounted(async () => {
  const data = await get('/dialects/provinces')
  if (Array.isArray(data)) provinces.value = data
})
</script>
