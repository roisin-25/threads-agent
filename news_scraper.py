import feedparser
import requests
from datetime import datetime, timedelta
from config import Config


class NewsScraper:
    def __init__(self):
        self.feeds = Config.NEWS_FEEDS
        self.keywords = Config.KEYWORDS

    def fetch_latest_news(self, hours_back=24):
        """Fetch news from the last N hours"""
        all_articles = []
        cutoff_time = datetime.now() - timedelta(hours=hours_back)

        for feed_url in self.feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    # Parse published date
                    pub_date = datetime(*entry.published_parsed[:6])

                    if pub_date > cutoff_time:
                        # Check if article matches keywords
                        text = f"{entry.title} {entry.get('summary', '')}"
                        if any(keyword.lower() in text.lower()
                               for keyword in self.keywords):
                            all_articles.append({
                                'title': entry.title,
                                'link': entry.link,
                                'summary': entry.get('summary', ''),
                                'published': pub_date,
                                'source': feed.feed.title
                            })
            except Exception as e:
                print(f"Error fetching {feed_url}: {e}")

        # Sort by recency and return top 5
        all_articles.sort(key=lambda x: x['published'], reverse=True)
        return all_articles[:5]


if __name__ == "__main__":
    scraper = NewsScraper()
    news = scraper.fetch_latest_news()

    print(f"Found {len(news)} articles:\n")
    for article in news:
        print(f"Title: {article['title']}")
        print(f"Source: {article['source']}")
        print(f"Link: {article['link']}")
        print("-" * 50)
