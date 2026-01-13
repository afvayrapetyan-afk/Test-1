import { useState, useRef, useEffect } from 'react'
import { X, Send } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

interface Message {
  id: string
  role: 'user' | 'ai'
  content: string
  timestamp: string
}

interface AIChatPanelProps {
  isOpen: boolean
  onClose: () => void
}

export default function AIChatPanel({ isOpen, onClose }: AIChatPanelProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'ai',
      content:
        'Привет! Я AI консультант. Я уже изучил все ваши бизнес-идеи.\n\n**Чем могу помочь?**\n• Оценить перспективность идеи\n• Сравнить несколько идей\n• Проанализировать риски\n• Предложить стратегию',
      timestamp: 'Сейчас',
    },
  ])
  const [inputValue, setInputValue] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const getAIResponse = (message: string): string => {
    const msg = message.toLowerCase()

    if (msg.includes('прибыльн') || msg.includes('доход')) {
      return '**No-Code Automation Platform** — самая прибыльная идея!\n\n💰 ARR: $540K через год\n📊 Маржа: 78%\n💵 Инвестиции: $120K\n\nВысокий спрос на автоматизацию + SaaS модель = отличная маржинальность.'
    }

    if (msg.includes('окуп') || msg.includes('быстр')) {
      return '**Telemedicine for Pets** окупится быстрее всех!\n\n⏱️ Окупаемость: 6 месяцев\n💵 Инвестиции: всего $28K\n💰 ARR: $95K\n\nНебольшие вложения + растущий рынок pet health = быстрый ROI.'
    }

    if (msg.includes('сравни') || msg.includes('топ')) {
      return '**Сравнение топ-3 идей:**\n\n1️⃣ **No-Code Platform** (9.1/10)\n✅ Самая высокая маржа 78%\n✅ Огромный рынок\n⚠️ Высокие инвестиции $120K\n\n2️⃣ **AI Personal Chef** (8.4/10)\n✅ Баланс инвестиций/дохода\n✅ Быстрая окупаемость 8 мес\n\n3️⃣ **Telemedicine for Pets** (7.8/10)\n✅ Минимальные вложения $28K\n✅ Самая быстрая окупаемость 6 мес'
    }

    if (msg.includes('риск')) {
      return '**Основные риски:**\n\n⚠️ **Конкуренция:** Крупные игроки могут скопировать\n⚠️ **AI costs:** OpenAI API может быть дорогим\n⚠️ **Retention:** Сложно удержать пользователей\n\n**Рекомендация:** Начните с MVP, тестируйте retention, потом масштабируйте.'
    }

    return 'Отличный вопрос! Я проанализировал данные.\n\nМогу дать более конкретный ответ, если уточните:\n• О какой именно идее?\n• Что вас интересует?\n• Какой бюджет?'
  }

  const sendMessage = (content: string) => {
    if (!content.trim()) return

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: 'Только что',
    }
    setMessages((prev) => [...prev, userMessage])
    setInputValue('')

    // Show typing indicator
    setIsTyping(true)

    // Simulate AI response
    setTimeout(() => {
      setIsTyping(false)
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'ai',
        content: getAIResponse(content),
        timestamp: 'Только что',
      }
      setMessages((prev) => [...prev, aiMessage])
    }, 1500)
  }

  const quickActions = [
    { label: '💰 Самая прибыльная?', query: 'Какая идея самая прибыльная?' },
    { label: '⚡ Быстрая окупаемость?', query: 'Какая идея быстрее окупится?' },
    { label: '📊 Сравни топ-3', query: 'Сравни топ 3 идеи' },
    { label: '⚠️ Риски?', query: 'Какие риски?' },
  ]

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage(inputValue)
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
            className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40 lg:hidden"
          />

          {/* Panel */}
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="fixed top-0 right-0 h-screen w-full lg:w-[420px] bg-surface border-l border-border shadow-2xl z-50 flex flex-col"
          >
            {/* Header */}
            <div className="bg-gradient-to-r from-accent-purple to-accent-pink p-4 flex items-center justify-between">
              <div className="flex items-center gap-2 text-white">
                <span className="text-2xl">🤖</span>
                <h2 className="text-lg font-bold">AI Консультант</h2>
              </div>
              <button
                onClick={onClose}
                className="w-8 h-8 rounded-full bg-white/20 hover:bg-white/30 transition-colors flex items-center justify-center text-white"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex gap-3 ${
                    message.role === 'user' ? 'flex-row-reverse' : ''
                  }`}
                >
                  {/* Avatar */}
                  <div
                    className={`w-9 h-9 rounded-full flex items-center justify-center text-lg flex-shrink-0 ${
                      message.role === 'ai'
                        ? 'bg-gradient-to-br from-accent-purple to-accent-pink'
                        : 'bg-accent-blue'
                    }`}
                  >
                    {message.role === 'ai' ? '🤖' : '👤'}
                  </div>

                  {/* Message Bubble */}
                  <div className="flex-1 max-w-[280px]">
                    <div
                      className={`rounded-xl p-3 ${
                        message.role === 'ai'
                          ? 'bg-background border border-border'
                          : 'bg-accent-blue text-white'
                      }`}
                    >
                      <div
                        className="text-sm leading-relaxed whitespace-pre-line"
                        dangerouslySetInnerHTML={{
                          __html: message.content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>'),
                        }}
                      />
                    </div>
                    <div className="text-xs text-text-tertiary mt-1 px-1">
                      {message.timestamp}
                    </div>
                  </div>
                </div>
              ))}

              {/* Typing Indicator */}
              {isTyping && (
                <div className="flex gap-3">
                  <div className="w-9 h-9 rounded-full bg-gradient-to-br from-accent-purple to-accent-pink flex items-center justify-center text-lg">
                    🤖
                  </div>
                  <div className="bg-background border border-border rounded-xl p-3">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 rounded-full bg-text-tertiary animate-bounce" />
                      <div
                        className="w-2 h-2 rounded-full bg-text-tertiary animate-bounce"
                        style={{ animationDelay: '0.2s' }}
                      />
                      <div
                        className="w-2 h-2 rounded-full bg-text-tertiary animate-bounce"
                        style={{ animationDelay: '0.4s' }}
                      />
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Quick Actions */}
            <div className="border-t border-border p-3">
              <div className="flex flex-wrap gap-2">
                {quickActions.map((action, index) => (
                  <button
                    key={index}
                    onClick={() => sendMessage(action.query)}
                    className="px-3 py-1.5 text-xs font-medium border border-border bg-surface rounded-lg hover:bg-accent-blue hover:text-white hover:border-accent-blue transition-colors"
                  >
                    {action.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Input */}
            <div className="border-t border-border p-4">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Задайте вопрос..."
                  className="flex-1 px-4 py-2 border border-border rounded-xl bg-background focus:outline-none focus:ring-2 focus:ring-accent-purple/50 text-sm"
                />
                <button
                  onClick={() => sendMessage(inputValue)}
                  className="w-10 h-10 bg-gradient-to-r from-accent-purple to-accent-pink text-white rounded-xl flex items-center justify-center hover:scale-105 transition-transform"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
