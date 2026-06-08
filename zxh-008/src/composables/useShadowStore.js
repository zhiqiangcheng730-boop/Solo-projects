import { ref, computed } from 'vue'
import { load, save } from '../utils/storage.js'

const STORAGE_KEY = 'items'

const items = ref(load(STORAGE_KEY) || [])

function persist() {
  save(STORAGE_KEY, items.value)
}

let nextId = Date.now()

export function useShadowStore() {
  const count = computed(() => items.value.length)

  function add(originalBase64, shadowBase64, threshold) {
    const entry = {
      id: String(nextId++),
      original: originalBase64,
      shadow: shadowBase64,
      threshold,
      createdAt: Date.now(),
    }
    items.value.push(entry)
    persist()
    return entry
  }

  function remove(id) {
    const idx = items.value.findIndex((item) => item.id === id)
    if (idx !== -1) {
      items.value.splice(idx, 1)
      persist()
    }
  }

  function clear() {
    items.value.length = 0
    persist()
  }

  return { items, count, add, remove, clear }
}
