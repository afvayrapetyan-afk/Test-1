# 🚀 Deployment Guide - AI Business Portfolio Manager

Полная инструкция по деплою проекта на production.

## 📋 Что нужно задеплоить

1. **Backend (FastAPI)** → Railway.app
2. **Frontend (React + Vite)** → Vercel (https://test-1-iota-sepia.vercel.app)

---

## 🔧 ЧАСТЬ 1: Деплой Backend на Railway

### Шаг 1: Создайте проект на Railway

1. Перейдите на https://railway.app и войдите через GitHub
2. Нажмите "New Project" → "Deploy from GitHub repo"
3. Выберите ваш репозиторий
4. Укажите Root Directory: **backend**

### Шаг 2: Настройте переменные окружения

В Railway Dashboard → Variables добавьте:

```env
# OpenAI (ОБЯЗАТЕЛЬНО!)
OPENAI_API_KEY=your-openai-api-key-here

# Database
DATABASE_URL=sqlite:///./business_portfolio.db

# Security
SECRET_KEY=your-super-secret-production-key-min-32-chars-please-change
ENVIRONMENT=production
DEBUG=false

# CORS (добавьте ваш Vercel URL)
CORS_ORIGINS=https://test-1-iota-sepia.vercel.app,http://localhost:5173
```

### Шаг 3: Настройте Start Command

Settings → Start Command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Шаг 4: Деплой

Railway автоматически задеплоит проект. Вы получите URL:
```
https://your-app.up.railway.app
```

**СОХРАНИТЕ ЭТОТ URL!** Он понадобится для фронтенда.

---

## 🎨 ЧАСТЬ 2: Деплой Frontend на Vercel

### Вариант 1: Через Vercel Dashboard (Рекомендуется)

1. Перейдите на https://vercel.com/new
2. Импортируйте GitHub репозиторий
3. Настройте:
   - **Framework:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

4. Environment Variables:
   - Name: **VITE_API_URL**
   - Value: **https://your-app.up.railway.app** (ваш Railway URL)

5. Deploy!

### Вариант 2: Через Vercel CLI

```bash
cd frontend
npm install -g vercel
vercel login
vercel --prod
```

---

## ✅ Быстрая проверка

### 1. Backend работает?
```bash
curl https://your-app.up.railway.app/health
curl https://your-app.up.railway.app/api/v1/trends/
```

### 2. Frontend работает?
Откройте https://test-1-iota-sepia.vercel.app

### 3. Нет CORS ошибок?
Проверьте Console в DevTools (F12)

---

## 🐛 Частые проблемы

### CORS Error
**Решение:** Добавьте Vercel URL в CORS_ORIGINS на Railway

### API не работает
**Решение:** Проверьте VITE_API_URL в Vercel Environment Variables

### 500 Error на Railway
**Решение:** Проверьте логи Railway Dashboard → Logs

---

## 🎯 После деплоя

Ваше приложение доступно:
- **Frontend:** https://test-1-iota-sepia.vercel.app  
- **Backend API:** https://your-app.up.railway.app
- **Swagger UI:** https://your-app.up.railway.app/docs

**Готово!** 🚀
