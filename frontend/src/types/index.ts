export type IdeaCategory =
  | 'ai'
  | 'saas'
  | 'ecommerce'
  | 'fintech'
  | 'health'
  | 'education'
  | 'entertainment'

export interface Idea {
  id: string
  title: string
  emoji: string
  source: string
  timeAgo: string
  score: number
  isTrending?: boolean
  isRussiaRelevant?: boolean
  category: IdeaCategory
  createdAt: string // ISO date string
  metrics: {
    marketSize: number
    competition: number
    demand: number
    monetization: number
  }
  financial: {
    investment: number // в долларах
    paybackMonths: number // месяцев
    margin: number // процент 0-100
    arr: number // годовой доход в долларах
  }
}

// Названия категорий на русском
export const categoryLabels: Record<IdeaCategory, string> = {
  ai: 'Искусственный интеллект',
  saas: 'SaaS',
  ecommerce: 'E-commerce',
  fintech: 'Финтех',
  health: 'Здоровье',
  education: 'Образование',
  entertainment: 'Развлечения',
}

export interface Project {
  id: string
  title: string
  emoji: string
  status: 'development' | 'launched'
  statusText: string
  progress?: {
    backend: number
    frontend: number
  }
  metrics?: {
    mrr: number
    users: number
    growth: number
  }
}
