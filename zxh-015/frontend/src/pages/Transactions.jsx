import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { transactions as txnApi, reviews } from '../api'
import ReviewForm from '../components/ReviewForm'

export default function Transactions({ user }) {
  const [txns, setTxns] = useState([])
  const [message, setMessage] = useState('')

  useEffect(() => {
    if (user) txnApi.list(user.id).then(({ data }) => setTxns(data))
  }, [user])

  if (!user) {
    return (
      <div className="text-center py-16">
        <p className="text-gray-400 mb-4">请先登录查看交易记录</p>
        <Link to="/login" className="text-indigo-600">去登录</Link>
      </div>
    )
  }

  const handleAction = async (txnId, action) => {
    setMessage('')
    try {
      await txnApi[action](txnId, user.id)
      const { data } = await txnApi.list(user.id)
      setTxns(data)
    } catch (err) {
      setMessage(err.response?.data?.detail || '操作失败')
    }
  }

  const handleReview = (txnId) => async ({ rating, comment }) => {
    await reviews.create({ transaction_id: txnId, rating, comment }, user.id)
    const { data } = await txnApi.list(user.id)
    setTxns(data)
  }

  const statusText = {
    pending: '待接受', accepted: '进行中', completed: '已完成', cancelled: '已取消',
  }
  const statusColor = {
    pending: 'bg-yellow-100 text-yellow-700',
    accepted: 'bg-blue-100 text-blue-700',
    completed: 'bg-green-100 text-green-700',
    cancelled: 'bg-red-100 text-red-700',
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-800 mb-6">交易记录</h2>
      {message && <p className="text-sm text-red-500 mb-3">{message}</p>}

      {txns.length === 0 ? (
        <p className="text-gray-400 text-center py-8">暂无交易记录</p>
      ) : (
        <div className="space-y-4">
          {txns.map((t) => (
            <div key={t.id} className="bg-white rounded-xl border border-gray-200 p-4">
              <div className="flex items-center justify-between mb-2">
                <div>
                  <span className="font-medium text-gray-800">#{t.id}</span>
                  <span className="text-sm text-gray-500 ml-3">
                    {t.from_user_id === user.id ? '我发出' : '我收到'} · {t.hours}小时 · {t.coins}币
                  </span>
                </div>
                <span className={`text-xs px-2 py-0.5 rounded-full ${statusColor[t.status]}`}>
                  {statusText[t.status]}
                </span>
              </div>
              <div className="text-xs text-gray-400 mb-3">
                {new Date(t.created_at).toLocaleString()}
                {t.completed_at && ` · 完成于 ${new Date(t.completed_at).toLocaleString()}`}
              </div>

              <div className="flex gap-2">
                {t.status === 'pending' && t.to_user_id === user.id && (
                  <button onClick={() => handleAction(t.id, 'accept')} className="text-sm text-indigo-600 hover:underline">接受交易</button>
                )}
                {t.status === 'pending' && t.from_user_id === user.id && (
                  <button onClick={() => handleAction(t.id, 'cancel')} className="text-sm text-red-400 hover:underline">取消交易</button>
                )}
                {t.status === 'accepted' && (t.from_user_id === user.id || t.to_user_id === user.id) && (
                  <button onClick={() => handleAction(t.id, 'complete')} className="text-sm text-green-600 hover:underline">确认完成</button>
                )}
              </div>

              {t.status === 'completed' && (
                <div className="mt-3">
                  <ReviewForm onSubmit={handleReview(t.id)} />
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
