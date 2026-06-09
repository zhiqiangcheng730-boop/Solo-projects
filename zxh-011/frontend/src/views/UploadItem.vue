<template>
  <div class="upload-page">
    <el-card>
      <template #header><h2>上传旧物</h2></template>
      <el-form :model="form" label-width="80px" @submit.prevent="submit">
        <el-form-item label="标题" required>
          <el-input v-model="form.title" maxlength="200" placeholder="给旧物起个名字" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="描述这个旧物的故事" />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.category" placeholder="选择类型">
            <el-option label="衣物" value="clothing" />
            <el-option label="家具" value="furniture" />
            <el-option label="电子" value="electronics" />
            <el-option label="包装" value="packaging" />
          </el-select>
        </el-form-item>
        <el-form-item label="难度">
          <el-select v-model="form.difficulty" placeholder="改造难度">
            <el-option label="简单" value="easy" />
            <el-option label="中等" value="medium" />
            <el-option label="困难" value="hard" />
          </el-select>
        </el-form-item>
        <el-form-item label="材质">
          <el-input v-model="form.material" placeholder="如：棉、木、塑料" />
        </el-form-item>
        <el-form-item label="尺寸">
          <el-input v-model="form.size_desc" placeholder="如：50x30cm" />
        </el-form-item>
        <el-form-item label="图片URL" required>
          <el-input v-model="form.image_url" placeholder="输入图片URL地址" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submit" :loading="submitting">提交旧物</el-button>
          <el-button @click="$router.push('/')">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { createItem } from '../api/item'

const router = useRouter()
const submitting = ref(false)
const form = reactive({
  title: '', description: '', category: 'clothing', difficulty: 'easy',
  material: '', size_desc: '', image_url: '', creator_id: 1,
})

async function submit() {
  if (!form.title || !form.image_url) {
    ElMessage.warning('请填写标题和图片URL')
    return
  }
  submitting.value = true
  try {
    await createItem(form)
    ElMessage.success('上传成功')
    router.push('/')
  } catch { ElMessage.error('上传失败') }
  submitting.value = false
}
</script>

<style scoped>
.upload-page { max-width: 700px; margin: 0 auto; }
</style>
