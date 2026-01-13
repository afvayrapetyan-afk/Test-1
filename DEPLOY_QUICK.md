# ⚡ Быстрый деплой за 10 минут

## 📋 Что вы получите

- **Frontend:** https://test-1-iota-sepia.vercel.app
- **Backend API:** https://your-app.up.railway.app

---

## 🚀 ШАГ 1: Деплой Backend (5 мин)

1. Откройте https://railway.app → Login через GitHub
2. New Project → Deploy from GitHub → Выберите репозиторий
3. Root Directory: **`backend`**
4. Variables → Add:
   ```
   OPENAI_API_KEY=your-openai-api-key-here
   
   CORS_ORIGINS=https://test-1-iota-sepia.vercel.app
   
   DATABASE_URL=sqlite:///./business_portfolio.db
   SECRET_KEY=change-this-to-random-32-chars
   ```
5. Settings → Start Command:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
6. Deploy! → **Копируйте ваш Railway URL!**

**Проверка:**
```bash
curl https://your-app.up.railway.app/health
```

---

## 🎨 ШАГ 2: Деплой Frontend (5 мин)

1. Откройте https://vercel.com/new → Login через GitHub
2. Import Repository → Выберите ваш проект
3. Настройки:
   - Framework: **Vite**
   - Root Directory: **`frontend`**
   - Build Command: **`npm run build`**
   - Output Directory: **`dist`**

4. Environment Variables:
   ```
   VITE_API_URL = https://your-app.up.railway.app
   ```
   (используйте ваш Railway URL из Шага 1!)

5. Deploy!

**Готово!** Откройте https://test-1-iota-sepia.vercel.app

---

## ✅ Проверка

### Backend:
- Health: https://your-app.up.railway.app/health
- Swagger: https://your-app.up.railway.app/docs
- Trends: https://your-app.up.railway.app/api/v1/trends/

### Frontend:
- Dashboard: https://test-1-iota-sepia.vercel.app

### Всё работает?
Откройте https://test-1-iota-sepia.vercel.app и проверьте что данные загружаются!

---

## 🐛 Если что-то не работает

### CORS Error?
Убедитесь что CORS_ORIGINS на Railway содержит ваш Vercel URL

### API не подключается?
Проверьте VITE_API_URL в Vercel Environment Variables

### 500 Error?
Проверьте Logs в Railway Dashboard

---

**Нужна подробная инструкция?** Смотрите [DEPLOYMENT.md](DEPLOYMENT.md)

**Готово!** 🎉
