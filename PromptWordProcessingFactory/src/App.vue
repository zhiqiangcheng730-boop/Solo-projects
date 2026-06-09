<template>
  <div class="app-shell">
    <header class="topbar glass-panel">
      <div class="brand">
        <span class="brand-mark"></span>
        <div>
          <p class="brand-overline">PromptWordProcessingFactory</p>
          <h1 class="brand-title">提示词精修工厂</h1>
        </div>
      </div>

      <div class="topbar-status">
        <span class="status-dot"></span>
        <span>{{ loading ? '处理中' : '系统待命' }}</span>
      </div>
    </header>

    <section class="hero glass-panel">
      <div class="hero-copy">
        <span class="eyebrow">Glass workflow / future editing lab</span>
        <h2 class="hero-title">保留原流程，把提示词处理做得更清晰、更顺手。</h2>
        <p class="hero-description">
          先选处理策略，再贴入原文，最后直接拿到优化后的版本。界面只保留高频动作，
          用更轻的操作路径把“选择、输入、输出”三步串起来。
        </p>

        <div class="hero-tags">
          <span class="hero-tag">毛玻璃面板</span>
          <span class="hero-tag">科技蓝高光</span>
          <span class="hero-tag">多策略叠加</span>
        </div>
      </div>

      <div class="hero-metrics">
        <article class="metric-card">
          <span class="metric-label">已选策略</span>
          <strong class="metric-value">{{ selectedSkills.length }}</strong>
          <span class="metric-foot">当前组合</span>
        </article>
        <article class="metric-card">
          <span class="metric-label">输入字数</span>
          <strong class="metric-value">{{ inputText.length }}</strong>
          <span class="metric-foot">原文长度</span>
        </article>
        <article class="metric-card">
          <span class="metric-label">输出字数</span>
          <strong class="metric-value">{{ outputText.length }}</strong>
          <span class="metric-foot">结果统计</span>
        </article>
      </div>
    </section>

    <section class="workflow-strip">
      <article class="workflow-card glass-panel">
        <span class="workflow-index">01</span>
        <h3>选择策略</h3>
        <p>按目标选自然化、去 AI 味或流畅度优化，也可以叠加使用。</p>
      </article>
      <article class="workflow-card glass-panel">
        <span class="workflow-index">02</span>
        <h3>贴入原文</h3>
        <p>直接粘贴待处理文本，不需要提前重写结构，保留最原始状态即可。</p>
      </article>
      <article class="workflow-card glass-panel">
        <span class="workflow-index">03</span>
        <h3>生成并交付</h3>
        <p>处理完成后在右侧查看结果，一键复制，继续迭代下一版。</p>
      </article>
    </section>

    <main class="studio-grid">
      <section class="control-panel glass-panel">
        <div class="panel-header">
          <div>
            <span class="section-kicker">Method matrix</span>
            <h3 class="section-title">处理策略</h3>
          </div>
          <span class="section-meta">支持组合使用</span>
        </div>

        <SkillSelector v-model="selectedSkill" />

        <div class="panel-divider"></div>

        <div class="panel-header">
          <div>
            <span class="section-kicker">Source input</span>
            <h3 class="section-title">原始文本</h3>
          </div>
          <span class="section-meta">{{ inputText.length }} 字</span>
        </div>

        <InputPanel v-model="inputText" />

        <div class="status-board">
          <div class="status-copy">
            <span class="section-kicker">System signal</span>
            <p class="status-text">{{ statusText }}</p>
          </div>

          <button
            class="convert-btn"
            type="button"
            :disabled="!canConvert"
            @click="handleConvert"
          >
            <span v-if="loading" class="btn-inner">
              <span class="btn-spinner"></span>
              正在处理
            </span>
            <span v-else class="btn-inner">开始转换</span>
          </button>
        </div>
      </section>

      <aside class="result-panel glass-panel">
        <div class="result-head">
          <div>
            <span class="section-kicker">Output stage</span>
            <h3 class="section-title result-title">输出结果</h3>
          </div>
          <span class="result-status">{{ resultMeta }}</span>
        </div>

        <div class="result-summary">
          <article class="summary-card">
            <span class="summary-label">当前策略</span>
            <strong class="summary-value">{{ selectedSkillNames }}</strong>
          </article>
          <article class="summary-card">
            <span class="summary-label">处理模式</span>
            <strong class="summary-value">
              {{ selectedSkills.length > 1 ? '多策略叠加' : '单策略精修' }}
            </strong>
          </article>
        </div>

        <OutputPanel
          :result="outputText"
          :loading="loading"
          :error="errorText"
        />
      </aside>
    </main>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import SkillSelector from './components/SkillSelector.vue';
