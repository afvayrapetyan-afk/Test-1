import { Search, Bell, User, Moon, Sun, Command } from 'lucide-react'
import { useTheme } from '../../contexts/ThemeContext'
import { useSearch } from '../../contexts/SearchContext'

interface TopBarProps {
  onCommandClick?: () => void
  onNotificationsClick?: () => void
  onProfileClick?: () => void
}

export default function TopBar({ onCommandClick, onNotificationsClick, onProfileClick }: TopBarProps) {
  const { theme, toggleTheme } = useTheme()
  const { openSearch } = useSearch()

  return (
    <div className="sticky top-0 z-50 bg-surface/90 backdrop-blur-md border-b border-border">
      <div className="container mx-auto px-3 max-w-[1536px]">
        <div className="flex items-center justify-between py-2">
          {/* Logo */}
          <div className="flex items-center gap-1">
            <span className="text-2xl">🚀</span>
            <span className="text-lg font-bold text-text-primary">
              AI Portfolio Manager
            </span>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-2">
            {/* Search Box */}
            <button
              onClick={openSearch}
              className="flex items-center gap-2 bg-background border border-border rounded-md px-2 py-1 min-w-[300px] transition-smooth hover:border-accent-blue focus-within:border-accent-blue focus-within:shadow-[0_0_0_3px_rgba(59,130,246,0.1)]"
            >
              <Search className="w-4 h-4 text-text-tertiary" />
              <span className="flex-1 text-left text-sm text-text-tertiary">
                Поиск идей, трендов...
              </span>
              <kbd className="px-1.5 py-0.5 text-xs font-medium text-text-tertiary bg-surface border border-border rounded">
                ⌘ F
              </kbd>
            </button>

            {/* Icon Buttons */}
            <button
              onClick={toggleTheme}
              className="w-9 h-9 rounded-md border border-border bg-surface flex items-center justify-center transition-smooth hover:-translate-y-0.5 hover:shadow-md"
              title="Toggle Dark Mode (⌘+D)"
            >
              {theme === 'dark' ? (
                <Sun className="w-4 h-4" />
              ) : (
                <Moon className="w-4 h-4" />
              )}
            </button>

            <button
              onClick={onCommandClick}
              className="w-9 h-9 rounded-md border border-border bg-surface flex items-center justify-center transition-smooth hover:-translate-y-0.5 hover:shadow-md"
              title="Command Palette (⌘+K)"
            >
              <Command className="w-4 h-4" />
            </button>

            <button
              onClick={onNotificationsClick}
              className="w-9 h-9 rounded-md border border-border bg-surface flex items-center justify-center transition-smooth hover:-translate-y-0.5 hover:shadow-md relative"
              title="Уведомления"
            >
              <Bell className="w-4 h-4" />
              <span className="absolute -top-1 -right-1 w-4 h-4 bg-accent-red text-white text-[10px] font-bold rounded-full flex items-center justify-center">
                3
              </span>
            </button>

            <button
              onClick={onProfileClick}
              className="w-9 h-9 rounded-md border border-border bg-surface flex items-center justify-center transition-smooth hover:-translate-y-0.5 hover:shadow-md"
              title="Профиль"
            >
              <User className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
