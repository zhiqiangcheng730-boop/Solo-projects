import { ref } from 'vue'
import { loadImageFromFile, imageToSilhouette, imageToBase64 } from '../utils/imageProcessor.js'

export function useImageProcessor() {
  const originalBase64 = ref(null)
  const silhouetteBase64 = ref(null)
  const processing = ref(false)
  const error = ref(null)

  async function loadOriginal(file) {
    error.value = null
    processing.value = true
    try {
      const img = await loadImageFromFile(file)
      originalBase64.value = imageToBase64(img)
      return img
    } catch (e) {
      error.value = e.message
      return null
    } finally {
      processing.value = false
    }
  }

  async function processSilhouette(img, threshold) {
    if (!img) return
    processing.value = true
    try {
      silhouetteBase64.value = imageToSilhouette(img, threshold)
    } finally {
      processing.value = false
    }
  }

  function reset() {
    originalBase64.value = null
    silhouetteBase64.value = null
    error.value = null
  }

  return { originalBase64, silhouetteBase64, processing, error, loadOriginal, processSilhouette, reset }
}
