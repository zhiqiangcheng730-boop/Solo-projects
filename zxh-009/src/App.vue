<template>
  <div class="app-shell">
    <header class="app-header">
      <h1>🎨 字体心情配对器</h1>
      <p class="subtitle">选择心情，发现最适合的字体搭配</p>
    </header>
    <div class="app-body">
      <aside class="left-panel">
        <MoodSelector
          :moods="moods"
          :selectedMood="selectedMood"
          @select="selectMood"
        />
        <FontList
          :fonts="recommendedFonts"
          :loading="fontsLoading"
          :copiedId="copiedId"
          @copy-css="copyCss"
        />
      </aside>
      <main class="right-panel">
        <PreviewArea
          v-model:text="previewText"
          :fonts="recommendedFonts"
          @save-favorite="saveFavorite"
        />
        <FavoritesPanel
          :favorites="favorites"
          @remove="removeFavorite"
        />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import MoodSelector from './components/MoodSelector.vue'
import FontList from './components/FontList.vue'
import PreviewArea from './components/PreviewArea.vue'
import FavoritesPanel from './components/FavoritesPanel.vue'
import { useMoodFont } from './composables/useMoodFont.js'
import { useFavorites } from './composables/useFavorites.js'
import { useCssCopy } from './composables/useCssCopy.js'

const { moods, selectedMood, currentMood, recommendedFonts, fontsLoading, selectMood } = useMoodFont()
const { favorites, addFavorite, removeFavorite } = useFavorites()
const { copiedId, copyCss } = useCssCopy()

const previewText = ref('')

function saveFavorite() {
  if (!currentMood.value || !previewText.value.trim()) return
  addFavorite({
    moodId: selectedMood.value,
    moodEmoji: currentMood.value.emoji,
    moodLabel: currentMood.value.label,
    text: previewText.value.trim(),
    fonts: recommendedFonts.value.map((f) => ({ family: f.family, label: f.label, fallback: f.fallback })),
  })
}
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f3f5f9;
  color: #333;
  min-height: 100vh;
}
#app { width: 100%; }
</style>

<style scoped>
.app-shell {
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px 20px;
}
.app-header {
  text-align: center;
  margin-bottom: 24px;
}
.app-header h1 { font-size: 1.6rem; color: #333; margin-bottom: 4px; }
.subtitle { font-size: 0.85rem; color: #888; }
.app-body {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 20px;
  align-items: start;
}
.left-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
  background: #fff;
  border-radius: 14px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  position: sticky;
  top: 20px;
}
.right-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
  background: #fff;
  border-radius: 14px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

@media (max-width: 700px) {
  .app-body { grid-template-columns: 1fr; }
  .left-panel { position: static; }
}
</style>
