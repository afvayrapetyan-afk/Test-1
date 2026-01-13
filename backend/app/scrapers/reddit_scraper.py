"""
Reddit Scraper
Scrapes trending posts from Reddit using PRAW
"""

from typing import List, Dict, Any
import praw
from datetime import datetime
import structlog

from app.scrapers.base_scraper import BaseScraper, ScraperError
from app.core.config import settings

logger = structlog.get_logger()


class RedditScraper(BaseScraper):
    """
    Reddit Scraper using PRAW (Python Reddit API Wrapper)

    Scrapes:
    - Hot posts from specified subreddits
    - Top posts (daily/weekly/monthly)
    - Post metadata (upvotes, comments, awards)
    - User engagement signals
    """

    def __init__(self):
        super().__init__(source_name="reddit")

        # Initialize PRAW client
        try:
            self.reddit = praw.Reddit(
                client_id=settings.REDDIT_CLIENT_ID,
                client_secret=settings.REDDIT_CLIENT_SECRET,
                user_agent=settings.REDDIT_USER_AGENT,
                username=settings.REDDIT_USERNAME,
                password=settings.REDDIT_PASSWORD
            )

            # Test connection
            self.reddit.user.me()
            self.logger.info("Reddit client initialized successfully")

        except Exception as e:
            self.logger.error("Failed to initialize Reddit client", error=str(e))
            raise ScraperError(f"Reddit initialization failed: {str(e)}")

    async def scrape(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Scrape Reddit posts

        Args:
            params: {
                "subreddits": ["SideProject", "startups"],
                "limit": 100,
                "time_filter": "week",  # hour, day, week, month, year, all
                "sort": "hot"  # hot, top, new, rising
            }

        Returns:
            List of processed Reddit posts
        """
        subreddits = params.get("subreddits", ["SideProject", "startups", "Entrepreneur"])
        limit = params.get("limit", 100)
        time_filter = params.get("time_filter", "week")
        sort = params.get("sort", "hot")

        self.logger.info(
            "Scraping Reddit",
            subreddits=subreddits,
            limit=limit,
            sort=sort,
            time_filter=time_filter
        )

        all_posts = []

        for subreddit_name in subreddits:
            try:
                posts = self._scrape_subreddit(
                    subreddit_name,
                    limit=limit // len(subreddits),
                    sort=sort,
                    time_filter=time_filter
                )
                all_posts.extend(posts)

                self.logger.info(
                    "Scraped subreddit",
                    subreddit=subreddit_name,
                    posts_count=len(posts)
                )

            except Exception as e:
                self.logger.error(
                    "Failed to scrape subreddit",
                    subreddit=subreddit_name,
                    error=str(e)
                )
                continue

        self.logger.info(
            "Reddit scraping completed",
            total_posts=len(all_posts)
        )

        return all_posts

    def _scrape_subreddit(
        self,
        subreddit_name: str,
        limit: int,
        sort: str,
        time_filter: str
    ) -> List[Dict[str, Any]]:
        """
        Scrape posts from a single subreddit

        Args:
            subreddit_name: Name of subreddit
            limit: Number of posts to fetch
            sort: Sorting method (hot, top, new, rising)
            time_filter: Time filter for top posts

        Returns:
            List of processed posts
        """
        try:
            subreddit = self.reddit.subreddit(subreddit_name)

            # Get posts based on sort method
            if sort == "hot":
                submissions = subreddit.hot(limit=limit)
            elif sort == "top":
                submissions = subreddit.top(time_filter=time_filter, limit=limit)
            elif sort == "new":
                submissions = subreddit.new(limit=limit)
            elif sort == "rising":
                submissions = subreddit.rising(limit=limit)
            else:
                raise ValueError(f"Unknown sort method: {sort}")

            posts = []
            for submission in submissions:
                post = self._process_submission(submission, subreddit_name)
                if post and self.validate_item(post):
                    posts.append(post)

            return posts

        except Exception as e:
            self.logger.error(
                "Error scraping subreddit",
                subreddit=subreddit_name,
                error=str(e)
            )
            raise ScraperError(f"Failed to scrape r/{subreddit_name}: {str(e)}")

    def _process_submission(self, submission, subreddit_name: str) -> Dict[str, Any]:
        """
        Process a Reddit submission into structured data

        Args:
            submission: PRAW Submission object
            subreddit_name: Name of subreddit

        Returns:
            Processed post data
        """
        try:
            # Calculate engagement score
            engagement_score = self._calculate_engagement(submission)

            # Extract category based on flair or heuristics
            category = self._extract_category(submission)

            # Extract tags from title and flair
            tags = self._extract_tags_from_submission(submission)

            # Calculate velocity (upvotes per hour)
            post_age_hours = (datetime.utcnow() - datetime.utcfromtimestamp(submission.created_utc)).total_seconds() / 3600
            velocity = submission.score / max(post_age_hours, 1)  # Avoid division by zero

            return {
                "title": self.clean_text(submission.title),
                "description": self.clean_text(submission.selftext) if submission.selftext else "",
                "url": f"https://reddit.com{submission.permalink}",
                "source": "reddit",
                "category": category,
                "tags": tags,
                "engagement_score": engagement_score,
                "velocity": round(velocity, 2),
                "metadata": {
                    "subreddit": subreddit_name,
                    "author": str(submission.author) if submission.author else "[deleted]",
                    "upvotes": submission.score,
                    "upvote_ratio": submission.upvote_ratio,
                    "num_comments": submission.num_comments,
                    "awards": submission.total_awards_received,
                    "created_utc": submission.created_utc,
                    "flair": submission.link_flair_text if submission.link_flair_text else None,
                    "is_self": submission.is_self,
                    "domain": submission.domain
                }
            }

        except Exception as e:
            self.logger.error(
                "Error processing submission",
                submission_id=submission.id,
                error=str(e)
            )
            return None

    def _calculate_engagement(self, submission) -> int:
        """
        Calculate engagement score from Reddit metrics

        Formula: upvotes + (comments * 2) + (awards * 10)
        Comments are weighted 2x because they indicate higher engagement
        Awards are weighted 10x because they cost money
        """
        score = submission.score
        comments = submission.num_comments * 2
        awards = submission.total_awards_received * 10

        return score + comments + awards

    def _extract_category(self, submission) -> str:
        """
        Extract category from submission

        Uses flair, title keywords, or domain heuristics
        """
        # Check flair first
        if submission.link_flair_text:
            flair = submission.link_flair_text.lower()
            if "product" in flair or "launch" in flair:
                return "saas"
            elif "question" in flair or "help" in flair:
                return "discussion"
            elif "showcase" in flair or "demo" in flair:
                return "showcase"

        # Check title keywords
        title_lower = submission.title.lower()

        if any(word in title_lower for word in ["ai", "ml", "gpt", "chatbot", "automation"]):
            return "ai"
        elif any(word in title_lower for word in ["saas", "software", "app", "platform"]):
            return "saas"
        elif any(word in title_lower for word in ["marketplace", "e-commerce", "shop"]):
            return "marketplace"
        elif any(word in title_lower for word in ["productivity", "tool", "workflow"]):
            return "productivity"
        elif any(word in title_lower for word in ["fintech", "crypto", "blockchain", "payment"]):
            return "fintech"
        elif any(word in title_lower for word in ["health", "fitness", "wellness"]):
            return "health"
        elif any(word in title_lower for word in ["education", "learning", "course"]):
            return "education"
        else:
            return "other"

    def _extract_tags_from_submission(self, submission) -> List[str]:
        """
        Extract tags from submission title, flair, and content

        Returns list of relevant tags
        """
        tags = []

        # Add flair as tag
        if submission.link_flair_text:
            tags.append(submission.link_flair_text.lower())

        # Extract hashtags from title
        title_tags = self.extract_tags(submission.title)
        tags.extend(title_tags)

        # Add domain-based tags for link posts
        if not submission.is_self:
            if "github.com" in submission.domain:
                tags.append("github")
            elif "youtube.com" in submission.domain or "youtu.be" in submission.domain:
                tags.append("youtube")

        # Add keyword-based tags
        text = f"{submission.title} {submission.selftext}".lower()

        keywords = [
            "ai", "ml", "gpt", "chatbot", "saas", "productivity",
            "no-code", "automation", "startup", "mvp", "side-project",
            "open-source", "api", "mobile", "web", "react", "next.js",
            "firebase", "supabase", "stripe", "payment"
        ]

        for keyword in keywords:
            if keyword in text and keyword not in tags:
                tags.append(keyword)

        # Remove duplicates and limit
        tags = list(dict.fromkeys(tags))  # Preserve order while removing duplicates
        return tags[:10]
