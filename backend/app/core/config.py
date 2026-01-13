"""
Application Configuration
Loads settings from environment variables
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """
    Application settings loaded from .env file
    """

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 0

    # Redis (Optional для быстрого старта)
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_MAX_CONNECTIONS: int = 50

    # Qdrant (Optional)
    QDRANT_URL: str = "http://localhost:6333"

    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

    # Anthropic (Optional - Fallback)
    ANTHROPIC_API_KEY: str = ""

    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS string into list"""
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        return self.CORS_ORIGINS

    # Celery (Optional для быстрого старта)
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 100

    # Logging
    LOG_LEVEL: str = "INFO"

    # Sentry (Optional)
    SENTRY_DSN: str = ""

    # Feature Flags
    ENABLE_KAFKA: bool = False
    ENABLE_TEMPORAL: bool = False
    ENABLE_BATCH_EMBEDDINGS: bool = True
    ENABLE_PROMPT_CACHING: bool = True

    # Data Sources (все опциональные)
    REDDIT_CLIENT_ID: str = ""
    REDDIT_CLIENT_SECRET: str = ""
    REDDIT_USER_AGENT: str = "BusinessPortfolioBot/1.0"
    REDDIT_USERNAME: str = ""
    REDDIT_PASSWORD: str = ""

    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_API_ID: str = ""
    TELEGRAM_API_HASH: str = ""

    VK_ACCESS_TOKEN: str = ""

    TGSTAT_API_TOKEN: str = ""

    YANDEX_WORDSTAT_USER: str = ""
    YANDEX_WORDSTAT_TOKEN: str = ""

    YOUTUBE_API_KEY: str = ""

    # GitHub Integration (Optional)
    GITHUB_TOKEN: str = ""
    GITHUB_REPO: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields from .env that aren't defined in Settings


# Global settings instance
settings = Settings()
