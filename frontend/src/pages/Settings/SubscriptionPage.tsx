import { Link } from 'react-router-dom'
import { Check, Crown, Zap, Star, ArrowLeft } from 'lucide-react'
import { useAuth } from '../../contexts/AuthContext'
import { motion } from 'framer-motion'

interface Plan {
  id: 'free' | 'pro' | 'enterprise'
  name: string
  price: number
  period: string
  description: string
  features: string[]
  popular?: boolean
}

const plans: Plan[] = [
  {
    id: 'free',
    name: 'Free',
    price: 0,
    period: 'навсегда',
    description: 'Для начинающих предпринимателей',
    features: [
      'До 10 идей',
      'Базовая аналитика',
      'AI чат (10 сообщений/день)',
      'Экспорт в PDF',
      'Email поддержка',
    ],
  },
  {
    id: 'pro',
    name: 'Pro',
    price: 1990,
    period: 'месяц',
    description: 'Для активных пользователей',
    features: [
      'Неограниченные идеи',
      'Расширенная аналитика',
      'AI чат (неограниченно)',
      'Приоритетная поддержка',
      'API доступ',
      'Кастомные отчеты',
      'Командная работа (до 5 человек)',
    ],
    popular: true,
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    price: 9990,
    period: 'месяц',
    description: 'Для крупных команд',
    features: [
      'Все функции Pro',
      'Неограниченная команда',
      'Персональный менеджер',
      'Custom AI модели',
      'On-premise решения',
      'SLA 99.9%',
      'Индивидуальная интеграция',
    ],
  },
]

