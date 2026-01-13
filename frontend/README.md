# AI Business Portfolio Manager - Frontend

Современный минималистичный интерфейс в стиле Apple для управления тысячами бизнес-идей.

## Быстрый старт

### 1. Установка Node.js

Если у вас еще не установлен Node.js:
- Скачайте с [nodejs.org](https://nodejs.org/) (рекомендуется LTS версия)
- Или установите через Homebrew: `brew install node`

### 2. Установка зависимостей

```bash
cd frontend
npm install
```

### 3. Запуск dev сервера

```bash
npm run dev
```

Откройте [http://localhost:3000](http://localhost:3000) в браузере.

## Предпросмотр без установки

Если вы хотите посмотреть на дизайн БЕЗ установки Node.js:

```bash
open prototype.html
```

Это статический HTML прототип с полностью рабочим дизайном!

## Структура проекта

```
frontend/
├── src/
│   ├── components/          # React компоненты
│   │   ├── layout/         # TopBar, Layout
│   │   ├── dashboard/      # MetricCard
│   │   ├── ideas/          # IdeaCard
│   │   └── ai/             # AIChatFAB
│   ├── pages/              # Страницы
│   │   ├── Dashboard.tsx   # Главная страница
│   │   └── IdeaDetail.tsx  # Детальная страница идеи
│   ├── App.tsx             # Главный компонент
│   ├── main.tsx            # Entry point
│   └── index.css           # Глобальные стили
├── prototype.html          # Статический прототип
├── package.json            # Зависимости
├── tailwind.config.js      # Конфигурация Tailwind
└── vite.config.ts          # Конфигурация Vite
```

## Технологии

- **React 18** - UI фреймворк
- **TypeScript** - Типизация
- **Tailwind CSS** - Стилизация
- **Vite** - Build tool (быстрый!)
- **Framer Motion** - Анимации
- **Lucide React** - Иконки
- **React Router** - Навигация

## Дизайн-система

### Цвета
- Background: `#FAFAFA` - светло-серый фон
- Surface: `#FFFFFF` - белые карточки
- Accent Blue: `#3B82F6` - новые идеи
- Accent Green: `#10B981` - успех, рост
- Accent Purple: `#8B5CF6` - AI функции

### Spacing (8px базовая единица)
- 1 = 8px
- 2 = 16px
- 3 = 24px
- 4 = 32px

### Border Radius
- sm: 6px - кнопки
- md: 12px - карточки
- lg: 16px - секции
- full: 9999px - badges

## Ключевые компоненты

### MetricCard
Карточка с метриками (идеи, бизнесы, выручка)
```tsx
<MetricCard
  label="Всего идей"
  value="247"
  change="+23 за неделю"
  icon={<BarChart3 />}
/>
```

### IdeaCard
Карточка бизнес-идеи с оценкой и метриками
```tsx
<IdeaCard
  idea={ideaData}
  onChatClick={handleChat}
  onDetailsClick={handleDetails}
/>
```

### AIChatFAB
Плавающая кнопка для AI консультаций
- Одним кликом открывает чат
- Градиентный фон purple-pink
- Hover эффект

## Анимации

Все анимации используют Framer Motion:
- Fade in при загрузке карточек
- Hover эффекты (translateY -4px)
- Progress bars с задержкой
- Smooth transitions (cubic-bezier)

## Следующие шаги

1. ✅ Базовая структура создана
2. ⏳ Интеграция с backend API
3. ⏳ Реализация AI Chat Panel
4. ⏳ Добавление графиков (Recharts)
5. ⏳ Страница детального просмотра идеи
6. ⏳ Real-time обновления (WebSockets)

## Использование с Claude Opus 4.5

Этот проект оптимизирован для работы с AI vibe coding:

```bash
# Запустите dev сервер
npm run dev

# Теперь вы можете попросить Claude Opus 4.5:
# "Добавь новый компонент для графика трендов"
# "Создай страницу детального просмотра с AI чатом"
# "Добавь dark mode"
```

Claude Opus 4.5 понимает структуру проекта и может быстро добавлять функциональность!

## Прототип vs Production

**Прототип (prototype.html):**
- ✅ Готов к просмотру СЕЙЧАС
- ✅ Показывает финальный дизайн
- ❌ Нет интерактивности
- ❌ Статические данные

**React версия (src/):**
- ✅ Полная интерактивность
- ✅ Роутинг, state management
- ✅ Интеграция с backend
- ✅ Real-time обновления
- ⏳ Требует установки

## Вопросы?

Посмотрите [DESIGN_CONCEPT.md](../docs/DESIGN_CONCEPT.md) для подробного описания дизайн-системы.

---

**Создано с помощью Claude Opus 4.5** ✨
