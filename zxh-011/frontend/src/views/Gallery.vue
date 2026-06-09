<template>
  <div class="gallery-page">
    <TagFilter @filter="onFilter" />
    <div v-if="loading" style="text-align:center;padding:60px">
      <el-icon class="is-loading"><Loading /></el-icon> 加载中...
    </div>
    <div v-else class="item-grid">
      <el-card v-for="item in items" :key="item.id" class="item-card" shadow="hover"
        @click="$router.push(`/detail/${item.id}`)">
        <img :src="item.image_url" class="item-img" />
        <div class="item-info">
          <h3>{{ item.title }}</h3>
          <el-tag size="small" :type="categoryType(item.category)">{{ categoryLabel(item.category) }}</el-tag>
          <el-tag size="small" :type="difficultyType(item.difficulty)">{{ difficultyLabel(item.difficulty) }}</el-tag>
          <span class="item-status">{{ statusLabel(item.status) }}</span>
        </div>
      </el-card>
    </div>
    <div v-if="!loading && items.length === 0" style="text-align:center;padding:60px;color:#909399">
      暂无旧物，快去上传第一个吧
    </div>
    <el-pagination
      v-if="total > pageSize"
      style="margin-top:20px;justify-content:center"
      background layout="prev, pager, next"
      :total="total" :page-size="pageSize" v-model:current-page="page"
      @current-change="fetchItems"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Loading } from '@element-plus/icons-vue'
import TagFilter from '../components/TagFilter.vue'
import { listItems } from '../api/item'

const items = ref([])
const loading = ref(true)
const total = ref(0)
const page = ref(1)
const pageSize = 12
const currentFilter = ref({})

function categoryType(c) { return { clothing: '', furniture: 'success', electronics: 'warning', packaging: 'danger' }[c] || '' }
function categoryLabel(c) { return { clothing: '衣物', furniture: '家具', electronics: '电子', packaging: '包装' }[c] || c }
function difficultyType(d) { return { easy: 'success', medium: 'warning', hard: 'danger' }[d] || '' }
function difficultyLabel(d) { return { easy: '简单', medium: '中等', hard: '困难' }[d] || d }
function statusLabel(s) { return { pending: '待改造', in_progress: '改造中', completed: '已完成' }[s] || s }

function onFilter(f) { currentFilter.value = f; page.value = 1; fetchItems() }

async function fetchItems() {
  loading.value = true
  try {
    const res = await listItems({ ...currentFilter.value, page: page.value, page_size: pageSize })
    items.value = res.items
    total.value = res.total
  } catch { /* fallback */ }
  loading.value = false
}

onMounted(fetchItems)
</script>

<style scoped>
.item-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.item-card { cursor: pointer; overflow: hidden; }
.item-img { width: 100%; height: 200px; object-fit: cover; }
.item-info { padding: 8px 0; display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.item-info h3 { width: 100%; font-size: 16px; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.item-status { font-size: 12px; color: #909399; }
</style>
