import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { skills as skillsApi, matching, transactions, auth } from '../api'
import SkillCard from '../components/SkillCard'
import UrgentBadge from '../components/UrgentBadge'

export default function SkillDetail({ user }) {
  const { id } = useParams()
  const [skill, setSkill] = useState(null)
  const [matches, setMatches] = useState([])
  const [provider, setProvider] = useState(null)
  const [hours, setHours] = useState(1)
  const [message, setMessage] = useState('')

  useEffect(() => {
    skillsApi.getById(id).then(async ({ data }) => {
      setSkill(data)
      const [{ data: m }, { data: u }] = await Promise.all([
        matching.matchSkill(data.id),
        auth.getUser(data.user_id),
      ])
      setMatches(m)
      setProvider(u)
    })
  }, [id])

  const handleCreateTxn = async () => {
    if (!user) return setMessage('请先登录')
    try {
      await transactions.create({ to_user_id: skill.user_id, skill_id: skill.id, hours, coins: hours }, user.id)
      setMessage('交易请求已发送')
    } catch (err) {
      setMessage(err.response?.data?.detail || '交易失败')
    }
  }

  if (!skill) return <p className="text-gray-400 text-center py-8">加载中...</p>

  const tags = JSON.parse(skill.tags || '[]')

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2 space-y-4">
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <div className="flex items-center gap-2 mb-2">
            <span className={`text-xs px-2 py-0.5 rounded-full ${
              skill.type === 'offer' ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'
            }`}>
              {skill.type === 'offer' ? '提供服务' : '寻求帮助'}
            </span>
            {skill.is_urgent && <UrgentBadge reason={skill.urgent_reason} />}
          </div>
          <h2 className="text-xl font-bold text-gray-800 mb-2">{skill.title}</h2>
          <p className="text-gray-600 mb-3">{skill.description}</p>
          <div className="flex flex-wrap gap-1 mb-3">
            {tags.map((t, i) => (
              <span key={i} className="text-xs bg-indigo-50 text-indigo-600 px-2 py-0.5 rounded">{t}</span>
            ))}
          </div>
          <div className="text-sm text-gray-400 flex gap-4">
            <span>分类: {skill.category}</span>
            <span>城市: {skill.city}</span>
            {provider && <span>发布者: {provider.username} (信用 {provider.credit_score})</span>}
          </div>
        </div>

        <div>
          <h3 className="font-semibold text-gray-700 mb-3">匹配推荐</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {matches.length === 0 ? (
              <p className="text-gray-400 text-sm">暂无匹配</p>
            ) : (
              matches.map((m) => <SkillCard key={m.id} skill={m} />)
            )}
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <div className="bg-white rounded-xl border border-gray-200 p-4">
          <h4 className="font-semibold text-gray-700 mb-3">发起交易</h4>
          {message && <p className={`text-sm mb-2 ${message.includes('成功') ? 'text-green-600' : 'text-red-500'}`}>{message}</p>}
          <label className="text-sm text-gray-500 block mb-1">服务时长（小时）</label>
          <input
            type="number"
            min="1"
            max="24"
            value={hours}
            onChange={(e) => setHours(parseInt(e.target.value) || 1)}
            className="w-full border border-gray-200 rounded-lg p-2 text-sm mb-2"
          />
          <p className="text-xs text-gray-400 mb-3">需要 {hours} 时间币</p>
          <button
            onClick={handleCreateTxn}
            disabled={!user || user.id === skill.user_id}
            className="w-full bg-indigo-600 text-white py-2 rounded-lg text-sm hover:bg-indigo-700 disabled:bg-gray-300"
          >
            {!user ? '请先登录' : user.id === skill.user_id ? '不能交易自己的技能' : '发起交易'}
          </button>
        </div>

        {provider && (
          <div className="bg-white rounded-xl border border-gray-200 p-4">
            <h4 className="font-semibold text-gray-700 mb-2">发布者信息</h4>
            <p className="text-sm text-gray-800">{provider.username}</p>
            <p className="text-xs text-gray-400">{provider.city}</p>
            <p className="text-xs text-gray-400">信用分: {provider.credit_score}</p>
          </div>
        )}
      </div>
    </div>
  )
}
