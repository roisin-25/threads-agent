import feedparser
import requests
from datetime import datetime, timedelta
from config import Config

class NewsScraper:
    def __init__(self):
        self.feeds = Config.NEWS_FEEDS
        self.keywords = Config.KEYWORDS
        self.australian_indicators = Config.AUSTRALIAN_INDICATORS
        self.relevance_signals = Config.RELEVANCE_SIGNALS

    def calculate_relevance_score(self, article_text):
        """Score article relevance based on Australian context and strategic signals"""
        score = 0
        text_lower = article_text.lower()

        # Australian context bonus (+3 points per match)
        australian_matches = sum(1 for indicator in self.australian_indicators
                                if indicator.lower() in text_lower)
        score += australian_matches * 3

        # High-relevance signal bonus (+2 points per match)
        relevance_matches = sum(1 for signal in self.relevance_signals
                               if signal.lower() in text_lower)
        score += relevance_matches * 2

        # Keyword match bonus (+1 point per match)
        keyword_matches = sum(1 for keyword in self.keywords
                             if keyword.lower() in text_lower)
        score += keyword_matches

        return score

    def fetch_latest_news(self, hours_back=24):
        """Fetch news from the last N hours, ranked by relevance"""
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

                            # Calculate relevance score
                            relevance_score = self.calculate_relevance_score(text)

                            all_articles.append({
                                'title': entry.title,
                                'link': entry.link,
                                'summary': entry.get('summary', ''),
                                'published': pub_date,
                                'source': feed.feed.title,
                                'relevance_score': relevance_score
                            })
            except Exception as e:
                print(f"Error fetching {feed_url}: {e}")

        # Sort by relevance score first, then recency
        all_articles.sort(key=lambda x: (x['relevance_score'], x['published']),
                         reverse=True)

        # Return top 5 most relevant
        return all_articles[:5]


if __name__ == "__main__":
    scraper = NewsScraper()
    news = scraper.fetch_latest_news()

    print(f"Found {len(news)} articles:\n")
    for article in news:
        print(f"Title: {article['title']}")
        print(f"Source: {article['source']}")
        print(f"Relevance Score: {article.get('relevance_score', 0)}")
        print(f"Link: {article['link']}")
        print("-" * 50)
