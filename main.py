import schedule
import time
import json
import os
from datetime import datetime
from news_scraper import NewsScraper
from insight_generator import InsightGenerator
from threads_poster import ThreadsPoster
from config import Config

class ThreadsAgent:
    def __init__(self):
        self.scraper = NewsScraper()
        self.generator = InsightGenerator()
        self.poster = ThreadsPoster()
        self.posted_links_file = Config.POSTED_LINKS_FILE
        self.posted_links = self._load_posted_links()

    def _load_posted_links(self):
        """Load previously posted links from file"""
        if os.path.exists(self.posted_links_file):
            try:
                with open(self.posted_links_file, 'r') as f:
                    return set(json.load(f))
            except (json.JSONDecodeError, IOError):
                return set()
        return set()

    def _save_posted_links(self):
        """Save posted links to file"""
        with open(self.posted_links_file, 'w') as f:
            json.dump(list(self.posted_links), f, indent=2)

    def run_daily_post(self):
        """Main function to create and post daily content"""
        print(f"\n{'='*60}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Starting daily post generation...")
        print(f"{'='*60}\n")

        # 1. Fetch latest news
        print("Fetching latest news...")
        articles = self.scraper.fetch_latest_news(hours_back=48)

        if not articles:
            print("No relevant articles found")
            return

        print(f"Found {len(articles)} relevant articles\n")

        # 2. Filter out already posted articles
        new_articles = [a for a in articles if a['link'] not in self.posted_links]

        if not new_articles:
            print("All recent articles already posted")
            return

        # 3. Select most relevant article
        article = new_articles[0]
        print(f"Selected article:")
        print(f"   Title: {article['title']}")
        print(f"   Source: {article['source']}")
        print(f"   Relevance Score: {article.get('relevance_score', 0)}")
        print(f"   Link: {article['link']}\n")

        # 4. Generate insight
        print("Generating insight with Neoma's voice...")
        try:
            post_content = self.generator.generate_insight(article)

            print(f"\n{'-'*60}")
            print("Generated Post:")
            print(f"{'-'*60}")
            print(post_content)
            print(f"{'-'*60}")
            print(f"Character count: {len(post_content)}/490\n")

        except Exception as e:
            print(f"Error generating insight: {e}")
            return

        # 5. Post to Threads
        print("Posting to Threads...")
        result = self.poster.create_post(post_content)

        if result['success']:
            print(f"Successfully posted!")
            print(f"   Thread ID: {result['thread_id']}")
            self.posted_links.add(article['link'])
            self._save_posted_links()  # Persist to file
            print(f"   Saved to posted links ({len(self.posted_links)} total)")
        else:
            print(f"Failed to post: {result['error']}")

        print(f"\n{'='*60}\n")

    def start_scheduler(self):
        """Start the daily scheduler"""
        # Schedule for 9 AM and 2 PM daily (Sydney time - for local runs)
        schedule.every().day.at("09:00").do(self.run_daily_post)
        schedule.every().day.at("14:00").do(self.run_daily_post)

        print("Neoma Threads Agent Started")
        print("Scheduled: Daily at 9:00 AM and 2:00 PM")
        print("Press Ctrl+C to stop\n")

        # Run immediately on start (optional - comment out if you want to wait for scheduled time)
        print("Running initial post now...")
        self.run_daily_post()

        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

if __name__ == "__main__":
    import sys
    agent = ThreadsAgent()

    if "--once" in sys.argv:
        # Single run mode (for GitHub Actions)
        agent.run_daily_post()
    else:
        # Continuous scheduler mode
        agent.start_scheduler()
