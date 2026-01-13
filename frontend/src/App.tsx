import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ThemeProvider } from './contexts/ThemeContext'
import { ChatProvider } from './contexts/ChatContext'
import { SearchProvider } from './contexts/SearchContext'
import { FilterProvider } from './contexts/FilterContext'
import { AuthProvider } from './contexts/AuthContext'
import { ProtectedRoute } from './components/ProtectedRoute'
import Layout from './components/layout/Layout'
import Dashboard from './pages/Dashboard'
import IdeaDetail from './pages/IdeaDetail'

// Auth pages
import LoginPage from './components/LoginPage'
import UserLoginPage from './pages/Auth/UserLoginPage'
import RegisterPage from './pages/Auth/RegisterPage'
import ForgotPasswordPage from './pages/Auth/ForgotPasswordPage'
import ResetPasswordPage from './pages/Auth/ResetPasswordPage'

// Settings pages
import ProfileSettingsPage from './pages/Settings/ProfileSettingsPage'
import SubscriptionPage from './pages/Settings/SubscriptionPage'

// Other
import AgentsPage from './pages/AgentsPage'

function App() {
  return (
    <AuthProvider>
      <ThemeProvider>
        <SearchProvider>
          <FilterProvider>
            <ChatProvider>
              <Router>
                <Routes>
                  {/* Admin Login (AI Agents Panel) */}
                  <Route path="/login" element={<LoginPage />} />

                  {/* User Authentication Routes */}
                  <Route path="/user/login" element={<UserLoginPage />} />
                  <Route path="/register" element={<RegisterPage />} />
                  <Route path="/forgot-password" element={<ForgotPasswordPage />} />
                  <Route path="/reset-password" element={<ResetPasswordPage />} />

                  {/* Protected Agents Page */}
                  <Route
                    path="/agents"
                    element={
                      <ProtectedRoute>
                        <AgentsPage />
                      </ProtectedRoute>
                    }
                  />

                  {/* Settings Pages (no Layout) */}
                  <Route path="/settings" element={<ProfileSettingsPage />} />
                  <Route path="/subscription" element={<SubscriptionPage />} />

                  {/* Main App Routes (with Layout) */}
                  <Route
                    path="/"
                    element={
                      <Layout>
                        <Dashboard />
                      </Layout>
                    }
                  />
                  <Route
                    path="/idea/:id"
                    element={
                      <Layout>
                        <IdeaDetail />
                      </Layout>
                    }
                  />
                </Routes>
              </Router>
            </ChatProvider>
          </FilterProvider>
        </SearchProvider>
      </ThemeProvider>
    </AuthProvider>
  )
}

export default App
