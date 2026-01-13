import { MessageCircle } from 'lucide-react'
import { useChat } from '../../contexts/ChatContext'
import AIChatPanel from './AIChatPanel'

export default function AIChatFAB() {
  const { isChatOpen, openChat, closeChat } = useChat()

  return (
    <>
      <button
        onClick={openChat}
        className="fixed bottom-4 right-4 w-[60px] h-[60px] rounded-full bg-gradient-to-br from-accent-purple to-accent-pink text-white shadow-xl hover:scale-110 transition-smooth flex items-center justify-center z-30 animate-pulse-subtle"
        style={{
          boxShadow: '0 8px 24px rgba(139, 92, 246, 0.4)',
        }}
        title="Открыть AI Консультант"
      >
        <MessageCircle className="w-7 h-7" />
      </button>

      <AIChatPanel isOpen={isChatOpen} onClose={closeChat} />
    </>
  )
}
