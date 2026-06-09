import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { skills } from '../api'

const CATEGORIES = ['编程开发', '语言学习', '设计创意', '生活服务', '运动健身', '音乐艺术', '宠物照看', '搬家运输', '其他']

export default function PostSkill({ user }) {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    type: 'offer', title: '', description: '', category: '编程开发',
    tags: '', city: user?.city || '', lat: user?.lat || 0, lon: user?.lon || 0,
    is_urgent: false, urgent_reason: '', urgent_deadline: '',
  })
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!user) return setError('请先登录')
    setError('')
    try {
      const tags = form.tags.split(',').map((t) => t.trim()).filter(Boolean)
      await skills.create({ ...form, tags }, user.id)
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.detail || '发布失败')
    }
  }

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value })

  if (!user) return <p className="text-gray-400 text-center py-8">请先登录</p>

  return (
    <div className="max-w-lg mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">发布技能</h2>
      {error && <p className="text-red-500 text-sm mb-3">{error}</p>}
      <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
        <div className="flex gap-3">
          <label className="flex items-center gap-1 text-sm">
            <input type="radio" name="type" checked={form.type === 'offer'} onChange={() => setForm({ ...form, type: 'offer' })} />
            提供服务
          </label>
          <label className="flex items-center gap-1 text-sm">
            <input type="radio" name="type" checked={form.type === 'request'} onChange={() => setForm({ ...form, type: 'request' })} />
            寻求帮助
          </label>
        </div>

        <input className="w-full border border-gray-200 rounded-lg p-2.5 text-sm" placeholder="标题" value={form.title} onChange={set('title')} required />
        <textarea className="w-full border border-gray-200 rounded-lg p-2.5 text-sm" rows={3} placeholder="详细描述..." value={form.description} onChange={set('description')} />

        <select className="w-full border border-gray-200 rounded-lg p-2.5 text-sm" value={form.category} onChange={set('category')}>
          {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
        </select>

        <input className="w-full border border-gray-200 rounded-lg p-2.5 text-sm" placeholder="标签，用逗号分隔（如: Python,教学,线上）" value={form.tags} onChange={set('tags')} />
        <input className="w-full border border-gray-200 rounded-lg p-2.5 text-sm" placeholder="所在城市" value={form.city} onChange={set('city')} required />

        <label className="flex items-center gap-2 text-sm">
          <input type="checkbox" checked={form.is_urgent} onChange={(e) => setForm({ ...form, is_urgent: e.target.checked })} />
          标记为紧急需求
        </label>
        {form.is_urgent && (
          <>
            <input className="w-full border border-gray-200 rounded-lg p-2.5 text-sm" placeholder="紧急原因" value={form.urgent_reason} onChange={set('urgent_reason')} />
            <input className="w-full border border-gray-200 rounded-lg p-2.5 text-sm" type="datetime-local" value={form.urgent_deadline} onChange={set('urgent_deadline')} />
          </>
        )}

        <button type="submit" className="w-full bg-indigo-600 text-white py-2.5 rounded-lg text-sm hover:bg-indigo-700">
          发布
        </button>
      </form>
    </div>
  )
}
