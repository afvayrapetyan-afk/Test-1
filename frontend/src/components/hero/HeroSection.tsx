import { motion } from 'framer-motion'
import { TrendingUp, Lightbulb, BarChart3 } from 'lucide-react'

interface FeatureCardProps {
  emoji: string
  title: string
  description: string
  icon: React.ReactNode
  delay?: number
}

function FeatureCard({ emoji, title, description, icon, delay = 0 }: FeatureCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay, ease: [0.25, 0.1, 0.25, 1] }}
      whileHover={{ y: -4, transition: { duration: 0.2 } }}
      className="bg-background border border-border rounded-lg p-4 hover:shadow-md transition-smooth"
    >
      <div className="flex items-center gap-2 mb-2">
        <span className="text-2xl">{emoji}</span>
        <div className="w-8 h-8 rounded-lg bg-accent-blue/10 flex items-center justify-center text-accent-blue">
          {icon}
        </div>
      </div>
      <h3 className="font-bold text-text-primary mb-1">{title}</h3>
      <p className="text-sm text-text-secondary">{description}</p>
    </motion.div>
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
    <div className="bg-surface border border-border rounded-xl p-6 sm:p-8 lg:p-12 shadow-sm overflow-hidden">
      {/* Icon/Logo - Apple-style bounce entrance */}
      <motion.div
        initial={{ opacity: 0, scale: 0.5, y: -20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ duration: 0.7, type: "spring", bounce: 0.4 }}
        className="flex justify-center mb-4 sm:mb-6"
      >
        <div className="w-14 h-14 sm:w-16 sm:h-16 bg-gradient-to-br from-accent-blue to-accent-purple rounded-2xl flex items-center justify-center text-3xl sm:text-4xl">
          💼
        </div>
      </motion.div>

      {/* Title - Fade up */}
      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.15, ease: [0.25, 0.1, 0.25, 1] }}
        className="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-center mb-3 sm:mb-4 text-text-primary"
      >
        AI Портфолио Менеджер
      </motion.h1>

      {/* Subtitle - Fade up with delay */}
      <motion.p
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.25, ease: [0.25, 0.1, 0.25, 1] }}
        className="text-sm sm:text-base lg:text-lg text-center text-text-secondary mb-6 sm:mb-8 max-w-3xl mx-auto px-4"
      >
        Анализируйте тренды, генерируйте бизнес-идеи и управляйте портфелем проектов с помощью искусственного интеллекта
      </motion.p>

      {/* Features Grid - Staggered entrance */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6 mb-6 sm:mb-8">
        <FeatureCard
          emoji="🔍"
          title="Поиск трендов"
          description="Комплексный и онлайн анализ потребностей пользователей в ИИ через динамический поиск и многофакторный анализ соц сетей, новостных лент, инвест порталов и др"
          icon={<TrendingUp className="w-4 h-4" />}
          delay={0.35}
        />
        <FeatureCard
          emoji="💡"
          title="Анализ идей"
          description="Оценка идей по 6 метрикам: рынок, конкуренция, спрос, монетизация, реализуемость, время"
          icon={<Lightbulb className="w-4 h-4" />}
          delay={0.45}
        />
        <FeatureCard
          emoji="📊"
          title="Управление портфелем"
          description="Управление активными проектами с отслеживанием прогресса и метрик"
          icon={<BarChart3 className="w-4 h-4" />}
          delay={0.55}
        />
      </div>

      {/* CTA Button - Entrance with hover effects */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.65, ease: [0.25, 0.1, 0.25, 1] }}
        className="flex justify-center"
      >
        <motion.button
          onClick={handleGetStarted}
          whileHover={{ scale: 1.05, y: -2 }}
          whileTap={{ scale: 0.98 }}
          className="bg-accent-blue hover:bg-accent-purple text-white px-6 sm:px-8 py-2.5 sm:py-3 rounded-lg font-semibold transition-colors hover:shadow-lg text-sm sm:text-base"
        >
          Начать сейчас
        </motion.button>
      </motion.div>
    </div>
  )
}