export default function SubscriptionPage() {
  const { user } = useAuth()

  const handleUpgrade = (planId: string) => {
    // В реальном приложении здесь будет redirect на страницу оплаты
    alert(`Переход на оплату плана: ${planId}`)
  }

  const currentPlan = user?.plan || 'free'
  const daysLeft = user?.planExpiry
    ? Math.ceil((user.planExpiry.getTime() - Date.now()) / (1000 * 60 * 60 * 24))
    : null

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Back Link */}
        <Link
          to="/"
          className="inline-flex items-center gap-2 text-sm text-text-secondary hover:text-text-primary transition-colors mb-6"
        >
          <ArrowLeft className="w-4 h-4" />
          Назад к дашборду
        </Link>

        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">
            Выберите свой план
          </h1>
          <p className="text-lg text-text-secondary max-w-2xl mx-auto">
            Получите доступ ко всем возможностям AI Portfolio Manager
          </p>
        </div>

        {/* Current Plan Status */}
        {currentPlan !== 'free' && (
          <div className="max-w-3xl mx-auto mb-8">
            <div className="bg-gradient-to-r from-accent-purple to-accent-pink p-6 rounded-xl text-white">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
                    <Crown className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-lg">
                      Текущий план: {plans.find(p => p.id === currentPlan)?.name}
                    </h3>
                    {daysLeft && (
                      <p className="text-sm text-white/90">
                        Активен еще {daysLeft} {daysLeft === 1 ? 'день' : daysLeft < 5 ? 'дня' : 'дней'}
                      </p>
                    )}
                  </div>
                </div>
                <Link
                  to="/settings"
                  className="px-4 py-2 bg-white text-accent-purple font-semibold rounded-lg hover:bg-white/90 transition-all"
                >
                  Управление
                </Link>
              </div>
            </div>
          </div>
        )}

        {/* Plans Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {plans.map((plan) => (
            <motion.div
              key={plan.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className={`relative bg-surface border ${
                plan.popular
                  ? 'border-accent-purple shadow-xl scale-105'
                  : 'border-border'
              } rounded-2xl p-6 transition-all hover:shadow-lg ${
                plan.id === currentPlan ? 'ring-2 ring-accent-green' : ''
              }`}
            >
              {/* Popular Badge */}
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                  <div className="bg-gradient-to-r from-accent-purple to-accent-pink text-white px-4 py-1 rounded-full text-sm font-bold flex items-center gap-1">
                    <Star className="w-4 h-4" />
                    Популярный
                  </div>
                </div>
              )}

              {/* Current Plan Badge */}
              {plan.id === currentPlan && (
                <div className="absolute -top-4 right-4">
                  <div className="bg-accent-green text-white px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1">
                    <Check className="w-3 h-3" />
                    Текущий
                  </div>
                </div>
              )}

              {/* Plan Header */}
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
                <p className="text-text-secondary text-sm mb-4">
                  {plan.description}
                </p>
                <div className="flex items-baseline justify-center gap-2">
                  <span className="text-4xl font-bold">
                    {plan.price === 0 ? 'Бесплатно' : `₽${plan.price.toLocaleString()}`}
                  </span>
                  {plan.price > 0 && (
                    <span className="text-text-secondary">/ {plan.period}</span>
                  )}
                </div>
              </div>

              {/* Features */}
              <ul className="space-y-3 mb-6">
                {plan.features.map((feature, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <Check className="w-5 h-5 text-accent-green flex-shrink-0 mt-0.5" />
                    <span className="text-sm">{feature}</span>
                  </li>
                ))}
              </ul>

              {/* CTA Button */}
              <button
                onClick={() => handleUpgrade(plan.id)}
                disabled={plan.id === currentPlan}
                className={`w-full py-3 font-semibold rounded-lg transition-all ${
                  plan.id === currentPlan
                    ? 'bg-gray-200 dark:bg-gray-700 text-text-secondary cursor-not-allowed'
                    : plan.popular
                    ? 'bg-gradient-to-r from-accent-purple to-accent-pink text-white hover:shadow-lg'
                    : 'bg-accent-blue text-white hover:bg-accent-blue/90'
                }`}
              >
                {plan.id === currentPlan
                  ? 'Текущий план'
                  : plan.price === 0
                  ? 'Начать бесплатно'
                  : 'Выбрать план'}
              </button>
            </motion.div>
          ))}
        </div>

        {/* Payment Methods */}
        <div className="mt-16 max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold text-center mb-8">
            Способы оплаты
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {['Visa', 'Mastercard', 'Мир', 'СБП'].map((method) => (
              <div
                key={method}
                className="bg-surface border border-border rounded-lg p-4 flex items-center justify-center hover:border-accent-purple transition-colors"
              >
                <span className="font-semibold text-text-secondary">{method}</span>
              </div>
            ))}
          </div>
        </div>

        {/* FAQ */}
        <div className="mt-16 max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold text-center mb-8">
            Частые вопросы
          </h2>
          <div className="space-y-4">
            <div className="bg-surface border border-border rounded-lg p-6">
              <h3 className="font-semibold mb-2">Могу ли я отменить подписку в любой момент?</h3>
              <p className="text-text-secondary text-sm">
                Да, вы можете отменить подписку в любой момент. Доступ к функциям Pro сохранится до конца оплаченного периода.
              </p>
            </div>
            <div className="bg-surface border border-border rounded-lg p-6">
              <h3 className="font-semibold mb-2">Есть ли корпоративные скидки?</h3>
              <p className="text-text-secondary text-sm">
                Да, для команд от 10 человек мы предлагаем индивидуальные условия. Свяжитесь с нами для обсуждения.
              </p>
            </div>
            <div className="bg-surface border border-border rounded-lg p-6">
              <h3 className="font-semibold mb-2">Какие методы оплаты поддерживаются?</h3>
              <p className="text-text-secondary text-sm">
                Мы принимаем все основные банковские карты (Visa, Mastercard, МИР), а также СБП и другие способы оплаты.
              </p>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="mt-16 bg-gradient-to-r from-accent-purple to-accent-pink rounded-2xl p-12 text-white text-center">
          <h2 className="text-3xl font-bold mb-4">
            Готовы начать?
          </h2>
          <p className="text-lg text-white/90 mb-8 max-w-2xl mx-auto">
            Присоединяйтесь к тысячам предпринимателей, которые уже используют AI Portfolio Manager
          </p>
          <Link
            to="/register"
            className="inline-flex items-center gap-2 px-8 py-4 bg-white text-accent-purple font-bold rounded-lg hover:bg-white/90 transition-all"
          >
            <Zap className="w-5 h-5" />
            Начать бесплатно
          </Link>
        </div>
      </div>
    </div>
  )
}
