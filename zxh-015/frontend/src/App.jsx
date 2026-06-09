import { useState, useEffect } from 'react'
import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Register from './pages/Register'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Skills from './pages/Skills'
import SkillDetail from './pages/SkillDetail'
import PostSkill from './pages/PostSkill'
import Transactions from './pages/Transactions'
import Ranking from './pages/Ranking'
import SkillMap from './pages/SkillMap'
import UrgentNeeds from './pages/UrgentNeeds'

export default function App() {
  const [user, setUser] = useState(null)

  useEffect(() => {
    const stored = localStorage.getItem('timebank_user')
    if (stored) setUser(JSON.parse(stored))
  }, [])

  const handleLogin = (userData) => {
    setUser(userData)
    localStorage.setItem('timebank_user', JSON.stringify(userData))
  }

  const handleLogout = () => {
    setUser(null)
    localStorage.removeItem('timebank_user')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar user={user} onLogout={handleLogout} />
      <div className="max-w-7xl mx-auto px-4 py-6">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/register" element={<Register onLogin={handleLogin} />} />
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
          <Route path="/dashboard" element={<Dashboard user={user} />} />
          <Route path="/skills" element={<Skills user={user} />} />
          <Route path="/skills/:id" element={<SkillDetail user={user} />} />
          <Route path="/post-skill" element={<PostSkill user={user} />} />
          <Route path="/transactions" element={<Transactions user={user} />} />
          <Route path="/ranking" element={<Ranking />} />
          <Route path="/map" element={<SkillMap />} />
          <Route path="/urgent" element={<UrgentNeeds user={user} />} />
        </Routes>
      </div>
    </div>
  )
}
