import { Idea, Project } from '../types'

export const mockIdeas: Idea[] = [
  {
    id: '1',
    title: 'AI Personal Chef App',
    emoji: '🍽️',
    source: 'Reddit r/FoodTech',
    timeAgo: '2 часа назад',
    score: 8.4,
    isTrending: true,
    metrics: {
      marketSize: 8,
      competition: 6,
      demand: 9,
      monetization: 8,
    },
    financial: {
      investment: 45000,
      paybackMonths: 8,
      margin: 65,
      arr: 180000,
    },
  },
  {
    id: '2',
    title: 'No-Code Automation Platform',
    emoji: '⚡',
    source: 'Product Hunt',
    timeAgo: '5 часов назад',
    score: 9.1,
    isTrending: false,
    metrics: {
      marketSize: 9.5,
      competition: 7,
      demand: 9.5,
      monetization: 8.5,
    },
    financial: {
      investment: 120000,
      paybackMonths: 14,
      margin: 78,
      arr: 540000,
    },
  },
  {
    id: '3',
    title: 'Telemedicine for Pets',
    emoji: '🏥',
    source: 'TechCrunch',
    timeAgo: '1 день назад',
    score: 7.8,
    isTrending: true,
    metrics: {
      marketSize: 7.5,
      competition: 5.5,
      demand: 8.5,
      monetization: 8,
    },
    financial: {
      investment: 28000,
      paybackMonths: 6,
      margin: 52,
      arr: 95000,
    },
  },
]

export const mockProjects: Project[] = [
  {
    id: '1',
    title: 'SaaS Analytics Dashboard',
    emoji: '💼',
    status: 'development',
    statusText: 'В разработке • Запуск через 2 недели',
    progress: {
      backend: 75,
      frontend: 60,
    },
  },
  {
    id: '2',
    title: 'E-commerce Optimizer',
    emoji: '🛒',
    status: 'launched',
    statusText: 'Запущен • $12K MRR',
    metrics: {
      mrr: 12450,
      users: 1247,
      growth: 23,
    },
  },
]
