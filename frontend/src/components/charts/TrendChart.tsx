export default function TrendChart() {
  return (
    <div className="bg-surface border border-border rounded-xl p-4 sm:p-6 mb-4 sm:mb-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 sm:gap-4 mb-4 sm:mb-6">
        <h3 className="text-sm sm:text-lg font-bold text-text-primary">
          📈 Статистика поиска AI-решений (Google Trends)
        </h3>
        <div className="flex flex-wrap items-center gap-2 sm:gap-4 text-xs sm:text-sm">
          <div className="flex items-center gap-1 sm:gap-2">
            <span
              className="w-2 h-2 rounded-full"
              style={{ background: '#3B82F6' }}
            />
            <span className="text-text-secondary">AI Agents</span>
          </div>
          <div className="flex items-center gap-1 sm:gap-2">
            <span
              className="w-2 h-2 rounded-full"
              style={{ background: '#10B981' }}
            />
            <span className="text-text-secondary">AI Automation</span>
          </div>
          <div className="flex items-center gap-1 sm:gap-2">
            <span
              className="w-2 h-2 rounded-full"
              style={{ background: '#F59E0B' }}
            />
            <span className="text-text-secondary">AI SaaS</span>
          </div>
        </div>
      </div>

      {/* SVG Chart - more realistic with fluctuations */}
      <svg
        className="w-full h-24"
        viewBox="0 0 400 90"
        preserveAspectRatio="none"
      >
        {/* Grid lines */}
        <line x1="0" y1="22" x2="400" y2="22" stroke="var(--border)" strokeWidth="1" strokeDasharray="4" />
        <line x1="0" y1="45" x2="400" y2="45" stroke="var(--border)" strokeWidth="1" strokeDasharray="4" />
        <line x1="0" y1="68" x2="400" y2="68" stroke="var(--border)" strokeWidth="1" strokeDasharray="4" />

        {/* AI Agents trend (blue) - fastest growth */}
        <path
          d="M0,72 L25,70 L50,68 L75,65 L100,62 L125,58 L150,52 L175,48 L200,42 L225,38 L250,32 L275,28 L300,22 L325,18 L350,15 L375,12 L400,10 L400,90 L0,90 Z"
          fill="#3B82F6"
          opacity="0.15"
        />
        <path
          d="M0,72 L25,70 L50,68 L75,65 L100,62 L125,58 L150,52 L175,48 L200,42 L225,38 L250,32 L275,28 L300,22 L325,18 L350,15 L375,12 L400,10"
          stroke="#3B82F6"
          strokeWidth="2.5"
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
        />

        {/* AI Automation trend (green) - steady growth with dips */}
        <path
          d="M0,75 L25,74 L50,72 L75,70 L100,68 L125,65 L150,60 L175,58 L200,52 L225,50 L250,45 L275,42 L300,38 L325,35 L350,30 L375,26 L400,22 L400,90 L0,90 Z"
          fill="#10B981"
          opacity="0.12"
        />
        <path
          d="M0,75 L25,74 L50,72 L75,70 L100,68 L125,65 L150,60 L175,58 L200,52 L225,50 L250,45 L275,42 L300,38 L325,35 L350,30 L375,26 L400,22"
          stroke="#10B981"
          strokeWidth="2"
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
        />

        {/* AI SaaS trend (orange) - moderate growth */}
        <path
          d="M0,78 L25,77 L50,76 L75,74 L100,72 L125,70 L150,67 L175,64 L200,60 L225,58 L250,54 L275,50 L300,46 L325,42 L350,38 L375,35 L400,32 L400,90 L0,90 Z"
          fill="#F59E0B"
          opacity="0.1"
        />
        <path
          d="M0,78 L25,77 L50,76 L75,74 L100,72 L125,70 L150,67 L175,64 L200,60 L225,58 L250,54 L275,50 L300,46 L325,42 L350,38 L375,35 L400,32"
          stroke="#F59E0B"
          strokeWidth="2"
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
        />

        {/* Data points for AI Agents */}
        <circle cx="100" cy="62" r="3" fill="#3B82F6" />
        <circle cx="200" cy="42" r="3" fill="#3B82F6" />
        <circle cx="300" cy="22" r="3" fill="#3B82F6" />
        <circle cx="400" cy="10" r="4" fill="#3B82F6" />
      </svg>

      {/* X-axis labels */}
      <div className="flex justify-between text-[10px] text-text-tertiary mt-1 px-1">
        <span>4 нед. назад</span>
        <span>3 нед.</span>
        <span>2 нед.</span>
        <span>1 нед.</span>
        <span>Сегодня</span>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-2 sm:gap-6 mt-4 sm:mt-6">
        <div className="text-center">
          <div className="text-lg sm:text-2xl font-bold" style={{ color: '#3B82F6' }}>
            +243%
          </div>
          <div className="text-xs text-text-secondary mt-1">
            AI Agents
          </div>
        </div>
        <div className="text-center">
          <div className="text-lg sm:text-2xl font-bold" style={{ color: '#10B981' }}>
            +178%
          </div>
          <div className="text-xs text-text-secondary mt-1">
            AI Automation
          </div>
        </div>
        <div className="text-center">
          <div className="text-lg sm:text-2xl font-bold" style={{ color: '#F59E0B' }}>
            +134%
          </div>
          <div className="text-xs text-text-secondary mt-1">
            AI SaaS
          </div>
        </div>
      </div>
    </div>
  )
}
