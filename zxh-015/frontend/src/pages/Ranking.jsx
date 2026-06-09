import { useState, useEffect } from 'react'
import { ranking as rankingApi } from '../api'
import RankingList from '../components/RankingList'

export default function Ranking() {
  const [helpers, setHelpers] = useState([])
  const [creditList, setCreditList] = useState([])
  const [tab, setTab] = useState('helpers')

  useEffect(() => {
    rankingApi.topHelpers(20).then(({ data }) => setHelpers(data))
    rankingApi.highestCredit(20).then(({ data }) => setCreditList(data))
  }, [])

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-800 mb-6">排行榜</h2>

      <div className="flex gap-4 mb-6">
        <button
          onClick={() => setTab('helpers')}
          className={`px-4 py-2 rounded-lg text-sm font-medium ${
            tab === 'helpers' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-500 hover:bg-gray-100'
          }`}
        >
          时间币排行榜
        </button>
        <button
          onClick={() => setTab('credit')}
          className={`px-4 py-2 rounded-lg text-sm font-medium ${
            tab === 'credit' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-500 hover:bg-gray-100'
          }`}
        >
          信用分排行榜
        </button>
      </div>

      {tab === 'helpers' && (
        <div>
          <h3 className="font-semibold text-gray-700 mb-3">帮助他人最多的用户</h3>
          <RankingList data={helpers} type="helpers" />
        </div>
      )}

      {tab === 'credit' && (
        <div>
          <h3 className="font-semibold text-gray-700 mb-3">信用分最高用户</h3>
          <RankingList data={creditList} type="credit" />
        </div>
      )}
    </div>
  )
}
