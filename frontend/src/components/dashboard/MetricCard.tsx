import { ReactNode } from 'react'
import { TrendingUp, TrendingDown } from 'lucide-react'

interface MetricCardProps {
  label: string
  value: string | number
  change: string
  isPositive?: boolean
  icon: ReactNode
}

export default function MetricCard({
  label,
  value,
  change,
  isPositive = true,
  icon,
}: MetricCardProps) {
  return (
    <div className="bg-surface border border-border rounded-lg p-3 shadow-sm transition-smooth hover:-translate-y-1 hover:shadow-lg cursor-pointer">
      <div className="flex items-start justify-between mb-2">
        <div className="text-sm font-medium text-text-secondary">{label}</div>
        <div className="text-2xl">{icon}</div>
      </div>

      <div className="text-[32px] font-extrabold mb-1">{value}</div>

      <div
        className={`text-sm flex items-center gap-1 ${
          isPositive ? 'text-accent-green' : 'text-accent-red'
        }`}
      >
        {isPositive ? (
          <TrendingUp className="w-4 h-4" />
        ) : (
          <TrendingDown className="w-4 h-4" />
        )}
        <span>{change}</span>
      </div>
    </div>
  )
}
