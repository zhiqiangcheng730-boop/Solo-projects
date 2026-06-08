<script setup>
import { ref } from 'vue'
import { useShadowStore } from '../composables/useShadowStore.js'
import ShadowViewer from './ShadowViewer.vue'

const { items, remove } = useShadowStore()

const viewerVisible = ref(false)
const viewerItem = ref(null)

function openViewer(item) {
  viewerItem.value = item
  viewerVisible.value = true
}

function handleDelete(id) {
  if (viewerItem.value?.id === id) {
    viewerVisible.value = false
    viewerItem.value = null
  }
  remove(id)
}
</script>

<template>
  <section class="gallery-section">
    <h2 class="section-title">影子墙</h2>
    <p v-if="items.length === 0" class="empty-hint">还没有影子照片，上传一张照片开始创作吧</p>

    <div v-else class="gallery-grid">
      <div v-for="item in items" :key="item.id" class="gallery-item">
        <img
          :src="item.shadow"
          :alt="'剪影 ' + item.id"
          class="thumbnail"
          @click="openViewer(item)"
        />
        <button class="delete-btn" @click.stop="handleDelete(item.id)" title="删除">×</button>
      </div>
    </div>

    <ShadowViewer
      v-if="viewerVisible"
      :item="viewerItem"
      @close="viewerVisible = false"
      @delete="handleDelete"
    />
  </section>
</template>

<style scoped>
.gallery-section {
  margin-top: 48px;
  padding-top: 24px;
  border-top: 1px solid #333;
}
.section-title {
  text-align: center;
  font-weight: 400;
  font-size: 18px;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 3px;
  margin: 0 0 20px;
}
.empty-hint {
  text-align: center;
  color: #555;
  font-size: 14px;
}
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
}
.gallery-item {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
  border-radius: 4px;
  background: #1a1a1a;
  border: 1px solid #2a2a2a;
  cursor: pointer;
  transition: border-color 0.2s;
}
.gallery-item:hover {
  border-color: #666;
}
.thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.delete-btn {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 24px;
  height: 24px;
  border: none;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.7);
  color: #999;
  font-size: 16px;
  line-height: 1;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s, color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.gallery-item:hover .delete-btn {
  opacity: 1;
}
.delete-btn:hover {
  color: #f66;
}
</style>
