#!/bin/bash

echo "🚀 Quick Deploy Script"
echo "====================="
echo ""

# Проверка что мы в правильной директории
if [ ! -f "DEPLOY_GUIDE.md" ]; then
    echo "❌ Error: Запустите этот скрипт из корня проекта"
    exit 1
fi

# Спрашиваем пользователя хочет ли он продолжить
echo "Этот скрипт подготовит проект для развертывания."
echo ""
read -p "Хотите продолжить? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Отменено пользователем"
    exit 1
fi

# Проверка Git
echo ""
echo "📦 Шаг 1: Git Push"
echo "=================="

if [ ! -d ".git" ]; then
    echo "Инициализация Git репозитория..."
    git init
    echo "✅ Git инициализирован"
fi

# Добавляем все файлы
echo "Добавление файлов..."
git add .

# Коммит
echo "Создание коммита..."
git commit -m "Deploy: AI Business Portfolio Manager with auto-updates at 9AM" || echo "Нет изменений для коммита"

# Проверка remote
if ! git remote | grep -q "origin"; then
    echo ""
    echo "⚠️  Не настроен remote репозиторий"
    echo ""
    echo "Создайте репозиторий на GitHub и выполните:"
    echo "git remote add origin https://github.com/your-username/your-repo.git"
    echo "git branch -M main"
    echo "git push -u origin main"
    echo ""
else
    echo "Pushing to GitHub..."
    git push || echo "⚠️  Возможно нужно выполнить: git push -u origin main"
    echo "✅ Код загружен на GitHub"
fi

echo ""
echo "🎉 Готово!"
echo ""
echo "📖 Следующие шаги:"
echo "1. Прочитайте DEPLOY_GUIDE.md"
echo "2. Разверните backend на Railway: https://railway.app"
echo "3. Разверните frontend на Vercel: https://vercel.com"
echo ""
echo "Ваша production ссылка будет: https://test-1-iota-sepia.vercel.app"
echo ""
