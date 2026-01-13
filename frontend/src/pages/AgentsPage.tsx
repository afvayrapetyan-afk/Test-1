/**
 * AI Agents Page - защищённая страница для работы с агентами
 */
import { useState, useRef } from 'react'
import { AgentPanel } from '../components/AgentPanel'
import { useAuth } from '../contexts/AuthContext'
import { useNavigate } from 'react-router-dom'
import { LogOut, Sparkles, Shield, Code, Bot } from 'lucide-react'

export default function AgentsPage() {
  const { logout } = useAuth()
  const navigate = useNavigate()
  const panelRef = useRef<HTMLDivElement>(null)

  // Получаем админское имя из localStorage
  const adminUser = localStorage.getItem('admin_user') || 'Админ'

  // Активная вкладка агента
  const [activeTab, setActiveTab] = useState<'analyst' | 'dev'>('analyst')

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const handleCardClick = (tab: 'analyst' | 'dev') => {
    setActiveTab(tab)
    // Скролл к панели агентов
    setTimeout(() => {
      panelRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }, 100)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-blue-900">
      {/* Header */}
      <header className="bg-black/20 backdrop-blur-sm border-b border-white/10">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-purple-600 rounded-lg flex items-center justify-center">
                <Bot className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">AI Agents Control Panel</h1>
                <p className="text-xs text-gray-400">Управление AI агентами</p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 px-4 py-2 bg-white/10 rounded-lg">
                <Shield className="w-4 h-4 text-green-400" />
                <span className="text-sm text-white">{adminUser}</span>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition"
              >
                <LogOut className="w-4 h-4" />
                Выйти
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        {/* Welcome Banner */}
        <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl p-6 mb-6 shadow-2xl">
          <div className="flex items-center gap-4">
            <Sparkles className="w-12 h-12 text-white" />
            <div>
              <h2 className="text-2xl font-bold text-white mb-1">
                Добро пожаловать, {adminUser}!
              </h2>
              <p className="text-white/80">
                Управляй AI агентами: анализируй код, создавай фичи, генерируй тесты
              </p>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          {/* CodeAnalystAgent Card - Кликабельная */}
          <button
            onClick={() => handleCardClick('analyst')}
            className={`bg-white/10 backdrop-blur-sm border rounded-xl p-4 transition-all hover:bg-white/20 hover:scale-105 cursor-pointer ${
              activeTab === 'analyst' ? 'border-blue-500 ring-2 ring-blue-500' : 'border-white/20'
            }`}
          >
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center">
                <Code className="w-6 h-6 text-white" />
              </div>
              <div className="text-left">
                <p className="text-sm text-gray-400">CodeAnalystAgent</p>
                <p className="text-xl font-bold text-white">GPT-4o</p>
              </div>
            </div>
          </button>

          {/* DevAgent Card - Кликабельная */}
          <button
            onClick={() => handleCardClick('dev')}
            className={`bg-white/10 backdrop-blur-sm border rounded-xl p-4 transition-all hover:bg-white/20 hover:scale-105 cursor-pointer ${
              activeTab === 'dev' ? 'border-purple-500 ring-2 ring-purple-500' : 'border-white/20'
            }`}
          >
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-purple-600 rounded-lg flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <div className="text-left">
                <p className="text-sm text-gray-400">DevAgent</p>
                <p className="text-xl font-bold text-white">Claude Opus</p>
              </div>
            </div>
          </button>

          {/* Status Card - Просто информация */}
          <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl p-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-green-600 rounded-lg flex items-center justify-center">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div>
                <p className="text-sm text-gray-400">Status</p>
                <p className="text-xl font-bold text-green-400">Active</p>
              </div>
            </div>
          </div>
        </div>

        {/* Agent Panel */}
        <div ref={panelRef} className="bg-white dark:bg-gray-900 rounded-2xl shadow-2xl">
          <AgentPanel activeTab={activeTab} />
        </div>

        {/* Quick Tips - также кликабельные */}
        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
          <button
            onClick={() => handleCardClick('analyst')}
            className="bg-blue-900/30 border border-blue-500/30 rounded-xl p-4 hover:bg-blue-900/40 transition-all cursor-pointer text-left"
          >
            <h3 className="font-semibold text-white mb-2">💡 CodeAnalystAgent</h3>
            <p className="text-sm text-gray-300">
              Анализирует качество кода, находит баги и проверяет безопасность
            </p>
          </button>

          <button
            onClick={() => handleCardClick('dev')}
            className="bg-purple-900/30 border border-purple-500/30 rounded-xl p-4 hover:bg-purple-900/40 transition-all cursor-pointer text-left"
          >
            <h3 className="font-semibold text-white mb-2">✨ DevAgent</h3>
            <p className="text-sm text-gray-300">
              Создаёт фичи автоматически, генерирует тесты и делает рефакторинг
            </p>
          </button>
        </div>
      </main>
    </div>
  )
}
