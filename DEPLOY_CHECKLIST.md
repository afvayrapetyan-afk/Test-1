# ✅ Чеклист развертывания на production

## 📋 Перед началом

- [x] ✅ Код закоммичен
- [x] ✅ OpenAI API ключ готов
- [x] ✅ GitHub репозиторий: `afvayrapetyan-afk/Test-1`
- [x] ✅ Frontend на Vercel: `https://test-1-iota-sepia.vercel.app`
- [x] ✅ 10 идей в базе (русский язык)
- [x] ✅ Автоматизация настроена (9:00 UTC)

---

## 🚀 Шаги развертывания

### Шаг 1: Push на GitHub ⏱️ 2 минуты

```bash
cd "/Users/vardanajrapetan/Project 1"
git push origin main
```

- [ ] Код загружен на GitHub
- [ ] Коммит виден на https://github.com/afvayrapetyan-afk/Test-1

---

### Шаг 2: Railway - PostgreSQL ⏱️ 2 минуты

1. Откройте: https://railway.app
2. New Project → Add PostgreSQL

- [ ] PostgreSQL создан
- [ ] Скопировали `DATABASE_URL`

---

### Шаг 3: Railway - Redis ⏱️ 2 минуты

1. В том же проекте: + New → Add Redis

- [ ] Redis создан
- [ ] Скопировали `REDIS_URL`

---

### Шаг 4: Railway - Backend API ⏱️ 5 минут

1. + New → GitHub Repo → `afvayrapetyan-afk/Test-1`
2. Settings → Root Directory: `backend`
3. Variables:
   ```
   OPENAI_API_KEY=<ваш_OpenAI_API_ключ>
   DATABASE_URL=<из шага 2>
   REDIS_URL=<из шага 3>
   CORS_ORIGINS=https://test-1-iota-sepia.vercel.app
   PORT=8000
   ```
4. Settings → Start Command:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
5. Settings → Generate Domain (активируйте)

- [ ] Backend API развернут
- [ ] Public URL работает (проверьте /health)
- [ ] Скопировали URL: `https://________.railway.app`

---

### Шаг 5: Railway - Celery Worker ⏱️ 3 минуты

1. + New → GitHub Repo → `afvayrapetyan-afk/Test-1`
2. Settings → Root Directory: `backend`
3. Variables: **ТЕ ЖЕ** что и для Backend API
4. Settings → Start Command:
   ```
   celery -A app.tasks.scheduled_tasks worker --loglevel=info
   ```

- [ ] Celery Worker развернут
- [ ] Статус "Active"

---

### Шаг 6: Railway - Celery Beat ⏱️ 3 минуты

**⭐ САМЫЙ ВАЖНЫЙ - отвечает за автоматизацию!**

1. + New → GitHub Repo → `afvayrapetyan-afk/Test-1`
2. Settings → Root Directory: `backend`
3. Variables: **ТЕ ЖЕ** что и для Backend API
4. Settings → Start Command:
   ```
   celery -A app.tasks.scheduled_tasks beat --loglevel=info
   ```

- [ ] Celery Beat развернут
- [ ] Статус "Active"
- [ ] В логах видно: "Scheduler: Sending due task..."

---

### Шаг 7: Vercel - Обновление ⏱️ 5 минут

1. Откройте: https://vercel.com
2. Найдите проект "test-1"
3. Settings → Environment Variables
4. Добавьте или обновите:
   ```
   Name: VITE_API_URL
   Value: <URL из Шага 4>
   ```
5. Deployments → Last deployment → Redeploy

- [ ] VITE_API_URL обновлен
- [ ] Redeploy завершен
- [ ] Frontend перезагружен

---

## ✅ Финальная проверка

### Проверка Backend

Откройте в браузере:
```
https://your-backend.railway.app/health
```
- [ ] Показывает: `{"status":"healthy"}`

```
https://your-backend.railway.app/api/v1/ideas/
```
- [ ] Показывает 10 идей на русском

### Проверка Frontend

Откройте:
```
https://test-1-iota-sepia.vercel.app
```

- [ ] Показывает 10 идей на главной
- [ ] Все тексты на русском
- [ ] Детальные страницы открываются
- [ ] Метрики отображаются корректно

### Проверка Автоматизации

Railway → Celery Beat → Deployments → View Logs

- [ ] Видно: "celery beat v5.3.6 is starting"
- [ ] Видно: "Scheduler: Sending due task discover-trends-daily"
- [ ] Нет ошибок в логах

---

## 🎉 Всё готово!

Если все чекбоксы отмечены, ваша система:

✅ Развернута на production
✅ Автоматически обновляется каждый день в 9:00 UTC
✅ Доступна по постоянной ссылке
✅ Работает без вашего участия

**Ваша ссылка:** https://test-1-iota-sepia.vercel.app

**Что будет происходить:**
- 🕘 9:00 UTC - Поиск 10 новых трендов
- 🕤 9:30 UTC - Генерация 5+ новых идей
- 📊 Пользователи видят новые идеи автоматически

**Стоимость:** ~$11-22 в месяц

---

## 🆘 Если что-то не работает

Читайте: [RAILWAY_DEPLOY_STEPS.md](RAILWAY_DEPLOY_STEPS.md) - там есть Troubleshooting раздел.
