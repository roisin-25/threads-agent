import schedule
import time
import logging
import sys
from datetime import datetime
from news_scraper import NewsScraper
from insight_generator import InsightGenerator
from threads_poster import ThreadsPoster

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),  # Console output (captured by GitHub Actions)
    ]
)
logger = logging.getLogger(__name__)


class ThreadsAgent:
    def __init__(self):
        self.scraper = NewsScraper()
        self.generator = InsightGenerator()
        self.poster = ThreadsPoster()
        self.posted_links = set()  # Track posted articles

    def run_daily_post(self):
        """Main function to create and post daily content"""
        logger.info("Starting daily post generation...")

        # 1. Fetch latest news
        articles = self.scraper.fetch_latest_news(hours_back=24)

        if not articles:
            logger.warning("No relevant articles found")
            return

        # 2. Filter out already posted articles
        new_articles = [a for a in articles if a['link'] not in self.posted_links]

        if not new_articles:
            logger.info("All recent articles already posted")
            return

        # 3. Select most recent article
        article = new_articles[0]
        logger.info(f"Selected article: {article['title']}")

        # 4. Generate insight
        try:
            post_content = self.generator.generate_insight(article)
            logger.info(f"Generated post:\n{post_content}")
        except Exception as e:
            logger.error(f"Error generating insight: {e}")
            return

        # 5. Post to Threads
        result = self.poster.create_post(post_content)

        if result['success']:
            logger.info(f"Successfully posted! Thread ID: {result['thread_id']}")
            self.posted_links.add(article['link'])
        else:
            logger.error(f"Failed to post: {result['error']}")

    def start_scheduler(self):
        """Start the daily scheduler"""
        # Schedule for 9 AM and 2 PM daily (Sydney time - for local runs)
        schedule.every().day.at("09:00").do(self.run_daily_post)
        schedule.every().day.at("14:00").do(self.run_daily_post)

        logger.info("Threads Agent started. Scheduled for 9:00 AM and 2:00 PM daily...")
        logger.info("Press Ctrl+C to stop")

        # Run immediately on start (optional)
        # self.run_daily_post()

        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute


if __name__ == "__main__":
    agent = ThreadsAgent()

    if "--once" in sys.argv:
        # Single run mode (for GitHub Actions)
        agent.run_daily_post()
    else:
        # Continuous scheduler mode
        agent.start_scheduler()
