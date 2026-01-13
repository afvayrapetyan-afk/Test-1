import MetricCard from '../components/dashboard/MetricCard'
import IdeaCard from '../components/ideas/IdeaCard'
import TrendChart from '../components/charts/TrendChart'
import HeroSection from '../components/hero/HeroSection'
import { BarChart3, Code, Sparkles, Filter, SortAsc, Heart, ChevronDown } from 'lucide-react'
import { mockProjects, mockIdeas } from '../data/mockData'
import { useChat } from '../contexts/ChatContext'
import { useNavigate } from 'react-router-dom'
import { useState, useEffect, useMemo } from 'react'
import { API_ENDPOINTS } from '../config/api'
import { Idea, IdeaCategory, categoryLabels } from '../types'
import { AnimatePresence } from 'framer-motion'

type SortOption = 'date' | 'score'
type ViewTab = 'all' | 'favorites'

// localStorage keys
const LIKED_KEY = 'idea_liked_ids'
const HIDDEN_KEY = 'idea_hidden_ids'

export default function Dashboard() {
  const { openChat } = useChat()
  const navigate = useNavigate()
  const [ideas, setIdeas] = useState<Idea[]>([])
  const [loading, setLoading] = useState(true)
  const [useMockData, setUseMockData] = useState(false)

  // Фильтры и сортировка
  const [selectedCategory, setSelectedCategory] = useState<IdeaCategory | 'all'>('all')
  const [sortBy, setSortBy] = useState<SortOption>('date')
  const [viewTab, setViewTab] = useState<ViewTab>('all')
  const [showFilters, setShowFilters] = useState(false)
  const [visibleCount, setVisibleCount] = useState(6)

  // Лайки и скрытые
  const [likedIds, setLikedIds] = useState<Set<string>>(new Set())
  const [hiddenIds, setHiddenIds] = useState<Set<string>>(new Set())

  // Загрузка из localStorage
  useEffect(() => {
    const savedLiked = localStorage.getItem(LIKED_KEY)
    const savedHidden = localStorage.getItem(HIDDEN_KEY)
    if (savedLiked) setLikedIds(new Set(JSON.parse(savedLiked)))
    if (savedHidden) setHiddenIds(new Set(JSON.parse(savedHidden)))
  }, [])

  // Сохранение в localStorage
  useEffect(() => {
    localStorage.setItem(LIKED_KEY, JSON.stringify([...likedIds]))
  }, [likedIds])

  useEffect(() => {
    localStorage.setItem(HIDDEN_KEY, JSON.stringify([...hiddenIds]))
  }, [hiddenIds])

  useEffect(() => {
    const fetchData = async () => {
      const isLocalhost = API_ENDPOINTS.ideas.list.includes('localhost')

      if (isLocalhost) {
        setUseMockData(true)
        setLoading(false)
        return
      }

      try {
        const controller = new AbortController()
        const timeoutId = setTimeout(() => controller.abort(), 5000)

        const ideasResponse = await fetch(API_ENDPOINTS.ideas.list, {
          signal: controller.signal
        })
        clearTimeout(timeoutId)

        if (!ideasResponse.ok) {
          throw new Error('API error')
        }

        const ideasData = await ideasResponse.json()

        if (ideasData.items && ideasData.items.length > 0) {
          setIdeas(ideasData.items)
        } else {
          setUseMockData(true)
        }
      } catch (error) {
        console.error('Error loading data:', error)
        setUseMockData(true)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  // Обработчики лайков
  const handleLike = (id: string) => {
    setLikedIds(prev => {
      const next = new Set(prev)
      if (next.has(id)) {
        next.delete(id)
      } else {
        next.add(id)
      }
      return next
    })
  }

  const handleDislike = (id: string) => {
    setHiddenIds(prev => new Set([...prev, id]))
    // Убираем из лайков если был
    setLikedIds(prev => {
      const next = new Set(prev)
      next.delete(id)
      return next
    })
  }

  const handleChatClick = () => {
    openChat()
  }

  const handleDetailsClick = (ideaId: string) => {
    navigate(`/idea/${ideaId}`)
  }

  // Получаем идеи (mock или API)
  const allIdeas = useMockData ? mockIdeas : ideas

  // Фильтрация и сортировка
  const filteredIdeas = useMemo(() => {
    let result = [...allIdeas]

    // Убираем скрытые
    result = result.filter(idea => !hiddenIds.has(idea.id))

    // Вкладка избранных
    if (viewTab === 'favorites') {
      result = result.filter(idea => likedIds.has(idea.id))
    }

    // Фильтр по категории
    if (selectedCategory !== 'all') {
      result = result.filter(idea => idea.category === selectedCategory)
    }

    // Сортировка
    if (sortBy === 'score') {
      result.sort((a, b) => b.score - a.score)
    } else {
      result.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())
    }

    return result
  }, [allIdeas, hiddenIds, likedIds, viewTab, selectedCategory, sortBy])

  // Видимые идеи (пагинация)
  const visibleIdeas = filteredIdeas.slice(0, visibleCount)
  const hasMore = visibleCount < filteredIdeas.length

  const handleLoadMore = () => {
    setVisibleCount(prev => prev + 6)
  }

  // Получаем уникальные категории
  const categories = useMemo(() => {
    const cats = new Set(allIdeas.map(idea => idea.category).filter(Boolean))
    return ['all', ...cats] as (IdeaCategory | 'all')[]
  }, [allIdeas])

  return (
    <div className="space-y-6">
      {/* Hero Section */}
      <HeroSection />

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        <MetricCard
          label="Всего идей"
          value={loading ? '...' : allIdeas.length.toString()}
          change={`${allIdeas.filter(i => i.score >= 7.5).length} топовых`}
          isPositive={true}
          icon={<BarChart3 />}
        />
        <MetricCard
          label="В избранном"
          value={likedIds.size.toString()}
          change="Ваш выбор"
          isPositive={true}
          icon={<Heart />}
        />
        <MetricCard
          label="Средняя оценка"
          value={loading ? '...' : allIdeas.length > 0 ? (allIdeas.reduce((sum, i) => sum + i.score, 0) / allIdeas.length).toFixed(1) : '0'}
          change="AI анализ"
          isPositive={true}
          icon={<Code />}
        />
        <MetricCard
          label="Скрыто"
          value={hiddenIds.size.toString()}
          change="Не интересует"
          isPositive={false}
          icon={<Sparkles />}
        />
      </div>

      {/* Trend Analytics Chart */}
      <TrendChart />

      {/* Ideas Section */}
      <section data-section="ideas" className="bg-surface border border-border rounded-lg p-4 shadow-sm">
        {/* Tabs */}
        <div className="flex items-center gap-4 mb-4 border-b border-border pb-3">
          <button
            onClick={() => { setViewTab('all'); setVisibleCount(6); }}
            className={`flex items-center gap-2 pb-2 border-b-2 transition-colors ${
              viewTab === 'all'
                ? 'border-accent-blue text-accent-blue font-semibold'
                : 'border-transparent text-text-secondary hover:text-text-primary'
            }`}
          >
            🔥 Все идеи
            <span className="text-xs bg-background px-2 py-0.5 rounded-full">
              {allIdeas.filter(i => !hiddenIds.has(i.id)).length}
            </span>
          </button>
          <button
            onClick={() => { setViewTab('favorites'); setVisibleCount(6); }}
            className={`flex items-center gap-2 pb-2 border-b-2 transition-colors ${
              viewTab === 'favorites'
                ? 'border-accent-blue text-accent-blue font-semibold'
                : 'border-transparent text-text-secondary hover:text-text-primary'
            }`}
          >
            ❤️ Избранное
            <span className="text-xs bg-background px-2 py-0.5 rounded-full">
              {likedIds.size}
            </span>
          </button>
        </div>

        {/* Filters Bar */}
        <div className="flex flex-wrap items-center gap-2 mb-4">
          {/* Category Filter */}
          <div className="relative">
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="flex items-center gap-2 px-3 py-1.5 bg-background border border-border rounded-lg text-sm hover:border-accent-blue transition-colors"
            >
              <Filter className="w-4 h-4" />
              <span className="hidden sm:inline">Категория:</span>
              <span className="font-medium">
                {selectedCategory === 'all' ? 'Все' : categoryLabels[selectedCategory]}
              </span>
              <ChevronDown className="w-4 h-4" />
            </button>
            {showFilters && (
              <div className="absolute top-full left-0 mt-1 bg-surface border border-border rounded-lg shadow-lg z-20 min-w-[180px]">
                {categories.map(cat => (
                  <button
                    key={cat}
                    onClick={() => { setSelectedCategory(cat); setShowFilters(false); setVisibleCount(6); }}
                    className={`w-full text-left px-3 py-2 text-sm hover:bg-background transition-colors first:rounded-t-lg last:rounded-b-lg ${
                      selectedCategory === cat ? 'text-accent-blue font-medium' : 'text-text-primary'
                    }`}
                  >
                    {cat === 'all' ? 'Все категории' : categoryLabels[cat]}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Sort */}
          <div className="flex items-center gap-1 bg-background border border-border rounded-lg p-0.5">
            <button
              onClick={() => setSortBy('date')}
              className={`flex items-center gap-1.5 px-3 py-1 rounded-md text-sm transition-colors ${
                sortBy === 'date'
                  ? 'bg-accent-blue text-white'
                  : 'text-text-secondary hover:text-text-primary'
              }`}
            >
              <SortAsc className="w-4 h-4" />
              <span className="hidden sm:inline">По дате</span>
            </button>
            <button
              onClick={() => setSortBy('score')}
              className={`flex items-center gap-1.5 px-3 py-1 rounded-md text-sm transition-colors ${
                sortBy === 'score'
                  ? 'bg-accent-blue text-white'
                  : 'text-text-secondary hover:text-text-primary'
              }`}
            >
              <Sparkles className="w-4 h-4" />
              <span className="hidden sm:inline">По оценке</span>
            </button>
          </div>

          {/* Results count */}
          <span className="text-sm text-text-tertiary ml-auto">
            Показано {visibleIdeas.length} из {filteredIdeas.length}
          </span>
        </div>

        {/* Demo mode banner */}
        {useMockData && viewTab === 'all' && (
          <div className="bg-accent-blue/10 border border-accent-blue/20 rounded-lg p-3 mb-4">
            <p className="text-sm text-accent-blue">
              📌 Демо-режим: показаны примеры идей. Подключите бэкенд для реальных данных.
            </p>
          </div>
        )}

        {/* Ideas Grid */}
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="text-text-secondary">Загрузка данных...</div>
          </div>
        ) : filteredIdeas.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <div className="text-4xl mb-3">
              {viewTab === 'favorites' ? '❤️' : '🔍'}
            </div>
            <div className="text-text-secondary mb-2">
              {viewTab === 'favorites'
                ? 'Пока нет избранных идей'
                : 'Нет идей по выбранным фильтрам'}
            </div>
            <p className="text-sm text-text-tertiary">
              {viewTab === 'favorites'
                ? 'Нажмите ❤️ на карточке чтобы добавить в избранное'
                : 'Попробуйте изменить фильтры'}
            </p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              <AnimatePresence>
                {visibleIdeas.map((idea) => (
                  <IdeaCard
                    key={idea.id}
                    idea={idea}
                    onChatClick={handleChatClick}
                    onDetailsClick={() => handleDetailsClick(idea.id)}
                    onLike={handleLike}
                    onDislike={handleDislike}
                    isLiked={likedIds.has(idea.id)}
                  />
                ))}
              </AnimatePresence>
            </div>

            {/* Load More */}
            {hasMore && (
              <div className="flex justify-center mt-6">
                <button
                  onClick={handleLoadMore}
                  className="px-6 py-2 bg-background border border-border rounded-lg text-sm font-medium hover:border-accent-blue hover:text-accent-blue transition-colors"
                >
                  Показать ещё ({filteredIdeas.length - visibleCount} осталось)
                </button>
              </div>
            )}
          </>
        )}
      </section>

      {/* Active Projects Section */}
      <section className="bg-surface border border-border rounded-lg p-4 shadow-sm">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-lg font-bold flex items-center gap-1">
            <span>📈</span>
            <span>Активные проекты</span>
          </h2>
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
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
