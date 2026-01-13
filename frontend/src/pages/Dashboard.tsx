import MetricCard from '../components/dashboard/MetricCard'
import IdeaCard from '../components/ideas/IdeaCard'
import TrendChart from '../components/charts/TrendChart'
import HeroSection from '../components/hero/HeroSection'
import { BarChart3, Briefcase, Code, Sparkles } from 'lucide-react'
import { mockProjects } from '../data/mockData'
import { useChat } from '../contexts/ChatContext'
import { useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { API_ENDPOINTS } from '../config/api'

export default function Dashboard() {
  const { openChat } = useChat()
  const navigate = useNavigate()
  const [ideas, setIdeas] = useState<any[]>([])
  const [trends, setTrends] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Загружаем идеи
        const ideasResponse = await fetch(API_ENDPOINTS.ideas.list)
        const ideasData = await ideasResponse.json()

        // Загружаем тренды
        const trendsResponse = await fetch(API_ENDPOINTS.trends.list)
        const trendsData = await trendsResponse.json()

        setIdeas(ideasData.items || [])
        setTrends(trendsData.items || [])
      } catch (error) {
        console.error('Error loading data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  const handleChatClick = () => {
    openChat()
  }

  const handleDetailsClick = (ideaId: string) => {
    navigate(`/idea/${ideaId}`)
  }

  const handleViewAllIdeas = () => {
    // Прокрутка к секции идей
    const ideasSection = document.querySelector('section')
    ideasSection?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  const handleViewAllProjects = () => {
    // Прокрутка к секции проектов
    const projectsSection = document.querySelectorAll('section')[1]
    projectsSection?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  const handleProjectAction = (projectId: string, action: string) => {
    console.log(`Project ${projectId}: ${action}`)
    // TODO: Implement actual actions
    alert(`${action} для проекта ${projectId} - скоро будет доступно!`)
  }

  return (
    <div className="space-y-6">
      {/* Hero Section */}
      <HeroSection />

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        <MetricCard
          label="Всего идей"
          value={loading ? '...' : ideas.length.toString()}
          change={loading ? '' : `${ideas.filter((i: any) => i.total_score >= 75).length} высокорейтинговых`}
          isPositive={true}
          icon={<BarChart3 />}
        />
        <MetricCard
          label="Трендов собрано"
          value={loading ? '...' : trends.length.toString()}
          change={loading ? '' : `${trends.filter((t: any) => t.engagement_score > 1000).length} с высоким engagement`}
          isPositive={true}
          icon={<Briefcase />}
        />
        <MetricCard
          label="Средний рейтинг"
          value={loading ? '...' : ideas.length > 0 ? `${(ideas.reduce((sum: number, i: any) => sum + i.total_score, 0) / ideas.length).toFixed(0)}/100` : '0'}
          change={loading ? '' : 'AI анализ'}
          isPositive={true}
          icon={<Code />}
        />
        <MetricCard
          label="Топ идей"
          value={loading ? '...' : ideas.filter((i: any) => i.total_score >= 75).length.toString()}
          change={loading ? '' : 'Готовы к реализации'}
          isPositive={true}
          icon={<Sparkles />}
        />
      </div>

      {/* Trend Analytics Chart */}
      <TrendChart />

      {/* Trending Ideas Section */}
      <section data-section="ideas" className="bg-surface border border-border rounded-lg p-4 shadow-sm">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-lg font-bold flex items-center gap-1">
            <span>🔥</span>
            <span>Горячие тренды</span>
          </h2>
          <button
            onClick={handleViewAllIdeas}
            className="text-sm font-medium text-accent-blue hover:text-accent-purple transition-colors"
          >
            Смотреть все ({ideas.length})
          </button>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="text-text-secondary">Загрузка данных...</div>
          </div>
        ) : ideas.length === 0 ? (
          <div className="flex items-center justify-center py-8">
            <div className="text-text-secondary">Нет данных. Запустите demo.py для генерации идей.</div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {ideas.map((apiIdea: any) => {
              // Конвертируем API формат в формат компонента
              const idea = {
                id: apiIdea.id.toString(),
                title: apiIdea.title,
                emoji: '💡',
                source: `Trend #${apiIdea.trend_id}`,
                timeAgo: new Date(apiIdea.analyzed_at).toLocaleDateString('ru-RU'),
                score: apiIdea.total_score / 10,
                isTrending: apiIdea.total_score >= 75,
                metrics: {
                  marketSize: apiIdea.market_size_score / 10,
                  competition: apiIdea.competition_score / 10,
                  demand: apiIdea.demand_score / 10,
                  monetization: apiIdea.monetization_score / 10,
                },
                financial: {
                  investment: 50000,
                  paybackMonths: 12,
                  margin: 70,
                  arr: 200000,
                },
              }
              return (
                <IdeaCard
                  key={idea.id}
                  idea={idea}
                  onChatClick={handleChatClick}
                  onDetailsClick={() => handleDetailsClick(idea.id)}
                />
              )
            })}
          </div>
        )}
      </section>

      {/* Active Projects Section */}
      <section className="bg-surface border border-border rounded-lg p-4 shadow-sm">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-lg font-bold flex items-center gap-1">
            <span>📈</span>
            <span>Активные проекты</span>
          </h2>
          <button
            onClick={handleViewAllProjects}
            className="text-sm font-medium text-accent-blue hover:text-accent-purple transition-colors"
          >
            Смотреть все →
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {mockProjects.map((project) => (
            <div
              key={project.id}
              className="bg-surface border border-border rounded-md p-3 transition-smooth hover:-translate-y-1 hover:shadow-lg"
            >
              <h3 className="text-base font-semibold mb-1">
                {project.emoji} {project.title}
              </h3>
              <div className="text-xs text-text-tertiary mb-2">
                {project.statusText}
              </div>

              <div className="space-y-1 my-2">
                {project.status === 'development' && project.progress && (
                  <>
                    <div className="flex items-center justify-between gap-2 text-sm">
                      <span className="text-text-secondary whitespace-nowrap">Backend</span>
                      <div className="flex items-center gap-1 flex-1 min-w-0">
                        <div className="flex-1 h-2 bg-border rounded-full overflow-hidden">
                          <div
                            className="h-full bg-accent-green rounded-full"
                            style={{ width: `${project.progress.backend}%` }}
                          />
                        </div>
                        <span className="font-semibold whitespace-nowrap text-xs sm:text-sm">
                          {project.progress.backend}%
                        </span>
                      </div>
                    </div>
                    <div className="flex items-center justify-between gap-2 text-sm">
                      <span className="text-text-secondary whitespace-nowrap">Frontend</span>
                      <div className="flex items-center gap-1 flex-1 min-w-0">
                        <div className="flex-1 h-2 bg-border rounded-full overflow-hidden">
                          <div
                            className="h-full bg-accent-blue rounded-full"
                            style={{ width: `${project.progress.frontend}%` }}
                          />
                        </div>
                        <span className="font-semibold whitespace-nowrap text-xs sm:text-sm">
                          {project.progress.frontend}%
                        </span>
                      </div>
                    </div>
                  </>
                )}

                {project.status === 'launched' && project.metrics && (
                  <>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-text-secondary">💰 MRR</span>
                      <span className="font-semibold text-accent-green">
                        ${project.metrics.mrr.toLocaleString()}
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-text-secondary">👥 Users</span>
                      <span className="font-semibold">
                        {project.metrics.users.toLocaleString()}
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-text-secondary">📈 Growth</span>
                      <span className="font-semibold text-accent-green">
                        +{project.metrics.growth}% ↑
                      </span>
                    </div>
                  </>
                )}
              </div>

              <div className="flex gap-1 pt-2 border-t border-border">
                {project.status === 'development' ? (
                  <>
                    <button
                      onClick={() => handleProjectAction(project.id, 'Открыть код')}
                      className="flex-1 bg-accent-blue text-white px-2 py-1 rounded-sm text-sm font-medium transition-smooth hover:-translate-y-0.5"
                    >
                      💻 Открыть код
                    </button>
                    <button
                      onClick={() => handleProjectAction(project.id, 'Метрики')}
                      className="flex-1 bg-background border border-border px-2 py-1 rounded-sm text-sm font-medium transition-smooth hover:-translate-y-0.5"
                    >
                      📊 Метрики
                    </button>
                  </>
                ) : (
                  <>
                    <button
                      onClick={() => handleProjectAction(project.id, 'Dashboard')}
                      className="flex-1 bg-accent-blue text-white px-2 py-1 rounded-sm text-sm font-medium transition-smooth hover:-translate-y-0.5"
                    >
                      📊 Dashboard
                    </button>
                    <button
                      onClick={() => handleProjectAction(project.id, 'Sales')}
                      className="flex-1 bg-background border border-border px-2 py-1 rounded-sm text-sm font-medium transition-smooth hover:-translate-y-0.5"
                    >
                      💰 Sales
                    </button>
                  </>
                )}
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
