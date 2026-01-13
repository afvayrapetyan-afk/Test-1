#!/bin/bash

echo "🚀 БЫСТРЫЙ ДЕПЛОЙ (открываю все ссылки)"
echo "========================================"
echo ""

# 1. Копируем переменные для Railway (без API ключа - возьмите из .env)
echo "CORS_ORIGINS=https://test-1-iota-sepia.vercel.app
PORT=8000" | pbcopy

echo "✅ Базовые переменные скопированы!"
echo "⚠️  OPENAI_API_KEY возьмите из backend/.env"
echo ""

# 2. Открываем GitHub
echo "📂 Открываю GitHub..."
sleep 1
open "https://github.com/afvayrapetyan-afk/Test-1"

# 3. Открываем Railway
echo "🚂 Открываю Railway..."
sleep 2
open "https://railway.app/new"

# 4. Открываем Vercel
echo "▲ Открываю Vercel..."
sleep 2
open "https://vercel.com"

# 5. Открываем чеклист
echo "📋 Открываю чеклист..."
sleep 1
open "DEPLOY_CHECKLIST.md"

echo ""
echo "🎯 ЧТО ДЕЛАТЬ ДАЛЬШЕ:"
echo ""
echo "1️⃣ В GitHub (первая вкладка):"
echo "   - Sync/Push изменения"
echo ""
echo "2️⃣ В Railway (вторая вкладка):"
echo "   - New Project → Deploy from GitHub"
echo "   - Выберите: Test-1"
echo "   - Создайте 5 сервисов (смотри чеклист)"
echo "   - Вставьте переменные (Cmd+V - уже скопированы!)"
echo ""
echo "3️⃣ В Vercel (третья вкладка):"
echo "   - Найдите проект test-1"
echo "   - Settings → Environment Variables"
echo "   - VITE_API_URL=<URL из Railway>"
echo "   - Redeploy"
echo ""
echo "4️⃣ Следуйте DEPLOY_CHECKLIST.md (открыт в редакторе)"
echo ""
echo "⏱️ Время: ~25 минут"
echo ""
