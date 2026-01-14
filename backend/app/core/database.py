"""
Database configuration and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator

from app.core.config import settings

# Handle Railway PostgreSQL URL format (postgres:// -> postgresql://)
database_url = settings.DATABASE_URL
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# Determine if using SQLite (for local dev) or PostgreSQL (for production)
is_sqlite = database_url.startswith("sqlite")

# Create database engine with appropriate settings
engine_kwargs = {
    "pool_pre_ping": True,  # Verify connections before using
    "echo": settings.DEBUG  # Log SQL queries in debug mode
}

# Only add pool settings for non-SQLite databases
if not is_sqlite:
    engine_kwargs["pool_size"] = settings.DATABASE_POOL_SIZE
    engine_kwargs["max_overflow"] = settings.DATABASE_MAX_OVERFLOW
else:
    # SQLite specific settings
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(database_url, **engine_kwargs)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for ORM models
Base = declarative_base()


def get_db() -> Generator:
    """
    Database session dependency for FastAPI

    Usage:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Database initialization
def init_db():
    """
    Initialize database tables
    Should be called on application startup
    """
    # Import all models here to ensure they're registered
    # from app.modules.trends.models import Trend
    # from app.modules.ideas.models import Idea
    # from app.modules.businesses.models import Business

    # Create all tables
    Base.metadata.create_all(bind=engine)


def drop_db():
    """
    Drop all database tables
    WARNING: Only use in development/testing!
    """
    Base.metadata.drop_all(bind=engine)
