import { Link, useNavigate } from 'react-router-dom'

export default function Navbar({ user, onLogout }) {
  const navigate = useNavigate()

  const handleLogout = () => {
    onLogout()
    navigate('/')
  }

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 flex items-center justify-between h-14">
        <Link to="/" className="text-xl font-bold text-indigo-600">
          技能时间银行
        </Link>

        <div className="flex items-center gap-4 text-sm">
          <Link to="/skills" className="text-gray-600 hover:text-indigo-600">技能广场</Link>
          <Link to="/ranking" className="text-gray-600 hover:text-indigo-600">排行榜</Link>
          <Link to="/map" className="text-gray-600 hover:text-indigo-600">技能地图</Link>
          <Link to="/urgent" className="text-gray-600 hover:text-red-500">紧急求助</Link>

          {user ? (
            <>
              <Link to="/dashboard" className="text-gray-800 font-medium">
                {user.username}
                <span className="ml-1 text-xs text-amber-600">({user.time_coins}币)</span>
              </Link>
              <button onClick={handleLogout} className="text-gray-400 hover:text-red-500">退出</button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-gray-600 hover:text-indigo-600">登录</Link>
              <Link
                to="/register"
                className="bg-indigo-600 text-white px-3 py-1.5 rounded-lg hover:bg-indigo-700"
              >
                注册
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}
