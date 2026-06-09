import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <div className="text-center py-16">
      <h1 className="text-4xl font-bold text-gray-800 mb-4">
        技能时间银行
      </h1>
      <p className="text-lg text-gray-500 mb-2">
        用你的技能帮助他人，赚取时间币，换取你需要的帮助
      </p>
      <p className="text-sm text-gray-400 mb-8">
        1小时帮助 = 1时间币 · 注册即送3时间币
      </p>

      <div className="flex justify-center gap-4 mb-12">
        <Link
          to="/register"
          className="bg-indigo-600 text-white px-6 py-3 rounded-xl text-lg hover:bg-indigo-700 shadow"
        >
          立即注册
        </Link>
        <Link
          to="/skills"
          className="bg-white text-indigo-600 border border-indigo-200 px-6 py-3 rounded-xl text-lg hover:bg-indigo-50"
        >
          浏览技能
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-3xl mx-auto text-left">
        {[
          { title: '发布技能', desc: '分享你擅长的技能，如修电脑、教英语、遛狗、设计PPT', icon: '🔧' },
          { title: '匹配需求', desc: '系统根据城市和技能标签智能匹配，找到附近能互相帮助的人', icon: '🤝' },
          { title: '时间币交易', desc: '每次帮助赚取时间币，用来换取你需要的服务', icon: '⏱️' },
          { title: '信用评价', desc: '交易完成后互相评价，建立可靠社区信用体系', icon: '⭐' },
          { title: '技能地图', desc: '在地图上浏览附近的技能提供者（仅显示大区域保护隐私）', icon: '🗺️' },
          { title: '紧急求助', desc: '紧急需求优先展示，社区第一时间响应', icon: '🚨' },
        ].map((f, i) => (
          <div key={i} className="bg-white rounded-xl border border-gray-200 p-5">
            <span className="text-2xl">{f.icon}</span>
            <h3 className="font-semibold text-gray-800 mt-2 mb-1">{f.title}</h3>
            <p className="text-sm text-gray-500">{f.desc}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
