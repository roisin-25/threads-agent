"""
Test script to preview voice variations without posting to Threads
Run this to see how different voices handle the same article
"""

from news_scraper import NewsScraper
from insight_generator import InsightGenerator

def test_voice_variations():
    """Generate multiple variations for the same article"""

    print("\n" + "="*70)
    print("NEOMA THREADS AGENT - VOICE TESTING")
    print("="*70 + "\n")

    # Fetch a test article
    scraper = NewsScraper()
    articles = scraper.fetch_latest_news(hours_back=48)  # Wider window for testing

    if not articles:
        print("No articles found. Try adjusting the time window or keywords.")
        return

    # Test with the top article
    article = articles[0]

    print(f"TEST ARTICLE:")
    print(f"   Title: {article['title']}")
    print(f"   Source: {article['source']}")
    print(f"   Relevance Score: {article.get('relevance_score', 0)}")
    print(f"   Link: {article['link'][:50]}...")
    print(f"\n{'-'*70}\n")

    # Generate 3 variations
    generator = InsightGenerator()

    print("Generating 3 voice variations...\n")

    for i in range(3):
        print(f"\n{'='*70}")
        print(f"VARIATION {i+1}")
        print(f"{'='*70}\n")

        post = generator.generate_insight(article)

        print(post)
        print(f"\nLength: {len(post)}/490 characters")
        print(f"{'='*70}\n")

        if i < 2:  # Don't pause after the last one
            input("Press Enter for next variation...")

if __name__ == "__main__":
    test_voice_variations()
