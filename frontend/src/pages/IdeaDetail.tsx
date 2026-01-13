import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { mockIdeas } from '../data/mockData'

export default function IdeaDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const idea = mockIdeas.find((i) => i.id === id) || mockIdeas[0]

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
              {idea.emoji} {idea.title}
            </h1>
            <p className="text-blue-100 text-lg mb-6">
              AI-powered персонализированное питание с доставкой на дом
            </p>
            <div className="flex gap-4">
              <div className="bg-white/20 backdrop-blur-sm rounded-lg px-4 py-2">
                <div className="text-sm text-blue-100">Инвестиции</div>
                <div className="text-2xl font-bold">
                  ${idea.financial.investment / 1000}K
                </div>
              </div>
              <div className="bg-white/20 backdrop-blur-sm rounded-lg px-4 py-2">
                <div className="text-sm text-blue-100">Окупаемость</div>
                <div className="text-2xl font-bold">
                  {idea.financial.paybackMonths} мес
                </div>
              </div>
              <div className="bg-white/20 backdrop-blur-sm rounded-lg px-4 py-2">
                <div className="text-sm text-blue-100">Маржа</div>
                <div className="text-2xl font-bold">
                  {idea.financial.margin}%
                </div>
              </div>
            </div>
          </div>
          <div className="bg-white/20 backdrop-blur-sm rounded-2xl px-6 py-4 text-center">
            <div className="text-sm text-blue-100 mb-2">Общий Score</div>
            <div className="text-5xl font-bold">{idea.score}</div>
            <div className="text-sm text-blue-100">/10</div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Executive Summary */}
          <section className="bg-surface border border-border rounded-xl p-6">
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
              📊 Executive Summary
            </h2>
            <div className="space-y-4 text-text-secondary">
              <p>
                AI Personal Chef — это инновационный сервис персонализированного
                питания, использующий искусственный интеллект для создания
                индивидуальных планов питания и автоматической доставки
                ингредиентов.
              </p>
              <div className="bg-blue-50 dark:bg-blue-950/20 border-l-4 border-blue-500 p-4 rounded">
                <h3 className="font-semibold text-text-primary mb-2">
                  Ключевая ценность
                </h3>
                <p>
                  Экономия 10+ часов в неделю на планирование питания и покупки
                  + улучшение здоровья через персонализированное питание
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-text-primary mb-2">
                  Целевая аудитория
                </h3>
                <ul className="list-disc list-inside space-y-1">
                  <li>Молодые профессионалы 25-40 лет</li>
                  <li>Семьи с детьми</li>
                  <li>Люди с особыми диетическими потребностями</li>
                  <li>Фитнес-энтузиасты</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Market Analysis */}
          <section className="bg-surface border border-border rounded-xl p-6">
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
              🌍 Анализ рынка
            </h2>
            <div className="space-y-4">
              <div className="grid grid-cols-3 gap-4">
                <div className="bg-background rounded-lg p-4 text-center">
                  <div className="text-sm text-text-secondary mb-1">TAM</div>
                  <div className="text-2xl font-bold text-accent-blue">$52B</div>
                  <div className="text-xs text-text-tertiary">Total Market</div>
                </div>
                <div className="bg-background rounded-lg p-4 text-center">
                  <div className="text-sm text-text-secondary mb-1">SAM</div>
                  <div className="text-2xl font-bold text-accent-green">$8B</div>
                  <div className="text-xs text-text-tertiary">Serviceable</div>
                </div>
                <div className="bg-background rounded-lg p-4 text-center">
                  <div className="text-sm text-text-secondary mb-1">SOM</div>
                  <div className="text-2xl font-bold text-accent-orange">$400M</div>
                  <div className="text-xs text-text-tertiary">Obtainable</div>
                </div>
              </div>
              <div className="bg-green-50 dark:bg-green-950/20 border-l-4 border-green-500 p-4 rounded">
                <h3 className="font-semibold text-text-primary mb-2">
                  Темп роста
                </h3>
                <p className="text-text-secondary">
                  Рынок персонализированного питания растет на{' '}
                  <span className="font-bold text-green-600">+23% CAGR</span>{' '}
                  (2024-2029)
                </p>
              </div>
            </div>
          </section>

          {/* Competitors */}
          <section className="bg-surface border border-border rounded-xl p-6">
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
              🏪 Конкуренты
            </h2>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border">
                    <th className="text-left py-2 font-semibold">Компания</th>
                    <th className="text-left py-2 font-semibold">Доля рынка</th>
                    <th className="text-left py-2 font-semibold">Слабости</th>
                  </tr>
                </thead>
                <tbody className="text-text-secondary">
                  <tr className="border-b border-border">
                    <td className="py-3">HelloFresh</td>
                    <td className="py-3">24%</td>
                    <td className="py-3">Нет AI, стандартные рецепты</td>
                  </tr>
                  <tr className="border-b border-border">
                    <td className="py-3">Blue Apron</td>
                    <td className="py-3">8%</td>
                    <td className="py-3">Высокая цена, нет персонализации</td>
                  </tr>
                  <tr className="border-b border-border">
                    <td className="py-3">Factor</td>
                    <td className="py-3">5%</td>
                    <td className="py-3">Только готовые блюда</td>
                  </tr>
                  <tr>
                    <td className="py-3">Sunbasket</td>
                    <td className="py-3">4%</td>
                    <td className="py-3">Ограниченный ассортимент</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          {/* Strategy */}
          <section className="bg-surface border border-border rounded-xl p-6">
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
              🎯 Стратегия запуска
            </h2>
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold text-text-primary mb-2">
                  Фаза 1: MVP (Месяцы 1-3)
                </h3>
                <ul className="list-disc list-inside text-text-secondary space-y-1">
                  <li>Запуск в одном городе (SF Bay Area)</li>
                  <li>AI модель на базе GPT-4 для планирования меню</li>
                  <li>Партнерство с 3-5 локальными поставщиками</li>
                  <li>Целевая метрика: 100 платящих клиентов</li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold text-text-primary mb-2">
                  Фаза 2: Масштабирование (Месяцы 4-12)
                </h3>
                <ul className="list-disc list-inside text-text-secondary space-y-1">
                  <li>Расширение на 5 крупных городов</li>
                  <li>Мобильное приложение (iOS + Android)</li>
                  <li>Интеграция с фитнес-трекерами</li>
                  <li>Целевая метрика: 2,000 клиентов, $50K MRR</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Financials */}
          <section className="bg-surface border border-border rounded-xl p-6">
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
              💰 Финансовый прогноз
            </h2>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border">
                    <th className="text-left py-2 font-semibold">Метрика</th>
                    <th className="text-right py-2 font-semibold">Год 1</th>
                    <th className="text-right py-2 font-semibold">Год 2</th>
                    <th className="text-right py-2 font-semibold">Год 3</th>
                  </tr>
                </thead>
                <tbody className="text-text-secondary">
                  <tr className="border-b border-border">
                    <td className="py-3">Выручка</td>
                    <td className="py-3 text-right font-semibold">$180K</td>
                    <td className="py-3 text-right font-semibold">$850K</td>
                    <td className="py-3 text-right font-semibold">$2.4M</td>
                  </tr>
                  <tr className="border-b border-border">
                    <td className="py-3">Валовая маржа</td>
                    <td className="py-3 text-right">65%</td>
                    <td className="py-3 text-right">68%</td>
                    <td className="py-3 text-right">70%</td>
                  </tr>
                  <tr className="border-b border-border">
                    <td className="py-3">Операционные расходы</td>
                    <td className="py-3 text-right">$120K</td>
                    <td className="py-3 text-right">$400K</td>
                    <td className="py-3 text-right">$950K</td>
                  </tr>
                  <tr>
                    <td className="py-3 font-semibold">Чистая прибыль</td>
                    <td className="py-3 text-right font-semibold text-red-500">
                      -$3K
                    </td>
                    <td className="py-3 text-right font-semibold text-green-500">
                      +$178K
                    </td>
                    <td className="py-3 text-right font-semibold text-green-500">
                      +$730K
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          {/* Risks */}
          <section className="bg-surface border border-border rounded-xl p-6">
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
              ⚠️ Риски и митигация
            </h2>
            <div className="space-y-3">
              <div className="bg-red-50 dark:bg-red-950/20 border-l-4 border-red-500 p-4 rounded">
                <h3 className="font-semibold text-text-primary mb-2">
                  🔴 Высокий: Конкуренция с крупными игроками
                </h3>
                <p className="text-text-secondary text-sm mb-2">
                  HelloFresh и другие могут добавить AI функции
                </p>
                <p className="text-text-secondary text-sm">
                  <strong>Митигация:</strong> Фокус на superior AI, быстрая
                  итерация, патенты на алгоритмы
                </p>
              </div>
              <div className="bg-orange-50 dark:bg-orange-950/20 border-l-4 border-orange-500 p-4 rounded">
                <h3 className="font-semibold text-text-primary mb-2">
                  🟠 Средний: Unit economics
                </h3>
                <p className="text-text-secondary text-sm mb-2">
                  Высокие затраты на доставку могут убить маржу
                </p>
                <p className="text-text-secondary text-sm">
                  <strong>Митигация:</strong> Оптимизация маршрутов, партнерство
                  с DoorDash, минимальный заказ $50
                </p>
              </div>
            </div>
          </section>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Quick Stats */}
          <div className="bg-surface border border-border rounded-xl p-6">
            <h3 className="font-bold mb-4">Ключевые метрики</h3>
            <div className="space-y-3">
              <div>
                <div className="text-sm text-text-secondary">Размер рынка</div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-2 bg-border rounded-full overflow-hidden">
                    <div
                      className="h-full bg-accent-blue rounded-full"
                      style={{ width: `${idea.metrics.marketSize * 10}%` }}
                    />
                  </div>
                  <span className="text-sm font-semibold">
                    {idea.metrics.marketSize}/10
                  </span>
                </div>
              </div>
              <div>
                <div className="text-sm text-text-secondary">Конкуренция</div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-2 bg-border rounded-full overflow-hidden">
                    <div
                      className="h-full bg-accent-orange rounded-full"
                      style={{ width: `${idea.metrics.competition * 10}%` }}
                    />
                  </div>
                  <span className="text-sm font-semibold">
                    {idea.metrics.competition}/10
                  </span>
                </div>
              </div>
              <div>
                <div className="text-sm text-text-secondary">Спрос</div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-2 bg-border rounded-full overflow-hidden">
                    <div
                      className="h-full bg-accent-green rounded-full"
                      style={{ width: `${idea.metrics.demand * 10}%` }}
                    />
                  </div>
                  <span className="text-sm font-semibold">
                    {idea.metrics.demand}/10
                  </span>
                </div>
              </div>
              <div>
                <div className="text-sm text-text-secondary">Монетизация</div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-2 bg-border rounded-full overflow-hidden">
                    <div
                      className="h-full bg-accent-purple rounded-full"
                      style={{ width: `${idea.metrics.monetization * 10}%` }}
                    />
                  </div>
                  <span className="text-sm font-semibold">
                    {idea.metrics.monetization}/10
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Roadmap */}
          <div className="bg-surface border border-border rounded-xl p-6">
            <h3 className="font-bold mb-4">🗺️ Roadmap</h3>
            <div className="space-y-4">
              <div className="relative pl-6 border-l-2 border-accent-blue pb-4">
                <div className="absolute -left-2 top-0 w-4 h-4 rounded-full bg-accent-blue" />
                <div className="text-sm font-semibold">Q1 2024</div>
                <div className="text-sm text-text-secondary">MVP Launch</div>
              </div>
              <div className="relative pl-6 border-l-2 border-border pb-4">
                <div className="absolute -left-2 top-0 w-4 h-4 rounded-full bg-border" />
                <div className="text-sm font-semibold">Q2 2024</div>
                <div className="text-sm text-text-secondary">
                  Mobile App + 5 cities
                </div>
              </div>
              <div className="relative pl-6 border-l-2 border-border pb-4">
                <div className="absolute -left-2 top-0 w-4 h-4 rounded-full bg-border" />
                <div className="text-sm font-semibold">Q3 2024</div>
                <div className="text-sm text-text-secondary">
                  Series A + 20 cities
                </div>
              </div>
              <div className="relative pl-6">
                <div className="absolute -left-2 top-0 w-4 h-4 rounded-full bg-border" />
                <div className="text-sm font-semibold">Q4 2024</div>
                <div className="text-sm text-text-secondary">
                  National expansion
                </div>
              </div>
            </div>
          </div>

          {/* Team */}
          <div className="bg-surface border border-border rounded-xl p-6">
            <h3 className="font-bold mb-4">👥 Команда</h3>
            <div className="space-y-3 text-sm">
              <div>
                <div className="font-semibold">CEO / Tech Lead</div>
                <div className="text-text-secondary">
                  ex-Google AI, Stanford CS
                </div>
              </div>
              <div>
                <div className="font-semibold">COO / Logistics</div>
                <div className="text-text-secondary">
                  ex-DoorDash Operations
                </div>
              </div>
              <div>
                <div className="font-semibold">Hiring</div>
                <div className="text-text-secondary">
                  Lead Chef, Marketing Head
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