import InputPanel from './components/InputPanel.vue';
import OutputPanel from './components/OutputPanel.vue';
import { factory } from './core/PromptWordProcessingFactory.js';
import { getAllSkills } from './skills/index.js';

const skills = getAllSkills();
const selectedSkill = ref([skills[0]?.id].filter(Boolean));
const inputText = ref('');
const outputText = ref('');
const loading = ref(false);
const errorText = ref('');

const selectedSkills = computed(() =>
  skills.filter((skill) => selectedSkill.value.includes(skill.id)),
);

const canConvert = computed(
  () => Boolean(inputText.value.trim()) && selectedSkills.value.length > 0 && !loading.value,
);

const selectedSkillNames = computed(() => {
  if (!selectedSkills.value.length) {
    return '未选择策略';
  }

  return selectedSkills.value.map((skill) => skill.name).join(' / ');
});

const statusText = computed(() => {
  if (loading.value) return '系统正在根据当前策略重写文本，请稍等片刻。';
  if (!selectedSkills.value.length) return '先选择本轮要启用的处理策略。';
  if (!inputText.value.trim()) return '贴入待处理文本后，就可以开始生成结果。';
  if (outputText.value) return '结果已生成，可以直接复制，也可以继续切换策略再试一版。';
  return `准备按“${selectedSkillNames.value}”处理这段文本。`;
});

const resultMeta = computed(() => {
  if (loading.value) return '处理中';
  if (errorText.value) return '处理失败';
  if (outputText.value) return '已生成';
  return '等待生成';
});

