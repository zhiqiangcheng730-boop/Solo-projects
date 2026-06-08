import { ref } from 'vue'

const LOADED_FAMILIES = new Set()

export function useFontLoader() {
  const loading = ref(false)

  function loadGoogleFont(family) {
    if (LOADED_FAMILIES.has(family)) return
    LOADED_FAMILIES.add(family)

    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = `https://fonts.googleapis.com/css2?family=${encodeURIComponent(family)}&display=swap`
    document.head.appendChild(link)
  }

  async function loadFonts(fonts) {
    loading.value = true
    try {
      fonts.forEach((f) => loadGoogleFont(f.family))
    } finally {
      loading.value = false
    }
  }

  return { loading, loadFonts }
}
