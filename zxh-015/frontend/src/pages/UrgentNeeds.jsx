import { useState, useEffect } from 'react'
import { urgent as urgentApi } from '../api'
import SkillCard from '../components/SkillCard'

export default function UrgentNeeds({ user }) {
  const [urgentList, setUrgentList] = useState([])
  const [city, setCity] = useState(user?.city || '')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    urgentApi.list().then(({ data }) => setUrgentList(data))
  }, [])

  const handleSearch = async () => {
    setLoading(true)
    const { data } = await urgentApi.list(city || undefined)
    setUrgentList(data)
    setLoading(false)
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">紧急求助</h2>
          <p className="text-sm text-gray-400 mt-1">这些需求需要第一时间响应</p>
        </div>
      </div>

      <div className="flex gap-2 mb-4">
        <input
          className="border border-gray-200 rounded-lg p-2 text-sm w-40"
          placeholder="筛选城市..."
          value={city}
          onChange={(e) => setCity(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
        />
        <button onClick={handleSearch} className="bg-red-500 text-white px-4 py-2 rounded-lg text-sm hover:bg-red-600">
          {loading ? '搜索中...' : '筛选'}
        </button>
        <button onClick={() => { setCity(''); urgentApi.list().then(({ data }) => setUrgentList(data)) }} className="text-sm text-gray-400 hover:text-gray-600">
          清除筛选
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {urgentList.length === 0 ? (
          <p className="text-gray-400 col-span-full text-center py-8">
            暂无紧急需求 {city ? `（在 ${city}）` : ''}
          </p>
        ) : (
          urgentList.map((s) => (
            <div key={s.id} className="relative">
              <SkillCard skill={s} />
            </div>
          ))
        )}
      </div>
    </div>
  )
}
