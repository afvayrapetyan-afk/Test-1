import { motion, AnimatePresence } from 'framer-motion'
import { X, CheckCheck, TrendingUp, Code, DollarSign, Bell } from 'lucide-react'

interface NotificationsPanelProps {
  isOpen: boolean
  onClose: () => void
}

interface Notification {
  id: string
  type: 'trend' | 'project' | 'revenue' | 'info'
  title: string
  message: string
  timeAgo: string
  isRead: boolean
}

const mockNotifications: Notification[] = [
  {
    id: '1',
    type: 'trend',
    title: 'Новый тренд обнаружен',
    message: 'AI-помощник для питания набирает популярность (+45% за неделю)',
    timeAgo: '5 мин назад',
    isRead: false,
  },
  {
    id: '2',
    type: 'revenue',
    title: 'Цель по выручке достигнута',
    message: 'Платформа автоматизации достигла $15K в месяц',
    timeAgo: '1 час назад',
    isRead: false,
  },
  {
    id: '3',
    type: 'project',
    title: 'Проект обновлен',
    message: 'Умный сад: Бэкенд 85% → 92%',
    timeAgo: '3 часа назад',
    isRead: true,
  },
]

export default function NotificationsPanel({
  isOpen,
  onClose,
}: NotificationsPanelProps) {
  const getIcon = (type: Notification['type']) => {
    switch (type) {
      case 'trend':
        return <TrendingUp className="w-5 h-5 text-accent-orange" />
      case 'project':
        return <Code className="w-5 h-5 text-accent-blue" />
      case 'revenue':
        return <DollarSign className="w-5 h-5 text-accent-green" />
      default:
        return <Bell className="w-5 h-5 text-accent-purple" />
    }
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
            className="fixed inset-0 bg-black/20 z-40"
          />

          {/* Panel */}
          <motion.div
            initial={{ opacity: 0, x: 300 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 300 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className="fixed top-0 right-0 h-full w-full max-w-md bg-surface border-l border-border shadow-2xl z-50 flex flex-col"
          >
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-border">
              <h2 className="text-lg font-bold flex items-center gap-2">
                <Bell className="w-5 h-5" />
                Уведомления
              </h2>
              <div className="flex items-center gap-2">
                <button className="text-sm text-accent-blue hover:text-accent-purple transition-colors font-medium">
                  <CheckCheck className="w-4 h-4" />
                </button>
                <button
                  onClick={onClose}
                  className="text-text-secondary hover:text-text-primary transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* Notifications List */}
            <div className="flex-1 overflow-y-auto">
              {mockNotifications.map((notification) => (
                <div
                  key={notification.id}
                  className={`p-4 border-b border-border cursor-pointer transition-colors hover:bg-background ${
                    !notification.isRead ? 'bg-accent-blue/5' : ''
                  }`}
                >
                  <div className="flex gap-3">
                    <div className="flex-shrink-0 mt-1">
                      {getIcon(notification.type)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-2">
                        <h3 className="font-semibold text-sm text-text-primary">
                          {notification.title}
                        </h3>
                        {!notification.isRead && (
                          <div className="w-2 h-2 bg-accent-blue rounded-full flex-shrink-0 mt-1" />
                        )}
                      </div>
                      <p className="text-sm text-text-secondary mt-1">
                        {notification.message}
                      </p>
                      <p className="text-xs text-text-tertiary mt-2">
                        {notification.timeAgo}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Footer */}
            <div className="p-4 border-t border-border">
              <button className="w-full py-2 text-sm font-medium text-accent-blue hover:text-accent-purple transition-colors">
                Показать все уведомления
              </button>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
