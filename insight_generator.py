import anthropic
from config import Config


class InsightGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)

    def generate_insight(self, article):
        """Generate an insightful take on a news article"""

        prompt = f"""You are a thought leader in workforce transformation and AI.

Given this news article:
Title: {article['title']}
Summary: {article['summary'][:500]}
Link: {article['link']}

Generate a compelling Threads post (max 450 characters) that:
1. Highlights a key insight or implication for the workforce/tech industry
2. Adds original perspective - don't just summarize
3. Ends with a relevant question or call-to-action
4. Is conversational and engaging
5. Does NOT use hashtags or emoji

Format: Just the post text, nothing else."""

        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )

        post_text = message.content[0].text.strip()

        # Add link at the end
        full_post = f"{post_text}\n\n{article['link']}"

        # Ensure we're under 500 characters
        if len(full_post) > 495:
            # Trim the insight, keep the link
            max_text_length = 490 - len(article['link']) - 2
            post_text = post_text[:max_text_length] + "..."
            full_post = f"{post_text}\n\n{article['link']}"

        return full_post
