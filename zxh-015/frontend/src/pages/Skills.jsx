import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { skills as skillsApi } from '../api'
import SkillCard from '../components/SkillCard'

export default function Skills({ user }) {
  const [skillsList, setSkillsList] = useState([])
  const [filters, setFilters] = useState({ city: '', type: '', category: '' })
  const [search, setSearch] = useState('')

  useEffect(() => {
    skillsApi.list({}).then(({ data }) => setSkillsList(data))
  }, [])

  const handleSearch = async () => {
    if (search.trim()) {
      const { data } = await skillsApi.search({ keyword: search, ...filters })
      setSkillsList(data)
    } else {
      const { data } = await skillsApi.list(filters)
      setSkillsList(data)
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800">技能广场</h2>
        {user && (
          <Link to="/post-skill" className="bg-indigo-600 text-white px-3 py-1.5 rounded-lg text-sm hover:bg-indigo-700">
            发布技能
          </Link>
        )}
      </div>

      <div className="flex gap-3 mb-4 flex-wrap">
        <input
          className="border border-gray-200 rounded-lg p-2 text-sm w-48"
          placeholder="搜索关键词..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
        />
        <select className="border border-gray-200 rounded-lg p-2 text-sm" value={filters.type} onChange={(e) => setFilters({ ...filters, type: e.target.value })}>
          <option value="">全部类型</option>
          <option value="offer">提供服务</option>
          <option value="request">寻求帮助</option>
        </select>
        <input className="border border-gray-200 rounded-lg p-2 text-sm w-32" placeholder="城市" value={filters.city} onChange={(e) => setFilters({ ...filters, city: e.target.value })} />
        <button onClick={handleSearch} className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-indigo-700">
          搜索
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {skillsList.length === 0 ? (
          <p className="text-gray-400 col-span-full text-center py-8">暂未找到技能</p>
        ) : (
          skillsList.map((s) => <SkillCard key={s.id} skill={s} />)
        )}
      </div>
    </div>
  )
}
