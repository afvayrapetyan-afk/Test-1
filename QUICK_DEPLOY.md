# ⚡ Быстрый деплой (3 простых шага)

## Шаг 1: Создайте GitHub репозиторий (2 минуты)

1. Откройте: **https://github.com/new**
2. Название: `ai-business-portfolio-manager`
3. Выберите: **Public**
4. Нажмите: **Create repository**

## Шаг 2: Отправьте код на GitHub (1 минута)

Скопируйте и выполните в терминале (замените YOUR_USERNAME):

```bash
cd "/Users/vardanajrapetan/Project 1"
git remote add origin https://github.com/YOUR_USERNAME/ai-business-portfolio-manager.git
git push -u origin main
```

**Пример** (замените `vardanajrapetan` на ваш username):
```bash
git remote add origin https://github.com/vardanajrapetan/ai-business-portfolio-manager.git
git push -u origin main
```

## Шаг 3: Деплой на Vercel (2 минуты)

1. Откройте: **https://vercel.com/signup**
2. Войдите через **GitHub**
3. Нажмите: **Add New... → Project**
4. Выберите: `ai-business-portfolio-manager`
5. Нажмите: **Deploy**

**Готово!** Через 2-3 минуты получите ссылку вида:
```
https://ai-business-portfolio-manager.vercel.app
```

---

## 🎁 Бонус: Тестовые учетные данные

Для демонстрации используйте:

**Пользователь:**
- Email: `vardana@example.com`
- Password: `demo123`

**Админ (AI Agents):**
- URL: `/login`
- Username: `Админ`
- Password: `987654`

---

## ❓ Проблемы?

### Ошибка "remote origin already exists"
```bash
git remote remove origin
# Потом повторите команду git remote add...
```

### Требует авторизацию при git push
Создайте Personal Access Token:
1. https://github.com/settings/tokens/new
2. Выберите права: `repo`
3. Используйте токен вместо пароля

---

📖 Подробная инструкция: [DEPLOYMENT.md](DEPLOYMENT.md)
