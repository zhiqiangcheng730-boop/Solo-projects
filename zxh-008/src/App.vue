<script setup>
import ShadowCreator from './components/ShadowCreator.vue'
import ShadowGallery from './components/ShadowGallery.vue'
</script>

<template>
  <div class="app-shell">
    <header class="app-header">
      <h1>影子照片墙</h1>
      <p class="subtitle">Shadow Photo Wall</p>
    </header>
    <main class="app-main">
      <ShadowCreator />
      <ShadowGallery />
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  max-width: 960px;
  margin: 0 auto;
  padding: 32px 20px 60px;
}
.app-header {
  text-align: center;
  margin-bottom: 36px;
}
.app-header h1 {
  margin: 0;
  font-weight: 300;
  font-size: 28px;
  letter-spacing: 6px;
  color: #eee;
}
.subtitle {
  margin: 6px 0 0;
  font-size: 12px;
  color: #555;
  letter-spacing: 3px;
}
.app-main {
  display: flex;
  flex-direction: column;
}
</style>
