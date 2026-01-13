import { MessageCircle, FileText, TrendingUp, Users, DollarSign, Clock, Heart, X } from 'lucide-react'
import { motion } from 'framer-motion'
import { Idea, categoryLabels } from '../../types'

interface IdeaCardProps {
  idea: Idea
  onChatClick?: () => void
  onDetailsClick?: () => void
  onLike?: (id: string) => void
  onDislike?: (id: string) => void
  isLiked?: boolean
  showActions?: boolean
}

// Система рейтинга с понятными русскими названиями
const getRating = (score: number) => {
  if (score >= 8.5) {
    return {
      label: 'Топ',
      emoji: '🔥',
      bgColor: 'bg-orange-500',
      textColor: 'text-white',
      borderColor: 'border-l-orange-500',
    }
  }
  if (score >= 7.5) {
    return {
      label: 'Отлично',
      emoji: '✨',
      bgColor: 'bg-green-500',
      textColor: 'text-white',
      borderColor: 'border-l-green-500',
    }
  }
  if (score >= 6.5) {
    return {
      label: 'Хорошо',
      emoji: '👍',
      bgColor: 'bg-blue-500',
      textColor: 'text-white',
      borderColor: 'border-l-blue-500',
    }
  }
  return {
    label: 'Средне',
    emoji: '📊',
    bgColor: 'bg-gray-500',
    textColor: 'text-white',
    borderColor: 'border-l-gray-500',
  }
}

export default function IdeaCard({
  idea,
  onChatClick,
  onDetailsClick,
  onLike,
  onDislike,
  isLiked = false,
  showActions = true,
}: IdeaCardProps) {
  const rating = getRating(idea.score)

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, x: -100, scale: 0.9 }}
      whileHover={{ y: -4 }}
      className={`relative bg-surface border border-border ${rating.borderColor} border-l-4 rounded-lg p-4 transition-smooth hover:shadow-lg cursor-pointer`}
      onClick={onDetailsClick}
    >
      {/* Like/Dislike buttons - top right */}
      {showActions && (
        <div className="absolute top-2 right-2 flex gap-1 z-10">
          <button
            onClick={(e) => {
              e.stopPropagation()
              onDislike?.(idea.id)
            }}
            className="w-8 h-8 flex items-center justify-center rounded-full bg-background border border-border text-text-tertiary hover:text-red-500 hover:border-red-500 transition-colors"
            title="Скрыть"
          >
            <X className="w-4 h-4" />
          </button>
          <button
            onClick={(e) => {
              e.stopPropagation()
              onLike?.(idea.id)
            }}
            className={`w-8 h-8 flex items-center justify-center rounded-full border transition-colors ${
              isLiked
                ? 'bg-red-500 border-red-500 text-white'
                : 'bg-background border-border text-text-tertiary hover:text-red-500 hover:border-red-500'
            }`}
            title={isLiked ? 'Убрать из избранного' : 'В избранное'}
          >
            <Heart className={`w-4 h-4 ${isLiked ? 'fill-current' : ''}`} />
          </button>
        </div>
      )}

      {/* Заголовок с эмодзи и рейтингом */}
      <div className="flex items-start justify-between gap-3 mb-3 pr-20">
        <div className="flex-1 min-w-0">
          <h3 className="text-base font-bold text-text-primary leading-tight mb-1">
            <span className="mr-1.5">{idea.emoji}</span>
            {idea.title}
          </h3>
          <div className="flex items-center gap-2 text-xs text-text-tertiary flex-wrap">
            <span>{idea.source}</span>
            <span>•</span>
            <span>{idea.timeAgo}</span>
            {idea.category && (
              <>
                <span>•</span>
                <span className="bg-background px-1.5 py-0.5 rounded text-text-secondary">
                  {categoryLabels[idea.category]}
                </span>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Score + Rating badge */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-baseline gap-2">
          <span className="text-3xl font-extrabold text-text-primary">
            {idea.score.toFixed(1)}
          </span>
          <span className="text-sm text-text-tertiary">из 10</span>
        </div>
        <div className={`${rating.bgColor} ${rating.textColor} px-2.5 py-1 rounded-full text-xs font-bold whitespace-nowrap flex items-center gap-1`}>
          <span>{rating.emoji}</span>
          <span>{rating.label}</span>
        </div>
      </div>

      {/* Метрики в виде сетки */}
      <div className="grid grid-cols-2 gap-2 mb-4">
        <div className="bg-background rounded-md p-2">
          <div className="flex items-center gap-1.5 text-text-secondary mb-1">
            <TrendingUp className="w-3.5 h-3.5" />
            <span className="text-xs">Рынок</span>
          </div>
          <div className="text-sm font-bold text-text-primary">
            {idea.metrics.marketSize}/10
          </div>
        </div>

        <div className="bg-background rounded-md p-2">
          <div className="flex items-center gap-1.5 text-text-secondary mb-1">
            <Users className="w-3.5 h-3.5" />
            <span className="text-xs">Спрос</span>
          </div>
          <div className="text-sm font-bold text-text-primary">
            {idea.metrics.demand}/10
          </div>
        </div>
      </div>

      {/* Финансы */}
      <div className="bg-background rounded-md p-2.5 mb-4">
        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center gap-1.5">
            <DollarSign className="w-3.5 h-3.5 text-accent-green" />
            <span className="text-text-secondary">Инвестиции:</span>
            <span className="font-bold text-text-primary">${(idea.financial.investment / 1000).toFixed(0)}K</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Clock className="w-3.5 h-3.5 text-accent-blue" />
            <span className="text-text-secondary">Окупаемость:</span>
            <span className="font-bold text-text-primary">{idea.financial.paybackMonths} мес</span>
          </div>
        </div>
      </div>

      {/* Кнопки действий */}
      <div className="flex gap-2">
        <button
          onClick={(e) => {
            e.stopPropagation()
            onChatClick?.()
          }}
          className="flex-1 bg-accent-purple hover:bg-accent-purple/90 text-white px-3 py-2 rounded-md text-sm font-medium flex items-center justify-center gap-1.5 transition-smooth"
        >
          <MessageCircle className="w-4 h-4" />
          <span className="hidden sm:inline">Спросить AI</span>
          <span className="sm:hidden">AI</span>
        </button>
        <button
          onClick={(e) => {
            e.stopPropagation()
            onDetailsClick?.()
          }}
          className="flex-1 bg-background hover:bg-border text-text-primary px-3 py-2 rounded-md text-sm font-medium border border-border flex items-center justify-center gap-1.5 transition-smooth"
        >
          <FileText className="w-4 h-4" />
          <span>Подробнее</span>
        </button>
      </div>
    </motion.div>
  )
}
