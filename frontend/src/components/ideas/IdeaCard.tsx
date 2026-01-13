import { MessageCircle, FileText } from 'lucide-react'
import { motion } from 'framer-motion'
import { Idea } from '../../types'

interface IdeaCardProps {
  idea: Idea
  onChatClick?: () => void
  onDetailsClick?: () => void
}

export default function IdeaCard({
  idea,
  onChatClick,
  onDetailsClick,
}: IdeaCardProps) {
  const getScoreColor = (score: number) => {
    if (score >= 8.5)
      return 'bg-gradient-to-r from-orange-400 to-red-500'
    if (score >= 7.5)
      return 'bg-gradient-to-r from-green-400 to-emerald-500'
    return 'bg-gradient-to-r from-blue-400 to-purple-500'
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -4 }}
      className="relative bg-surface border border-border rounded-md p-3 transition-smooth hover:shadow-lg cursor-pointer overflow-hidden group"
    >
      {/* Trending Badge */}
      {idea.isTrending && (
        <div className="absolute top-2 right-2 bg-gradient-to-r from-orange-400 to-red-500 text-white px-2 sm:px-2.5 py-0.5 sm:py-1 rounded-full text-[10px] sm:text-[11px] font-bold flex items-center gap-0.5 sm:gap-1 animate-pulse-subtle z-10">
          <span className="hidden xs:inline">🔥</span>
          <span className="whitespace-nowrap">TRENDING</span>
        </div>
      )}

      {/* Left Border on Hover */}
      <div className="absolute left-0 top-0 h-full w-1 bg-accent-blue scale-y-0 group-hover:scale-y-100 transition-transform origin-top" />

      {/* Header */}
      <div className={`mb-2 ${idea.isTrending ? 'pr-20 sm:pr-24' : ''}`}>
        <h3 className="text-sm sm:text-base font-semibold mb-1 flex items-center gap-1">
          <span>{idea.emoji}</span>
          <span className="break-words">{idea.title}</span>
        </h3>
        <div className="text-xs text-text-tertiary">
          {idea.source} • {idea.timeAgo}
        </div>
      </div>

      {/* Score Badge */}
      <div
        className={`inline-flex items-center gap-1 ${getScoreColor(
          idea.score
        )} text-white px-3 py-1 rounded-full text-sm font-bold mb-2`}
      >
        ⭐ {idea.score.toFixed(1)}/10
      </div>

      {/* Metrics */}
      <div className="space-y-1 mb-2">
        <MetricBar
          label="💡 Размер рынка"
          value={idea.metrics.marketSize}
        />
        <MetricBar
          label="🎯 Конкуренция"
          value={idea.metrics.competition}
        />
        <MetricBar label="🔥 Спрос" value={idea.metrics.demand} />
        <MetricBar
          label="💰 Монетизация"
          value={idea.metrics.monetization}
        />
      </div>

      {/* Financial Metrics */}
      <div className="bg-gradient-to-br from-blue-50/50 to-purple-50/50 dark:from-blue-950/20 dark:to-purple-950/20 border border-border rounded-md p-2 my-2">
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
          <FinancialMetric
            label="💵 Инвестиции"
            value={`$${idea.financial.investment / 1000}K`}
            subtitle="стартовый капитал"
            valueClass="text-accent-blue"
          />
          <FinancialMetric
            label="⏱️ Окупаемость"
            value={`${idea.financial.paybackMonths} мес`}
            subtitle={
              idea.financial.paybackMonths < 8 ? 'быстрый ROI' : 'средний ROI'
            }
            valueClass="text-accent-green"
          />
          <FinancialMetric
            label="📊 Маржа"
            value={`${idea.financial.margin}%`}
            subtitle={idea.financial.margin > 60 ? 'высокая' : 'хорошая'}
            valueClass="text-accent-green"
          />
          <FinancialMetric
            label="💰 Годовой доход"
            value={`$${idea.financial.arr / 1000}K`}
            subtitle="ARR через 1 год"
            valueClass="text-accent-green"
          />
        </div>
      </div>

      {/* Actions */}
      <div className="flex gap-1 pt-2 border-t border-border">
        <button
          onClick={onChatClick}
          className="flex-1 bg-gradient-to-r from-accent-purple to-accent-pink text-white px-2 py-1 rounded-sm text-sm font-medium flex items-center justify-center gap-1.5 transition-smooth hover:-translate-y-0.5 hover:shadow-md"
        >
          <MessageCircle className="w-3.5 h-3.5" />
          Спросить AI
        </button>
        <button
          onClick={onDetailsClick}
          className="flex-1 bg-background text-text-primary px-2 py-1 rounded-sm text-sm font-medium border border-border flex items-center justify-center gap-1.5 transition-smooth hover:-translate-y-0.5"
        >
          <FileText className="w-3.5 h-3.5" />
          Детали
        </button>
      </div>
    </motion.div>
  )
}

interface MetricBarProps {
  label: string
  value: number
}

function MetricBar({ label, value }: MetricBarProps) {
  return (
    <div className="flex items-center justify-between gap-2 text-xs sm:text-[13px]">
      <span className="text-text-secondary whitespace-nowrap flex-shrink-0">{label}</span>
      <div className="flex items-center gap-1 flex-1 min-w-0">
        <div className="flex-1 h-1.5 bg-border rounded-full overflow-hidden min-w-[60px]">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${value * 10}%` }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="h-full bg-gradient-to-r from-accent-blue to-accent-purple rounded-full"
          />
        </div>
        <span className="font-semibold text-text-primary w-7 sm:w-8 text-right whitespace-nowrap text-[11px] sm:text-xs">
          {value}/10
        </span>
      </div>
    </div>
  )
}

interface FinancialMetricProps {
  label: string
  value: string
  subtitle: string
  valueClass?: string
}

function FinancialMetric({
  label,
  value,
  subtitle,
  valueClass = '',
}: FinancialMetricProps) {
  return (
    <div className="text-center px-1">
      <div className="text-[10px] sm:text-[11px] text-text-secondary uppercase tracking-wide font-semibold mb-1 break-words">
        {label}
      </div>
      <div className={`text-sm sm:text-base font-bold ${valueClass} break-words`}>{value}</div>
      <div className="text-[9px] sm:text-[10px] text-text-tertiary mt-0.5 break-words">{subtitle}</div>
    </div>
  )
}
