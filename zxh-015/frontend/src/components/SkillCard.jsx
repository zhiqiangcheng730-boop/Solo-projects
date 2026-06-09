import { Link } from 'react-router-dom'
import UrgentBadge from './UrgentBadge'

export default function SkillCard({ skill }) {
  const tags = JSON.parse(skill.tags || '[]')

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-4 hover:shadow-md transition">
      <div className="flex items-start justify-between mb-2">
        <span className={`text-xs px-2 py-0.5 rounded-full ${
          skill.type === 'offer' ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'
        }`}>
          {skill.type === 'offer' ? '提供服务' : '寻求帮助'}
        </span>
        {skill.is_urgent && <UrgentBadge />}
      </div>

      <Link to={`/skills/${skill.id}`} className="block">
        <h3 className="font-semibold text-gray-800 mb-1">{skill.title}</h3>
        <p className="text-sm text-gray-500 line-clamp-2 mb-2">{skill.description}</p>
      </Link>

      <div className="flex flex-wrap gap-1 mb-2">
        {tags.map((t, i) => (
          <span key={i} className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded">
            {t}
          </span>
        ))}
      </div>

      <div className="flex items-center justify-between text-xs text-gray-400">
        <span>{skill.category}</span>
        <span>{skill.city}</span>
      </div>
    </div>
  )
}
