export default function TrendChart() {
  return (
    <div className="bg-surface border border-border rounded-xl p-4 sm:p-6 mb-4 sm:mb-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 sm:gap-4 mb-4 sm:mb-6">
        <h3 className="text-sm sm:text-lg font-bold text-text-primary">
          📈 Анализ трендов за последние 30 дней
        </h3>
        <div className="flex flex-wrap items-center gap-2 sm:gap-4 text-xs sm:text-sm">
          <div className="flex items-center gap-1 sm:gap-2">
            <span
              className="w-2 h-2 rounded-full"
              style={{ background: '#3B82F6' }}
            />
            <span className="text-text-secondary">Запросы</span>
          </div>
          <div className="flex items-center gap-1 sm:gap-2">
            <span
              className="w-2 h-2 rounded-full"
              style={{ background: '#10B981' }}
            />
            <span className="text-text-secondary">Соцсети</span>
          </div>
          <div className="flex items-center gap-1 sm:gap-2">
            <span
              className="w-2 h-2 rounded-full"
              style={{ background: '#F59E0B' }}
            />
            <span className="text-text-secondary">Инвестиции</span>
          </div>
        </div>
      </div>

      {/* SVG Chart */}
      <svg
        className="w-full h-20"
        viewBox="0 0 400 80"
        preserveAspectRatio="none"
      >
        {/* Grid lines */}
        <line
          x1="0"
          y1="20"
          x2="400"
          y2="20"
          stroke="var(--border)"
          strokeWidth="1"
        />
        <line
          x1="0"
          y1="40"
          x2="400"
          y2="40"
          stroke="var(--border)"
          strokeWidth="1"
        />
        <line
          x1="0"
          y1="60"
          x2="400"
          y2="60"
          stroke="var(--border)"
          strokeWidth="1"
        />

        {/* Search queries trend (blue) */}
        <path
          d="M0,70 L50,65 L100,58 L150,50 L200,42 L250,35 L300,28 L350,22 L400,18 L400,80 L0,80 Z"
          fill="#3B82F6"
          opacity="0.1"
        />
        <path
          d="M0,70 L50,65 L100,58 L150,50 L200,42 L250,35 L300,28 L350,22 L400,18"
          stroke="#3B82F6"
          strokeWidth="2"
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
        />

        {/* Social media mentions (green) */}
        <path
          d="M0,75 L50,72 L100,68 L150,62 L200,55 L250,48 L300,40 L350,32 L400,25 L400,80 L0,80 Z"
          fill="#10B981"
          opacity="0.1"
        />
        <path
          d="M0,75 L50,72 L100,68 L150,62 L200,55 L250,48 L300,40 L350,32 L400,25"
          stroke="#10B981"
          strokeWidth="2"
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
        />

        {/* Investments (orange) */}
        <path
          d="M0,78 L50,76 L100,74 L150,70 L200,65 L250,58 L300,50 L350,42 L400,35 L400,80 L0,80 Z"
          fill="#F59E0B"
          opacity="0.1"
        />
        <path
          d="M0,78 L50,76 L100,74 L150,70 L200,65 L250,58 L300,50 L350,42 L400,35"
          stroke="#F59E0B"
          strokeWidth="2"
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-2 sm:gap-6 mt-4 sm:mt-6">
        <div className="text-center">
          <div className="text-lg sm:text-2xl font-bold" style={{ color: '#3B82F6' }}>
            +127%
          </div>
          <div className="text-xs text-text-secondary mt-1">
            Рост запросов
          </div>
        </div>
        <div className="text-center">
          <div className="text-lg sm:text-2xl font-bold" style={{ color: '#10B981' }}>
            +94%
          </div>
          <div className="text-xs text-text-secondary mt-1">
            Рост упоминаний
          </div>
        </div>
        <div className="text-center">
          <div className="text-lg sm:text-2xl font-bold" style={{ color: '#F59E0B' }}>
            +156%
          </div>
          <div className="text-xs text-text-secondary mt-1">
            Рост инвестиций
          </div>
        </div>
      </div>
    </div>
  )
}
