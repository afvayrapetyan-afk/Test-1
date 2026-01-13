#!/bin/bash

echo "🚀 Создание постоянной публичной ссылки"
echo "======================================"
echo ""

# Копируем SSH ключ в буфер обмена
cat ~/.ssh/id_ed25519.pub | pbcopy
echo "✅ SSH ключ скопирован в буфер обмена"
echo ""

# Открываем страницу для добавления SSH ключа
echo "Шаг 1: Добавление SSH ключа на GitHub..."
echo "Открываю страницу в браузере..."
open "https://github.com/settings/ssh/new"

echo ""
echo "В браузере:"
echo "  1. Title: AI Portfolio Manager"
echo "  2. Key: нажмите Cmd+V (ключ уже скопирован)"
echo "  3. Нажмите 'Add SSH key'"
echo ""
read -p "Нажмите Enter когда добавите ключ..."

# Создаём GitHub репозиторий
echo ""
echo "Шаг 2: Создание GitHub репозитория..."
open "https://github.com/new"

echo ""
echo "В браузере:"
echo "  Repository name: ai-business-portfolio-manager"
echo "  Visibility: Public"
echo "  НЕ добавляйте README, .gitignore, license"
echo "  Нажмите 'Create repository'"
echo ""
read -p "Введите ваш GitHub username: " github_user

if [ -z "$github_user" ]; then
    echo "❌ Username не может быть пустым"
    exit 1
fi

# Настраиваем Git remote
cd "/Users/vardanajrapetan/Project 1"
git remote remove origin 2>/dev/null
git remote add origin "git@github.com:$github_user/ai-business-portfolio-manager.git"

echo ""
echo "Шаг 3: Отправка кода на GitHub..."
git push -u origin main

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Ошибка при push. Возможно нужно добавить SSH ключ."
    echo "Попробуйте вручную:"
    echo "  git push -u origin main"
    exit 1
fi

echo ""
echo "✅ Код успешно отправлен на GitHub!"
echo ""

# Открываем Vercel для деплоя
echo "Шаг 4: Деплой на Vercel..."
open "https://vercel.com/new"

echo ""
echo "В браузере Vercel:"
echo "  1. Войдите через GitHub"
echo "  2. Нажмите 'Import' напротив ai-business-portfolio-manager"
echo "  3. Нажмите 'Deploy'"
echo "  4. Скопируйте публичную ссылку!"
echo ""
echo "======================================"
echo "✅ Через 2-3 минуты получите постоянную ссылку!"
echo "======================================"
