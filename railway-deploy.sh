#!/bin/bash

# Цвета
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

clear
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║           🚀 АВТОМАТИЧЕСКИЙ ДЕПЛОЙ НА RAILWAY              ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Открываем Railway
echo -e "${BLUE}📂 Открываю Railway...${NC}"
sleep 1
open "https://railway.app/new"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${YELLOW}📋 ШАГ 1: СОЗДАЙТЕ ПРОЕКТ${NC}"
echo ""
echo "В открывшейся вкладке Railway:"
echo "  1. Нажмите 'New Project'"
echo "  2. Выберите 'Add PostgreSQL'"
echo ""
read -p "✅ PostgreSQL создан? Нажмите Enter..."

echo ""
echo "Скопируйте DATABASE_URL:"
echo "  Railway → PostgreSQL → Variables → DATABASE_URL → Copy"
echo ""
read -p "📋 Вставьте DATABASE_URL: " DATABASE_URL

if [ -z "$DATABASE_URL" ]; then
    echo -e "${YELLOW}❌ DATABASE_URL пустой, попробуйте еще раз${NC}"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${YELLOW}📋 ШАГ 2: ДОБАВЬТЕ REDIS${NC}"
echo ""
echo "В том же проекте Railway:"
echo "  1. Нажмите '+ New'"
echo "  2. Выберите 'Add Redis'"
echo ""
read -p "✅ Redis создан? Нажмите Enter..."

echo ""
echo "Скопируйте REDIS_URL:"
echo "  Railway → Redis → Variables → REDIS_URL → Copy"
echo ""
read -p "📋 Вставьте REDIS_URL: " REDIS_URL

if [ -z "$REDIS_URL" ]; then
    echo -e "${YELLOW}❌ REDIS_URL пустой, попробуйте еще раз${NC}"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${YELLOW}📋 ШАГ 3: BACKEND API${NC}"
echo ""
echo "В Railway:"
echo "  1. '+ New' → 'GitHub Repo' → выберите 'Test-1'"
echo "  2. Settings → Root Directory: backend"
echo "  3. Variables → Add Variable (добавляйте по одной):"
echo ""

# Читаем OpenAI key из .env
OPENAI_KEY=$(grep OPENAI_API_KEY backend/.env | cut -d '=' -f2)

echo -e "${GREEN}Variables для копирования:${NC}"
echo ""
echo "OPENAI_API_KEY"
echo "$OPENAI_KEY"
echo ""
echo "DATABASE_URL"
echo "$DATABASE_URL"
echo ""
echo "REDIS_URL"
echo "$REDIS_URL"
echo ""
echo "CORS_ORIGINS"
echo "https://test-1-iota-sepia.vercel.app"
echo ""
echo "PORT"
echo "8000"
echo ""

read -p "✅ Все переменные добавлены? Нажмите Enter..."

echo ""
echo "Включите публичный доступ:"
echo "  Settings → Networking → Generate Domain"
echo ""
read -p "✅ Domain создан? Нажмите Enter..."

echo ""
read -p "📋 Вставьте Backend URL (https://...railway.app): " BACKEND_URL

if [ -z "$BACKEND_URL" ]; then
    echo -e "${YELLOW}❌ Backend URL пустой, попробуйте еще раз${NC}"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${YELLOW}📋 ШАГ 4: CELERY WORKER${NC}"
echo ""
echo "В Railway:"
echo "  1. '+ New' → 'GitHub Repo' → 'Test-1'"
echo "  2. Settings → Root Directory: backend"
echo "  3. Variables → Добавьте ТЕ ЖЕ переменные что выше"
echo "  4. Settings → Start Command:"
echo "     celery -A app.tasks.scheduled_tasks worker --loglevel=info"
echo ""
read -p "✅ Celery Worker создан? Нажмите Enter..."

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${YELLOW}📋 ШАГ 5: CELERY BEAT ⭐ (АВТОМАТИЗАЦИЯ!)${NC}"
echo ""
echo "В Railway:"
echo "  1. '+ New' → 'GitHub Repo' → 'Test-1'"
echo "  2. Settings → Root Directory: backend"
echo "  3. Variables → Добавьте ТЕ ЖЕ переменные"
echo "  4. Settings → Start Command:"
echo "     celery -A app.tasks.scheduled_tasks beat --loglevel=info"
echo ""
read -p "✅ Celery Beat создан? Нажмите Enter..."

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${YELLOW}📋 ШАГ 6: ОБНОВЛЕНИЕ VERCEL${NC}"
echo ""
echo "Открываю Vercel..."
sleep 1
open "https://vercel.com/dashboard"

echo ""
echo "В Vercel:"
echo "  1. Найдите проект 'test-1'"
echo "  2. Settings → Environment Variables"
echo "  3. VITE_API_URL = $BACKEND_URL"
echo "  4. Deployments → Redeploy"
echo ""
read -p "✅ Vercel обновлен? Нажмите Enter..."

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}🎉 ДЕПЛОЙ ЗАВЕРШЕН!${NC}"
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                     ✅ ВСЁ ГОТОВО!                         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Ваши ссылки:"
echo "  🌐 Frontend: https://test-1-iota-sepia.vercel.app"
echo "  🔧 Backend:  $BACKEND_URL"
echo ""
echo "Автоматизация:"
echo "  🕘 9:00 UTC - Поиск 10 трендов"
echo "  🕤 9:30 UTC - Генерация 5+ идей"
echo ""
echo "Проверка:"
echo "  Backend:  $BACKEND_URL/health"
echo "  Frontend: https://test-1-iota-sepia.vercel.app"
echo ""

# Открываем для проверки
sleep 2
open "$BACKEND_URL/health"
sleep 1
open "https://test-1-iota-sepia.vercel.app"

echo -e "${GREEN}✅ Страницы открыты для проверки!${NC}"
echo ""
