<template>
  <div class="map-wrapper" ref="mapWrapper"></div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import L from 'leaflet'
import 'leaflet.heat'
import { api } from '../services/api.js'

const props = defineProps({ activeTool: String })
const emit = defineEmits(['map-click'])

const mapWrapper = ref(null)
let map = null
let markerLayer = null
let heatLayer = null
let routeLayer = null
let newMarkerIcon = null

const CATEGORY_ICONS = {
  traffic_jam: { color: '#e74c3c', label: '堵' },
  accident: { color: '#e67e22', label: '事' },
  hot_zone: { color: '#2ecc71', label: '热' },
  police: { color: '#3498db', label: '警' },
  toilet: { color: '#9b59b6', label: '厕' },
  gas_station: { color: '#f1c40f', label: '油' },
  other: { color: '#95a5a6', label: '点' },
}

function createIcon(category) {
  const cfg = CATEGORY_ICONS[category] || CATEGORY_ICONS.other
  return L.divIcon({
    className: 'custom-marker',
    html: `<div style="background:${cfg.color};color:#fff;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:bold;border:2px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,0.3)">${cfg.label}</div>`,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
  })
}

function getBounds() {
  const b = map.getBounds()
  return { south: b.getSouth(), north: b.getNorth(), east: b.getEast(), west: b.getWest() }
}

async function loadMarkers() {
  if (!map) return
  try {
    const markers = await api.getMarkers(getBounds())
    if (markerLayer) map.removeLayer(markerLayer)
    markerLayer = L.layerGroup()
    markers.forEach(m => {
      const icon = createIcon(m.category)
      const popup = L.popup().setContent(`
        <div style="min-width:180px">
          <strong>${m.title}</strong>
          <span style="background:#eee;padding:1px 6px;border-radius:3px;font-size:11px;margin-left:6px">${m.category}</span>
          <p style="margin:6px 0">${m.description || ''}</p>
          <small>赞同: ${m.vote_count}</small>
          <br><button class="vote-btn" data-id="${m.id}">同意 (+1)</button>
        </div>
      `)
      const marker = L.marker([m.latitude, m.longitude], { icon }).bindPopup(popup)
      marker.on('popupopen', () => {
        setTimeout(() => {
          const btn = document.querySelector(`.vote-btn[data-id="${m.id}"]`)
          if (btn) {
            btn.onclick = async () => {
              try {
                await api.vote(m.id)
                btn.textContent = '已投票'
                btn.disabled = true
              } catch (e) { alert(e.message) }
            }
          }
        }, 100)
      })
      markerLayer.addLayer(marker)
    })
    markerLayer.addTo(map)
  } catch (e) { console.error('加载标记失败', e) }
}

async function loadHeatmap() {
  if (!map) return
  if (props.activeTool !== 'heatmap') {
    if (heatLayer) { map.removeLayer(heatLayer); heatLayer = null }
    return
  }
  try {
    const points = await api.getHeatmap(getBounds())
    if (heatLayer) map.removeLayer(heatLayer)
    if (points.length > 0) {
      const heatData = points.map(p => [p.lat, p.lng, p.weight])
      heatLayer = L.heatLayer(heatData, { radius: 25, blur: 15, maxZoom: 17, max: 50 }).addTo(map)
    }
  } catch (e) { console.error('加载热力图失败', e) }
}

function focusRegion(center, radiusKm) {
  const zoom = Math.round(14 - Math.log2(radiusKm / 0.5))
  map.setView([center.lat, center.lng], Math.min(16, Math.max(10, zoom)))
}

onMounted(() => {
  map = L.map(mapWrapper.value).setView([39.9042, 116.4074], 13)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 19,
  }).addTo(map)

  map.on('click', e => emit('map-click', e.latlng))
  map.on('moveend', () => {
    loadMarkers()
    loadHeatmap()
  })

  loadMarkers()
})

watch(() => props.activeTool, () => {
  loadMarkers()
  loadHeatmap()
})

onBeforeUnmount(() => {
  if (map) { map.remove(); map = null }
})

defineExpose({ reloadMarkers: loadMarkers, focusRegion })
</script>

<style>
.map-wrapper { height: 100%; }
.custom-marker { background: transparent !important; border: none !important; }
.vote-btn { margin-top: 4px; padding: 2px 10px; background: #e94560; color: #fff; border: none; border-radius: 3px; cursor: pointer; }
.vote-btn:disabled { background: #aaa; cursor: default; }
</style>
