# Research: Data Sources для Trend Discovery

**Дата**: 2026-01-13
**Статус**: ✅ Completed

## Summary

Изучили источники данных для автоматизированного поиска трендов с фокусом на международные и российские платформы. Определили API, методы доступа и best practices для мониторинга социальных сетей, поисковых систем и новостных агрегаторов.

---

## Международные Источники

### 1. Twitter/X API

**Возможности**:
- Real-time stream trending topics
- Search recent tweets (last 7 days)
- Trending hashtags по геолокации
- Engagement metrics (likes, retweets, replies)

**API Endpoints**:
```python
# Twitter API v2
import tweepy

client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Get trending topics
trends = client.get_place_trends(id=1)  # Worldwide

# Search recent tweets
tweets = client.search_recent_tweets(
    query="startup OR SaaS",
    max_results=100,
    tweet_fields=['created_at', 'public_metrics']
)
```

**Rate Limits**:
- Free tier: 500k tweets/month
- Basic: $100/mo для 1M tweets
- Pro: $5000/mo для 10M tweets

**Pros**: Высокая скорость трендов, большой охват
**Cons**: Дорого при масштабе, требует модерацию (много шума)

---

### 2. Reddit API (PRAW)

**Возможности**:
- Hot/Rising/Top posts по subreddits
- Comment analysis
- Cross-post tracking
- Award tracking (показатель качества)

**API Implementation**:
```python
import praw

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent="TrendScout/1.0"
)

# Monitor trending subreddits
for subreddit_name in ['entrepreneur', 'startups', 'SaaS']:
    subreddit = reddit.subreddit(subreddit_name)

    for post in subreddit.hot(limit=100):
        # Analyze engagement
        trend_score = post.score + post.num_comments * 2
```

**Rate Limits**:
- 60 requests/minute
- OAuth required

**Pros**: Высокое качество дискуссий, early signals
**Cons**: Меньший масштаб чем Twitter

---

### 3. Google Trends API (pytrends)

**Возможности**:
- Interest over time
- Related queries
- Rising queries (fast-growing)
- Geographic distribution

**Implementation**:
```python
from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)

# Build payload
pytrends.build_payload(
    kw_list=['AI agents', 'automation'],
    timeframe='now 7-d',
    geo='',  # Worldwide or 'US', 'RU'
)

# Get rising queries (best for trends)
rising = pytrends.related_queries()
interest_over_time = pytrends.interest_over_time()
```

**Rate Limits**:
- Unofficial API (через pytrends)
- ~1 request/second рекомендуется
- Rotate proxies для масштаба

**Pros**: Официальные данные Google, показывает macro trends
**Cons**: Неофициальный API, может блокировать

---

### 4. Product Hunt API

**Возможности**:
- Daily featured products
- Upvote tracking
- Category trends
- Maker profiles

**Implementation**:
```python
import requests

headers = {
    'Authorization': f'Bearer {PRODUCT_HUNT_TOKEN}'
}

# Get today's featured products
response = requests.get(
    'https://api.producthunt.com/v2/api/graphql',
    headers=headers,
    json={
        'query': '''
        {
          posts(order: VOTES, postedAfter: "2026-01-13") {
            edges {
              node {
                name
                tagline
                votesCount
                topics { edges { node { name } } }
              }
            }
          }
        }
        '''
    }
)
```

**Rate Limits**:
- 500 requests/day (free)
- GraphQL API

**Pros**: Качественные startup идеи, high signal
**Cons**: Ограниченный scope (только tech products)

---

## Российские Источники

### 1. Яндекс Wordstat API

**Возможности**:
- Статистика поисковых запросов
- Динамика спроса (trends over time)
- Сезонность запросов
- Региональная разбивка
- Конкурентный анализ

**Официальное API** (бета с 2025):
```python
import requests

# Яндекс Wordstat API (официальный)
API_KEY = "your_yandex_api_key"

response = requests.post(
    'https://api.direct.yandex.com/json/v5/keywordsresearch',
    headers={
        'Authorization': f'Bearer {API_KEY}',
        'Accept-Language': 'ru'
    },
    json={
        'method': 'get',
        'params': {
            'Keywords': ['стартап', 'AI агенты', 'автоматизация'],
            'RegionIds': [225],  # Россия
        }
    }
)

# Получаем frequency, competition, trends
data = response.json()
```

