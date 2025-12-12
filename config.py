import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # API credentials
    THREADS_ACCESS_TOKEN = os.getenv('THREADS_ACCESS_TOKEN')
    THREADS_USER_ID = os.getenv('THREADS_USER_ID')
    THREADS_API_BASE = "https://graph.threads.net/v1.0"
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

    # Rate limits
    DAILY_POST_LIMIT = 250

    # News sources (RSS feeds)
    NEWS_FEEDS = [
        'https://techcrunch.com/feed/',
        'https://www.theverge.com/rss/index.xml',
        'https://www.wired.com/feed/rss',
        'https://news.ycombinator.com/rss',
    ]

    # Keywords to filter for relevant content
    KEYWORDS = [
        'AI', 'artificial intelligence', 'workforce',
        'automation', 'tech hiring', 'upskilling',
        'reskilling', 'future of work'
    ]

    # Posting schedule (24-hour format)
    POSTING_TIMES = ["09:00", "12:00", "18:00"]

    # Maximum post length for Threads
    MAX_POST_LENGTH = 500

    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        required = [
            ("THREADS_ACCESS_TOKEN", cls.THREADS_ACCESS_TOKEN),
            ("THREADS_USER_ID", cls.THREADS_USER_ID),
            ("ANTHROPIC_API_KEY", cls.ANTHROPIC_API_KEY),
        ]

        missing = [name for name, value in required if not value]

        if missing:
            print(f"Missing required configuration: {', '.join(missing)}")
            print("Please ensure these are set in your .env file")
            return False

        return True
