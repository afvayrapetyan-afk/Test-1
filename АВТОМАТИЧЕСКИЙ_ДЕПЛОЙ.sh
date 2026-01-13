#!/bin/bash

echo "🚀 АВТОМАТИЧЕСКИЙ ДЕПЛОЙ"
echo "======================="
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Проверка что мы в правильной директории
if [ ! -f "DEPLOY_CHECKLIST.md" ]; then
    echo -e "${RED}❌ Ошибка: Запустите из корня проекта${NC}"
    exit 1
fi

echo "📋 Шаг 1: Push на GitHub"
echo "========================"
echo ""
echo -e "${YELLOW}⚠️  Сейчас откроется GitHub Desktop для push${NC}"
echo "   Если у вас нет GitHub Desktop, установите:"
echo "   https://desktop.github.com/"
echo ""
read -p "Нажмите Enter когда будете готовы..."

# Пробуем разные способы открыть GitHub Desktop
if command -v github &> /dev/null; then
    github .
elif [ -d "/Applications/GitHub Desktop.app" ]; then
    open -a "GitHub Desktop" .
else
    echo -e "${YELLOW}Открываю GitHub в браузере...${NC}"
    open "https://github.com/afvayrapetyan-afk/Test-1"
    echo ""
    echo "Вручную push изменения:"
    echo "1. Откройте GitHub Desktop"
    echo "2. Commit изменения"
    echo "3. Push origin/main"
fi

echo ""
read -p "✅ Push завершен? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}Деплой отменен${NC}"
    exit 1
fi

echo ""
echo "📋 Шаг 2: Railway Deployment"
echo "============================"
echo ""
echo -e "${GREEN}✅ Код загружен на GitHub!${NC}"
echo ""
echo "Теперь откройте Railway в браузере:"
echo ""
open "https://railway.app/new"

echo -e "${YELLOW}📝 ДОБАВЬТЕ ЭТИ ПЕРЕМЕННЫЕ В RAILWAY:${NC}"
echo ""
echo "OPENAI_API_KEY=<ваш_ключ_из_.env>"
echo "CORS_ORIGINS=https://test-1-iota-sepia.vercel.app"
echo "PORT=8000"
echo ""
echo "(DATABASE_URL и REDIS_URL создадутся автоматически)"
echo ""
echo -e "${YELLOW}⚠️  Возьмите OPENAI_API_KEY из файла backend/.env${NC}"
echo ""

# Копируем в буфер обмена (без API ключа)
echo "CORS_ORIGINS=https://test-1-iota-sepia.vercel.app
PORT=8000" | pbcopy

echo -e "${GREEN}✅ Переменные скопированы в буфер обмена!${NC}"
echo ""

echo "Следуйте инструкциям в браузере Railway:"
echo "1. New Project → Deploy from GitHub"
echo "2. Выберите: afvayrapetyan-afk/Test-1"
echo "3. Создайте 5 сервисов (следуйте DEPLOY_CHECKLIST.md)"
echo ""

read -p "✅ Railway развернут? Введите URL backend: " BACKEND_URL

if [ -z "$BACKEND_URL" ]; then
    echo -e "${RED}❌ URL не введен${NC}"
    exit 1
fi

echo ""
echo "📋 Шаг 3: Vercel Deployment"
echo "==========================="
echo ""
echo "Открываю Vercel..."
open "https://vercel.com"

echo ""
echo -e "${YELLOW}📝 Добавьте в Vercel Environment Variables:${NC}"
echo ""
echo "VITE_API_URL=$BACKEND_URL"
echo ""

# Копируем в буфер
echo "VITE_API_URL=$BACKEND_URL" | pbcopy
echo -e "${GREEN}✅ Переменная скопирована в буфер обмена!${NC}"
echo ""

echo "В Vercel:"
echo "1. Найдите проект 'test-1'"
echo "2. Settings → Environment Variables"
echo "3. Вставьте: VITE_API_URL (Cmd+V)"
echo "4. Deployments → Redeploy"
echo ""

read -p "✅ Vercel обновлен? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🎉 ДЕПЛОЙ ЗАВЕРШЕН!"
    echo "=================="
    echo ""
    echo -e "${GREEN}✅ Ваша система развернута!${NC}"
    echo ""
    echo "Ссылки:"
    echo "  Frontend: https://test-1-iota-sepia.vercel.app"
    echo "  Backend:  $BACKEND_URL"
    echo ""
    echo "Автоматизация:"
    echo "  🕘 9:00 UTC - Поиск 10 трендов"
    echo "  🕤 9:30 UTC - Генерация 5+ идей"
    echo ""
    echo "Проверьте работу:"
    open "https://test-1-iota-sepia.vercel.app"
fi

echo ""
echo "📖 Полная документация: DEPLOY_CHECKLIST.md"
echo ""
