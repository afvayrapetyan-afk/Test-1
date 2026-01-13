import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { useState, useEffect } from 'react'
import { API_ENDPOINTS } from '../config/api'
import { mockIdeaDetails } from '../data/mockData'

interface IdeaDetail {
  id: number
  title: string
  description: string
  trend_id: number
  total_score: number
  scores: {
    market_size: { score: number; reasoning: string; evidence: string }
    competition: { score: number; reasoning: string; evidence: string }
    demand: { score: number; reasoning: string; evidence: string }
    monetization: { score: number; reasoning: string; evidence: string }
    feasibility: { score: number; reasoning: string; evidence: string }
    time_to_market: { score: number; reasoning: string; evidence: string }
  }
  status: string
  analyzed_at: string
}

export default function IdeaDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [idea, setIdea] = useState<IdeaDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchIdea = async () => {
      try {
        setLoading(true)

        // Загружаем детальные данные из API
        const response = await fetch(API_ENDPOINTS.ideas.get(Number(id)))
        if (!response.ok) {
          // Пробуем mock данные при ошибке
          const mockIdea = mockIdeaDetails[id || '']
          if (mockIdea) {
            setIdea(mockIdea)
            setLoading(false)
            return
          }
          throw new Error('Идея не найдена')
        }
        const data = await response.json()
        setIdea(data)
      } catch (err) {
        // Пробуем mock данные при ошибке
        const mockIdea = mockIdeaDetails[id || '']
        if (mockIdea) {
          setIdea(mockIdea)
        } else {
          setError(err instanceof Error ? err.message : 'Ошибка загрузки')
        }
      } finally {
        setLoading(false)
      }
    }

    if (id) {
      fetchIdea()
    }
  }, [id])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-text-secondary">Загрузка...</div>
      </div>
    )
  }

  if (error || !idea) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen">
        <div className="text-red-500 mb-4">{error || 'Идея не найдена'}</div>
        <button
          onClick={() => navigate('/')}
          className="text-accent-blue hover:underline"
        >
          Вернуться назад
        </button>
      </div>
    )
  }

  return (
    <div className="max-w-5xl mx-auto">
      {/* Back Button */}
      <button
        onClick={() => navigate('/')}
        className="flex items-center gap-2 text-text-secondary hover:text-text-primary transition-colors mb-6"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Назад к идеям</span>
      </button>

      {/* Hero Section */}
      <div className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl p-8 text-white mb-6">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h1 className="text-4xl font-bold mb-4">
              💡 {idea.title}
            </h1>
            <p className="text-blue-100 text-lg mb-6">
              {idea.description}
            </p>
            <div className="flex gap-2 flex-wrap">
              <div className="bg-white/20 backdrop-blur-sm rounded-lg px-4 py-2">
                <div className="text-sm text-blue-100">Статус</div>
                <div className="text-lg font-bold capitalize">
                  {idea.status === 'pending' ? 'К реализации' : idea.status}
                </div>
              </div>
              <div className="bg-white/20 backdrop-blur-sm rounded-lg px-4 py-2">
                <div className="text-sm text-blue-100">Trend ID</div>
                <div className="text-lg font-bold">
                  #{idea.trend_id}
                </div>
              </div>
              <div className="bg-white/20 backdrop-blur-sm rounded-lg px-4 py-2">
                <div className="text-sm text-blue-100">Дата анализа</div>
                <div className="text-lg font-bold">
                  {new Date(idea.analyzed_at).toLocaleDateString('ru-RU')}
                </div>
              </div>
            </div>
          </div>
          <div className="bg-white/20 backdrop-blur-sm rounded-2xl px-6 py-4 text-center">
            <div className="text-sm text-blue-100 mb-2">AI Score</div>
            <div className="text-5xl font-bold">{idea.total_score}</div>
            <div className="text-sm text-blue-100">/100</div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* AI Analysis - Detailed Metrics */}
          <section className="bg-surface border border-border rounded-xl p-6">
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
              🤖 AI-анализ метрик
            </h2>
            <div className="space-y-6">
              {/* Market Size */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-semibold text-text-primary">Размер рынка</h3>
                  <span className="text-2xl font-bold text-accent-blue">{idea.scores.market_size.score}/100</span>
                </div>
                <div className="bg-blue-50 dark:bg-blue-950/20 border-l-4 border-blue-500 p-4 rounded space-y-2">
                  <p className="text-sm text-text-secondary">
                    <strong className="text-text-primary">Анализ:</strong> {idea.scores.market_size.reasoning}
                  </p>
                  <p className="text-sm text-text-tertiary italic">
                    <strong>Факты:</strong> {idea.scores.market_size.evidence}
                  </p>
                </div>
              </div>

              {/* Competition */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-semibold text-text-primary">Конкурентная среда</h3>
                  <span className="text-2xl font-bold text-accent-orange">{idea.scores.competition.score}/100</span>
                </div>
                <div className="bg-orange-50 dark:bg-orange-950/20 border-l-4 border-orange-500 p-4 rounded space-y-2">
                  <p className="text-sm text-text-secondary">
                    <strong className="text-text-primary">Анализ:</strong> {idea.scores.competition.reasoning}
                  </p>
                  <p className="text-sm text-text-tertiary italic">
                    <strong>Факты:</strong> {idea.scores.competition.evidence}
                  </p>
                </div>
              </div>

              {/* Demand */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-semibold text-text-primary">Спрос и актуальность</h3>
                  <span className="text-2xl font-bold text-accent-green">{idea.scores.demand.score}/100</span>
                </div>
                <div className="bg-green-50 dark:bg-green-950/20 border-l-4 border-green-500 p-4 rounded space-y-2">
                  <p className="text-sm text-text-secondary">
                    <strong className="text-text-primary">Анализ:</strong> {idea.scores.demand.reasoning}
                  </p>
                  <p className="text-sm text-text-tertiary italic">
                    <strong>Факты:</strong> {idea.scores.demand.evidence}
                  </p>
                </div>
              </div>

              {/* Monetization */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-semibold text-text-primary">Монетизация</h3>
                  <span className="text-2xl font-bold text-accent-purple">{idea.scores.monetization.score}/100</span>
                </div>
                <div className="bg-purple-50 dark:bg-purple-950/20 border-l-4 border-purple-500 p-4 rounded space-y-2">
                  <p className="text-sm text-text-secondary">
                    <strong className="text-text-primary">Анализ:</strong> {idea.scores.monetization.reasoning}
                  </p>
                  <p className="text-sm text-text-tertiary italic">
                    <strong>Факты:</strong> {idea.scores.monetization.evidence}
                  </p>
                </div>
              </div>

              {/* Feasibility */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-semibold text-text-primary">Реализуемость</h3>
                  <span className="text-2xl font-bold text-accent-blue">{idea.scores.feasibility.score}/100</span>
                </div>
                <div className="bg-blue-50 dark:bg-blue-950/20 border-l-4 border-blue-500 p-4 rounded space-y-2">
                  <p className="text-sm text-text-secondary">
                    <strong className="text-text-primary">Анализ:</strong> {idea.scores.feasibility.reasoning}
                  </p>
                  <p className="text-sm text-text-tertiary italic">
                    <strong>Факты:</strong> {idea.scores.feasibility.evidence}
                  </p>
                </div>
              </div>

              {/* Time to Market */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-semibold text-text-primary">Скорость выхода на рынок</h3>
                  <span className="text-2xl font-bold text-accent-green">{idea.scores.time_to_market.score}/100</span>
                </div>
                <div className="bg-green-50 dark:bg-green-950/20 border-l-4 border-green-500 p-4 rounded space-y-2">
                  <p className="text-sm text-text-secondary">
                    <strong className="text-text-primary">Анализ:</strong> {idea.scores.time_to_market.reasoning}
                  </p>
                  <p className="text-sm text-text-tertiary italic">
                    <strong>Факты:</strong> {idea.scores.time_to_market.evidence}
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* Summary Section */}
          <section className="bg-surface border border-border rounded-xl p-6">
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
              📝 Резюме
            </h2>
            <div className="space-y-4 text-text-secondary">
              <p className="text-base leading-relaxed">
                {idea.description}
              </p>
              <div className="grid grid-cols-2 gap-4 mt-6">
                <div className="bg-blue-50 dark:bg-blue-950/20 border-l-4 border-blue-500 p-4 rounded">
                  <h3 className="font-semibold text-text-primary mb-2">
                    ✅ Сильные стороны
                  </h3>
                  <ul className="text-sm space-y-1">
                    {(() => {
                      const metrics = [
                        { name: 'Крупный рынок', score: idea.scores.market_size.score, threshold: 75 },
                        { name: 'Высокий спрос', score: idea.scores.demand.score, threshold: 75 },
                        { name: 'Низкая конкуренция', score: 100 - idea.scores.competition.score, threshold: 30 },
                        { name: 'Потенциал монетизации', score: idea.scores.monetization.score, threshold: 70 },
                        { name: 'Легкая реализация', score: idea.scores.feasibility.score, threshold: 70 },
                        { name: 'Быстрый выход на рынок', score: idea.scores.time_to_market.score, threshold: 70 },
                      ]
                      const strengths = metrics
                        .filter(m => m.score >= m.threshold)
                        .sort((a, b) => b.score - a.score)
                        .slice(0, 4)

                      return strengths.length > 0 ? (
                        strengths.map((s, i) => <li key={i}>• {s.name}</li>)
                      ) : (
                        <li className="text-text-tertiary italic">Нет явных преимуществ</li>
                      )
                    })()}
                  </ul>
                </div>
                <div className="bg-orange-50 dark:bg-orange-950/20 border-l-4 border-orange-500 p-4 rounded">
                  <h3 className="font-semibold text-text-primary mb-2">
                    ⚠️ Основные вызовы
                  </h3>
                  <ul className="text-sm space-y-1">
                    {(() => {
                      const challenges = [
                        { name: 'Конкурентная среда', score: idea.scores.competition.score, reason: idea.scores.competition.reasoning },
                        { name: 'Реализуемость', score: idea.scores.feasibility.score, reason: idea.scores.feasibility.reasoning },
                        { name: 'Размер рынка', score: idea.scores.market_size.score, reason: idea.scores.market_size.reasoning },
                        { name: 'Спрос', score: idea.scores.demand.score, reason: idea.scores.demand.reasoning },
                        { name: 'Монетизация', score: idea.scores.monetization.score, reason: idea.scores.monetization.reasoning },
                        { name: 'Время на рынок', score: idea.scores.time_to_market.score, reason: idea.scores.time_to_market.reasoning },
                      ]
                      // Сортируем по возрастанию score (самые слабые первыми)
                      const weakest = challenges
                        .sort((a, b) => a.score - b.score)
                        .slice(0, 4)

                      return weakest.map((c, i) => (
                        <li key={i} className="leading-relaxed">
                          • <strong>{c.name}</strong> ({c.score}/100): {c.reason.split('.')[0]}.
                        </li>
                      ))
                    })()}
                  </ul>
                </div>
              </div>
            </div>
          </section>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Quick Stats */}
          <div className="bg-surface border border-border rounded-xl p-6">
            <h3 className="font-bold mb-4">Сводка по метрикам</h3>
            <div className="space-y-3">
              <div>
                <div className="text-sm text-text-secondary">Размер рынка</div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-2 bg-border rounded-full overflow-hidden">
                    <div
                      className="h-full bg-accent-blue rounded-full"
                      style={{ width: `${idea.scores.market_size.score}%` }}
                    />
                  </div>
                  <span className="text-sm font-semibold">
                    {idea.scores.market_size.score}/100
                  </span>
                </div>
              </div>
              <div>
                <div className="text-sm text-text-secondary">Конкуренция</div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-2 bg-border rounded-full overflow-hidden">
                    <div
                      className="h-full bg-accent-orange rounded-full"
                      style={{ width: `${idea.scores.competition.score}%` }}
                    />
                  </div>
                  <span className="text-sm font-semibold">
                    {idea.scores.competition.score}/100
                  </span>
                </div>
              </div>
              <div>
                <div className="text-sm text-text-secondary">Спрос</div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-2 bg-border rounded-full overflow-hidden">
                    <div
                      className="h-full bg-accent-green rounded-full"
                      style={{ width: `${idea.scores.demand.score}%` }}
                    />
                  </div>
                  <span className="text-sm font-semibold">
                    {idea.scores.demand.score}/100
                  </span>
                </div>
              </div>
              <div>
                <div className="text-sm text-text-secondary">Монетизация</div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-2 bg-border rounded-full overflow-hidden">
                    <div
                      className="h-full bg-accent-purple rounded-full"
                      style={{ width: `${idea.scores.monetization.score}%` }}
                    />
                  </div>
                  <span className="text-sm font-semibold">
                    {idea.scores.monetization.score}/100
                  </span>
                </div>
              </div>
              <div>
                <div className="text-sm text-text-secondary">Реализуемость</div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-2 bg-border rounded-full overflow-hidden">
                    <div
                      className="h-full bg-accent-blue rounded-full"
                      style={{ width: `${idea.scores.feasibility.score}%` }}
                    />
                  </div>
                  <span className="text-sm font-semibold">
                    {idea.scores.feasibility.score}/100
                  </span>
                </div>
              </div>
              <div>
                <div className="text-sm text-text-secondary">Выход на рынок</div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-2 bg-border rounded-full overflow-hidden">
                    <div
                      className="h-full bg-accent-green rounded-full"
                      style={{ width: `${idea.scores.time_to_market.score}%` }}
                    />
                  </div>
                  <span className="text-sm font-semibold">
                    {idea.scores.time_to_market.score}/100
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* AI Confidence */}
          <div className="bg-surface border border-border rounded-xl p-6">
            <h3 className="font-bold mb-4">🎯 Уверенность AI</h3>
            <div className="space-y-4">
              <div>
                <div className="text-sm text-text-secondary mb-2">Общая оценка</div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-3 bg-border rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-blue-500 to-purple-600 rounded-full"
                      style={{ width: `${idea.total_score}%` }}
                    />
                  </div>
                  <span className="text-lg font-bold">{idea.total_score}%</span>
                </div>
              </div>

              <div className="pt-4 border-t border-border">
                <div className="text-sm font-semibold text-text-primary mb-3">Рекомендация:</div>
                {idea.total_score >= 75 ? (
                  <div className="bg-green-50 dark:bg-green-950/20 border-l-4 border-green-500 p-3 rounded">
                    <p className="text-sm text-text-secondary">
                      ✅ <strong>Рекомендуется к реализации.</strong> Идея показывает высокий потенциал по большинству метрик.
                    </p>
                  </div>
                ) : idea.total_score >= 60 ? (
                  <div className="bg-yellow-50 dark:bg-yellow-950/20 border-l-4 border-yellow-500 p-3 rounded">
                    <p className="text-sm text-text-secondary">
                      ⚠️ <strong>Требует доработки.</strong> Некоторые метрики нуждаются в улучшении перед запуском.
                    </p>
                  </div>
                ) : (
                  <div className="bg-red-50 dark:bg-red-950/20 border-l-4 border-red-500 p-3 rounded">
                    <p className="text-sm text-text-secondary">
                      ❌ <strong>Не рекомендуется.</strong> Идея имеет существенные недостатки.
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
