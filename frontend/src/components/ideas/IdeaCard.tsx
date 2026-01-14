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
      whileHover={{ y: -2 }}
      className={`relative bg-surface border border-border ${rating.borderColor} border-l-4 rounded-lg p-3 sm:p-4 transition-smooth hover:shadow-lg cursor-pointer`}
      onClick={onDetailsClick}
    >
      {/* Action buttons */}
      {showActions && (
        <>
          {/* Close button - top left, small red */}
          <button
            onClick={(e) => {
              e.stopPropagation()
              onDislike?.(idea.id)
            }}
            className="absolute top-1 left-1 w-5 h-5 flex items-center justify-center rounded-full bg-red-500/10 text-red-500 hover:bg-red-500 hover:text-white transition-colors z-10"
            title="Скрыть"
          >
            <X className="w-3 h-3" />
          </button>

          {/* Like button - top right */}
          <button
            onClick={(e) => {
              e.stopPropagation()
              onLike?.(idea.id)
            }}
            className={`absolute top-1 right-1 w-6 h-6 flex items-center justify-center rounded-full border transition-colors z-10 ${
              isLiked
                ? 'bg-red-500 border-red-500 text-white'
                : 'bg-background border-border text-text-tertiary hover:text-red-500 hover:border-red-500'
            }`}
            title={isLiked ? 'Убрать из избранного' : 'В избранное'}
          >
            <Heart className={`w-3 h-3 ${isLiked ? 'fill-current' : ''}`} />
          </button>
        </>
      )}

      {/* Header: Title + Region Flags */}
      <div className="mt-5 mb-2">
        <div className="flex items-start gap-1 mb-1">
          <span>{idea.emoji}</span>
          {/* Region flags */}
          {idea.regions?.russia && <span title="Актуально для России">🇷🇺</span>}
          {idea.regions?.armenia && <span title="Актуально для Армении">🇦🇲</span>}
          {idea.regions?.global && <span title="Глобально">🌍</span>}
        </div>
        <h3 className="text-sm sm:text-base font-bold text-text-primary leading-snug line-clamp-2">
          {idea.title}
        </h3>
      </div>

      {/* Meta info */}
      <div className="flex items-center gap-1 text-xs text-text-tertiary mb-3 flex-wrap">
        <span className="truncate max-w-[100px]">{idea.source}</span>
        <span>•</span>
        <span className="whitespace-nowrap">{idea.timeAgo}</span>
        {idea.category && (
          <>
            <span>•</span>
            <span className="bg-background px-1.5 py-0.5 rounded text-text-secondary truncate max-w-[80px] sm:max-w-none">
              {categoryLabels[idea.category]}
            </span>
          </>
        )}
      </div>

      {/* Score + Rating */}
      <div className="flex items-center justify-between mb-3 gap-2">
        <div className="flex items-baseline gap-1">
          <span className="text-2xl sm:text-3xl font-extrabold text-text-primary">
            {idea.score.toFixed(1)}
          </span>
          <span className="text-xs text-text-tertiary">/10</span>
        </div>
        <div className={`${rating.bgColor} ${rating.textColor} px-2 py-0.5 rounded-full text-xs font-bold whitespace-nowrap flex items-center gap-1`}>
          <span>{rating.emoji}</span>
          <span className="hidden xs:inline">{rating.label}</span>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 gap-1.5 sm:gap-2 mb-3">
        <div className="bg-background rounded p-1.5 sm:p-2">
          <div className="flex items-center gap-1 text-text-secondary mb-0.5">
            <TrendingUp className="w-3 h-3" />
            <span className="text-xs">Рынок</span>
          </div>
          <div className="text-xs sm:text-sm font-bold text-text-primary">
            {idea.metrics.marketSize}/10
          </div>
        </div>

        <div className="bg-background rounded p-1.5 sm:p-2">
          <div className="flex items-center gap-1 text-text-secondary mb-0.5">
            <Users className="w-3 h-3" />
            <span className="text-xs">Спрос</span>
          </div>
          <div className="text-xs sm:text-sm font-bold text-text-primary">
            {idea.metrics.demand}/10
          </div>
        </div>
      </div>

      {/* Financial info - compact */}
      <div className="bg-background rounded p-1.5 sm:p-2 mb-3">
        <div className="flex items-center justify-between text-xs gap-2">
          <div className="flex items-center gap-1 min-w-0">
            <DollarSign className="w-3 h-3 text-accent-green flex-shrink-0" />
            <span className="text-text-secondary hidden sm:inline">Старт:</span>
            <span className="font-bold text-text-primary">${(idea.financial.investment / 1000).toFixed(0)}K</span>
          </div>
          <div className="flex items-center gap-1 min-w-0">
            <Clock className="w-3 h-3 text-accent-blue flex-shrink-0" />
            <span className="text-text-secondary hidden sm:inline">Окуп.:</span>
            <span className="font-bold text-text-primary">{idea.financial.paybackMonths}м</span>
          </div>
        </div>
      </div>

      {/* Action buttons */}
      <div className="flex gap-1.5 sm:gap-2">
        <button
          onClick={(e) => {
            e.stopPropagation()
            onChatClick?.()
          }}
          className="flex-1 bg-accent-purple hover:bg-accent-purple/90 text-white px-2 py-1.5 sm:py-2 rounded text-xs sm:text-sm font-medium flex items-center justify-center gap-1 transition-smooth"
        >
          <MessageCircle className="w-3.5 h-3.5" />
          <span>AI</span>
        </button>
        <button
          onClick={(e) => {
            e.stopPropagation()
            onDetailsClick?.()
          }}
          className="flex-1 bg-background hover:bg-border text-text-primary px-2 py-1.5 sm:py-2 rounded text-xs sm:text-sm font-medium border border-border flex items-center justify-center gap-1 transition-smooth"
        >
          <FileText className="w-3.5 h-3.5" />
          <span>Детали</span>
        </button>
      </div>
    </motion.div>
  )
}
