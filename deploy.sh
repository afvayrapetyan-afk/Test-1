#!/bin/bash

# 🚀 Скрипт автоматического деплоя AI Business Portfolio Manager
# Автор: Claude Sonnet 4.5

set -e  # Выход при ошибке

echo "🚀 AI Business Portfolio Manager - Автоматический деплой"
echo "=========================================================="
echo ""

# Проверка, что мы в правильной директории
if [ ! -f "package.json" ] && [ ! -d "frontend" ]; then
    echo "❌ Ошибка: Запустите скрипт из корня проекта!"
    exit 1
fi

# Шаг 1: Проверка git конфигурации
echo "📋 Шаг 1: Проверка git конфигурации..."
if ! git config user.name > /dev/null 2>&1; then
    echo "⚙️  Настройка git username..."
    read -p "Введите ваше имя для git: " git_name
    git config --global user.name "$git_name"
fi

if ! git config user.email > /dev/null 2>&1; then
    echo "⚙️  Настройка git email..."
    read -p "Введите ваш email для git: " git_email
    git config --global user.email "$git_email"
fi

echo "✅ Git конфигурация готова"
echo "   Имя: $(git config user.name)"
echo "   Email: $(git config user.email)"
echo ""

# Шаг 2: Проверка коммита
echo "📋 Шаг 2: Проверка git commit..."
if ! git log -1 > /dev/null 2>&1; then
    echo "⚙️  Создание первого коммита..."
    git add .
    git commit -m "Initial commit: AI Business Portfolio Manager

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
    echo "✅ Коммит создан"
else
    echo "✅ Коммит уже существует"
fi
echo ""

# Шаг 3: Создание GitHub репозитория
echo "📋 Шаг 3: Подключение к GitHub..."
echo ""
echo "ВАЖНО: Вам нужно создать GitHub репозиторий!"
echo ""
echo "Откройте в браузере: https://github.com/new"
echo ""
echo "Настройки:"
echo "  - Repository name: ai-business-portfolio-manager"
echo "  - Visibility: Public"
echo "  - НЕ добавляйте README, .gitignore, license"
echo ""
read -p "Нажмите Enter, когда создадите репозиторий на GitHub..."
echo ""

# Запрос GitHub username
read -p "Введите ваш GitHub username: " github_username

if [ -z "$github_username" ]; then
    echo "❌ Ошибка: GitHub username не может быть пустым!"
    exit 1
fi

REPO_URL="https://github.com/$github_username/ai-business-portfolio-manager.git"

echo ""
echo "📦 Подключение к репозиторию: $REPO_URL"

# Проверка, есть ли уже remote origin
if git remote | grep -q "^origin$"; then
    echo "⚠️  Remote 'origin' уже существует, обновляю..."
    git remote remove origin
fi

git remote add origin "$REPO_URL"
echo "✅ Remote добавлен"
echo ""

# Шаг 4: Push на GitHub
echo "📋 Шаг 4: Отправка кода на GitHub..."
echo "⚙️  Выполняю git push..."

if git push -u origin main; then
    echo "✅ Код успешно отправлен на GitHub!"
else
    echo ""
    echo "❌ Ошибка при push на GitHub!"
    echo ""
    echo "Возможные причины:"
    echo "1. Неверный username репозитория"
    echo "2. Требуется авторизация"
    echo ""
    echo "Для авторизации используйте Personal Access Token:"
    echo "1. Создайте токен: https://github.com/settings/tokens/new"
    echo "2. Выберите права: repo (full control)"
    echo "3. Используйте токен вместо пароля"
    echo ""
    echo "Или выполните вручную:"
    echo "  git push -u origin main"
    exit 1
fi
echo ""

# Шаг 5: Деплой на Vercel
echo "📋 Шаг 5: Деплой на Vercel..."
echo ""
echo "Теперь нужно задеплоить проект на Vercel:"
echo ""
echo "Вариант 1 (Рекомендуется): Через веб-интерфейс"
echo "  1. Откройте: https://vercel.com/signup"
echo "  2. Зарегистрируйтесь через GitHub"
echo "  3. Нажмите 'Add New... → Project'"
echo "  4. Выберите репозиторий: ai-business-portfolio-manager"
echo "  5. Настройки:"
echo "     - Build Command: cd frontend && npm install && npm run build"
echo "     - Output Directory: frontend/dist"
echo "  6. Нажмите 'Deploy'"
echo ""
echo "Вариант 2: Через Vercel CLI"
echo "  npm install -g vercel"
echo "  vercel"
echo ""

# Проверка установлен ли vercel CLI
if command -v vercel &> /dev/null; then
    echo "✅ Vercel CLI установлен"
    read -p "Хотите запустить деплой сейчас? (y/n): " deploy_now

    if [ "$deploy_now" = "y" ] || [ "$deploy_now" = "Y" ]; then
        echo "⚙️  Запускаю Vercel деплой..."
        vercel --yes
    fi
else
    echo "ℹ️  Vercel CLI не установлен"
    echo "   Используйте веб-интерфейс или установите:"
    echo "   npm install -g vercel"
fi

echo ""
echo "=========================================================="
echo "✨ Деплой настроен!"
echo ""
echo "📝 Что дальше:"
echo "  1. Если еще не сделали - задеплойте на Vercel"
echo "  2. Получите публичную ссылку (будет вида: https://...vercel.app)"
echo "  3. Делитесь ссылкой с другими!"
echo ""
echo "📖 Подробная инструкция: DEPLOYMENT.md"
echo "🔗 Ваш репозиторий: https://github.com/$github_username/ai-business-portfolio-manager"
echo ""
echo "=========================================================="
