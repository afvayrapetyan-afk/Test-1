# 🚀 Quick Start Guide - Пошаговый Запуск Проекта

## 📋 Текущий Статус

✅ OpenAI API key настроен
❌ Docker не установлен
❌ PostgreSQL не установлен
❌ Python зависимости не установлены

## 🎯 Варианты Запуска

### **Вариант 1: Быстрый Тест (без БД) ⚡**
Самый простой способ - тестируем AI agents без базы данных.

### **Вариант 2: С SQLite (локальная БД) 💾**
Используем SQLite вместо PostgreSQL - проще для старта.

### **Вариант 3: Полная Установка (Docker + PostgreSQL) 🐳**
Полноценный setup как задумано.

---

## ⚡ Вариант 1: Быстрый Тест (БЕЗ БД)

**Что работает:**
- ✅ TrendScoutAgent (LLM mode) - генерирует mock trends
- ✅ Базовое API
- ❌ Сохранение в БД не работает

**Шаги:**

```bash
# 1. Перейти в backend
cd "/Users/vardanajrapetan/Project 1/backend"

# 2. Установить зависимости
pip3 install fastapi uvicorn openai pydantic structlog python-multipart

# 3. Запустить (БЕЗ БД)
# Создадим временный запуск без БД
python3 -c "
from fastapi import FastAPI
app = FastAPI()

@app.get('/')
def root():
    return {'status': 'API работает!', 'message': 'Для полного функционала нужна БД'}

@app.get('/health')
def health():
    return {'status': 'healthy'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
" &

# 4. Открыть
open http://localhost:8000
```

**Результат:**
- API запущен на http://localhost:8000
- Можно протестировать endpoints
- Данные НЕ сохраняются

---

## 💾 Вариант 2: С SQLite (Рекомендуется для Старта)

**Что работает:**
- ✅ Все AI agents
- ✅ Сохранение в БД
- ✅ Полный CRUD
- ✅ Не нужен Docker

**Шаги:**

### 1. Установить Зависимости

```bash
cd "/Users/vardanajrapetan/Project 1/backend"

# Установить все зависимости
pip3 install -r requirements.txt
```

### 2. Изменить DATABASE_URL на SQLite

Откройте `.env` файл:
```bash
nano .env
```

Найдите строку:
```bash
DATABASE_URL=postgresql://admin:admin123@localhost:5432/business_portfolio
```

Замените на:
```bash
DATABASE_URL=sqlite:///./business_portfolio.db
```

Сохраните (Ctrl+O, Enter, Ctrl+X).

### 3. Запустить Backend

```bash
cd "/Users/vardanajrapetan/Project 1/backend"

# Запустить
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Открыть Swagger UI

```bash
open http://localhost:8000/docs
```

### 5. Протестировать AI Agent

В Swagger UI:

1. Найти `POST /api/v1/agents/run`
2. Нажать "Try it out"
3. Вставить:
```json
{
  "agent_type": "trend_scout",
  "params": {
    "sources": ["reddit"],
    "limit": 5
  }
}
```
4. Нажать "Execute"

**Результат:**
- Agent запустится
- Сгенерирует 5 trends через GPT-4o-mini
- Сохранит в SQLite БД
- Вернет execution_id

---

## 🐳 Вариант 3: Полная Установка (Docker + PostgreSQL)

**Требует:**
- Docker Desktop (нужно установить)
- Время: ~20 минут

### Шаг 1: Установить Docker Desktop

1. Скачать: https://www.docker.com/products/docker-desktop/
2. Установить Docker Desktop для Mac
3. Запустить Docker Desktop
4. Дождаться запуска (иконка в menu bar)

### Шаг 2: Проверить Docker

```bash
docker --version
# Должно вывести: Docker version XX.X.X
```

### Шаг 3: Запустить PostgreSQL

```bash
cd "/Users/vardanajrapetan/Project 1"

# Запустить PostgreSQL через Docker Compose
docker-compose up -d postgres

# Проверить статус
docker ps
```

### Шаг 4: Инициализировать БД

```bash
# Подождать 10 секунд пока PostgreSQL запустится
sleep 10

# Инициализировать схему
docker exec -i postgres psql -U admin -d business_portfolio < backend/db/init.sql
```

### Шаг 5: Установить Зависимости

```bash
cd backend
pip3 install -r requirements.txt
```

### Шаг 6: Запустить Backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Шаг 7: Открыть Swagger UI

```bash
open http://localhost:8000/docs
```

---

## 🧪 Тестирование

### Тест 1: Проверка API

```bash
curl http://localhost:8000/health
# Должно вернуть: {"status":"healthy"}
```

### Тест 2: Создать Trend

```bash
curl -X POST http://localhost:8000/api/v1/trends \
  -H "Content-Type: application/json" \
  -d '{
    "title": "AI Chatbot Platform",
    "description": "No-code platform for building AI chatbots",
    "source": "reddit",
    "category": "ai",
    "tags": ["ai", "chatbot", "no-code"]
  }'
```

### Тест 3: Запустить AI Agent

Через Swagger UI:
- POST /api/v1/agents/run
- Body:
```json
{
  "agent_type": "trend_scout",
  "params": {
    "sources": ["reddit"],
    "limit": 10
  }
}
```

### Тест 4: Получить Результаты

```bash
# Получить все trends
curl http://localhost:8000/api/v1/trends

# Получить executions
curl http://localhost:8000/api/v1/agents/executions
```

---

## ❓ Troubleshooting

### Проблема: "Module not found"

```bash
pip3 install -r requirements.txt
```

### Проблема: "Connection refused" (БД)

```bash
# Проверить PostgreSQL запущен
docker ps

# Перезапустить
docker-compose restart postgres
```

### Проблема: "OpenAI API error"

Проверить OPENAI_API_KEY в `.env`:
```bash
grep OPENAI_API_KEY .env
```

Должно быть:
```
OPENAI_API_KEY=sk-proj-gGzADdxHZ...
```

### Проблема: "Port 8000 already in use"

```bash
# Найти процесс
lsof -ti:8000

# Убить процесс
kill -9 $(lsof -ti:8000)
```

---

## 📝 Что Дальше?

После успешного запуска:

1. **Настроить Reddit API** (опционально)
   - См. `docs/REDDIT_SETUP.md`
   - Для реального scraping вместо mock данных

2. **Протестировать IdeaAnalyst**
   - Создать несколько trends
   - Запустить `idea_analyst` agent
   - Получить scored business ideas

3. **Изучить Swagger UI**
   - http://localhost:8000/docs
   - Все endpoints с документацией
   - Можно тестировать прямо в браузере

4. **Следующие фичи:**
   - Google Trends scraper
   - Celery для async execution
   - Frontend dashboard

---

## 💡 Рекомендация

**Для первого запуска:**
→ Используйте **Вариант 2 (SQLite)** - самый простой и быстрый
→ Работает всё кроме Redis/Qdrant (они не критичны для MVP)
→ Можно сразу тестировать AI agents

**Для production:**
→ Переходите на **Вариант 3 (Docker + PostgreSQL)**
→ Масштабируемо и надежно

---

## 🆘 Нужна Помощь?

Если что-то не работает:
1. Проверьте `.env` файл (API ключи)
2. Проверьте логи в терминале
3. Проверьте Python version: `python3 --version` (нужна 3.9+)
4. Напишите мне - помогу разобраться!
