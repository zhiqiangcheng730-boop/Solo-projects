import { ref, computed } from 'vue'
import { MOODS, MOOD_FONT_MAP } from '../constants/moodFonts.js'
import { useFontLoader } from './useFontLoader.js'

export function useMoodFont() {
  const selectedMood = ref(null)
  const { loading: fontsLoading, loadFonts } = useFontLoader()

  const currentMood = computed(() =>
    MOODS.find((m) => m.id === selectedMood.value) ?? null
  )

  const recommendedFonts = computed(() => {
    if (!selectedMood.value) return []
    return MOOD_FONT_MAP[selectedMood.value] ?? []
  })

  function selectMood(moodId) {
    selectedMood.value = moodId
    loadFonts(MOOD_FONT_MAP[moodId])
  }

  return {
    moods: MOODS,
    selectedMood,
    currentMood,
    recommendedFonts,
    fontsLoading,
    selectMood,
  }
}
