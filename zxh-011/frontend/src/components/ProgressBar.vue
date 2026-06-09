<template>
  <div class="progress-bar">
    <div class="steps">
      <div v-for="(step, idx) in steps" :key="step.id" class="step" :class="{ active: idx <= currentStep }">
        <div class="step-dot">{{ idx + 1 }}</div>
        <img v-if="step.image_url" :src="step.image_url" class="step-img" @click="previewUrl = step.image_url" />
        <div class="step-desc">{{ step.description }}</div>
      </div>
    </div>
    <el-progress :percentage="progressPercent" :stroke-width="10" :color="progressColor" />
    <el-dialog v-model="showPreview" title="步骤图片" width="600px">
      <img :src="previewUrl" style="width: 100%; border-radius: 8px;" />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  steps: { type: Array, default: () => [] },
  currentStep: { type: Number, default: 0 },
})

const previewUrl = ref('')
const showPreview = ref(false)

const progressPercent = computed(() =>
  props.steps.length ? Math.round((props.currentStep / (props.steps.length - 1 || 1)) * 100) : 0
)

const progressColor = computed(() => {
  if (progressPercent.value >= 80) return '#67c23a'
  if (progressPercent.value >= 40) return '#e6a23c'
  return '#409eff'
})
</script>

<style scoped>
.progress-bar { padding: 16px 0; }
.steps { display: flex; gap: 16px; margin-bottom: 16px; overflow-x: auto; }
.step { display: flex; flex-direction: column; align-items: center; gap: 6px; min-width: 80px; opacity: .5; }
.step.active { opacity: 1; }
.step-dot {
  width: 32px; height: 32px; border-radius: 50%; background: #c0c4cc; color: #fff;
  display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: bold;
}
.step.active .step-dot { background: #409eff; }
.step-img { width: 60px; height: 60px; object-fit: cover; border-radius: 6px; cursor: pointer; }
.step-desc { font-size: 12px; color: #909399; text-align: center; max-width: 80px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
</style>
