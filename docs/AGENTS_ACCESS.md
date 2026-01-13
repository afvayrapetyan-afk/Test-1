# 🔐 Доступ к AI Агентам

## 📍 Страница агентов

**URL:** `http://localhost:5173/agents`

## 🔑 Учётные данные

```
Логин:  Админ
Пароль: 987654
```

## 🚀 Как использовать

### 1. Открыть страницу логина

```
http://localhost:5173/login
```

### 2. Ввести учётные данные

```
Логин:  Админ
Пароль: 987654
```

### 3. Нажать "Войти"

Автоматически перенаправит на: `http://localhost:5173/agents`

### 4. Управлять агентами

На странице агентов можешь:
- ✅ Анализировать код (CodeAnalystAgent)
- ✅ Искать баги
- ✅ Проверять security
- ✅ Создавать фичи (DevAgent)
- ✅ Генерировать тесты

### 5. Выйти

Кнопка "Выйти" в правом верхнем углу

---

## 🔗 Добавить ссылку в навигацию

### В Dashboard добавь кнопку:

```tsx
// В Dashboard.tsx
<a
  href="/agents"
  className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
>
  🤖 AI Агенты
</a>
```

### Или в Sidebar/Header:

```tsx
<nav>
  <Link to="/">Dashboard</Link>
  <Link to="/agents">🤖 AI Агенты</Link>
</nav>
```

---

## 📝 Настройка роутинга

**Файл:** `frontend/src/App.tsx`

Нужно добавить:

```tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import { ProtectedRoute } from './components/ProtectedRoute'
import LoginPage from './components/LoginPage'
import AgentsPage from './pages/AgentsPage'
import Dashboard from './pages/Dashboard'

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/agents"
            element={
              <ProtectedRoute>
                <AgentsPage />
              </ProtectedRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
```

---

## 🛡️ Безопасность

### Текущая реализация (Development)

- ✅ Логин/пароль в коде
- ✅ Сессия в localStorage
- ✅ Защита роута

**Подходит для:**
- ✅ Local development
- ✅ Demo
- ✅ Internal tools

### Production (TODO)

Для production нужно:
- [ ] Backend API для аутентификации
- [ ] JWT tokens
- [ ] Password hashing (bcrypt)
- [ ] Rate limiting
- [ ] 2FA (опционально)

---

## 💡 Дополнительно

### Изменить пароль

**Файл:** `frontend/src/contexts/AuthContext.tsx`

```tsx
const ADMIN_USERNAME = 'Админ'  // ← Изменить здесь
const ADMIN_PASSWORD = '987654'  // ← Изменить здесь
```

### Добавить больше пользователей

```tsx
const USERS = [
  { username: 'Админ', password: '987654', role: 'admin' },
  { username: 'User', password: '123456', role: 'viewer' },
]

const login = (username: string, password: string) => {
  const user = USERS.find(u =>
    u.username === username && u.password === password
  )
  if (user) {
    // ... login logic
  }
}
```

---

## ✅ Готово!

Теперь у тебя есть:
- 🔐 Защищённая страница агентов
- 🔑 Логин/пароль: Админ / 987654
- 🔗 URL: http://localhost:5173/agents
- 🎨 Красивый дизайн с градиентами
- 🚪 Кнопка выхода

**Доступ:**
1. Открыть: http://localhost:5173/login
2. Ввести: Админ / 987654
3. Войти → http://localhost:5173/agents
4. Управлять агентами! 🤖
