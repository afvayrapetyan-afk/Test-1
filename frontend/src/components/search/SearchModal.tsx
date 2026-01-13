import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, TrendingUp, Clock, X } from 'lucide-react'
import { useSearch } from '../../contexts/SearchContext'
import { mockIdeas } from '../../data/mockData'
import { useNavigate } from 'react-router-dom'

export default function SearchModal() {
  const { isSearchOpen, searchQuery, setSearchQuery, closeSearch } = useSearch()
  const [selectedIndex, setSelectedIndex] = useState(0)
  const navigate = useNavigate()

  const filteredIdeas = mockIdeas.filter(
    (idea) =>
      idea.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      idea.source.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const recentSearches = [
    'AI продуктовость',
    'EdTech стартапы',
    'SaaS с высокой маржой',
  ]

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!isSearchOpen) return

      if (e.key === 'ArrowDown') {
        e.preventDefault()
        setSelectedIndex((prev) =>
          prev < filteredIdeas.length - 1 ? prev + 1 : 0
        )
      } else if (e.key === 'ArrowUp') {
        e.preventDefault()
        setSelectedIndex((prev) =>
          prev > 0 ? prev - 1 : filteredIdeas.length - 1
        )
      } else if (e.key === 'Enter') {
        e.preventDefault()
        if (filteredIdeas[selectedIndex]) {
          navigate(`/idea/${filteredIdeas[selectedIndex].id}`)
          closeSearch()
        }
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [isSearchOpen, selectedIndex, filteredIdeas, navigate, closeSearch])

  useEffect(() => {
    if (isSearchOpen) {
      setSearchQuery('')
      setSelectedIndex(0)
    }
  }, [isSearchOpen, setSearchQuery])

  return (
    <AnimatePresence>
      {isSearchOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={closeSearch}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-[100]"
          />

          {/* Search Modal */}
          <div className="fixed inset-0 z-[101] flex items-start justify-center pt-[15vh] px-4">
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ type: 'spring', damping: 25, stiffness: 300 }}
              onClick={(e) => e.stopPropagation()}
              className="w-full max-w-2xl bg-surface border border-border rounded-xl shadow-2xl overflow-hidden"
            >
              {/* Search Input */}
              <div className="p-4 border-b border-border flex items-center gap-3">
                <Search className="w-5 h-5 text-text-tertiary" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Поиск идей, трендов, проектов..."
                  className="flex-1 bg-transparent border-none outline-none text-base"
                  autoFocus
                />
                <kbd className="hidden sm:inline-block px-2 py-1 text-xs font-medium text-text-tertiary bg-background border border-border rounded">
                  ESC
                </kbd>
                <button
                  onClick={closeSearch}
                  className="sm:hidden w-8 h-8 rounded-md border border-border bg-surface flex items-center justify-center hover:bg-background transition-colors"
                  aria-label="Close search"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              {/* Results */}
              <div className="max-h-[500px] overflow-y-auto">
                {searchQuery === '' ? (
                  <div className="p-4">
                    <h3 className="text-sm font-semibold text-text-secondary mb-3 flex items-center gap-2">
                      <Clock className="w-4 h-4" />
                      Недавние запросы
                    </h3>
                    <div className="space-y-2">
                      {recentSearches.map((search, index) => (
                        <button
                          key={index}
                          onClick={() => setSearchQuery(search)}
                          className="w-full text-left px-3 py-2 rounded-lg hover:bg-background transition-colors text-sm"
                        >
                          {search}
                        </button>
                      ))}
                    </div>
                  </div>
                ) : filteredIdeas.length === 0 ? (
                  <div className="p-8 text-center text-text-secondary">
                    Идеи не найдены
                  </div>
                ) : (
                  <div className="p-2">
                    <h3 className="text-sm font-semibold text-text-secondary mb-2 px-2">
                      Найдено идей: {filteredIdeas.length}
                    </h3>
                    {filteredIdeas.map((idea, index) => (
                      <button
                        key={idea.id}
                        onClick={() => {
                          navigate(`/idea/${idea.id}`)
                          closeSearch()
                        }}
                        className={`w-full text-left px-3 py-3 rounded-lg transition-colors flex items-start gap-3 ${
                          index === selectedIndex
                            ? 'bg-accent-blue/10'
                            : 'hover:bg-background'
                        }`}
                      >
                        <span className="text-2xl">{idea.emoji}</span>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            <div className="text-sm font-semibold text-text-primary">
                              {idea.title}
                            </div>
                            {idea.isTrending && (
                              <div className="flex items-center gap-1 bg-gradient-to-r from-orange-400 to-red-500 text-white px-2 py-0.5 rounded-full text-[10px] font-bold">
                                <TrendingUp className="w-3 h-3" />
                                HOT
                              </div>
                            )}
                          </div>
                          <div className="text-xs text-text-secondary">
                            {idea.source} • Score: {idea.score}/10
                          </div>
                          <div className="flex gap-2 mt-1">
                            <span className="text-xs bg-accent-blue/10 text-accent-blue px-2 py-0.5 rounded">
                              ${idea.financial.investment / 1000}K инвестиции
                            </span>
                            <span className="text-xs bg-accent-green/10 text-accent-green px-2 py-0.5 rounded">
                              {idea.financial.margin}% маржа
                            </span>
                          </div>
                        </div>
                        <div className="text-2xl font-bold text-accent-blue">
                          {idea.score}
                        </div>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </motion.div>
          </div>
        </>
      )}
    </AnimatePresence>
  )
}
