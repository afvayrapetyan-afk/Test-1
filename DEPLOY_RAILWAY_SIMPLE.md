# 🚂 Railway Деплой - 5 Минут

## Шаг 1: Откройте Railway
👉 https://railway.app/new

## Шаг 2: Deploy from GitHub
1. Нажмите "Deploy from GitHub repo"
2. Авторизуйтесь через GitHub (если нужно)
3. Выберите репозиторий: **afvayrapetyan-afk/Test-1**

## Шаг 3: Configure Service
После выбора репозитория Railway автоматически создаст сервис.

**ВАЖНО! Измените Root Directory:**
1. Кликните на ваш сервис
2. Settings → Root Directory
3. Введите: `backend`
4. Нажмите Update

## Шаг 4: Add Variables (переменные окружения)

Кликните на Variables (слева) и добавьте:

```
OPENAI_API_KEY=ваш-ключ-openai
DATABASE_URL=sqlite:///./business_portfolio.db
SECRET_KEY=any-random-string-minimum-32-characters-long-123456
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=https://test-1-iota-sepia.vercel.app,http://localhost:5173
```

**⚠️ OPENAI_API_KEY - возьмите из файла `/backend/.env`**

## Шаг 5: Deploy!

Railway автоматически задеплоит! Через 2-3 минуты получите URL:
```
https://test-1-production-XXXX.up.railway.app
```

**СОХРАНИТЕ ЭТОТ URL** - он нужен для фронтенда!

## Шаг 6: Проверка

Откройте в браузере:
```
https://your-app.up.railway.app/health
```

Должны увидеть:
```json
{"status":"healthy","version":"0.1.0","environment":"production"}
```

✅ **Backend готов!**

---

## Теперь Frontend на Vercel

👉 https://vercel.com/new

1. Import Git Repository: **afvayrapetyan-afk/Test-1**
2. Configure:
   - Framework: **Vite**
   - Root Directory: **frontend**
   - Build Command: **npm run build**
   - Output Directory: **dist**

3. Environment Variables:
   ```
   VITE_API_URL=ваш-railway-url-из-шага-5
   ```

4. Deploy!

**Готово! 🎉**

Ваше приложение:
- Frontend: https://test-1-iota-sepia.vercel.app
- Backend: https://your-app.up.railway.app
