<template>
  <div class="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-red-50">
    <header class="bg-white/80 backdrop-blur border-b border-orange-100 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <h1 class="text-2xl font-bold text-orange-800">方言声音档案馆</h1>
        <nav class="flex gap-1">
          <button v-for="tab in tabs" :key="tab.id"
            @click="activeTab = tab.id"
            :class="['px-4 py-2 rounded-lg text-sm font-medium transition',
              activeTab === tab.id
                ? 'bg-orange-600 text-white shadow'
                : 'text-gray-600 hover:bg-orange-100']">
            {{ tab.label }}
          </button>
        </nav>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 py-6">
      <RecordingUpload v-if="activeTab === 'upload'" @uploaded="onUploaded" />
      <RecordingList v-else-if="activeTab === 'browse'" @select="onSelectRecording" />
      <MapView v-else-if="activeTab === 'map'" :recording-id="selectedRecordingId" />
      <GameChallenge v-else-if="activeTab === 'game'" />
      <VocabularyPanel v-if="selectedRecordingId" :recording-id="selectedRecordingId"
        @close="selectedRecordingId = null" />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import RecordingUpload from './components/RecordingUpload.vue'
import RecordingList from './components/RecordingList.vue'
import MapView from './components/MapView.vue'
import GameChallenge from './components/GameChallenge.vue'
import VocabularyPanel from './components/VocabularyPanel.vue'

const tabs = [
  { id: 'upload', label: '上传录音' },
  { id: 'browse', label: '浏览录音' },
  { id: 'map', label: '相似度地图' },
  { id: 'game', label: '方言挑战' },
]
const activeTab = ref('browse')
const selectedRecordingId = ref(null)

function onUploaded() {
  activeTab.value = 'browse'
}

function onSelectRecording(id) {
  selectedRecordingId.value = id
}
</script>
