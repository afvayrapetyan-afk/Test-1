# Настройка Reddit API для Scraping

Для использования Reddit scraper необходимо создать Reddit API приложение и получить credentials.

## Шаг 1: Создать Reddit аккаунт

Если у вас нет аккаунта Reddit:
1. Перейти на https://www.reddit.com/register/
2. Создать аккаунт (запомните username и password)

## Шаг 2: Создать Reddit API приложение

1. Войти в Reddit аккаунт
2. Перейти на https://www.reddit.com/prefs/apps
3. Прокрутить вниз и нажать **"create another app..."** или **"create app"**

4. Заполнить форму:
   - **name**: `Business Portfolio Bot` (любое имя)
   - **App type**: Выбрать **"script"** (для personal use scripts)
   - **description**: `AI Business Portfolio Manager - Trend Discovery` (опционально)
   - **about url**: оставить пустым
   - **redirect uri**: `http://localhost:8080` (обязательно)

5. Нажать **"create app"**

## Шаг 3: Скопировать credentials

После создания приложения вы увидите:

```
[название вашего приложения]
personal use script

[CLIENT_ID - 14 символов под названием]
[...]
secret     [CLIENT_SECRET - длинная строка]
```

**Пример:**
```
Business Portfolio Bot
personal use script

AbC123XyZ4567     ← Это CLIENT_ID
secret     1234567890abcdefghijklmnopqrstuvwxyz     ← Это CLIENT_SECRET
```

## Шаг 4: Добавить credentials в .env

Откройте файл `.env` (скопируйте из `.env.example` если нет) и заполните:

```bash
# Reddit API
REDDIT_CLIENT_ID=AbC123XyZ4567                      # 14 символов под названием приложения
REDDIT_CLIENT_SECRET=1234567890abcdefghijklmnopqrst # Длинная строка после "secret"
REDDIT_USER_AGENT=BusinessPortfolioBot/1.0          # Можно оставить как есть
REDDIT_USERNAME=your_reddit_username                # Ваш Reddit username
REDDIT_PASSWORD=your_reddit_password                # Ваш Reddit password
```

## Шаг 5: Проверить настройку

Запустите тест:

```bash
cd backend
python -c "
from app.scrapers.reddit_scraper import RedditScraper
scraper = RedditScraper()
print('✅ Reddit scraper initialized successfully!')
"
```

Если видите `✅ Reddit scraper initialized successfully!` - всё настроено правильно!

## Использование

После настройки Reddit scraper будет автоматически использоваться в TrendScoutAgent:

```python
# Через API
POST /api/v1/agents/run
{
  "agent_type": "trend_scout",
  "params": {
    "sources": ["reddit"],
    "subreddits": ["SideProject", "startups", "Entrepreneur"],
    "limit": 50,
    "sort": "hot",
    "time_filter": "week"
  }
}
```

## Параметры scraping

**subreddits**: Список subreddits для scraping
- Рекомендуемые: `SideProject`, `startups`, `Entrepreneur`, `SaaS`, `EntrepreneurRideAlong`
- Можно добавить любые другие

**sort**: Метод сортировки
- `hot` - популярные сейчас (default)
- `top` - лучшие за период
- `new` - новые посты
- `rising` - набирающие популярность

**time_filter**: Временной фильтр (для `sort=top`)
- `hour` - за последний час
- `day` - за сутки
- `week` - за неделю (default)
- `month` - за месяц
- `year` - за год
- `all` - за всё время

**limit**: Количество постов для scraping (default: 100)

## Troubleshooting

### Ошибка: "Reddit initialization failed"

**Причина**: Неправильные credentials

**Решение**:
1. Проверьте CLIENT_ID (должен быть 14 символов)
2. Проверьте CLIENT_SECRET (длинная строка)
3. Проверьте USERNAME и PASSWORD

### Ошибка: "403 Forbidden"

**Причина**: Reddit блокирует request

**Решение**:
1. Проверьте USER_AGENT - должен быть уникальным
2. Добавьте задержку между requests (Reddit rate limiting)

### Fallback на LLM generation

Если Reddit scraper недоступен или не настроен, система автоматически переключится на LLM-generated trends (mock данные).

В логах вы увидите:
```
WARNING Reddit scraper not available, falling back to LLM generation
```

Это нормально для тестирования, но для production рекомендуется настроить Reddit API.

## Rate Limits

Reddit API имеет rate limits:
- **60 requests per minute** для OAuth2
- Рекомендуется scraping не чаще **1 раз в час**

TrendScoutAgent автоматически распределяет requests между subreddits.

## Privacy & Terms

- Reddit API Terms: https://www.reddit.com/wiki/api-terms
- Reddit User Agreement: https://www.redditinc.com/policies/user-agreement
- Используйте scraper только для личных/исследовательских целей
- Не создавайте spam и не нарушайте правила Reddit
