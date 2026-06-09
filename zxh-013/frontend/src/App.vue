<template>
  <div class="app-shell">
    <header class="app-header">
      <h1>城市雷达 CityRadar</h1>
      <nav class="toolbar">
        <button :class="{ active: activeTool === 'marker' }" @click="activeTool = 'marker'">标记</button>
        <button :class="{ active: activeTool === 'heatmap' }" @click="activeTool = 'heatmap'">热力图</button>
        <button :class="{ active: activeTool === 'route' }" @click="activeTool = 'route'">路线</button>
        <button :class="{ active: activeTool === 'leaderboard' }" @click="activeTool = 'leaderboard'">排行榜</button>
        <button :class="{ active: activeTool === 'notifications' }" @click="activeTool = 'notifications'">通知</button>
        <button :class="{ active: activeTool === 'subscribe' }" @click="activeTool = 'subscribe'">订阅</button>
      </nav>
    </header>
    <main class="app-main">
      <div class="map-container">
        <MapView ref="mapView" :activeTool="activeTool" @map-click="onMapClick" />
      </div>
      <aside class="side-panel">
        <MarkerForm v-if="activeTool === 'marker'" :position="clickedPos" @created="onMarkerCreated" />
        <HeatmapLayer v-if="activeTool === 'heatmap'" :bounds="currentBounds" />
        <RoutePlanner v-if="activeTool === 'route'" />
        <Leaderboard v-if="activeTool === 'leaderboard'" />
        <NotificationPanel v-if="activeTool === 'notifications'" />
        <SubscriptionPanel v-if="activeTool === 'subscribe'" @focus-region="onFocusRegion" />
      </aside>
    </main>
  </div>
</template>

<script setup>
import { ref, provide } from 'vue'
import MapView from './components/MapView.vue'
import MarkerForm from './components/MarkerForm.vue'
import HeatmapLayer from './components/HeatmapLayer.vue'
import RoutePlanner from './components/RoutePlanner.vue'
import Leaderboard from './components/Leaderboard.vue'
import NotificationPanel from './components/NotificationPanel.vue'
import SubscriptionPanel from './components/SubscriptionPanel.vue'

const activeTool = ref('marker')
const clickedPos = ref(null)
const currentBounds = ref(null)
const mapView = ref(null)

provide('mapView', mapView)

function onMapClick(latlng) {
  if (activeTool.value === 'marker') {
    clickedPos.value = { lat: latlng.lat, lng: latlng.lng }
  }
}

function onMarkerCreated() {
  clickedPos.value = null
  mapView.value?.reloadMarkers()
}

function onFocusRegion(center, radiusKm) {
  activeTool.value = 'marker'
  mapView.value?.focusRegion(center, radiusKm)
}
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body, #app { height: 100%; font-family: 'Microsoft YaHei', sans-serif; }
.app-shell { display: flex; flex-direction: column; height: 100%; }
.app-header { background: #1a1a2e; color: #fff; padding: 8px 16px; display: flex; align-items: center; gap: 16px; }
.app-header h1 { font-size: 18px; white-space: nowrap; }
.toolbar { display: flex; gap: 4px; }
.toolbar button { background: #16213e; color: #a0a0b0; border: none; padding: 6px 14px; border-radius: 4px; cursor: pointer; font-size: 13px; }
.toolbar button:hover { color: #fff; background: #0f3460; }
.toolbar button.active { background: #e94560; color: #fff; }
.app-main { display: flex; flex: 1; overflow: hidden; }
.map-container { flex: 1; min-width: 0; }
.side-panel { width: 340px; background: #f5f5f5; overflow-y: auto; padding: 12px; border-left: 1px solid #ddd; }
</style>
