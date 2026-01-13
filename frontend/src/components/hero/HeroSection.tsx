import { motion } from 'framer-motion'
import { TrendingUp, Lightbulb, BarChart3 } from 'lucide-react'

interface FeatureCardProps {
  emoji: string
  title: string
  description: string
  icon: React.ReactNode
}

function FeatureCard({ emoji, title, description, icon }: FeatureCardProps) {
  return (
    <div className="bg-background border border-border rounded-lg p-4 hover:shadow-md transition-smooth">
      <div className="flex items-center gap-2 mb-2">
        <span className="text-2xl">{emoji}</span>
        <div className="w-8 h-8 rounded-lg bg-accent-blue/10 flex items-center justify-center text-accent-blue">
          {icon}
        </div>
      </div>
      <h3 className="font-bold text-text-primary mb-1">{title}</h3>
      <p className="text-sm text-text-secondary">{description}</p>
    </div>
  )
}

export default function HeroSection() {
  const handleGetStarted = () => {
    // Scroll to ideas section
    const ideasSection = document.querySelector('[data-section="ideas"]')
    if (ideasSection) {
      ideasSection.scrollIntoView({ behavior: 'smooth' })
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="bg-surface border border-border rounded-xl p-6 sm:p-8 lg:p-12 shadow-sm"
    >
      {/* Icon/Logo */}
      <div className="flex justify-center mb-4 sm:mb-6">
        <div className="w-14 h-14 sm:w-16 sm:h-16 bg-gradient-to-br from-accent-blue to-accent-purple rounded-2xl flex items-center justify-center text-3xl sm:text-4xl">
          💼
        </div>
      </div>

      {/* Title */}
      <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-center mb-3 sm:mb-4 text-text-primary">
        AI Business Portfolio Manager
      </h1>

      {/* Subtitle */}
      <p className="text-sm sm:text-base lg:text-lg text-center text-text-secondary mb-6 sm:mb-8 max-w-3xl mx-auto px-4">
        Анализируйте тренды, генерируйте бизнес-идеи и управляйте портфелем проектов с помощью искусственного интеллекта
      </p>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6 mb-6 sm:mb-8">
        <FeatureCard
          emoji="🔍"
          title="AI Trend Scout"
          description="Автоматический поиск и анализ трендов из Reddit, Product Hunt, TechCrunch"
          icon={<TrendingUp className="w-4 h-4" />}
        />
        <FeatureCard
          emoji="💡"
          title="Idea Analyzer"
          description="Оценка идей по 6 метрикам: рынок, конкуренция, спрос, монетизация, реализуемость, время"
          icon={<Lightbulb className="w-4 h-4" />}
        />
        <FeatureCard
          emoji="📊"
          title="Portfolio Manager"
          description="Управление активными проектами с отслеживанием прогресса и метрик"
          icon={<BarChart3 className="w-4 h-4" />}
        />
      </div>

      {/* CTA Button */}
      <div className="flex justify-center">
        <button
          onClick={handleGetStarted}
          className="bg-accent-blue hover:bg-accent-purple text-white px-6 sm:px-8 py-2.5 sm:py-3 rounded-lg font-semibold transition-smooth hover:-translate-y-0.5 hover:shadow-lg text-sm sm:text-base"
        >
          Начать сейчас
        </button>
      </div>
    </motion.div>
  )
}
