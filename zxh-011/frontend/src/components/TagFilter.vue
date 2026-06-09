<template>
  <div class="tag-filter">
    <el-select v-model="selectedCategory" placeholder="旧物类型" clearable @change="emitFilter">
      <el-option label="衣物" value="clothing" />
      <el-option label="家具" value="furniture" />
      <el-option label="电子" value="electronics" />
      <el-option label="包装" value="packaging" />
    </el-select>
    <el-select v-model="selectedDifficulty" placeholder="改造难度" clearable @change="emitFilter">
      <el-option label="简单" value="easy" />
      <el-option label="中等" value="medium" />
      <el-option label="困难" value="hard" />
    </el-select>
    <el-input v-model="keyword" placeholder="搜索关键词" clearable @input="emitFilter" style="width: 200px" />
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['filter'])
const selectedCategory = ref(null)
const selectedDifficulty = ref(null)
const keyword = ref('')

function emitFilter() {
  emit('filter', {
    category: selectedCategory.value,
    difficulty: selectedDifficulty.value,
    keyword: keyword.value || null,
  })
}
</script>

<style scoped>
.tag-filter {
  display: flex; gap: 12px; align-items: center; flex-wrap: wrap;
  padding: 16px; background: #fff; border-radius: 8px; margin-bottom: 16px;
}
</style>