**Альтернатива - Парсинг** (через сторонние сервисы):
- arsenkin.ru/tools/wordstat/ (парсинг онлайн)
- Используя Selenium для автоматизации

**Rate Limits**:
- API: зависит от тарифа Яндекс.Директ
- Parsing: ~10-20 запросов/минуту (risk of ban)

**Применение**:
- Оценка спроса на товары/услуги
- Выявление новых трендов
- Планирование продаж с учётом сезонности
- Конкурентный анализ

**Pros**: Официальные данные Яндекса, показывает российский рынок
**Cons**: Требует аккаунт Яндекс.Директ для API, ограниченный бесплатный доступ

**Источники**:
- [Яндекс Вордстат обзавёлся API](https://yandex.ru/company/news/01-09-06-2025)
- [API Вордстата - Подробное руководство](https://osipenkov.ru/api-wordstat/)
- [Парсинг Яндекс Wordstat онлайн](https://arsenkin.ru/tools/wordstat/)

---

### 2. VK API (ВКонтакте)

**Возможности**:
- Мониторинг постов в группах/пабликах
- Trending hashtags
- Engagement metrics (лайки, репосты, комментарии)
- Новостная лента по темам
- Статистика сообществ

**API Methods**:
```python
import vk_api

vk_session = vk_api.VkApi(token=VK_ACCESS_TOKEN)
vk = vk_session.get_api()

# 1. Поиск трендовых постов (newsfeed.search)
trending_posts = vk.newsfeed.search(
    q='стартап OR бизнес',
    count=100,
    extended=1
)

# 2. Получение постов из группы (wall.get)
group_posts = vk.wall.get(
    owner_id=-123456789,  # ID группы
    count=100,
    filter='all'
)

# 3. Анализ engagement
for post in group_posts['items']:
    engagement = (
        post['likes']['count'] * 1 +
        post['reposts']['count'] * 3 +
        post['comments']['count'] * 2
    )
```

**Automation с n8n**:
- Мониторинг VK трендов через AI (newsfeed.search + кластеризация тем)
- Auto-drafts для быстрого постинга
- Интеграция с Google Sheets, CRM

**Сервисы аналитики**:
- **Popsters** - аналитика engagement постов
- **SocStat** - статистика групп ВКонтакте
- **SMMPLANNER** - планирование и аналитика

**Rate Limits**:
- 3 requests/second
- 5000 requests/day (стандартный токен)
- 100000 requests/day (server-side token)

**Применение**:
- Мониторинг конкурентов
- Отслеживание industry trends
- Определение optimal posting times
- Engagement analysis

**Pros**: Крупнейшая российская соцсеть, rich API
**Cons**: Требует OAuth, rate limits строже чем у Twitter

**Источники**:
- [Контент-завод ВКонтакте: Автоматизация с n8n и VK API](https://dobromarketing.ru/vk-content-automation-n8n/)
- [Как вытянуть данные через API ВК](https://habr.com/ru/articles/662858/)
- [Popsters - аналитика ВКонтакте](https://popsters.ru/vk/)

---

### 3. Telegram Monitoring

**Возможности**:
- Мониторинг публичных каналов
- Trending topics в реальном времени
- Engagement tracking (views, forwards)
- Keyword mentions
- Sentiment analysis

**Сервисы для мониторинга**:

#### TGStat (Лучший для автоматизации)
```python
import requests

# TGStat API
API_TOKEN = "your_tgstat_token"

# Поиск по каналам
response = requests.get(
    'https://api.tgstat.ru/channels/search',
    params={
        'token': API_TOKEN,
        'q': 'стартап',
        'limit': 50
    }
)

# Real-time мониторинг (5-10 секунд после публикации)
# Webhook для новых постов
response = requests.get(
    'https://api.tgstat.ru/posts/search',
    params={
        'token': API_TOKEN,
        'q': 'AI OR автоматизация',
        'extended': 1,
        'peer_type': 'channel'
    }
)

# Статистика канала
channel_stats = requests.get(
    f'https://api.tgstat.ru/channels/stat',
    params={
        'token': API_TOKEN,
        'channelId': '@channel_username'
    }
)
```

**API Coverage**:
- 2.8M+ Telegram каналов
- 54.3B+ публикаций
- 30M+ новых публикаций в день
- Real-time delivery (5-10 сек)

#### Telemetr
- Мониторинг роста подписчиков
- Engagement анализ
- Эффективность рекламы
- Поиск площадок для размещения

#### Медиалогия (Medialogia)
- Social media monitoring
- Sentiment analysis
- Reach metrics
- Message engagement
- Unlimited queries (платный тариф)

**Telegram Bot API** (для собственного бота):
```python
from telethon import TelegramClient

# Telethon для мониторинга каналов
client = TelegramClient('session', api_id, api_hash)

async def monitor_channels():
    # Подписка на каналы
    channels = ['@startup_ru', '@biznes_molodost', '@russianvc']

    @client.on(events.NewMessage(chats=channels))
    async def handler(event):
        # Analyze new post
        engagement_score = event.message.views or 0

        # Save to database
        await save_trend({
            'text': event.message.text,
            'views': event.message.views,
            'date': event.message.date,
            'channel': event.chat.title
        })
```

**Rate Limits**:
- TGStat API: зависит от тарифа (от $50/mo)
- Telegram Bot API: 30 messages/second

**Применение**:
- Tracking brand mentions
- Competitor monitoring
- Trend detection (viral posts)
- Keyword alerts
- Advertising campaign analysis

**Pros**: Telegram - главный источник инфо в РФ, rich analytics APIs
**Cons**: Требует платные API для масштаба (TGStat ~$50-200/mo)

**Источники**:
- [TGStat - Мониторинг Telegram](https://tgstat.ru/en/alerts)
- [TGStat API документация](https://tgstat.ru/en/api/stat)
- [ТОП-20 сервисов аналитики Телеграм каналов](https://vc.ru/telegram/1461828-analitika-telegramm-kanalov-top-20-servisov-i-botov-dlya-analiza-tg-kanalov)
- [Telemetr - аналитика Telegram](https://telemetr.me/)

---

### 4. Российские Новостные Агрегаторы

**Источники**:
- **Яндекс.Новости** - агрегатор новостей
- **Lenta.ru**, **RBC.ru**, **Vedomosti.ru** - RSS feeds
- **Habr** - IT/tech тренды (есть API)

**Habr API Example**:
```python
import requests

# Получение популярных статей
response = requests.get(
    'https://habr.com/ru/rss/all/',
    headers={'User-Agent': 'TrendScout/1.0'}
)

# Парсинг RSS
import feedparser
feed = feedparser.parse(response.text)

for entry in feed.entries:
    # Analyze tech trends
    if entry.published_parsed > recent_date:
        trends.append({
            'title': entry.title,
            'link': entry.link,
            'tags': entry.tags,
            'published': entry.published
        })
```

---

## Дополнительные Социальные Сети

### 5. YouTube Data API

**Возможности**:
- Trending videos по категориям
- Channel analytics & growth
- Video engagement metrics (views, likes, comments)
- Keyword search в названиях/описаниях
- Related videos clustering

**API Implementation**:
```python
from googleapiclient.discovery import build

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Get trending videos
trending_request = youtube.videos().list(
    part='snippet,statistics',
    chart='mostPopular',
    regionCode='RU',  # or 'US'
    maxResults=50,
    videoCategoryId='28'  # Science & Technology
)

trending_videos = trending_request.execute()

# Search for specific topics
search_request = youtube.search().list(
    part='snippet',
    q='AI startup OR автоматизация',
    type='video',
    order='viewCount',  # or 'date', 'relevance'
    publishedAfter='2026-01-01T00:00:00Z',
    maxResults=50
)

# Analyze channels
channel_stats = youtube.channels().list(
    part='statistics,snippet',
    id='UC_channel_id'
).execute()
```

**Rate Limits**:
- 10,000 quota units/day (free tier)
- search.list = 100 units
- videos.list = 1 unit
- ~100 searches/day free

**Применение**:
- Визуальные тренды (что люди смотрят)
- Влиятельные каналы в niche
- Educational content trends
- Product reviews & demos

**Pros**: Огромный объем данных, видео контент показывает interest
**Cons**: Quota limits строгие, нужен API key

---

### 6. Instagram (Meta Graph API)

**Возможности**:
- Hashtag trends
- Business account insights
- Post engagement (likes, comments, saves)
- Stories metrics
- Influencer tracking

**API Implementation** (требует Business account):
```python
import requests

# Instagram Graph API
access_token = "YOUR_ACCESS_TOKEN"
instagram_business_account_id = "YOUR_ID"

# Get media insights
url = f"https://graph.facebook.com/v18.0/{instagram_business_account_id}/media"
params = {
    'fields': 'id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count',
    'access_token': access_token
}

response = requests.get(url, params=params)
media = response.json()

# Hashtag search (ограниченный доступ)
hashtag_url = f"https://graph.facebook.com/v18.0/ig_hashtag_search"
hashtag_params = {
    'user_id': instagram_business_account_id,
    'q': 'startup',  # hashtag
    'access_token': access_token
}
```

**Ограничения**:
- Требуется Business/Creator account
- Доступ только к собственным данным + tagged content
- Hashtag search ограничен
- Rate limits: 200 calls/hour

**Альтернатива - Scraping** (risk of ban):
- Instaloader library (неофициальный)
- Apify Instagram Scraper

**Применение**:
- Visual trends (что популярно визуально)
- Influencer marketing opportunities
- Brand mentions
- Product launch tracking

**Pros**: Визуальный контент, influencer insights
**Cons**: Очень ограниченный API, требует авторизации

---

### 7. Facebook Graph API

**Возможности**:
- Public page posts
- Group discussions (ограниченный доступ)
- Events
- Reactions, comments, shares

**API Implementation**:
```python
import facebook

graph = facebook.GraphAPI(access_token=FB_ACCESS_TOKEN)

# Get public page posts
posts = graph.get_connections(
    id='page_id',
    connection_name='posts',
    fields='message,created_time,likes.summary(true),comments.summary(true),shares'
)

# Search public posts (ограниченный доступ)
search = graph.search(
    type='page',
    q='startup funding',
    fields='name,fan_count,category'
)
```

**Ограничения**:
- Доступ к public данным сильно ограничен после Cambridge Analytica
- Groups API требует специального разрешения
- Rate limits строгие

**Применение** (ограниченное):
- Public page monitoring
- Event discovery
- Brand mentions на страницах

**Pros**: Огромная аудитория
**Cons**: Очень ограниченный API, сложная авторизация

**Рекомендация**: Низкий приоритет из-за ограничений API. Лучше фокус на Reddit, YouTube, Telegram.

---

## Инвестиционные & Startup Порталы

### 8. Crunchbase API

**Возможности**:
- Новые стартапы и их описания
- Раунды финансирования
- Investors & VCs
- Acquisitions & IPOs
- Company categories & trends

**API Implementation**:
```python
import requests

CRUNCHBASE_API_KEY = "your_api_key"

# Search for recently funded startups
url = "https://api.crunchbase.com/api/v4/searches/organizations"
headers = {
    'X-cb-user-key': CRUNCHBASE_API_KEY,
    'Content-Type': 'application/json'
}

payload = {
    "field_ids": [
        "identifier",
        "name",
        "short_description",
        "categories",
        "funding_total",
        "last_funding_at",
        "founded_on"
    ],
    "order": [
        {
            "field_id": "last_funding_at",
            "sort": "desc"
        }
    ],
    "query": [
        {
            "type": "predicate",
            "field_id": "last_funding_at",
            "operator_id": "gte",
            "values": ["2026-01-01"]
        }
    ],
    "limit": 100
}

response = requests.post(url, json=payload, headers=headers)
startups = response.json()

# Get funding rounds
funding_url = "https://api.crunchbase.com/api/v4/searches/funding_rounds"
# Similar structure
```

**Pricing**:
- Free tier: нет
- Basic: $29/mo (limited API calls)
- Pro: $99/mo (1000 calls/month)
- Enterprise: Custom pricing

**Rate Limits**:
- Basic: 200 calls/day
- Pro: 1000 calls/month

**Применение**:
- Tracking новых стартапов в specific sectors
- Анализ funding trends (какие идеи получают деньги)
- Competitor monitoring
- Investment thesis validation

**Pros**: Официальные данные о финансировании, comprehensive
**Cons**: Дорого ($99/mo минимум для API), rate limits

---

### 9. AngelList/Wellfound API

**Возможности**:
- Startup listings
- Jobs at startups (показывает какие стартапы растут)
- Investor profiles
- Startup valuations

**API Status**:
⚠️ AngelList закрыл публичный API в 2023 году. Альтернативы:
- Wellfound (новое название) - нет публичного API
- Scraping (риск бана)

**Альтернативный подход**:
```python
# Web scraping (использовать осторожно)
import requests
from bs4 import BeautifulSoup

def scrape_wellfound_jobs():
    """Scrape job listings as proxy for startup growth"""
    url = "https://wellfound.com/role/r/software-engineer"

    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')

    # Parse listings
    # Identify growing startups by # of open positions
```

**Применение**:
- Proxy metric: много вакансий = растущий стартап
- Industry trends (AI, crypto, SaaS)
- Talent market analysis

**Pros**: Показывает реальный growth стартапов
**Cons**: Нет официального API, только scraping

---

### 10. Product Hunt (уже описан выше)

Остается в Tier 1 для daily startup launches.

---

## Новостные & Аналитические Порталы

### 11. TechCrunch RSS & API

**Возможности**:
- Tech news feed
- Startup launches
- Funding announcements
- Trend analysis articles

**RSS Implementation**:
```python
import feedparser

# TechCrunch RSS feeds
feeds = {
    'main': 'https://techcrunch.com/feed/',
    'startups': 'https://techcrunch.com/category/startups/feed/',
    'ai': 'https://techcrunch.com/category/artificial-intelligence/feed/',
    'funding': 'https://techcrunch.com/tag/funding/feed/'
}

for category, url in feeds.items():
    feed = feedparser.parse(url)

    for entry in feed.entries:
        article = {
            'title': entry.title,
            'link': entry.link,
            'published': entry.published,
            'summary': entry.summary,
            'categories': [tag.term for tag in entry.tags]
        }
```

**Rate Limits**:
- RSS: unlimited (politeness recommended)
- Scraping: 1 request/second

**Применение**:
- Breaking startup news
- Funding announcements (альтернатива Crunchbase)
- Industry trends
- Product launches

**Pros**: Free, high-quality content, early signals
**Cons**: Текстовый анализ нужен для extracting insights

---

### 12. Habr + VC.ru (Российские)

**Habr API/RSS**:
```python
# Habr RSS
habr_feeds = {
    'all': 'https://habr.com/ru/rss/all/',
    'top': 'https://habr.com/ru/rss/top/',
    'hubs/startup': 'https://habr.com/ru/hub/startup/rss/',
}

feed = feedparser.parse(habr_feeds['hubs/startup'])
```

**VC.ru Scraping**:
```python
# VC.ru не имеет официального API
# Рекомендуется RSS или scraping
vc_url = "https://vc.ru/feed"

response = requests.get(vc_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Парсинг статей про стартапы, венчур, бизнес
```

**Применение**:
- Российский tech landscape
- Local startup ecosystem
- Venту trends в РФ

**Pros**: Free, русскоязычный контент
**Cons**: Нет API, нужен scraping/RSS

---

## Сравнительная Таблица Источников

### Поисковые Системы (ПРИОРИТЕТ 1)
| Источник | Охват | API Качество | Cost/Month | Update Speed | Best For |
|----------|-------|--------------|------------|--------------|----------|
| **Google Trends** | 🌍 Global | ⭐⭐⭐ | Free* | Daily/Weekly | Macro search trends |
| **Яндекс Wordstat** | 🇷🇺 Russia | ⭐⭐⭐ | $50-100 (API) | Weekly | RU search demand |

### Социальные Сети (ПРИОРИТЕТ 2)
| Источник | Охват | API Качество | Cost/Month | Update Speed | Best For |
|----------|-------|--------------|------------|--------------|----------|
| **Reddit** | 🌍 Global | ⭐⭐⭐⭐⭐ | Free | Hourly | Niche communities, early signals |
| **YouTube** | 🌍 Global | ⭐⭐⭐⭐ | Free (10k quota/day) | Daily/Hourly | Video trends, educational |
| **Telegram (TGStat)** | 🇷🇺 Russia | ⭐⭐⭐⭐⭐ | $50-200 | Real-time (5s) | Viral content RU |
| **VK** | 🇷🇺 Russia | ⭐⭐⭐⭐ | Free | Hourly | Social trends RU |
| **Instagram** | 🌍 Global | ⭐⭐ | Free (limited) | Daily | Visual trends, influencers |
| **Facebook** | 🌍 Global | ⭐ | Free (very limited) | N/A | Low priority (API ограничен) |
| **Twitter/X** | 🌍 Global | ⭐⭐⭐⭐ | $100-5000 | Real-time | Breaking news (дорого) |

### Инвестиционные & Startup Порталы (ПРИОРИТЕТ 3)
| Источник | Охват | API Качество | Cost/Month | Update Speed | Best For |
|----------|-------|--------------|------------|--------------|----------|
| **Crunchbase** | 🌍 Global | ⭐⭐⭐⭐⭐ | $99-500 | Daily | Funding rounds, new startups |
| **AngelList/Wellfound** | 🌍 Global | ❌ | Free (scraping) | Daily | Startup jobs, growth signals |
| **Product Hunt** | 🌍 Tech | ⭐⭐⭐⭐ | Free | Daily | Daily startup launches |

### Новостные Порталы (ПРИОРИТЕТ 4)
| Источник | Охват | API Качество | Cost/Month | Update Speed | Best For |
|----------|-------|--------------|------------|--------------|----------|
| **TechCrunch** | 🌍 Global | ⭐⭐⭐ (RSS) | Free | Hourly | Tech news, funding announces |
| **Habr** | 🇷🇺 Russia | ⭐⭐⭐ (RSS) | Free | Daily | RU tech trends |
| **VC.ru** | 🇷🇺 Russia | ⭐ (scraping) | Free | Daily | RU business/VC trends |

**Легенда**:
- ⭐⭐⭐⭐⭐ = Отличное API, официальное, хорошая документация
- ⭐⭐⭐⭐ = Хорошее API с некоторыми ограничениями
- ⭐⭐⭐ = Работает, но есть issues (unofficial, rate limits)
- ⭐⭐ = Сильно ограниченное API
- ⭐ = Практически нет API, только scraping
- ❌ = Нет публичного API

\* Google Trends - неофициальный API через pytrends, риск блокировки

---

## Recommended Architecture для нашего проекта

### Data Sources Priority (MVP)

**ПРИОРИТЕТ 1: Поисковые Запросы** (основа системы)
1. **Google Trends** - macro trends, международный поисковый анализ
2. **Яндекс Wordstat** - поисковый спрос в РФ

**ПРИОРИТЕТ 2: Социальные Сети**
3. **Reddit** - high-quality discussions, early signals
4. **YouTube** - video trends, channel analytics
5. **Telegram (TGStat API)** - real-time российские тренды
6. **VK API** - российский social proof
7. **Instagram** - визуальные тренды, influencer marketing (опционально)
8. **Facebook** - group discussions, events (опционально)

**ПРИОРИТЕТ 3: Инвестиционные & Startup Порталы**
9. **Crunchbase** - новые стартапы, раунды финансирования
10. **AngelList/Wellfound** - startup jobs, funding
11. **Product Hunt** - daily startup launches

**ПРИОРИТЕТ 4: Новостные Порталы**
12. **TechCrunch** - tech news, startup launches
13. **TheInformation** - in-depth tech analysis
14. **Habr** - русскоязычные IT тренды
15. **VC.ru** - российский бизнес/венчур

**Tier 3 - Future Expansion**:
- Twitter/X (если бюджет позволяет - $100-5000/mo)
- LinkedIn (B2B trends, professional networks)

### Multi-Source Pipeline Architecture

```python
# backend/app/scrapers/multi_source_scraper.py

from typing import List, Dict
import asyncio

class MultiSourceTrendScout:
    def __init__(self):
        self.sources = {
            'google_trends': GoogleTrendsScraper(),
            'tgstat': TelegramScraper(),
            'vk': VKScraper(),
            'reddit': RedditScraper(),
            'yandex_wordstat': YandexWordstatScraper(),
        }

    async def fetch_all_trends(self, keywords: List[str]) -> List[Dict]:
        """Fetch trends from all sources in parallel"""

        tasks = [
            self.sources['google_trends'].scrape(keywords),
            self.sources['tgstat'].scrape(keywords),
            self.sources['vk'].scrape(keywords),
            self.sources['reddit'].scrape(keywords),
        ]

        # Parallel execution
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Merge and deduplicate
        all_trends = []
        for source_result in results:
            if isinstance(source_result, Exception):
                logger.error(f"Source failed: {source_result}")
                continue
            all_trends.extend(source_result)

        # Deduplicate by content similarity
        unique_trends = self._deduplicate_trends(all_trends)

        return unique_trends

    def _deduplicate_trends(self, trends: List[Dict]) -> List[Dict]:
        """Remove duplicate trends using semantic similarity"""
        # Use embeddings to find duplicates
        # Keep the one with highest engagement
        pass
```

### Cost Optimization Strategy

**Monthly Budget Estimate** (MVP):
- Telegram TGStat API: $50-100/mo
- VK API: Free (standard access)
- Google Trends: Free (с rate limiting)
- Reddit API: Free
- Яндекс Wordstat: $0 (парсинг) или $50-100/mo (API)
- **Total**: ~$50-200/mo для data sources

**Для Scale (1000+ бизнесов)**:
- Добавить Twitter: +$100-500/mo
- Upgrade TGStat: +$100/mo
- Яндекс Wordstat API: +$100/mo
- **Total**: ~$350-800/mo

---

## Best Practices

### 1. Rate Limiting & Politeness
```python
from ratelimit import limits, sleep_and_retry

class PoliteScraper:
    @sleep_and_retry
    @limits(calls=10, period=60)  # 10 calls per minute
    async def fetch_data(self, url: str):
        """Respectful rate limiting"""
        response = await aiohttp.get(url)
        return response
```

### 2. Error Handling & Retries
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def fetch_with_retry(self, source: str):
    """Retry on failures"""
    try:
        return await self.sources[source].scrape()
    except Exception as e:
        logger.error(f"Retry failed for {source}: {e}")
        raise
```

### 3. Caching для экономии API calls
```python
from functools import lru_cache
import redis

cache = redis.Redis(host='localhost', port=6379, db=0)

def cached_scrape(ttl: int = 3600):
    """Cache scraping results"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"

            # Check cache
            cached = cache.get(cache_key)
            if cached:
                return json.loads(cached)

            # Fetch fresh data
            result = await func(*args, **kwargs)

            # Store in cache
            cache.setex(cache_key, ttl, json.dumps(result))

            return result
        return wrapper
    return decorator
```

### 4. Monitoring & Alerts
```python
# Prometheus metrics
from prometheus_client import Counter, Histogram

scrape_requests = Counter(
    'scrape_requests_total',
    'Total scraping requests',
    ['source', 'status']
)

scrape_duration = Histogram(
    'scrape_duration_seconds',
    'Scraping duration',
    ['source']
)

async def monitored_scrape(source: str):
    with scrape_duration.labels(source=source).time():
        try:
            result = await scraper.fetch(source)
            scrape_requests.labels(source=source, status='success').inc()
            return result
        except Exception:
            scrape_requests.labels(source=source, status='error').inc()
            raise
```

---

## Implementation Priority

### Week 1: Foundation
- [ ] Setup Google Trends scraper (pytrends)
- [ ] Setup Reddit API (PRAW)
- [ ] Basic deduplication logic

### Week 2: Russian Sources
- [ ] Integrate TGStat API (Telegram)
- [ ] Setup VK API scraper
- [ ] Test Yandex Wordstat (парсинг или API)

### Week 3: Data Pipeline
- [ ] Parallel scraping с asyncio
- [ ] Caching layer (Redis)
- [ ] Error handling & retries
- [ ] Prometheus monitoring

### Week 4: Optimization
- [ ] Deduplication с embeddings
- [ ] Rate limiting optimization
- [ ] Cost tracking dashboard

---

## Resources & Documentation

### International
- [Twitter API v2 Documentation](https://developer.twitter.com/en/docs/twitter-api)
- [Reddit API (PRAW) Docs](https://praw.readthedocs.io/)
- [pytrends (Google Trends)](https://pypi.org/project/pytrends/)
- [Product Hunt API](https://api.producthunt.com/v2/docs)

### Russian
- [Яндекс Wordstat API](https://osipenkov.ru/api-wordstat/)
- [VK API Documentation](https://dev.vk.com/ru/reference)
- [TGStat API](https://tgstat.ru/en/api/stat)
- [Telemetr](https://telemetr.me/)

### Tools & Libraries
- [Tweepy (Twitter)](https://github.com/tweepy/tweepy)
- [PRAW (Reddit)](https://github.com/praw-dev/praw)
- [vk_api (VK)](https://github.com/python273/vk_api)
- [Telethon (Telegram)](https://github.com/LonamiWebs/Telethon)

---

## Next Steps

1. ✅ Определены все источники данных (международные + российские)
2. ⏳ Протестировать каждый API локально
3. ⏳ Измерить реальные rate limits
4. ⏳ Оценить cost на 100 trends/day
5. ⏳ Создать unified scraper interface

