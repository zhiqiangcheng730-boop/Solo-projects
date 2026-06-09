import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { auth } from '../api'

export default function Login({ onLogin }) {
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      const { data } = await auth.login(form)
      onLogin(data)
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.detail || '登录失败')
    }
  }

  return (
    <div className="max-w-md mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">登录</h2>
      {error && <p className="text-red-500 text-sm mb-3 text-center">{error}</p>}
      <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
        <input className="w-full border border-gray-200 rounded-lg p-2.5 text-sm" type="email" placeholder="邮箱" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
        <input className="w-full border border-gray-200 rounded-lg p-2.5 text-sm" type="password" placeholder="密码" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
        <button type="submit" className="w-full bg-indigo-600 text-white py-2.5 rounded-lg text-sm hover:bg-indigo-700">
          登录
        </button>
        <p className="text-center text-sm text-gray-400">
          没有账号？<Link to="/register" className="text-indigo-600">去注册</Link>
        </p>
      </form>
    </div>
  )
}
