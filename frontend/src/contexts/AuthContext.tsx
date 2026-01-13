/**
 * Auth Context - полноценная система аутентификации
 */
import { createContext, useContext, useState, useEffect, ReactNode } from 'react'

export interface User {
  id: string
  email: string
  name: string
  avatar?: string
  plan: 'free' | 'pro' | 'enterprise'
  planExpiry?: Date
  createdAt: Date
}

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (name: string, email: string, password: string) => Promise<void>
  logout: () => void
  forgotPassword: (email: string) => Promise<void>
  resetPassword: (token: string, newPassword: string) => Promise<void>
  updateProfile: (data: Partial<User>) => Promise<void>
  changePassword: (currentPassword: string, newPassword: string) => Promise<void>
  // Admin credentials для /agents
  adminLogin: (username: string, password: string) => boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

// Admin credentials для панели AI агентов
const ADMIN_USERNAME = 'Админ'
const ADMIN_PASSWORD = '987654'

// Mock user для демонстрации
const mockUser: User = {
  id: '1',
  email: 'vardana@example.com',
  name: 'Vardana Jrapetyan',
  avatar: undefined,
  plan: 'pro',
  planExpiry: new Date('2025-12-31'),
  createdAt: new Date('2024-01-15'),
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Проверка сохраненной сессии при загрузке
  useEffect(() => {
    const checkAuth = () => {
      const savedUser = localStorage.getItem('user')
      const token = localStorage.getItem('token')

      if (savedUser && token) {
        try {
          const parsedUser = JSON.parse(savedUser)
          // Восстановить Date объекты
          if (parsedUser.planExpiry) {
            parsedUser.planExpiry = new Date(parsedUser.planExpiry)
          }
          if (parsedUser.createdAt) {
            parsedUser.createdAt = new Date(parsedUser.createdAt)
          }
          setUser(parsedUser)
        } catch (error) {
          console.error('Error parsing saved user:', error)
          localStorage.removeItem('user')
          localStorage.removeItem('token')
        }
      }
      setIsLoading(false)
    }

    checkAuth()
  }, [])

  const login = async (email: string, password: string) => {
    setIsLoading(true)
    try {
      // Симуляция API запроса
      await new Promise((resolve) => setTimeout(resolve, 1000))

      // В реальном приложении здесь будет API call
      if (email === 'vardana@example.com' && password === 'demo123') {
        const token = 'mock-jwt-token-' + Date.now()
        localStorage.setItem('token', token)
        localStorage.setItem('user', JSON.stringify(mockUser))
        setUser(mockUser)
      } else {
        throw new Error('Неверный email или пароль')
      }
    } catch (error) {
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  const register = async (name: string, email: string, _password: string) => {
    setIsLoading(true)
    try {
      // Симуляция API запроса
      await new Promise((resolve) => setTimeout(resolve, 1500))

      // Проверка существующего пользователя
      if (email === 'vardana@example.com') {
        throw new Error('Пользователь с таким email уже существует')
      }

      // В реальном приложении здесь будет API call
      // Password будет использоваться в API: _password
      const newUser: User = {
        id: Date.now().toString(),
        email,
        name,
        plan: 'free',
        createdAt: new Date(),
      }

      const token = 'mock-jwt-token-' + Date.now()
      localStorage.setItem('token', token)
      localStorage.setItem('user', JSON.stringify(newUser))
      setUser(newUser)
    } catch (error) {
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('admin_auth')
    localStorage.removeItem('admin_user')
    setUser(null)
    window.location.href = '/login'
  }

  const forgotPassword = async (email: string) => {
    setIsLoading(true)
    try {
      // Симуляция отправки email
      await new Promise((resolve) => setTimeout(resolve, 1000))
      console.log('Password reset email sent to:', email)
    } catch (error) {
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  const resetPassword = async (token: string, _newPassword: string) => {
    setIsLoading(true)
    try {
      // Симуляция сброса пароля
      await new Promise((resolve) => setTimeout(resolve, 1000))
      // В реальном приложении: API call с token и _newPassword
      console.log('Password reset with token:', token)
    } catch (error) {
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  const updateProfile = async (data: Partial<User>) => {
    setIsLoading(true)
    try {
      // Симуляция обновления профиля
      await new Promise((resolve) => setTimeout(resolve, 1000))

      if (user) {
        const updatedUser = { ...user, ...data }
        localStorage.setItem('user', JSON.stringify(updatedUser))
        setUser(updatedUser)
      }
    } catch (error) {
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  const changePassword = async (
    currentPassword: string,
    _newPassword: string
  ) => {
    setIsLoading(true)
    try {
      // Симуляция смены пароля
      await new Promise((resolve) => setTimeout(resolve, 1000))

      // В реальном приложении проверяется текущий пароль
      if (currentPassword.length < 6) {
        throw new Error('Неверный текущий пароль')
      }

      // В реальном приложении: API call с currentPassword и _newPassword
      console.log('Password changed successfully')
    } catch (error) {
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  const adminLogin = (username: string, password: string): boolean => {
    if (username === ADMIN_USERNAME && password === ADMIN_PASSWORD) {
      localStorage.setItem('admin_auth', 'true')
      localStorage.setItem('admin_user', username)
      return true
    }
    return false
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        register,
        logout,
        forgotPassword,
        resetPassword,
        updateProfile,
        changePassword,
        adminLogin,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
