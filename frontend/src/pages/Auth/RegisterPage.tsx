import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Mail, Lock, User, AlertCircle, Eye, EyeOff, CheckCircle, Sparkles, Shield } from 'lucide-react'
import { useAuth } from '../../contexts/AuthContext'
import { motion } from 'framer-motion'

export default function RegisterPage() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [acceptTerms, setAcceptTerms] = useState(false)
  const [focusedField, setFocusedField] = useState<string | null>(null)

  const { register } = useAuth()
  const navigate = useNavigate()

  const validatePassword = () => {
    if (password.length < 8) {
      return 'Пароль должен быть не менее 8 символов'
    }
    if (password !== confirmPassword) {
      return 'Пароли не совпадают'
    }
    return null
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    const passwordError = validatePassword()
    if (passwordError) {
      setError(passwordError)
      return
    }

    if (!acceptTerms) {
      setError('Пожалуйста, примите условия использования')
      return
    }

    setIsLoading(true)

    try {
      await register(name, email, password)
      navigate('/')
    } catch (err: any) {
      setError(err.message || 'Ошибка при регистрации')
    } finally {
      setIsLoading(false)
    }
  }

  const passwordStrength = () => {
    if (password.length === 0) return { label: '', color: '', width: '0%' }
    if (password.length < 6) return { label: 'Слабый', color: 'bg-red-500', width: '33%' }
    if (password.length < 10) return { label: 'Средний', color: 'bg-yellow-500', width: '66%' }
    return { label: 'Надёжный', color: 'bg-emerald-500', width: '100%' }
  }

  const strength = passwordStrength()

  const InputField = ({
    type,
    value,
    onChange,
    placeholder,
    icon: Icon,
    name,
    showToggle,
    isVisible,
    onToggle
  }: {
    type: string
    value: string
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void
    placeholder: string
    icon: any
    name: string
    showToggle?: boolean
    isVisible?: boolean
    onToggle?: () => void
  }) => (
    <div className={`relative group transition-all duration-300 ${focusedField === name ? 'transform scale-[1.01]' : ''}`}>
      <div className={`absolute inset-0 rounded-xl bg-gradient-to-r from-emerald-500/20 to-emerald-600/20 opacity-0 transition-opacity duration-300 blur-xl ${focusedField === name ? 'opacity-100' : ''}`} />
      <div className="relative">
        <Icon className={`absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 transition-colors duration-300 ${focusedField === name ? 'text-emerald-400' : 'text-slate-500'}`} />
        <input
          type={showToggle ? (isVisible ? 'text' : 'password') : type}
          value={value}
          onChange={onChange}
          onFocus={() => setFocusedField(name)}
          onBlur={() => setFocusedField(null)}
          placeholder={placeholder}
          className="w-full pl-12 pr-14 py-4 bg-slate-900/50 border border-slate-700/50 rounded-xl text-white placeholder-slate-500 focus:border-emerald-500/50 focus:bg-slate-900/80 outline-none transition-all duration-300"
          required
        />
        {showToggle && (
          <button
            type="button"
            onClick={onToggle}
            className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 hover:text-emerald-400 transition-colors duration-300"
          >
            {isVisible ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
          </button>
        )}
      </div>
    </div>
  )

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden py-12">
      {/* Premium Dark Background with Gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950" />

      {/* Subtle Animated Glow Effects */}
      <div className="absolute top-1/4 -left-32 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl animate-pulse" />
      <div className="absolute bottom-1/4 -right-32 w-96 h-96 bg-emerald-600/8 rounded-full blur-3xl animate-pulse delay-1000" />
      <div className="absolute top-3/4 left-1/2 w-64 h-64 bg-emerald-400/5 rounded-full blur-3xl animate-pulse delay-500" />

      {/* Grid Pattern Overlay */}
      <div
        className="absolute inset-0 opacity-[0.02]"
        style={{
          backgroundImage: `linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
                           linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)`,
          backgroundSize: '50px 50px'
        }}
      />

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: 'easeOut' }}
        className="w-full max-w-md px-6 relative z-10"
      >
        {/* Logo & Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-center mb-8"
        >
          {/* Premium Logo */}
          <div className="inline-flex items-center justify-center mb-6">
            <div className="relative">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-emerald-400 to-emerald-600 flex items-center justify-center shadow-lg shadow-emerald-500/25">
                <Sparkles className="w-8 h-8 text-white" />
              </div>
              <div className="absolute -inset-1 rounded-2xl bg-gradient-to-br from-emerald-400 to-emerald-600 opacity-30 blur-lg" />
            </div>
          </div>

          <h1 className="text-3xl font-semibold text-white tracking-tight mb-2">
            Создать аккаунт
          </h1>
          <p className="text-slate-400 text-sm tracking-wide">
            Присоединитесь к Sber AI
          </p>
        </motion.div>

        {/* Form Card with Glassmorphism */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="backdrop-blur-xl bg-white/[0.03] border border-white/10 rounded-3xl p-8 shadow-2xl"
        >
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Name Field */}
            <div className="space-y-2">
              <label className="block text-xs font-medium text-slate-400 uppercase tracking-wider">
                Имя
              </label>
              <InputField
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Ваше имя"
                icon={User}
                name="name"
              />
            </div>

            {/* Email Field */}
            <div className="space-y-2">
              <label className="block text-xs font-medium text-slate-400 uppercase tracking-wider">
                Email
              </label>
              <InputField
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your@email.com"
                icon={Mail}
                name="email"
              />
            </div>

            {/* Password Field */}
            <div className="space-y-2">
              <label className="block text-xs font-medium text-slate-400 uppercase tracking-wider">
                Пароль
              </label>
              <InputField
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Минимум 8 символов"
                icon={Lock}
                name="password"
                showToggle
                isVisible={showPassword}
                onToggle={() => setShowPassword(!showPassword)}
              />
              {/* Password Strength Indicator */}
              {password && (
                <motion.div
                  initial={{ opacity: 0, y: -5 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="space-y-2"
                >
                  <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: strength.width }}
                      className={`h-full ${strength.color} transition-all duration-300`}
                    />
                  </div>
                  <p className="text-xs text-slate-500">
                    Надёжность: <span className={strength.color === 'bg-emerald-500' ? 'text-emerald-400' : strength.color === 'bg-yellow-500' ? 'text-yellow-400' : 'text-red-400'}>{strength.label}</span>
                  </p>
                </motion.div>
              )}
            </div>

            {/* Confirm Password Field */}
            <div className="space-y-2">
              <label className="block text-xs font-medium text-slate-400 uppercase tracking-wider">
                Подтвердите пароль
              </label>
              <InputField
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Повторите пароль"
                icon={Shield}
                name="confirmPassword"
                showToggle
                isVisible={showConfirmPassword}
                onToggle={() => setShowConfirmPassword(!showConfirmPassword)}
              />
              {confirmPassword && password === confirmPassword && (
                <motion.div
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="flex items-center gap-2 text-emerald-400 text-xs mt-2"
                >
                  <CheckCircle className="w-4 h-4" />
                  <span>Пароли совпадают</span>
                </motion.div>
              )}
            </div>

            {/* Terms Checkbox */}
            <div className="flex items-start gap-3 pt-2">
              <div className="relative mt-0.5">
                <input
                  type="checkbox"
                  id="terms"
                  checked={acceptTerms}
                  onChange={(e) => setAcceptTerms(e.target.checked)}
                  className="peer sr-only"
                />
                <div
                  onClick={() => setAcceptTerms(!acceptTerms)}
                  className={`w-5 h-5 rounded-md border-2 cursor-pointer transition-all duration-300 flex items-center justify-center ${
                    acceptTerms
                      ? 'bg-emerald-500 border-emerald-500'
                      : 'border-slate-600 hover:border-slate-500'
                  }`}
                >
                  {acceptTerms && (
                    <motion.svg
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      className="w-3 h-3 text-white"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      strokeWidth={3}
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                    </motion.svg>
                  )}
                </div>
              </div>
              <label htmlFor="terms" className="text-sm text-slate-400 cursor-pointer leading-relaxed">
                Я принимаю{' '}
                <Link to="/terms" className="text-emerald-400 hover:text-emerald-300 transition-colors">
                  условия использования
                </Link>{' '}
                и{' '}
                <Link to="/privacy" className="text-emerald-400 hover:text-emerald-300 transition-colors">
                  политику конфиденциальности
                </Link>
              </label>
            </div>

            {/* Error Message */}
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex items-center gap-3 p-4 bg-red-500/10 border border-red-500/20 rounded-xl"
              >
                <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
                <span className="text-sm text-red-400">{error}</span>
              </motion.div>
            )}

            {/* Submit Button */}
            <motion.button
              type="submit"
              disabled={isLoading}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="relative w-full py-4 bg-gradient-to-r from-emerald-500 to-emerald-600 text-white font-semibold rounded-xl overflow-hidden group disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-emerald-500/25 transition-shadow duration-300 hover:shadow-emerald-500/40"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-emerald-400 to-emerald-500 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
              <span className="relative flex items-center justify-center gap-2">
                {isLoading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Создание аккаунта...
                  </>
                ) : (
                  'Зарегистрироваться'
                )}
              </span>
            </motion.button>
          </form>

          {/* Divider */}
          <div className="flex items-center my-8">
            <div className="flex-1 h-px bg-gradient-to-r from-transparent via-slate-700 to-transparent" />
          </div>

          {/* Login Link */}
          <p className="text-center text-sm text-slate-400">
            Уже есть аккаунт?{' '}
            <Link
              to="/user/login"
              className="text-emerald-400 hover:text-emerald-300 font-medium transition-colors duration-300"
            >
              Войти
            </Link>
          </p>
        </motion.div>

        {/* Footer */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.7 }}
          className="text-center text-xs text-slate-600 mt-8"
        >
          © 2024 Sber AI. Все права защищены.
        </motion.p>
      </motion.div>
    </div>
  )
}
