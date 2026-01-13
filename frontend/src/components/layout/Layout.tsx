import { ReactNode, useState, useEffect } from 'react'
import TopBar from './TopBar'
import AIChatFAB from '../ai/AIChatFAB'
import CommandPalette from '../command/CommandPalette'
import SearchModal from '../search/SearchModal'
import NotificationsPanel from '../notifications/NotificationsPanel'
import ProfileDropdown from '../profile/ProfileDropdown'
import { useTheme } from '../../contexts/ThemeContext'
import { useChat } from '../../contexts/ChatContext'
import { useSearch } from '../../contexts/SearchContext'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false)
  const [isNotificationsOpen, setIsNotificationsOpen] = useState(false)
  const [isProfileOpen, setIsProfileOpen] = useState(false)
  const { toggleTheme } = useTheme()
  const { closeChat } = useChat()
  const { openSearch, closeSearch } = useSearch()

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // ⌘+K or Ctrl+K - Open command palette
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        setIsCommandPaletteOpen(true)
      }

      // ⌘+F or Ctrl+F - Open search
      if ((e.metaKey || e.ctrlKey) && e.key === 'f') {
        e.preventDefault()
        openSearch()
      }

      // ⌘+D or Ctrl+D - Toggle dark mode
      if ((e.metaKey || e.ctrlKey) && e.key === 'd') {
        e.preventDefault()
        toggleTheme()
      }

      // ESC - Close modals
      if (e.key === 'Escape') {
        setIsCommandPaletteOpen(false)
        setIsNotificationsOpen(false)
        setIsProfileOpen(false)
        closeChat()
        closeSearch()
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [toggleTheme, closeChat, openSearch, closeSearch])

  return (
    <div className="min-h-screen bg-background">
      <TopBar
        onCommandClick={() => setIsCommandPaletteOpen(true)}
        onNotificationsClick={() => setIsNotificationsOpen(true)}
        onProfileClick={() => setIsProfileOpen(true)}
      />
      <main className="container mx-auto px-3 py-6 max-w-[1536px]">
        {children}
      </main>
      <AIChatFAB />
      <CommandPalette
        isOpen={isCommandPaletteOpen}
        onClose={() => setIsCommandPaletteOpen(false)}
      />
      <SearchModal />
      <NotificationsPanel
        isOpen={isNotificationsOpen}
        onClose={() => setIsNotificationsOpen(false)}
      />
      <ProfileDropdown
        isOpen={isProfileOpen}
        onClose={() => setIsProfileOpen(false)}
      />
    </div>
  )
}
