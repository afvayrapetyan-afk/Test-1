export interface Idea {
  id: string
  title: string
  emoji: string
  source: string
  timeAgo: string
  score: number
  isTrending?: boolean
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
