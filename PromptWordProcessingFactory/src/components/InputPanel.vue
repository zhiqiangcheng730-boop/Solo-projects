<template>
  <div class="input-panel">
    <div class="panel-toolbar">
      <div class="toolbar-copy">
        <span class="toolbar-label">Raw prompt</span>
        <span class="toolbar-meta">保留原始表达，系统会按策略处理</span>
      </div>

      <button
        v-if="modelValue.length"
        class="toolbar-button"
        type="button"
        @click="$emit('update:modelValue', '')"
      >
        清空
      </button>
    </div>

    <textarea
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      placeholder="把需要处理的提示词、文案或草稿直接贴在这里。先不用提前润色，保留原本状态，结果通常会更稳定。"
      rows="15"
    ></textarea>

    <div class="input-footer">
      <span>{{ modelValue.length }} 字</span>
      <span>建议直接粘贴完整内容，不必先拆句重写</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  modelValue: { type: String, required: true },
});

defineEmits(['update:modelValue']);
</script>

<style scoped>
.input-panel {
  overflow: hidden;
  border: 1px solid rgba(127, 202, 255, 0.16);
  border-radius: 24px;
  background: rgba(5, 12, 28, 0.48);
  backdrop-filter: blur(18px);
}

.panel-toolbar,
.input-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 16px 18px;
}

.panel-toolbar {
  border-bottom: 1px solid rgba(127, 202, 255, 0.12);
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
  color: rgba(162, 198, 225, 0.84);
}

.toolbar-meta,
.input-footer {
  font-size: 12px;
  color: rgba(213, 232, 247, 0.6);
}

.toolbar-button {
  padding: 8px 12px;
  border: 1px solid rgba(130, 222, 255, 0.16);
  border-radius: 999px;
  color: rgba(233, 247, 255, 0.82);
  cursor: pointer;
  transition: background 0.2s ease, border-color 0.2s ease, color 0.2s ease;
}

.toolbar-button:hover {
  border-color: rgba(130, 222, 255, 0.28);
  background: rgba(96, 196, 255, 0.08);
  color: #fff;
}

textarea {
  width: 100%;
  min-height: 420px;
  padding: 22px 18px;
  border: none;
  outline: none;
  resize: vertical;
  background: transparent;
  color: #eef9ff;
  font-size: 15px;
  line-height: 1.9;
}

textarea::placeholder {
  color: rgba(185, 213, 233, 0.44);
}

.input-footer {
  border-top: 1px solid rgba(127, 202, 255, 0.12);
}

@media (max-width: 640px) {
  .input-panel {
    border-radius: 20px;
  }

  .panel-toolbar,
  .input-footer {
    flex-direction: column;
    align-items: flex-start;
  }

  textarea {
    min-height: 320px;
    font-size: 14px;
  }
}
</style>
