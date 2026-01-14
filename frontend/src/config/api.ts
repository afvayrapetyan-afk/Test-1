/**
 * API Configuration
 * Автоматически определяет правильный API URL для разных окружений
 */

// Получаем API URL из переменных окружения или используем дефолтное значение
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Базовые endpoint'ы
export const API_ENDPOINTS = {
  // Trends
  trends: {
    list: `${API_URL}/api/v1/trends/`,
    create: `${API_URL}/api/v1/trends/`,
    get: (id: number) => `${API_URL}/api/v1/trends/${id}`,
    search: `${API_URL}/api/v1/trends/search`,
    stats: `${API_URL}/api/v1/trends/stats`,
  },

  // Ideas
  ideas: {
    list: `${API_URL}/api/v1/ideas/`,
    create: `${API_URL}/api/v1/ideas/`,
    get: (id: number) => `${API_URL}/api/v1/ideas/${id}`,
    detailed: (id: number) => `${API_URL}/api/v1/ideas/${id}/detailed`,
    stats: `${API_URL}/api/v1/ideas/stats`,
    favorite: (id: string) => `${API_URL}/api/v1/ideas/${id}/favorite`,
    dislike: (id: string) => `${API_URL}/api/v1/ideas/${id}/dislike`,
  },

  // Agents
  agents: {
    run: `${API_URL}/api/v1/agents/run`,
    executions: `${API_URL}/api/v1/agents/executions`,
    execution: (id: number) => `${API_URL}/api/v1/agents/executions/${id}`,
    status: `${API_URL}/api/v1/agents/status`,
  },

  // Health
  health: `${API_URL}/health`,
}

// Helper функция для fetch с обработкой ошибок
export async function apiRequest<T>(
  url: string,
  options?: RequestInit
): Promise<T> {
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error?.message || 'API request failed')
    }

    return response.json()
  } catch (error) {
    console.error('API Request Error:', error)
    throw error
  }
}
