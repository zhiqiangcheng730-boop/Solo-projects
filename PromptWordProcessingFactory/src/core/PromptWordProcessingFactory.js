import { getSkillById } from '../skills/index.js';

class PromptWordProcessingFactory {
  async convert(text, skillIds) {
    if (!text || !text.trim()) {
      throw new Error('输入文本不能为空');
    }

    const ids = Array.isArray(skillIds) ? skillIds : [skillIds];
    if (ids.length === 0) {
      throw new Error('请至少选择一个 SKILL');
    }

    const skills = ids.map((id) => {
      const skill = getSkillById(id);
      if (!skill) throw new Error(`未找到 SKILL: ${id}`);
      return skill;
    });

    const combinedPrompt = skills
      .map((s, i) => `【步骤${i + 1}】${s.systemPrompt}`)
      .join('\n\n---\n\n');
    const avgTemp = skills.reduce((sum, s) => sum + s.options.temperature, 0) / skills.length;
    const maxTokens = Math.max(...skills.map((s) => s.options.maxTokens));

    const response = await fetch('/api/convert', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: text.trim(),
        systemPrompt: combinedPrompt,
        temperature: Math.round(avgTemp * 10) / 10,
        maxTokens,
      }),
    });

    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data.error || `请求失败 (${response.status})`);
    }

    const data = await response.json();
    return data.result;
  }
}

export const factory = new PromptWordProcessingFactory();
