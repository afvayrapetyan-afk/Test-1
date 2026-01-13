import MetricCard from '../components/dashboard/MetricCard'
import IdeaCard from '../components/ideas/IdeaCard'
import TrendChart from '../components/charts/TrendChart'
import { BarChart3, Briefcase, Code, Sparkles } from 'lucide-react'
import { mockIdeas, mockProjects } from '../data/mockData'
import { useChat } from '../contexts/ChatContext'
import { useNavigate } from 'react-router-dom'

export default function Dashboard() {
  const { openChat } = useChat()
  const navigate = useNavigate()

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
      {/* Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        <MetricCard
          label="Всего идей"
          value="247"
          change="+23 за неделю"
          isPositive={true}
          icon={<BarChart3 />}
        />
        <MetricCard
          label="Активных бизнесов"
          value="12"
          change="$47K выручка"
          isPositive={true}
          icon={<Briefcase />}
        />
        <MetricCard
          label="В разработке"
          value="8"
          change="+2 в этом месяце"
          isPositive={true}
          icon={<Code />}
        />
        <MetricCard
          label="AI анализов сегодня"
          value="34"
          change="+12 с утра"
          isPositive={true}
          icon={<Sparkles />}
        />
      </div>

      {/* Trend Analytics Chart */}
      <TrendChart />

      {/* Trending Ideas Section */}
      <section className="bg-surface border border-border rounded-lg p-4 shadow-sm">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-lg font-bold flex items-center gap-1">
            <span>🔥</span>
            <span>Горячие тренды</span>
          </h2>
          <button
            onClick={handleViewAllIdeas}
            className="text-sm font-medium text-accent-blue hover:text-accent-purple transition-colors"
          >
            Смотреть все →
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {mockIdeas.map((idea) => (
            <IdeaCard
              key={idea.id}
              idea={idea}
              onChatClick={handleChatClick}
              onDetailsClick={() => handleDetailsClick(idea.id)}
            />
          ))}
        </div>
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
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-text-secondary">Backend</span>
                      <div className="flex items-center gap-1">
                        <div className="w-[200px] h-2 bg-border rounded-full overflow-hidden">
                          <div
                            className="h-full bg-accent-green rounded-full"
                            style={{ width: `${project.progress.backend}%` }}
                          />
                        </div>
                        <span className="font-semibold">
                          {project.progress.backend}%
                        </span>
                      </div>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-text-secondary">Frontend</span>
                      <div className="flex items-center gap-1">
                        <div className="w-[200px] h-2 bg-border rounded-full overflow-hidden">
                          <div
                            className="h-full bg-accent-blue rounded-full"
                            style={{ width: `${project.progress.frontend}%` }}
                          />
                        </div>
                        <span className="font-semibold">
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
