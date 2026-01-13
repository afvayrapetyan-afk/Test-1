import { motion, AnimatePresence } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import {
  User,
  Settings,
  CreditCard,
  BarChart3,
  LogOut,
  Moon,
  Sun,
} from 'lucide-react'
import { useTheme } from '../../contexts/ThemeContext'
import { useAuth } from '../../contexts/AuthContext'

interface ProfileDropdownProps {
  isOpen: boolean
  onClose: () => void
}

export default function ProfileDropdown({
  isOpen,
  onClose,
}: ProfileDropdownProps) {
  const { theme, toggleTheme } = useTheme()
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const menuItems = [
    {
      icon: <User className="w-4 h-4" />,
      label: 'Мой профиль',
      action: () => {
        navigate('/settings')
        onClose()
      },
    },
    {
      icon: <BarChart3 className="w-4 h-4" />,
      label: 'Статистика',
      action: () => {
        // TODO: Создать страницу статистики
        console.log('Stats - coming soon')
        onClose()
      },
    },
    {
      icon: <CreditCard className="w-4 h-4" />,
      label: 'Подписка',
      badge: user?.plan === 'pro' ? 'PRO' : user?.plan === 'enterprise' ? 'ENT' : undefined,
      action: () => {
        navigate('/subscription')
        onClose()
      },
    },
    {
      icon: <Settings className="w-4 h-4" />,
      label: 'Настройки',
      action: () => {
        navigate('/settings')
        onClose()
      },
    },
  ]

  const getUserInitials = () => {
    if (!user?.name) return '?'
    return user.name
      .split(' ')
      .map((n) => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2)
  }

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
            className="fixed inset-0 z-40"
          />

          {/* Dropdown */}
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.15 }}
            className="fixed top-14 right-4 w-64 bg-surface border border-border rounded-xl shadow-2xl z-50 overflow-hidden"
          >
            {/* User Info */}
            <div className="p-4 border-b border-border bg-gradient-to-br from-blue-50/50 to-purple-50/50 dark:from-blue-950/20 dark:to-purple-950/20">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-accent-purple to-accent-pink flex items-center justify-center text-white font-bold text-lg">
                  {getUserInitials()}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="font-semibold text-sm truncate">
                    {user?.name || 'User'}
                  </div>
                  <div className="text-xs text-text-secondary truncate">
                    {user?.email || 'user@example.com'}
                  </div>
                </div>
              </div>
            </div>

            {/* Menu Items */}
            <div className="py-2">
              {menuItems.map((item, index) => (
                <button
                  key={index}
                  onClick={item.action}
                  className="w-full flex items-center gap-3 px-4 py-2.5 hover:bg-background transition-colors text-left"
                >
                  <span className="text-text-secondary">{item.icon}</span>
                  <span className="flex-1 text-sm font-medium">
                    {item.label}
                  </span>
                  {item.badge && (
                    <span className="px-2 py-0.5 bg-gradient-to-r from-accent-purple to-accent-pink text-white text-[10px] font-bold rounded-full">
                      {item.badge}
                    </span>
                  )}
                </button>
              ))}

              {/* Theme Toggle */}
              <button
                onClick={() => {
                  toggleTheme()
                }}
                className="w-full flex items-center gap-3 px-4 py-2.5 hover:bg-background transition-colors text-left"
              >
                <span className="text-text-secondary">
                  {theme === 'dark' ? (
                    <Sun className="w-4 h-4" />
                  ) : (
                    <Moon className="w-4 h-4" />
                  )}
                </span>
                <span className="flex-1 text-sm font-medium">
                  {theme === 'dark' ? 'Светлая тема' : 'Темная тема'}
                </span>
              </button>
            </div>

            {/* Logout */}
            <div className="border-t border-border p-2">
              <button
                onClick={() => {
                  logout()
                  onClose()
                }}
                className="w-full flex items-center gap-3 px-4 py-2.5 hover:bg-red-50 dark:hover:bg-red-950/20 text-accent-red transition-colors rounded-lg"
              >
                <LogOut className="w-4 h-4" />
                <span className="flex-1 text-sm font-medium text-left">
                  Выйти
                </span>
              </button>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
