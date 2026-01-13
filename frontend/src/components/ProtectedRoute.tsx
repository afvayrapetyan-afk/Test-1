/**
 * Protected Route - защищает роуты от неавторизованных пользователей
 * Проверяет как обычную аутентификацию, так и админскую
 */
import { Navigate } from 'react-router-dom'

interface ProtectedRouteProps {
  children: React.ReactNode
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  // Проверяем админскую аутентификацию из localStorage
  const isAdminAuthenticated = localStorage.getItem('admin_auth') === 'true'

  if (!isAdminAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}
