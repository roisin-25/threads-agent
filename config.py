import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    THREADS_ACCESS_TOKEN = os.getenv('THREADS_ACCESS_TOKEN')
    THREADS_USER_ID = os.getenv('THREADS_USER_ID')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

    # Rate limits
    DAILY_POST_LIMIT = 250
    CHARACTER_LIMIT = 490

    # News sources (RSS feeds) - mix of global and Australian
    NEWS_FEEDS = [
        'https://techcrunch.com/feed/',
        'https://www.theverge.com/rss/index.xml',
        'https://www.wired.com/feed/rss',
        'https://news.ycombinator.com/rss',
        'https://www.smh.com.au/rss/technology.xml',
        'https://www.afr.com/rss/technology',
        'https://www.innovationaus.com/feed/',
    ]

    # Primary keywords - broad net
    KEYWORDS = [
        'AI', 'artificial intelligence', 'workforce',
        'automation', 'tech hiring', 'upskilling',
        'reskilling', 'future of work', 'talent shortage',
        'skills gap', 'tech skills', 'recruitment',
        'layoffs', 'redundancies', 'redeployment',
        'career transition', 'hiring trends', 'tech careers'
    ]

    # Australian context indicators (boost relevance)
    AUSTRALIAN_INDICATORS = [
        'australia', 'australian', 'sydney', 'melbourne',
        'nsw', 'victoria', 'canberra', 'apac',
        'commonwealth', 'ato', 'fair work'
    ]

    # High-relevance signals (what matters to Neoma's audience)
    RELEVANCE_SIGNALS = [
        'enterprise', 'corporate', 'business transformation',
        'workforce planning', 'talent strategy', 'HR tech',
        'internal mobility', 'career pathways', 'policy',
        'government', 'regulation', 'ROI', 'business case',
        'skills assessment', 'alternative pathways'
    ]

    # US-centric indicators (penalize unless Australian context present)
    US_POLITICAL_INDICATORS = [
        'trump', 'biden', 'white house', 'congress', 'senate',
        'washington', 'federal government', 'executive order',
        'republican', 'democrat', 'us government'
    ]

    # File to track posted articles
    POSTED_LINKS_FILE = 'posted_links.json'
