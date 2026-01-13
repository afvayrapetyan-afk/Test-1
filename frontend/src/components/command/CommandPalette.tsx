import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Moon,
  Sun,
  MessageCircle,
  FileText,
  RotateCcw,
  FileDown,
} from 'lucide-react'
import { useTheme } from '../../contexts/ThemeContext'
import { useChat } from '../../contexts/ChatContext'
import { useFilters } from '../../contexts/FilterContext'

interface Command {
  id: string
  icon: React.ReactNode
  label: string
  subtitle: string
  shortcut?: string
  action: () => void
}

interface CommandPaletteProps {
  isOpen: boolean
  onClose: () => void
}

export default function CommandPalette({
  isOpen,
  onClose,
}: CommandPaletteProps) {
  const { theme, toggleTheme } = useTheme()
  const { openChat } = useChat()
  const { resetFilters } = useFilters()
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedIndex, setSelectedIndex] = useState(0)

  const commands: Command[] = [
    {
      id: 'dark-mode',
      icon: theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />,
      label: 'Toggle Dark Mode',
      subtitle: 'Переключить темную тему',
      shortcut: '⌘ D',
      action: () => {
        toggleTheme()
        onClose()
      },
    },
    {
      id: 'ai-chat',
      icon: <MessageCircle className="w-5 h-5" />,
      label: 'Open AI Chat',
      subtitle: 'Открыть AI консультанта',
      shortcut: '⌘ /',
      action: () => {
        openChat()
        onClose()
      },
    },
    {
      id: 'idea-detail',
      icon: <FileText className="w-5 h-5" />,
      label: 'View Idea Details',
      subtitle: 'Открыть детальную страницу',
      shortcut: '',
      action: () => {
        window.location.href = '/idea/1'
      },
    },
    {
      id: 'reset-filters',
      icon: <RotateCcw className="w-5 h-5" />,
      label: 'Reset Filters',
      subtitle: 'Сбросить все фильтры',
      shortcut: '',
      action: () => {
        resetFilters()
        onClose()
        // Show success notification
        const notification = document.createElement('div')
        notification.className = 'fixed top-20 right-4 bg-accent-green text-white px-4 py-3 rounded-lg shadow-xl z-[200]'
        notification.textContent = '✓ Фильтры сброшены'
        document.body.appendChild(notification)
        setTimeout(() => {
          notification.style.opacity = '0'
          notification.style.transition = 'opacity 0.3s'
          setTimeout(() => notification.remove(), 300)
        }, 2000)
      },
    },
    {
      id: 'export-pdf',
      icon: <FileDown className="w-5 h-5" />,
      label: 'Export to PDF',
      subtitle: 'Экспортировать бизнес-план в PDF',
      shortcut: '',
      action: () => {
        alert('Export to PDF coming soon!')
        onClose()
      },
    },
  ]

  const filteredCommands = commands.filter(
    (cmd) =>
      cmd.label.toLowerCase().includes(searchQuery.toLowerCase()) ||
      cmd.subtitle.toLowerCase().includes(searchQuery.toLowerCase())
  )

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!isOpen) return

      if (e.key === 'ArrowDown') {
        e.preventDefault()
        setSelectedIndex((prev) =>
          prev < filteredCommands.length - 1 ? prev + 1 : 0
        )
      } else if (e.key === 'ArrowUp') {
        e.preventDefault()
        setSelectedIndex((prev) =>
          prev > 0 ? prev - 1 : filteredCommands.length - 1
        )
      } else if (e.key === 'Enter') {
        e.preventDefault()
        if (filteredCommands[selectedIndex]) {
          filteredCommands[selectedIndex].action()
        }
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [isOpen, selectedIndex, filteredCommands])

  useEffect(() => {
    if (isOpen) {
      setSearchQuery('')
      setSelectedIndex(0)
    }
  }, [isOpen])

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-[100]"
          />

          {/* Command Palette */}
          <div className="fixed inset-0 z-[101] flex items-start justify-center pt-[15vh] px-4">
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ type: 'spring', damping: 25, stiffness: 300 }}
              className="w-full max-w-2xl bg-surface border border-border rounded-xl shadow-2xl overflow-hidden"
            >
              {/* Search Input */}
              <div className="p-4 border-b border-border">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Введите команду или поиск..."
                  className="w-full px-4 py-3 bg-background border border-border rounded-lg text-base focus:outline-none focus:ring-2 focus:ring-accent-purple/50"
                  autoFocus
                />
              </div>

              {/* Commands List */}
              <div className="max-h-[400px] overflow-y-auto">
                {filteredCommands.length === 0 ? (
                  <div className="p-8 text-center text-text-secondary">
                    Команды не найдены
                  </div>
                ) : (
                  filteredCommands.map((cmd, index) => (
                    <div
                      key={cmd.id}
                      onClick={cmd.action}
                      className={`flex items-center gap-3 px-4 py-3 cursor-pointer transition-colors ${
                        index === selectedIndex
                          ? 'bg-accent-blue/10'
                          : 'hover:bg-background'
                      }`}
                    >
                      <div className="flex-shrink-0 text-text-secondary">
                        {cmd.icon}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="text-sm font-medium text-text-primary">
                          {cmd.label}
                        </div>
                        <div className="text-xs text-text-secondary truncate">
                          {cmd.subtitle}
                        </div>
                      </div>
                      {cmd.shortcut && (
                        <div className="flex-shrink-0 px-2 py-1 text-xs font-medium text-text-tertiary bg-background border border-border rounded">
                          {cmd.shortcut}
                        </div>
                      )}
                    </div>
                  ))
                )}
              </div>
            </motion.div>
          </div>
        </>
      )}
    </AnimatePresence>
  )
}
