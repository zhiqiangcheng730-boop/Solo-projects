import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import Anthropic from '@anthropic-ai/sdk';

const app = express();
app.use(cors());
app.use(express.json({ limit: '100kb' }));

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
  baseURL: process.env.ANTHROPIC_BASE_URL || undefined,
});

app.post('/api/convert', async (req, res) => {
  const { text, systemPrompt, temperature, maxTokens } = req.body;

  if (!text) {
    return res.status(400).json({ error: 'text 不能为空' });
  }
  if (!systemPrompt) {
    return res.status(400).json({ error: 'systemPrompt 不能为空' });
  }

  try {
    const response = await anthropic.messages.create({
      model: 'claude-sonnet-4-6',
      max_tokens: maxTokens || 2000,
      temperature: temperature ?? 0.7,
      system: systemPrompt,
      messages: [{ role: 'user', content: text }],
    });

    const content = response.content
      .filter((block) => block.type === 'text')
      .map((block) => block.text)
      .join('');

    res.json({ result: content });
  } catch (err) {
    console.error('API 调用失败:', err.message);
    res.status(500).json({ error: err.message || '转换失败' });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
