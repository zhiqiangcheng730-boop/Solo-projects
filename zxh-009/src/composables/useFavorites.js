import { ref, watch } from 'vue'

const STORAGE_KEY = 'font-mood-favorites'

function loadFromStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

function saveToStorage(items) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items))
  } catch {
    // localStorage full or unavailable
  }
}

export function useFavorites() {
  const favorites = ref(loadFromStorage())

  watch(favorites, (val) => saveToStorage(val), { deep: true })

  function addFavorite(entry) {
    favorites.value.push({
      id: Date.now(),
      createdAt: new Date().toISOString(),
      ...entry,
    })
  }

  function removeFavorite(id) {
    favorites.value = favorites.value.filter((f) => f.id !== id)
  }

  return { favorites, addFavorite, removeFavorite }
}
