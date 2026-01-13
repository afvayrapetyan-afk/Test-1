"""
Scrapers Package
Data collection from various sources
"""

from app.scrapers.base_scraper import BaseScraper
from app.scrapers.reddit_scraper import RedditScraper

__all__ = [
    "BaseScraper",
    "RedditScraper"
]
