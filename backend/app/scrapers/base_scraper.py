"""
Base Scraper Class
Abstract interface for all data scrapers
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import structlog

logger = structlog.get_logger()


class BaseScraper(ABC):
    """
    Base class for all data scrapers

    Provides:
    - Common interface for scraping
    - Error handling
    - Rate limiting support
    - Data validation
    """

    def __init__(self, source_name: str):
        """
        Initialize base scraper

        Args:
            source_name: Name of the data source (reddit, twitter, etc.)
        """
        self.source_name = source_name
        self.logger = logger.bind(scraper=source_name)

    @abstractmethod
    async def scrape(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Scrape data from the source

        Args:
            params: Scraping parameters (keywords, limits, filters, etc.)

        Returns:
            List of raw data items

        Raises:
            ScraperError: If scraping fails
        """
        pass

    def validate_item(self, item: Dict[str, Any]) -> bool:
        """
        Validate a scraped item

        Args:
            item: Raw data item

        Returns:
            True if item is valid, False otherwise
        """
        required_fields = ["title", "url"]
        return all(field in item for field in required_fields)

    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text

        Args:
            text: Raw text

        Returns:
            Cleaned text
        """
        if not text:
            return ""

        # Remove extra whitespace
        text = " ".join(text.split())

        # Remove control characters
        text = "".join(char for char in text if char.isprintable() or char in "\n\t")

        return text.strip()

    def extract_tags(self, text: str, max_tags: int = 10) -> List[str]:
        """
        Extract potential tags from text

        This is a simple implementation. Can be enhanced with NER or keyword extraction.

        Args:
            text: Text to extract tags from
            max_tags: Maximum number of tags

        Returns:
            List of tags
        """
        # Simple implementation: extract hashtags or common words
        # TODO: Enhance with proper keyword extraction (RAKE, YAKE, etc.)

        tags = []

        # Extract hashtags
        words = text.split()
        for word in words:
            if word.startswith("#"):
                tag = word[1:].lower()
                if tag and tag not in tags:
                    tags.append(tag)

        return tags[:max_tags]


class ScraperError(Exception):
    """Custom exception for scraper errors"""
    pass
