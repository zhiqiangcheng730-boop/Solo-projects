import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { auth } from '../api'

export default function Register({ onLogin }) {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    username: '', email: '', password: '', city: '', lat: 0, lon: 0
  })
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      const { data } = await auth.register(form)
      onLogin(data)
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.detail || '注册失败')
    }
  }

  const handleLocate = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => setForm({ ...form, lat: pos.coords.latitude, lon: pos.coords.longitude }),
        () => setError('无法获取位置，请手动输入城市')
      )
    }
  }

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value })

  return (
    <div className="max-w-md mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">注册账号</h2>
      {error && <p className="text-red-500 text-sm mb-3 text-center">{error}</p>}
      <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
        <input className="w-full border border-gray-200 rounded-lg p-2.5 text-sm" placeholder="用户名" value={form.username} onChange={set('username')} required />
        <input className="w-full border border-gray-200 rounded-lg p-2.5 text-sm" type="email" placeholder="邮箱" value={form.email} onChange={set('email')} required />
        <input className="w-full border border-gray-200 rounded-lg p-2.5 text-sm" type="password" placeholder="密码" value={form.password} onChange={set('password')} required />
        <div className="flex gap-2">
          <input className="flex-1 border border-gray-200 rounded-lg p-2.5 text-sm" placeholder="城市" value={form.city} onChange={set('city')} required />
          <button type="button" onClick={handleLocate} className="bg-gray-100 text-gray-600 px-3 rounded-lg text-sm hover:bg-gray-200">
            定位
          </button>
        </div>
        <button type="submit" className="w-full bg-indigo-600 text-white py-2.5 rounded-lg text-sm hover:bg-indigo-700">
          注册（赠送3时间币）
        </button>
        <p className="text-center text-sm text-gray-400">
          已有账号？<Link to="/login" className="text-indigo-600">去登录</Link>
        </p>
      </form>
    </div>
  )
}
