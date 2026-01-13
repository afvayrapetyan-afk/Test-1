#!/bin/bash

echo "🚀 Auto Deploy Script - AI Business Portfolio Manager"
echo "======================================================"
echo ""

# Цвета для вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Этот скрипт задеплоит ваш проект на Vercel${NC}"
echo ""

# Переходим в директорию frontend
cd "$(dirname "$0")/frontend"

# Проверяем залогинен ли пользователь
echo -e "${YELLOW}🔐 Проверяем авторизацию Vercel...${NC}"
if ! vercel whoami > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Вы не залогинены в Vercel${NC}"
    echo ""
    echo -e "${BLUE}Сейчас откроется браузер для авторизации...${NC}"
    echo "После авторизации вернитесь в терминал и нажмите Enter"
    echo ""

    # Запускаем логин
    vercel login

    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Ошибка авторизации${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✅ Авторизация успешна!${NC}"
echo ""

# Показываем кто залогинен
VERCEL_USER=$(vercel whoami)
echo -e "${GREEN}👤 Залогинен как: $VERCEL_USER${NC}"
echo ""

# Деплоим на production
echo -e "${BLUE}🚀 Деплоим на production...${NC}"
echo ""

# Используем vercel --prod для деплоя
vercel --prod --yes

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ ДЕПЛОЙ УСПЕШЕН!${NC}"
    echo ""
    echo -e "${GREEN}🎉 Ваше приложение доступно на: https://test-1-iota-sepia.vercel.app${NC}"
    echo ""
    echo -e "${YELLOW}📝 Следующие шаги:${NC}"
    echo "1. Откройте https://test-1-iota-sepia.vercel.app"
    echo "2. Добавьте VITE_API_URL в Vercel Dashboard → Settings → Environment Variables"
    echo "3. Значение: URL вашего Railway backend"
    echo ""
else
    echo -e "${RED}❌ Ошибка при деплое${NC}"
    echo "Проверьте логи выше"
    exit 1
fi
