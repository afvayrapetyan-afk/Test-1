/**
 * Hook для работы с AI агентами
 */
import { useState } from 'react'

const API_URL = 'http://localhost:8000'

interface AnalysisResult {
  status: string
  data: {
    file: string
    analysis: {
      quality_score: number
      readability_score: number
      maintainability_score: number
      issues: Array<{
        type: string
        severity: string
        description: string
        line?: number
      }>
      strengths: string[]
    }
  }
}

interface ImplementResult {
  status: string
  data: {
    description: string
    branch: string
    files_modified: number
    pr?: {
      number: number
      url: string
    }
  }
}

export function useAgents() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // CodeAnalystAgent - Анализ файла
  const analyzeFile = async (filePath: string) => {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_URL}/api/agents/code-analyst/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_path: filePath })
      })

      if (!response.ok) throw new Error('Analysis failed')

      const result: AnalysisResult = await response.json()
      return result.data
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // CodeAnalystAgent - Поиск багов
  const findBugs = async (filePath: string) => {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_URL}/api/agents/code-analyst/find-bugs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_path: filePath })
      })

      if (!response.ok) throw new Error('Bug search failed')

      const result = await response.json()
      return result
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // CodeAnalystAgent - Security проверка
  const checkSecurity = async (filePath: string) => {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_URL}/api/agents/code-analyst/security`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_path: filePath })
      })

      if (!response.ok) throw new Error('Security check failed')

      const result = await response.json()
      return result.security_report
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // DevAgent - Реализовать фичу
  const implementFeature = async (description: string, createPR: boolean = true) => {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_URL}/api/agents/dev-agent/implement`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          description,
          create_pr: createPR
        })
      })

      if (!response.ok) throw new Error('Implementation failed')

      const result: ImplementResult = await response.json()
      return result.data
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // DevAgent - Генерация тестов
  const generateTests = async (filePath: string) => {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_URL}/api/agents/dev-agent/generate-tests`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_path: filePath })
      })

      if (!response.ok) throw new Error('Test generation failed')

      const result = await response.json()
      return result.data
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // Проверить статус агентов
  const checkStatus = async () => {
    try {
      const response = await fetch(`${API_URL}/api/agents/status`)
      const result = await response.json()
      return result
    } catch (err) {
      console.error('Failed to check agent status:', err)
      return null
    }
  }

  return {
    analyzeFile,
    findBugs,
    checkSecurity,
    implementFeature,
    generateTests,
    checkStatus,
    loading,
    error
  }
}