async function handleConvert() {
  if (!canConvert.value) {
    return;
  }

  loading.value = true;
  errorText.value = '';
  outputText.value = '';

  try {
    const result = await factory.convert(inputText.value, selectedSkill.value);
    outputText.value = result;
  } catch (err) {
    errorText.value = err.message || '转换失败，请稍后重试';
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.app-shell {
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.glass-panel {
  position: relative;
  overflow: hidden;
  border: 1px solid var(--panel-border);
  background: var(--panel-bg);
  box-shadow: var(--panel-shadow);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
}

.glass-panel::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    linear-gradient(135deg, rgba(122, 241, 255, 0.14), transparent 28%),
    radial-gradient(circle at top right, rgba(110, 142, 255, 0.16), transparent 32%);
  pointer-events: none;
}

.topbar,
.hero,
.workflow-card,
.control-panel,
.result-panel {
  border-radius: 28px;
}

.topbar,
.panel-header,
.result-head,
.status-board {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.topbar {
  padding: 18px 22px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 14px;
}

.brand-mark,
.status-dot {
  flex: none;
  border-radius: 999px;
}

.brand-mark {
  width: 14px;
  height: 14px;
  background: linear-gradient(135deg, #88f5ff 0%, #5b7dff 100%);
  box-shadow: 0 0 22px rgba(111, 219, 255, 0.72);
}

.brand-overline,
.eyebrow,
.section-kicker,
.workflow-index,
.metric-label,
.summary-label {
  font-size: 11px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--text-muted);
}

.brand-title {
  margin-top: 4px;
  font-size: 22px;
  font-weight: 600;
  color: var(--text-strong);
}

.topbar-status {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border: 1px solid rgba(128, 220, 255, 0.18);
  border-radius: 999px;
  background: rgba(8, 20, 43, 0.46);
  color: var(--text-soft);
  font-size: 13px;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: #79f5ff;
  box-shadow: 0 0 18px rgba(121, 245, 255, 0.9);
}

.hero {
  display: grid;
  grid-template-columns: minmax(0, 1.18fr) minmax(280px, 0.82fr);
  gap: 24px;
  padding: 32px;
}

.hero-title {
  max-width: 720px;
  margin-top: 14px;
  font-family: 'Bahnschrift', 'Segoe UI Variable Display', 'Microsoft YaHei UI', sans-serif;
  font-size: clamp(38px, 5vw, 62px);
  line-height: 1.04;
  letter-spacing: -0.05em;
  color: var(--text-strong);
  text-wrap: balance;
}

.hero-description {
  max-width: 700px;
  margin-top: 18px;
  font-size: 16px;
  line-height: 1.9;
  color: var(--text-soft);
}

.hero-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 22px;
}

.hero-tag {
  padding: 10px 14px;
  border: 1px solid rgba(127, 224, 255, 0.16);
  border-radius: 999px;
  background: rgba(7, 18, 40, 0.38);
  color: #dffcff;
  font-size: 13px;
}

.hero-metrics {
  display: grid;
  gap: 14px;
}

.metric-card {
  position: relative;
  padding: 20px;
  border: 1px solid rgba(122, 187, 255, 0.14);
  border-radius: 22px;
  background: rgba(5, 13, 30, 0.44);
}

.metric-value {
  display: block;
  margin-top: 14px;
  font-size: clamp(34px, 4vw, 46px);
  line-height: 1;
  color: #f3fcff;
}

.metric-foot {
  display: block;
  margin-top: 8px;
  font-size: 13px;
  color: var(--text-soft);
}

.workflow-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.workflow-card {
  padding: 22px;
}

.workflow-card h3 {
  margin-top: 14px;
  font-size: 22px;
  color: var(--text-strong);
}

.workflow-card p {
  margin-top: 10px;
  font-size: 14px;
  line-height: 1.85;
  color: var(--text-soft);
}

.studio-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(360px, 0.95fr);
  gap: 18px;
  align-items: start;
}

.control-panel,
.result-panel {
  padding: 28px;
}

.section-title {
  margin-top: 8px;
  font-size: 30px;
  letter-spacing: -0.04em;
  color: var(--text-strong);
}

.section-meta,
.result-status {
  font-size: 13px;
  color: var(--text-muted);
  white-space: nowrap;
}

.panel-divider {
  height: 1px;
  margin: 24px 0;
  background: linear-gradient(90deg, transparent, rgba(132, 198, 255, 0.18), transparent);
}

.status-board {
  margin-top: 20px;
  padding: 18px 20px;
  border: 1px solid rgba(123, 197, 255, 0.12);
  border-radius: 22px;
  background: rgba(6, 16, 37, 0.42);
}

.status-copy {
  min-width: 0;
}

.status-text {
  margin-top: 8px;
  font-size: 14px;
  line-height: 1.8;
  color: var(--text-soft);
}

.convert-btn {
  min-width: 160px;
  padding: 15px 22px;
  border: 1px solid rgba(132, 239, 255, 0.32);
  border-radius: 16px;
  background:
    linear-gradient(135deg, rgba(121, 245, 255, 0.24), rgba(91, 125, 255, 0.4));
  color: #f4fdff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    opacity 0.2s ease;
  box-shadow: 0 16px 28px rgba(58, 102, 227, 0.22);
}

.convert-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 20px 38px rgba(58, 102, 227, 0.32);
}

.convert-btn:disabled {
  opacity: 0.42;
  cursor: not-allowed;
}

.btn-inner {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.24);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.result-title {
  font-size: 34px;
}

.result-summary {
  display: grid;
  gap: 12px;
  margin: 22px 0 20px;
}

.summary-card {
  padding: 16px 18px;
  border: 1px solid rgba(136, 207, 255, 0.12);
  border-radius: 20px;
  background: rgba(6, 15, 34, 0.34);
}

.summary-value {
  display: block;
  margin-top: 10px;
  color: #f1fbff;
  font-size: 15px;
  line-height: 1.7;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 1120px) {
  .hero,
  .studio-grid,
  .workflow-strip {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 720px) {
  .topbar,
  .hero,
  .workflow-card,
  .control-panel,
  .result-panel {
    border-radius: 22px;
  }

  .topbar,
  .hero,
  .control-panel,
  .result-panel {
    padding: 20px;
  }

  .topbar,
  .status-board,
  .panel-header,
  .result-head {
    flex-direction: column;
    align-items: flex-start;
  }

  .hero-title {
    font-size: clamp(34px, 12vw, 48px);
  }

  .section-title {
    font-size: 26px;
  }

  .convert-btn {
    width: 100%;
  }
}
</style>
