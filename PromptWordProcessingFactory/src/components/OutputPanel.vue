<template>
  <div :class="['output-panel', statusClass]">
    <div class="output-toolbar">
      <div class="toolbar-copy">
        <span class="toolbar-label">Refined draft</span>
        <span class="toolbar-status">{{ statusText }}</span>
      </div>

      <button
        v-if="result && !loading"
        class="copy-btn"
        type="button"
        @click="copy"
      >
        {{ copied ? '已复制' : '复制结果' }}
      </button>
    </div>

    <div v-if="loading" class="state">
      <span class="loading-ring"></span>
      <h3>正在处理文本</h3>
      <p>系统会根据当前策略重新组织表达，通常几秒内返回结果。</p>
    </div>

    <div v-else-if="error" class="state is-error">
      <h3>这次处理没有成功</h3>
      <p>{{ error }}</p>
    </div>

    <div v-else-if="!result" class="state">
      <h3>结果会显示在这里</h3>
      <p>完成输入并点击“开始转换”后，这里会出现新的文本版本。</p>
    </div>

    <div v-else class="result-area">
      <div class="result-text">{{ result }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue';

const props = defineProps({
  result: { type: String, default: '' },
  loading: { type: Boolean, default: false },
  error: { type: String, default: '' },
});

const copied = ref(false);

const statusText = computed(() => {
  if (props.loading) return '处理中';
  if (props.error) return '处理失败';
  if (props.result) return '已生成';
  return '等待生成';
});

const statusClass = computed(() => {
  if (props.loading) return 'is-loading';
  if (props.error) return 'is-error';
  if (props.result) return 'has-result';
  return 'is-empty';
});

watch(
  () => props.result,
  () => {
    copied.value = false;
  },
);

async function copy() {
  try {
    await navigator.clipboard.writeText(props.result);
    copied.value = true;
    setTimeout(() => {
      copied.value = false;
    }, 2000);
  } catch {
    copied.value = false;
  }
}
</script>

<style scoped>
.output-panel {
  overflow: hidden;
  border: 1px solid rgba(139, 211, 255, 0.16);
  border-radius: 24px;
  background:
    linear-gradient(180deg, rgba(7, 15, 34, 0.82), rgba(4, 10, 24, 0.72));
  backdrop-filter: blur(20px);
}

.output-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 16px 18px;
  border-bottom: 1px solid rgba(139, 211, 255, 0.1);
}

.toolbar-copy {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.toolbar-label {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: rgba(171, 203, 231, 0.64);
}

.toolbar-status {
  font-size: 14px;
  color: #edf9ff;
}

.copy-btn {
  padding: 8px 12px;
  border: 1px solid rgba(130, 222, 255, 0.16);
  border-radius: 999px;
  color: rgba(239, 249, 255, 0.88);
  cursor: pointer;
  transition: background 0.2s ease, border-color 0.2s ease;
}

.copy-btn:hover {
  border-color: rgba(130, 222, 255, 0.28);
  background: rgba(91, 125, 255, 0.14);
}

.state,
.result-area {
  min-height: 560px;
}

.state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 14px;
  padding: 28px;
  text-align: center;
}

.state h3 {
  font-family: 'Bahnschrift', 'Segoe UI Variable Display', 'Microsoft YaHei UI', sans-serif;
  font-size: 32px;
  line-height: 1.1;
  color: #f4fbff;
}

.state p {
  max-width: 360px;
  font-size: 14px;
  line-height: 1.85;
  color: rgba(215, 234, 247, 0.66);
}

.state.is-error h3 {
  color: #ffd1d1;
}

.loading-ring {
  width: 28px;
  height: 28px;
  border: 2px solid rgba(130, 222, 255, 0.18);
  border-top-color: #7af1ff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.result-area {
  padding: 18px;
}

.result-text {
  min-height: 100%;
  padding: 18px;
  border: 1px solid rgba(132, 199, 255, 0.08);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.02);
  color: #f3fbff;
  font-size: 15px;
  line-height: 1.95;
  white-space: pre-wrap;
  word-break: break-word;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 720px) {
  .state,
  .result-area {
    min-height: 360px;
  }

  .output-panel {
    border-radius: 20px;
  }

  .output-toolbar {
    flex-direction: column;
    align-items: flex-start;
  }

  .state h3 {
    font-size: 28px;
  }
}
</style>
