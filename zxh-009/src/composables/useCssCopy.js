import { ref } from 'vue'

export function useCssCopy() {
  const copiedId = ref(null)

  async function copyCss(font) {
    const css = `font-family: '${font.family}', ${font.fallback};`
    try {
      await navigator.clipboard.writeText(css)
      copiedId.value = font.family
      setTimeout(() => { copiedId.value = null }, 2000)
    } catch {
      // Fallback for older browsers
      const ta = document.createElement('textarea')
      ta.value = css
      ta.style.position = 'fixed'
      ta.style.opacity = '0'
      document.body.appendChild(ta)
      ta.select()
      document.execCommand('copy')
      document.body.removeChild(ta)
      copiedId.value = font.family
      setTimeout(() => { copiedId.value = null }, 2000)
    }
  }

  return { copiedId, copyCss }
}
