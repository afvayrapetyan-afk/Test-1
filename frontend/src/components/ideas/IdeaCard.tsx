import { MessageCircle, FileText } from 'lucide-react'
import { motion } from 'framer-motion'
import { Idea } from '../../types'

interface IdeaCardProps {
  idea: Idea
  onChatClick?: () => void
  onDetailsClick?: () => void
}

// Tier system для визуальной оценки идеи
const getTier = (score: number) => {
  if (score >= 8.5) {
    return {
      tier: 'S',
      color: 'orange-500',
      bgColor: 'bg-orange-50 dark:bg-orange-950/20',
      borderColor: 'border-orange-500',
      textColor: 'text-orange-500',
      label: 'Превосходно',
    }
  }
  if (score >= 7.5) {
    return {
      tier: 'A',
      color: 'green-500',
      bgColor: 'bg-green-50 dark:bg-green-950/20',
      borderColor: 'border-green-500',
      textColor: 'text-green-500',
      label: 'Отлично',
    }
  }
  if (score >= 6.5) {
    return {
      tier: 'B',
      color: 'blue-500',
      bgColor: 'bg-blue-50 dark:bg-blue-950/20',
      borderColor: 'border-blue-500',
      textColor: 'text-blue-500',
      label: 'Хорошо',
    }
  }
  return {
    tier: 'C',
    color: 'gray-500',
    bgColor: 'bg-gray-50 dark:bg-gray-950/20',
    borderColor: 'border-gray-500',
    textColor: 'text-gray-500',
    label: 'Средне',
  }
}

export default function IdeaCard({
  idea,
  onChatClick,
  onDetailsClick,
}: IdeaCardProps) {
  const tier = getTier(idea.score)

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -4 }}
      className={`relative bg-surface border-l-4 ${tier.borderColor} border-r border-t border-b border-border rounded-md p-4 transition-smooth hover:shadow-lg cursor-pointer overflow-hidden`}
    >
      {/* Tier Badge */}
      <div className="absolute top-3 right-3 z-10">
        <div className={`${tier.bgColor} ${tier.borderColor} border-2 rounded-full w-10 h-10 sm:w-12 sm:h-12 flex items-center justify-center`}>
          <span className={`font-extrabold text-base sm:text-lg ${tier.textColor}`}>
            {tier.tier}
          </span>
        </div>
      </div>

      {/* Hero Section - Score + Title */}
      <div className="pr-14 sm:pr-16 mb-4">
        {/* Large Score */}
        <div className={`text-4xl sm:text-5xl font-extrabold mb-2 ${tier.textColor}`}>
          {idea.score.toFixed(1)}
          <span className="text-lg text-text-tertiary">/10</span>
        </div>

        {/* Title */}
        <h3 className="text-base sm:text-lg font-bold mb-1 flex items-center gap-2">
          <span>{idea.emoji}</span>
          <span className="break-words">{idea.title}</span>
        </h3>

        {/* Source & TimeAgo */}
        <div className="text-xs text-text-tertiary">
          {idea.source} • {idea.timeAgo}
        </div>
      </div>

      {/* Divider */}
      <div className="border-t border-border my-3" />

      {/* Key Metrics Section */}
      <div className="mb-3">
        <h4 className="text-xs font-semibold text-text-secondary mb-2 uppercase tracking-wide">
          🎯 Ключевые метрики
        </h4>
        <div className="space-y-2">
          {/* Размер рынка */}
          <div className="flex items-center justify-between gap-2 text-xs sm:text-sm">
            <span className="text-text-secondary whitespace-nowrap flex-shrink-0">
              💡 Размер рынка
            </span>
            <div className="flex items-center gap-1 flex-1 min-w-0">
              <div className="flex-1 h-2 bg-border rounded-full overflow-hidden min-w-[60px]">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${idea.metrics.marketSize * 10}%` }}
                  transition={{ duration: 0.5, delay: 0.1 }}
                  className="h-full bg-gradient-to-r from-accent-blue to-accent-purple rounded-full"
                />
              </div>
              <span className="font-semibold text-text-primary w-8 text-right whitespace-nowrap text-xs">
                {idea.metrics.marketSize}/10
              </span>
            </div>
          </div>

          {/* Спрос */}
          <div className="flex items-center justify-between gap-2 text-xs sm:text-sm">
            <span className="text-text-secondary whitespace-nowrap flex-shrink-0">
              🔥 Спрос
            </span>
            <div className="flex items-center gap-1 flex-1 min-w-0">
              <div className="flex-1 h-2 bg-border rounded-full overflow-hidden min-w-[60px]">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${idea.metrics.demand * 10}%` }}
                  transition={{ duration: 0.5, delay: 0.2 }}
                  className="h-full bg-gradient-to-r from-accent-blue to-accent-purple rounded-full"
                />
              </div>
              <span className="font-semibold text-text-primary w-8 text-right whitespace-nowrap text-xs">
                {idea.metrics.demand}/10
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Divider */}
      <div className="border-t border-border my-3" />

      {/* Financial Summary */}
      <div className="mb-3">
        <h4 className="text-xs font-semibold text-text-secondary mb-2 uppercase tracking-wide">
          💰 Финансы
        </h4>
        <div className="text-xs sm:text-sm text-text-primary flex flex-wrap gap-x-2 gap-y-1">
          <span className="whitespace-nowrap">
            <span className="font-bold text-accent-blue">
              ${idea.financial.investment / 1000}K
            </span>{' '}
            старт
          </span>
          <span className="text-text-tertiary">•</span>
          <span className="whitespace-nowrap">
            <span className="font-bold text-accent-green">
              {idea.financial.paybackMonths} мес
            </span>{' '}
            окупаемость
          </span>
          <span className="text-text-tertiary">•</span>
          <span className="whitespace-nowrap">
            <span className="font-bold text-accent-green">
              {idea.financial.margin}%
            </span>{' '}
            маржа
          </span>
        </div>
      </div>

      {/* Divider */}
      <div className="border-t border-border my-3" />

      {/* Actions */}
      <div className="flex gap-2">
        <button
          onClick={onChatClick}
          className="flex-1 bg-gradient-to-r from-accent-purple to-accent-pink text-white px-3 py-2 rounded-md text-xs sm:text-sm font-medium flex items-center justify-center gap-1.5 transition-smooth hover:-translate-y-0.5 hover:shadow-md"
        >
          <MessageCircle className="w-3.5 h-3.5" />
          Спросить AI
        </button>
        <button
          onClick={onDetailsClick}
          className="flex-1 bg-background text-text-primary px-3 py-2 rounded-md text-xs sm:text-sm font-medium border border-border flex items-center justify-center gap-1.5 transition-smooth hover:-translate-y-0.5"
        >
          <FileText className="w-3.5 h-3.5" />
          Подробнее
        </button>
      </div>
    </motion.div>
  )
}
