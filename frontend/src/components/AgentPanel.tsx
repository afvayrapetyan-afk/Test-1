/**
 * Панель для работы с AI агентами
 */
import { useState, useEffect } from 'react'
import { useAgents } from '../hooks/useAgents'
import { Sparkles, Code, Shield, TestTube, Loader2, CheckCircle, XCircle } from 'lucide-react'

interface AgentPanelProps {
  activeTab?: 'analyst' | 'dev'
}

export function AgentPanel({ activeTab = 'analyst' }: AgentPanelProps) {
  const { analyzeFile, implementFeature, findBugs, checkSecurity, generateTests, loading, error } = useAgents()

  const [currentTab, setCurrentTab] = useState<'analyst' | 'dev'>(activeTab)
  const [selectedAction, setSelectedAction] = useState<string | null>(null)
  const [filePath, setFilePath] = useState('backend/main.py')
  const [featureDescription, setFeatureDescription] = useState('')
  const [result, setResult] = useState<any>(null)

  // Синхронизация с prop activeTab
  useEffect(() => {
    setCurrentTab(activeTab)
  }, [activeTab])

  const handleAnalyze = async () => {
    setSelectedAction('analyze')
    setResult(null)

    try {
      const analysis = await analyzeFile(filePath)
      setResult(analysis)
    } catch (err) {
      console.error(err)
    }
  }

  const handleFindBugs = async () => {
    setSelectedAction('bugs')
    setResult(null)

    try {
      const bugs = await findBugs(filePath)
      setResult(bugs)
    } catch (err) {
      console.error(err)
    }
  }

  const handleSecurity = async () => {
    setSelectedAction('security')
    setResult(null)

    try {
      const security = await checkSecurity(filePath)
      setResult(security)
    } catch (err) {
      console.error(err)
    }
  }

  const handleImplement = async () => {
    if (!featureDescription.trim()) {
      alert('Опишите фичу!')
      return
    }

    setSelectedAction('implement')
    setResult(null)

    try {
      const implementation = await implementFeature(featureDescription)
      setResult(implementation)
    } catch (err) {
      console.error(err)
    }
  }

  const handleGenerateTests = async () => {
    setSelectedAction('tests')
    setResult(null)

    try {
      const tests = await generateTests(filePath)
      setResult(tests)
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="bg-surface border border-border rounded-lg p-6 shadow-sm">
      <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
        <Sparkles className="w-6 h-6 text-purple-500" />
        AI Агенты
      </h2>

      {/* Tabs */}
      <div className="flex gap-2 mb-6 border-b border-border">
        <button
          onClick={() => setCurrentTab('analyst')}
          className={`px-4 py-2 font-medium text-sm transition-all ${
            currentTab === 'analyst'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-text-secondary hover:text-text-primary'
          }`}
        >
          <div className="flex items-center gap-2">
            <Code className="w-4 h-4" />
            CodeAnalyst
          </div>
        </button>
        <button
          onClick={() => setCurrentTab('dev')}
          className={`px-4 py-2 font-medium text-sm transition-all ${
            currentTab === 'dev'
              ? 'text-purple-600 border-b-2 border-purple-600'
              : 'text-text-secondary hover:text-text-primary'
          }`}
        >
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4" />
            DevAgent
          </div>
        </button>
      </div>

      {/* CodeAnalystAgent Tab */}
      {currentTab === 'analyst' && (
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-text-secondary mb-3">
            CodeAnalystAgent (Анализ кода)
          </h3>

        <div className="space-y-2 mb-3">
          <input
            type="text"
            value={filePath}
            onChange={(e) => setFilePath(e.target.value)}
            placeholder="backend/main.py"
            className="w-full px-3 py-2 bg-background border border-border rounded text-sm"
          />
        </div>

        <div className="grid grid-cols-3 gap-2">
          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="flex items-center justify-center gap-2 px-3 py-2 bg-blue-600 text-white rounded text-sm hover:bg-blue-700 disabled:opacity-50"
          >
            <Code className="w-4 h-4" />
            Анализ
          </button>

          <button
            onClick={handleFindBugs}
            disabled={loading}
            className="flex items-center justify-center gap-2 px-3 py-2 bg-orange-600 text-white rounded text-sm hover:bg-orange-700 disabled:opacity-50"
          >
            🐛 Баги
          </button>

          <button
            onClick={handleSecurity}
            disabled={loading}
            className="flex items-center justify-center gap-2 px-3 py-2 bg-red-600 text-white rounded text-sm hover:bg-red-700 disabled:opacity-50"
          >
            <Shield className="w-4 h-4" />
            Security
          </button>
        </div>
        </div>
      )}

      {/* DevAgent Tab */}
      {currentTab === 'dev' && (
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-text-secondary mb-3">
            DevAgent (Разработка)
          </h3>

        <div className="space-y-2">
          <textarea
            value={featureDescription}
            onChange={(e) => setFeatureDescription(e.target.value)}
            placeholder="Опишите фичу, например: Add rate limiting to API endpoints"
            className="w-full px-3 py-2 bg-background border border-border rounded text-sm h-20 resize-none"
          />

          <div className="grid grid-cols-2 gap-2">
            <button
              onClick={handleImplement}
              disabled={loading}
              className="flex items-center justify-center gap-2 px-3 py-2 bg-purple-600 text-white rounded text-sm hover:bg-purple-700 disabled:opacity-50"
            >
              <Sparkles className="w-4 h-4" />
              Создать фичу
            </button>

            <button
              onClick={handleGenerateTests}
              disabled={loading}
              className="flex items-center justify-center gap-2 px-3 py-2 bg-green-600 text-white rounded text-sm hover:bg-green-700 disabled:opacity-50"
            >
              <TestTube className="w-4 h-4" />
              Тесты
            </button>
          </div>
        </div>
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="flex items-center gap-2 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded">
          <Loader2 className="w-5 h-5 animate-spin text-blue-600" />
          <span className="text-sm text-blue-600 dark:text-blue-400">
            Агент работает...
          </span>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="flex items-center gap-2 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded">
          <XCircle className="w-5 h-5 text-red-600" />
          <span className="text-sm text-red-600 dark:text-red-400">{error}</span>
        </div>
      )}

      {/* Results */}
      {result && !loading && (
        <div className="mt-4 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded">
          <div className="flex items-center gap-2 mb-3">
            <CheckCircle className="w-5 h-5 text-green-600" />
            <span className="font-semibold text-green-600 dark:text-green-400">
              Готово!
            </span>
          </div>

          {/* Analysis Result */}
          {selectedAction === 'analyze' && result.analysis && (
            <div className="space-y-2 text-sm">
              <div className="grid grid-cols-2 gap-2">
                <div>Quality: <strong>{result.analysis.quality_score}/100</strong></div>
                <div>Readability: <strong>{result.analysis.readability_score}/100</strong></div>
              </div>
              <div>
                <strong>Issues:</strong> {result.analysis.issues?.length || 0}
              </div>
              {result.analysis.issues?.slice(0, 3).map((issue: any, i: number) => (
                <div key={i} className="text-xs text-text-secondary">
                  • [{issue.severity}] {issue.description}
                </div>
              ))}
            </div>
          )}

          {/* Bugs Result */}
          {selectedAction === 'bugs' && (
            <div className="space-y-2 text-sm">
              <div>Найдено багов: <strong>{result.bugs_found}</strong></div>
              {result.bugs?.slice(0, 3).map((bug: any, i: number) => (
                <div key={i} className="text-xs text-text-secondary">
                  • Line {bug.line}: {bug.description}
                </div>
              ))}
            </div>
          )}

          {/* Security Result */}
          {selectedAction === 'security' && (
            <div className="space-y-2 text-sm">
              <div>Security Score: <strong>{result.security_score}/100</strong></div>
              <div>Vulnerabilities: <strong>{result.vulnerabilities?.length || 0}</strong></div>
            </div>
          )}

          {/* Implementation Result */}
          {selectedAction === 'implement' && (
            <div className="space-y-2 text-sm">
              <div>Branch: <code className="text-xs bg-black/10 px-1 rounded">{result.branch}</code></div>
              <div>Files: <strong>{result.files_modified}</strong></div>
              {result.pr && (
                <div>
                  <a
                    href={result.pr.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline"
                  >
                    Pull Request #{result.pr.number}
                  </a>
                </div>
              )}
            </div>
          )}

          {/* Tests Result */}
          {selectedAction === 'tests' && (
            <div className="space-y-2 text-sm">
              <div>Test file: <code className="text-xs bg-black/10 px-1 rounded">{result.test_file}</code></div>
              <div>Framework: <strong>{result.framework}</strong></div>
              <div>Coverage: <strong>{result.estimated_coverage}</strong></div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
