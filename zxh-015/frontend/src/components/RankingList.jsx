export default function RankingList({ data, type = 'helpers' }) {
  if (!data.length) return <p className="text-gray-400 text-center py-8">暂无数据</p>

  return (
    <div className="space-y-2">
      {data.map((item) => (
        <div
          key={item.user_id || item.rank}
          className="flex items-center gap-3 bg-white rounded-lg border border-gray-200 p-3"
        >
          <span className={`w-7 h-7 rounded-full flex items-center justify-center text-sm font-bold text-white ${
            item.rank === 1 ? 'bg-yellow-400' :
            item.rank === 2 ? 'bg-gray-300' :
            item.rank === 3 ? 'bg-amber-600' : 'bg-gray-400'
          }`}>
            {item.rank}
          </span>
          <div className="flex-1">
            <span className="font-medium text-gray-800">{item.username}</span>
            <span className="text-xs text-gray-400 ml-2">{item.city}</span>
          </div>
          <div className="text-right">
            {type === 'helpers' ? (
              <span className="text-sm text-indigo-600 font-medium">{item.total_hours}小时</span>
            ) : (
              <span className="text-sm text-indigo-600 font-medium">信用 {item.credit_score}</span>
            )}
          </div>
        </div>
      ))}
    </div>
  )
}
