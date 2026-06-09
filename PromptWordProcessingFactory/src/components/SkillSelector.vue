<template>
  <div class="skill-selector">
    <button
      v-for="(skill, index) in skills"
      :key="skill.id"
      :class="['skill-card', { active: modelValue.includes(skill.id) }]"
      type="button"
      @click="toggle(skill.id)"
    >
      <span class="skill-index">{{ String(index + 1).padStart(2, '0') }}</span>

      <span class="skill-main">
        <span class="skill-name">{{ skill.name }}</span>
        <span class="skill-desc">{{ skill.description }}</span>
      </span>

      <span class="skill-state">
        <span class="state-dot"></span>
        {{ modelValue.includes(skill.id) ? '已启用' : '待启用' }}
      </span>
    </button>
  </div>
</template>

<script setup>
import { getAllSkills } from '../skills/index.js';

const skills = getAllSkills();

const props = defineProps({
  modelValue: { type: Array, required: true },
});

const emit = defineEmits(['update:modelValue']);

function toggle(skillId) {
  const next = props.modelValue.includes(skillId)
    ? props.modelValue.filter((id) => id !== skillId)
    : [...props.modelValue, skillId];
  emit('update:modelValue', next);
}
</script>

<style scoped>
.skill-selector {
  display: grid;
  gap: 12px;
}

.skill-card {
  display: grid;
  grid-template-columns: 42px 1fr auto;
  gap: 16px;
  align-items: start;
  padding: 18px 20px;
  border: 1px solid rgba(128, 202, 255, 0.14);
  border-radius: 22px;
  background: rgba(7, 15, 33, 0.44);
  text-align: left;
  cursor: pointer;
  transition:
    transform 0.2s ease,
    border-color 0.2s ease,
    background 0.2s ease,
    box-shadow 0.2s ease;
}

.skill-card:hover {
  transform: translateY(-1px);
  border-color: rgba(128, 202, 255, 0.24);
  box-shadow: 0 18px 30px rgba(0, 0, 0, 0.18);
}

.skill-card.active {
  border-color: rgba(122, 241, 255, 0.42);
  background:
    linear-gradient(135deg, rgba(122, 241, 255, 0.08), rgba(91, 125, 255, 0.16)),
    rgba(7, 15, 33, 0.58);
}

.skill-index {
  padding-top: 2px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.14em;
  color: rgba(162, 198, 225, 0.78);
}

.skill-main {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}

.skill-name {
  font-size: 20px;
  font-weight: 600;
  letter-spacing: -0.03em;
  color: #f1fbff;
}

.skill-desc {
  font-size: 14px;
  line-height: 1.8;
  color: rgba(214, 233, 247, 0.68);
}

.skill-state {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding-top: 4px;
  font-size: 12px;
  color: rgba(171, 203, 231, 0.72);
  white-space: nowrap;
}

.state-dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: rgba(168, 191, 211, 0.45);
}

.skill-card.active .state-dot {
  background: #7af1ff;
  box-shadow: 0 0 16px rgba(122, 241, 255, 0.8);
}

.skill-card.active .skill-state {
  color: #effdff;
}

@media (max-width: 640px) {
  .skill-card {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .skill-name {
    font-size: 18px;
  }
}
</style>
