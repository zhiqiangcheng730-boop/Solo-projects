import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { skills, transactions, matching, reviews, auth } from '../api'
import SkillCard from '../components/SkillCard'
import ReviewForm from '../components/ReviewForm'

export default function Dashboard({ user }) {
  const [mySkills, setMySkills] = useState([])
  const [myTxns, setMyTxns] = useState([])
  const [recs, setRecs] = useState([])
  const [myReviews, setMyReviews] = useState([])
  const [tab, setTab] = useState('skills')

  useEffect(() => {
    if (!user) return
    skills.list({}).then(({ data }) => setMySkills(data.filter((s) => s.user_id === user.id)))
    transactions.list(user.id).then(({ data }) => setMyTxns(data))
    matching.recommendations(user.id).then(({ data }) => setRecs(data))
    reviews.getUserReviews(user.id).then(({ data }) => setMyReviews(data))
  }, [user])

  if (!user) {
    return (
      <div className="text-center py-16">
        <p className="text-gray-400 mb-4">请先登录</p>
        <Link to="/login" className="text-indigo-600">去登录</Link>
      </div>
    )
  }

  const handleReview = (txnId) => async ({ rating, comment }) => {
    await reviews.create({ transaction_id: txnId, rating, comment }, user.id)
    const { data } = await reviews.getUserReviews(user.id)
    setMyReviews(data)
  }

  const handleDeactivate = async (skillId) => {
    await skills.deactivate(skillId, user.id)
    setMySkills((prev) => prev.map((s) => (s.id === skillId ? { ...s, is_active: false } : s)))
  }

  const txnActions = async (txnId, action) => {
    const fn = transactions[action]
    await fn(txnId, user.id)
    const { data } = await transactions.list(user.id)
    setMyTxns(data)
  }

  return (
    <div>
      <div className="bg-white rounded-xl border border-gray-200 p-6 mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-gray-800">{user.username}</h2>
            <p className="text-sm text-gray-500">{user.city} · 信用分 {user.credit_score}</p>
          </div>
          <div className="text-right">
            <p className="text-2xl font-bold text-amber-600">{user.time_coins}</p>
            <p className="text-xs text-gray-400">时间币</p>
          </div>
        </div>
      </div>

      <div className="flex gap-4 mb-4 text-sm">
        {['skills', 'transactions', 'matches', 'reviews'].map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-3 py-1.5 rounded-lg ${tab === t ? 'bg-indigo-100 text-indigo-700' : 'text-gray-500 hover:bg-gray-100'}`}
          >
            {t === 'skills' ? '我的技能' : t === 'transactions' ? '交易记录' : t === 'matches' ? '推荐匹配' : '我的评价'}
          </button>
        ))}
        <Link to="/post-skill" className="ml-auto bg-indigo-600 text-white px-3 py-1.5 rounded-lg text-sm hover:bg-indigo-700">
          发布技能
        </Link>
      </div>

      {tab === 'skills' && (
        <div>
          {mySkills.length === 0 ? (
            <p className="text-gray-400 text-center py-8">还没有发布技能</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {mySkills.map((s) => (
                <div key={s.id}>
                  <SkillCard skill={s} />
                  {s.is_active && (
                    <button
                      onClick={() => handleDeactivate(s.id)}
                      className="text-xs text-red-400 mt-1 hover:text-red-600"
                    >
                      下架
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {tab === 'transactions' && (
        <div className="space-y-3">
          {myTxns.length === 0 ? (
            <p className="text-gray-400 text-center py-8">暂无交易</p>
          ) : (
            myTxns.map((t) => (
              <div key={t.id} className="bg-white rounded-lg border border-gray-200 p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-800">
                    交易 #{t.id} · {t.hours}小时 · {t.coins}币
                  </span>
                  <span className={`text-xs px-2 py-0.5 rounded-full ${
                    t.status === 'completed' ? 'bg-green-100 text-green-700' :
                    t.status === 'accepted' ? 'bg-blue-100 text-blue-700' :
                    t.status === 'cancelled' ? 'bg-red-100 text-red-700' :
                    'bg-yellow-100 text-yellow-700'
                  }`}>
                    {t.status === 'pending' ? '待接受' :
                     t.status === 'accepted' ? '进行中' :
                     t.status === 'completed' ? '已完成' : '已取消'}
                  </span>
                </div>
                <div className="text-xs text-gray-400 mb-2">
                  从 #{t.from_user_id} 到 #{t.to_user_id} · {new Date(t.created_at).toLocaleDateString()}
                </div>
                {t.status === 'pending' && t.to_user_id === user.id && (
                  <button onClick={() => txnActions(t.id, 'accept')} className="text-xs text-indigo-600 mr-2 hover:underline">接受</button>
                )}
                {t.status === 'accepted' && (t.from_user_id === user.id || t.to_user_id === user.id) && (
                  <button onClick={() => txnActions(t.id, 'complete')} className="text-xs text-green-600 mr-2 hover:underline">完成</button>
                )}
                {t.status === 'pending' && t.from_user_id === user.id && (
                  <button onClick={() => txnActions(t.id, 'cancel')} className="text-xs text-red-400 hover:underline">取消</button>
                )}
                {t.status === 'completed' && (
                  <ReviewForm onSubmit={handleReview(t.id)} />
                )}
              </div>
            ))
          )}
        </div>
      )}

      {tab === 'matches' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {recs.length === 0 ? (
            <p className="text-gray-400 col-span-full text-center py-8">暂无推荐</p>
          ) : (
            recs.map((s) => <SkillCard key={s.id} skill={s} />)
          )}
        </div>
      )}

      {tab === 'reviews' && (
        <div className="space-y-3">
          {myReviews.length === 0 ? (
            <p className="text-gray-400 text-center py-8">暂无评价</p>
          ) : (
            myReviews.map((r) => (
              <div key={r.id} className="bg-white rounded-lg border border-gray-200 p-4">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-yellow-400">{'★'.repeat(r.rating)}{'☆'.repeat(5 - r.rating)}</span>
                  <span className="text-xs text-gray-400">{new Date(r.created_at).toLocaleDateString()}</span>
                </div>
                {r.comment && <p className="text-sm text-gray-600">{r.comment}</p>}
              </div>
            ))
          )}
        </div>
      )}
    </div>
  )
}
