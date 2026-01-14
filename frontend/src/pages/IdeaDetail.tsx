import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, ChevronDown } from 'lucide-react'
import { useState, useEffect } from 'react'
import { motion, useScroll, useTransform } from 'framer-motion'
import { API_ENDPOINTS } from '../config/api'
import { mockIdeaDetails } from '../data/mockData'

interface IdeaDetailRegions {
  russia?: boolean
  armenia?: boolean
  global?: boolean
}

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
  regions?: IdeaDetailRegions
}

// Компонент для анимации появления при скролле (Apple-style)
function ScrollReveal({
  children,
  delay = 0,
  className = ''
}: {
  children: React.ReactNode
  delay?: number
  className?: string
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 60 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{
        duration: 0.8,
        delay,
        ease: [0.25, 0.1, 0.25, 1] // Apple-like easing
      }}
      className={className}
    >
      {children}
    </motion.div>
  )
}

export default function IdeaDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [idea, setIdea] = useState<IdeaDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showScrollHint, setShowScrollHint] = useState(true)

  const { scrollY } = useScroll()
  const heroOpacity = useTransform(scrollY, [0, 300], [1, 0.3])
  const heroScale = useTransform(scrollY, [0, 300], [1, 0.95])

  // Прокрутка наверх при загрузке страницы
  useEffect(() => {
    window.scrollTo(0, 0)
  }, [])

  // Скрываем подсказку скролла при прокрутке
  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 100) {
        setShowScrollHint(false)
      }
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  useEffect(() => {
    const fetchIdea = async () => {
      try {
        setLoading(true)

        const response = await fetch(API_ENDPOINTS.ideas.get(Number(id)))
        if (!response.ok) {
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
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-text-secondary"
        >
          Загрузка...
        </motion.div>
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
      <motion.button
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5 }}
        onClick={() => navigate('/')}
        className="flex items-center gap-2 text-text-secondary hover:text-text-primary transition-colors mb-6"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Назад к идеям</span>
      </motion.button>

      {/* Hero Section - Apple-style entrance */}
      <motion.div
        initial={{ opacity: 0, y: 40, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.8, ease: [0.25, 0.1, 0.25, 1] }}
        style={{ opacity: heroOpacity, scale: heroScale }}
        className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl sm:rounded-2xl p-4 sm:p-6 lg:p-8 text-white mb-4 sm:mb-6 relative"
      >
        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
          <div className="flex-1">
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.6 }}
              className="text-xl sm:text-2xl lg:text-4xl font-bold mb-2 sm:mb-4"
            >
              💡 {idea.title}
            </motion.h1>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.6 }}
              className="text-blue-100 text-sm sm:text-base lg:text-lg mb-4 sm:mb-6"
            >
              {idea.description}
            </motion.p>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4, duration: 0.6 }}
              className="flex gap-2 flex-wrap"
            >
              <div className="bg-white/20 backdrop-blur-sm rounded-lg px-3 sm:px-4 py-1.5 sm:py-2">
                <div className="text-xs sm:text-sm text-blue-100">Статус</div>
                <div className="text-sm sm:text-lg font-bold capitalize">
                  {idea.status === 'pending' ? 'К реализации' : idea.status}
                </div>
              </div>
              <div className="bg-white/20 backdrop-blur-sm rounded-lg px-3 sm:px-4 py-1.5 sm:py-2">
                <div className="text-xs sm:text-sm text-blue-100">Тренд</div>
                <div className="text-sm sm:text-lg font-bold">
                  #{idea.trend_id}
                </div>
              </div>
              <div className="bg-white/20 backdrop-blur-sm rounded-lg px-3 sm:px-4 py-1.5 sm:py-2">
                <div className="text-xs sm:text-sm text-blue-100">Дата анализа</div>
                <div className="text-sm sm:text-lg font-bold">
                  {new Date(idea.analyzed_at).toLocaleDateString('ru-RU')}
                </div>
              </div>
              {/* Regions */}
              {idea.regions && (idea.regions.russia || idea.regions.armenia || idea.regions.global) && (
                <div className="bg-white/20 backdrop-blur-sm rounded-lg px-3 sm:px-4 py-1.5 sm:py-2">
                  <div className="text-xs sm:text-sm text-blue-100">Регионы</div>
                  <div className="flex items-center gap-1 text-sm sm:text-lg">
                    {idea.regions.russia && <span title="Россия">🇷🇺</span>}
                    {idea.regions.armenia && <span title="Армения">🇦🇲</span>}
                    {idea.regions.global && <span title="Мир">🌍</span>}
                  </div>
                </div>
              )}
            </motion.div>
          </div>
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.5, duration: 0.6, type: "spring" }}
            className="bg-white/20 backdrop-blur-sm rounded-xl sm:rounded-2xl px-4 sm:px-6 py-3 sm:py-4 text-center self-start"
          >
            <div className="text-xs sm:text-sm text-blue-100 mb-1 sm:mb-2">Оценка</div>
            <div className="text-3xl sm:text-4xl lg:text-5xl font-bold">{idea.total_score}</div>
            <div className="text-xs sm:text-sm text-blue-100">/100</div>
          </motion.div>
        </div>

        {/* Scroll indicator - Apple style */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: showScrollHint ? 1 : 0 }}
          transition={{ delay: 1, duration: 0.5 }}
          className="absolute -bottom-12 left-1/2 -translate-x-1/2 flex flex-col items-center text-text-secondary"
        >
          <span className="text-xs mb-1">Листайте вниз</span>
          <motion.div
            animate={{ y: [0, 8, 0] }}
            transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
          >
            <ChevronDown className="w-5 h-5" />
          </motion.div>
        </motion.div>
      </motion.div>

      {/* Spacer for scroll hint */}
      <div className="h-8" />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-4 sm:space-y-6">
          {/* AI Analysis - Detailed Metrics */}
          <ScrollReveal>
            <section className="bg-surface border border-border rounded-xl p-4 sm:p-6">
              <h2 className="text-lg sm:text-xl lg:text-2xl font-bold mb-3 sm:mb-4 flex items-center gap-2">
                🤖 AI-анализ метрик
              </h2>
              <div className="space-y-6">
                {/* Market Size */}
                <ScrollReveal delay={0.1}>
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-semibold text-text-primary text-sm sm:text-base">Размер рынка</h3>
                      <span className="text-lg sm:text-2xl font-bold text-accent-blue">{idea.scores.market_size.score}/100</span>
                    </div>
                    <div className="bg-blue-50 dark:bg-blue-950/20 border-l-4 border-blue-500 p-3 sm:p-4 rounded space-y-2">
                      <p className="text-sm text-text-secondary">
                        <strong className="text-text-primary">Анализ:</strong> {idea.scores.market_size.reasoning}
                      </p>
                      <p className="text-sm text-text-tertiary italic">
                        <strong>Факты:</strong> {idea.scores.market_size.evidence}
                      </p>
                    </div>
                  </div>
                </ScrollReveal>

                {/* Competition */}
                <ScrollReveal delay={0.15}>
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-semibold text-text-primary text-sm sm:text-base">Конкурентная среда</h3>
                      <span className="text-lg sm:text-2xl font-bold text-accent-orange">{idea.scores.competition.score}/100</span>
                    </div>
                    <div className="bg-orange-50 dark:bg-orange-950/20 border-l-4 border-orange-500 p-3 sm:p-4 rounded space-y-2">
                      <p className="text-sm text-text-secondary">
                        <strong className="text-text-primary">Анализ:</strong> {idea.scores.competition.reasoning}
                      </p>
                      <p className="text-sm text-text-tertiary italic">
                        <strong>Факты:</strong> {idea.scores.competition.evidence}
                      </p>
                    </div>
                  </div>
                </ScrollReveal>

                {/* Demand */}
                <ScrollReveal delay={0.2}>
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-semibold text-text-primary text-sm sm:text-base">Спрос и актуальность</h3>
                      <span className="text-lg sm:text-2xl font-bold text-accent-green">{idea.scores.demand.score}/100</span>
                    </div>
                    <div className="bg-green-50 dark:bg-green-950/20 border-l-4 border-green-500 p-3 sm:p-4 rounded space-y-2">
                      <p className="text-sm text-text-secondary">
                        <strong className="text-text-primary">Анализ:</strong> {idea.scores.demand.reasoning}
                      </p>
                      <p className="text-sm text-text-tertiary italic">
                        <strong>Факты:</strong> {idea.scores.demand.evidence}
                      </p>
                    </div>
                  </div>
                </ScrollReveal>

                {/* Monetization */}
                <ScrollReveal delay={0.25}>
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-semibold text-text-primary text-sm sm:text-base">Монетизация</h3>
                      <span className="text-lg sm:text-2xl font-bold text-accent-purple">{idea.scores.monetization.score}/100</span>
                    </div>
                    <div className="bg-purple-50 dark:bg-purple-950/20 border-l-4 border-purple-500 p-3 sm:p-4 rounded space-y-2">
                      <p className="text-sm text-text-secondary">
                        <strong className="text-text-primary">Анализ:</strong> {idea.scores.monetization.reasoning}
                      </p>
                      <p className="text-sm text-text-tertiary italic">
                        <strong>Факты:</strong> {idea.scores.monetization.evidence}
                      </p>
                    </div>
                  </div>
                </ScrollReveal>

                {/* Feasibility */}
                <ScrollReveal delay={0.3}>
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-semibold text-text-primary text-sm sm:text-base">Реализуемость</h3>
                      <span className="text-lg sm:text-2xl font-bold text-accent-blue">{idea.scores.feasibility.score}/100</span>
                    </div>
                    <div className="bg-blue-50 dark:bg-blue-950/20 border-l-4 border-blue-500 p-3 sm:p-4 rounded space-y-2">
                      <p className="text-sm text-text-secondary">
                        <strong className="text-text-primary">Анализ:</strong> {idea.scores.feasibility.reasoning}
                      </p>
                      <p className="text-sm text-text-tertiary italic">
                        <strong>Факты:</strong> {idea.scores.feasibility.evidence}
                      </p>
                    </div>
                  </div>
                </ScrollReveal>

                {/* Time to Market */}
                <ScrollReveal delay={0.35}>
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-semibold text-text-primary text-sm sm:text-base">Скорость выхода на рынок</h3>
                      <span className="text-lg sm:text-2xl font-bold text-accent-green">{idea.scores.time_to_market.score}/100</span>
                    </div>
                    <div className="bg-green-50 dark:bg-green-950/20 border-l-4 border-green-500 p-3 sm:p-4 rounded space-y-2">
                      <p className="text-sm text-text-secondary">
                        <strong className="text-text-primary">Анализ:</strong> {idea.scores.time_to_market.reasoning}
                      </p>
                      <p className="text-sm text-text-tertiary italic">
                        <strong>Факты:</strong> {idea.scores.time_to_market.evidence}
                      </p>
                    </div>
                  </div>
                </ScrollReveal>
              </div>
            </section>
          </ScrollReveal>

          {/* Summary Section */}
          <ScrollReveal delay={0.1}>
            <section className="bg-surface border border-border rounded-xl p-4 sm:p-6">
              <h2 className="text-lg sm:text-xl lg:text-2xl font-bold mb-3 sm:mb-4 flex items-center gap-2">
                📝 Резюме
              </h2>
              <div className="space-y-4 text-text-secondary">
                <p className="text-sm sm:text-base leading-relaxed">
                  {idea.description}
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4 sm:mt-6">
                  <ScrollReveal delay={0.15}>
                    <div className="bg-blue-50 dark:bg-blue-950/20 border-l-4 border-blue-500 p-3 sm:p-4 rounded">
                      <h3 className="font-semibold text-text-primary mb-2 text-sm sm:text-base">
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
                  </ScrollReveal>
                  <ScrollReveal delay={0.2}>
                    <div className="bg-orange-50 dark:bg-orange-950/20 border-l-4 border-orange-500 p-3 sm:p-4 rounded">
                      <h3 className="font-semibold text-text-primary mb-2 text-sm sm:text-base">
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
                  </ScrollReveal>
                </div>
              </div>
            </section>
          </ScrollReveal>
        </div>

        {/* Sidebar */}
        <div className="space-y-4 sm:space-y-6">
          {/* Quick Stats */}
          <ScrollReveal delay={0.2}>
            <div className="bg-surface border border-border rounded-xl p-4 sm:p-6">
              <h3 className="font-bold mb-3 sm:mb-4 text-sm sm:text-base">Сводка по метрикам</h3>
              <div className="space-y-3">
                {[
                  { label: 'Размер рынка', score: idea.scores.market_size.score, color: 'bg-accent-blue' },
                  { label: 'Конкуренция', score: idea.scores.competition.score, color: 'bg-accent-orange' },
                  { label: 'Спрос', score: idea.scores.demand.score, color: 'bg-accent-green' },
                  { label: 'Монетизация', score: idea.scores.monetization.score, color: 'bg-accent-purple' },
                  { label: 'Реализуемость', score: idea.scores.feasibility.score, color: 'bg-accent-blue' },
                  { label: 'Выход на рынок', score: idea.scores.time_to_market.score, color: 'bg-accent-green' },
                ].map((metric, index) => (
                  <motion.div
                    key={metric.label}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <div className="text-sm text-text-secondary">{metric.label}</div>
                    <div className="flex items-center gap-2">
                      <div className="flex-1 h-2 bg-border rounded-full overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          whileInView={{ width: `${metric.score}%` }}
                          viewport={{ once: true }}
                          transition={{ delay: 0.3 + index * 0.1, duration: 0.8, ease: "easeOut" }}
                          className={`h-full ${metric.color} rounded-full`}
                        />
                      </div>
                      <span className="text-sm font-semibold">{metric.score}/100</span>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </ScrollReveal>

          {/* AI Confidence */}
          <ScrollReveal delay={0.3}>
            <div className="bg-surface border border-border rounded-xl p-4 sm:p-6">
              <h3 className="font-bold mb-3 sm:mb-4 text-sm sm:text-base">🎯 Уверенность AI</h3>
              <div className="space-y-4">
                <div>
                  <div className="text-sm text-text-secondary mb-2">Общая оценка</div>
                  <div className="flex items-center gap-2">
                    <div className="flex-1 h-3 bg-border rounded-full overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        whileInView={{ width: `${idea.total_score}%` }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.5, duration: 1, ease: "easeOut" }}
                        className="h-full bg-gradient-to-r from-blue-500 to-purple-600 rounded-full"
                      />
                    </div>
                    <span className="text-lg font-bold">{idea.total_score}%</span>
                  </div>
                </div>

                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: 0.7 }}
                  className="pt-4 border-t border-border"
                >
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
                </motion.div>
              </div>
            </div>
          </ScrollReveal>
        </div>
      </div>
    </div>
  )
}
