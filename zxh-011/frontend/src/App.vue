<template>
  <el-container class="app-container">
    <el-header class="app-header">
      <div class="logo" @click="$router.push('/')">♻ 旧物改造灵感交换站</div>
      <el-menu mode="horizontal" :default-active="activeMenu" router>
        <el-menu-item index="/">灵感画廊</el-menu-item>
        <el-menu-item index="/upload">上传旧物</el-menu-item>
        <el-menu-item index="/profile">个人中心</el-menu-item>
      </el-menu>
    </el-header>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Microsoft YaHei', sans-serif; }
.app-container { min-height: 100vh; background: #f5f7fa; }
.app-header { background: #fff; border-bottom: 1px solid #e4e7ed; display: flex; align-items: center; padding: 0 20px; }
.app-header .logo { font-size: 20px; font-weight: bold; color: #409EFF; cursor: pointer; margin-right: 40px; white-space: nowrap; }
.el-main { padding: 20px; max-width: 1400px; margin: 0 auto; width: 100%; }
</style>
