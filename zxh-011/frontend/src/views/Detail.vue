<template>
  <div class="detail-page" v-if="item">
    <el-row :gutter="20">
      <el-col :span="14">
        <el-card>
          <img :src="item.image_url" style="width:100%;max-height:400px;object-fit:cover;border-radius:8px" />
          <h2 style="margin-top:12px">{{ item.title }}</h2>
          <p style="color:#606266">{{ item.description || '暂无描述' }}</p>
          <div style="margin:8px 0;display:flex;gap:8px">
            <el-tag>{{ categoryLabel(item.category) }}</el-tag>
            <el-tag :type="difficultyType(item.difficulty)">{{ difficultyLabel(item.difficulty) }}</el-tag>
            <el-tag>{{ item.material }}</el-tag>
            <el-tag>{{ item.size_desc }}</el-tag>
          </div>
          <el-button :type="itemLiked ? 'danger' : 'default'" @click="toggleItemLike" style="margin-top:8px">
            {{ itemLiked ? '❤ 已赞' : '♡ 点赞' }} {{ itemLikeCount }}
          </el-button>
        </el-card>

        <el-card style="margin-top:16px">
          <template #header><h3>改造进度</h3></template>
          <ProgressBar :steps="progress" :currentStep="progress.length - 1" />
          <el-button size="small" @click="showAddStep = true" style="margin-top:8px">添加进度步骤</el-button>
        </el-card>

        <el-dialog v-model="showAddStep" title="添加进度步骤" width="500px">
          <el-form :model="newStep">
            <el-form-item label="步骤描述"><el-input v-model="newStep.description" /></el-form-item>
            <el-form-item label="图片URL"><el-input v-model="newStep.image_url" /></el-form-item>
            <el-button type="primary" @click="submitStep">添加</el-button>
          </el-form>
        </el-dialog>
      </el-col>

      <el-col :span="10">
        <el-card>
          <template #header>
            <div style="display:flex;justify-content:space-between;align-items:center">
              <h3>改造方案 ({{ plans.length }})</h3>
              <el-button size="small" type="primary" @click="showPlanForm = true">提交方案</el-button>
            </div>
          </template>
          <div v-for="plan in plans" :key="plan.id" class="plan-item">
            <h4>{{ plan.title }}</h4>
            <p>{{ plan.content }}</p>
            <el-image v-if="plan.reference_image_url" :src="plan.reference_image_url"
              style="width:100%;max-height:200px;object-fit:cover;border-radius:4px;margin:8px 0"
              preview-teleported :preview-src-list="[plan.reference_image_url]" />
            <div style="display:flex;gap:12px;align-items:center">
              <el-button size="small" @click="togglePlanLike(plan)">{{ plan.is_liked ? '❤' : '♡' }} {{ plan.likes_count }}</el-button>
              <a :href="`/api/export/plan/${plan.id}/pdf`" target="_blank" style="font-size:12px">导出PDF</a>
            </div>
            <CompareSlider v-if="plan.reference_image_url && plan.result_image_url"
              :before="plan.reference_image_url" :after="plan.result_image_url" />
          </div>
          <div v-if="plans.length === 0" style="text-align:center;color:#c0c4cc;padding:20px">
            暂无改造方案，快来提交第一个
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog v-model="showPlanForm" title="提交改造方案" width="600px">
      <el-form :model="newPlan">
        <el-form-item label="方案标题"><el-input v-model="newPlan.title" /></el-form-item>
        <el-form-item label="方案内容"><el-input v-model="newPlan.content" type="textarea" :rows="4" /></el-form-item>
        <el-form-item label="参考图片URL"><el-input v-model="newPlan.reference_image_url" /></el-form-item>
        <el-form-item label="成果图片URL"><el-input v-model="newPlan.result_image_url" /></el-form-item>
        <el-button type="primary" @click="submitPlan" :loading="planSubmitting">提交方案</el-button>
      </el-form>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getItem } from '../api/item'
import { listPlans, createPlan } from '../api/renovation'
import { listSteps, addStep } from '../api/progress'
import { toggleItemLike as apiToggleItemLike, togglePlanLike as apiTogglePlanLike, getItemLikes, getPlanLikes } from '../api/like'
import { useUserStore } from '../stores'
import ProgressBar from '../components/ProgressBar.vue'
import CompareSlider from '../components/CompareSlider.vue'

const route = useRoute()
const userStore = useUserStore()
const item = ref(null)
const plans = ref([])
const progress = ref([])
const itemLikeCount = ref(0)
const itemLiked = ref(false)
const showPlanForm = ref(false)
const showAddStep = ref(false)
const planSubmitting = ref(false)

const newPlan = ref({ title: '', content: '', reference_image_url: '', result_image_url: '', author_id: 1 })
const newStep = ref({ description: '', image_url: '' })

function categoryLabel(c) { return { clothing: '衣物', furniture: '家具', electronics: '电子', packaging: '包装' }[c] || c }
function difficultyType(d) { return { easy: 'success', medium: 'warning', hard: 'danger' }[d] || '' }
function difficultyLabel(d) { return { easy: '简单', medium: '中等', hard: '困难' }[d] || d }

async function load() {
  const id = Number(route.params.id)
  const res = await getItem(id)
  item.value = res.item
  progress.value = res.progress || []
  const planData = await listPlans(id)
  for (const p of planData) {
    const l = await getPlanLikes(p.id, userStore.userId)
    p.is_liked = l.is_liked
  }
  plans.value = planData
  const il = await getItemLikes(id, userStore.userId)
  itemLikeCount.value = il.count
  itemLiked.value = il.is_liked
}

async function toggleItemLike() {
  await apiToggleItemLike({ user_id: userStore.userId, target_id: item.value.id })
  itemLiked.value = !itemLiked.value
  itemLikeCount.value += itemLiked.value ? 1 : -1
}

async function togglePlanLike(plan) {
  await apiTogglePlanLike({ user_id: userStore.userId, target_id: plan.id })
  plan.is_liked = !plan.is_liked
  plan.likes_count += plan.is_liked ? 1 : -1
}

async function submitPlan() {
  if (!newPlan.value.title || !newPlan.value.content) { ElMessage.warning('请填写标题和内容'); return }
  planSubmitting.value = true
  try {
    await createPlan({ ...newPlan.value, item_id: item.value.id })
    ElMessage.success('方案提交成功')
    showPlanForm.value = false
    newPlan.value = { title: '', content: '', reference_image_url: '', result_image_url: '', author_id: 1 }
    await load()
  } catch { ElMessage.error('提交失败') }
  planSubmitting.value = false
}

async function submitStep() {
  if (!newStep.value.image_url) { ElMessage.warning('请填写图片URL'); return }
  await addStep({
    item_id: item.value.id,
    step_order: progress.value.length + 1,
    description: newStep.value.description,
    image_url: newStep.value.image_url,
  })
  ElMessage.success('步骤添加成功')
  showAddStep.value = false
  newStep.value = { description: '', image_url: '' }
  await load()
}

onMounted(load)
</script>

<style scoped>
.detail-page h2 { margin: 0; }
.detail-page h3 { margin: 0; }
.plan-item {
  padding: 12px 0; border-bottom: 1px solid #ebeef5;
}
.plan-item:last-child { border-bottom: none; }
</style>
