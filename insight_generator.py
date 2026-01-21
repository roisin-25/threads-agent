import anthropic
import random
import time
from config import Config

class InsightGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        # Weighted post types - hot_take less frequent than before
        self.post_types = [
            'hot_take',
            'genuine_question',
            'observation',
            'quick_reaction',
            'industry_insight',
            'challenging',
        ]

    def get_post_type_context(self, post_type):
        """Return guidance for each post type"""

        contexts = {
            'hot_take': {
                'description': 'Strong opinion that challenges conventional wisdom',
                'guidance': 'State your opinion directly. No hedging. Be sharp but not mean.',
                'examples': [
                    'Skills-based hiring isn\'t radical. Requiring a degree for a job that doesn\'t need one is what\'s radical.',
                    '"Talent shortage" is code for "we haven\'t looked internally yet."',
                    'Everyone\'s hiring AI engineers. Nobody\'s asking who on their team could become one.'
                ]
            },
            'genuine_question': {
                'description': 'Actually curious, not rhetorical performance',
                'guidance': 'Ask something you genuinely want to know. Don\'t already have the answer in your head.',
                'examples': [
                    'Genuinely curious - anyone actually seen DEI budget increases this year? Or is everyone just reshuffling what they had?',
                    'Has anyone figured out a good way to measure upskilling ROI? Everything I\'ve seen feels hand-wavy.',
                    'What am I missing here? This seems like it should be obvious but I keep seeing smart people disagree.'
                ]
            },
            'observation': {
                'description': 'Dry humor, industry absurdities, relatable moments',
                'guidance': 'Notice something funny or absurd. Don\'t over-explain the joke.',
                'examples': [
                    'Love how every job posting wants "5+ years experience" in a technology that\'s existed for 3 years.',
                    'The number of "AI strategy" decks I\'ve seen that are just "use ChatGPT" with extra steps.',
                    'Three coffees deep and finally making sense of these retention numbers.'
                ]
            },
            'quick_reaction': {
                'description': 'Short, in-the-moment response to news',
                'guidance': 'Keep it brief. One or two sentences max. Show genuine reaction.',
                'examples': [
                    'Well that\'s depressing.',
                    'Finally.',
                    'This is the part everyone keeps missing.'
                ]
            },
            'industry_insight': {
                'description': 'Connect dots others miss, reveal what\'s really at stake',
                'guidance': 'Share a non-obvious connection. What does this actually mean for people?',
                'examples': [
                    'The interesting question isn\'t whether this will work - it\'s what happens when it scales.',
                    'Third time this quarter I\'ve seen this pattern. Something\'s shifting.',
                    'Everyone\'s focused on the headline. The real story is in paragraph five.'
                ]
            },
            'challenging': {
                'description': 'Push back on something that seems off',
                'guidance': 'Be direct but not aggressive. Point out the flaw.',
                'examples': [
                    'I keep seeing this stat shared but the methodology is dodgy. Sample size of 200 and self-reported.',
                    'This sounds good until you think about who actually benefits.',
                    'Respectfully, this misses the point entirely.'
                ]
            }
        }

        return contexts[post_type]

    def generate_insight(self, article):
        """Generate an insightful take on a news article using Neoma's brand voice"""

        # Randomly select a post type for variety
        post_type = random.choice(self.post_types)
        post_context = self.get_post_type_context(post_type)

        prompt = f"""You are writing a Threads post for Neoma AI, an Australian company focused on workforce transformation and helping people reach their potential.

NEOMA'S CORE VALUES:
- We care about people and positively impacting the world
- We believe in driving innovation while finding opportunities for business growth
- We think companies should invest in their people, not just replace them
- We're pragmatic about business outcomes, but never lose sight of the human element

TARGET AUDIENCE:
Leaders in tech, AI, HR, and talent strategy who care about the future of work, technology's impact on society, and business innovation

POST TYPE: {post_type.upper().replace('_', ' ')}
What this is: {post_context['description']}
Guidance: {post_context['guidance']}

Examples of this post type:
{chr(10).join('- ' + ex for ex in post_context['examples'])}

ARTICLE:
Title: {article['title']}
Summary: {article['summary'][:600]}
Link: {article['link']}

SOUND HUMAN - THIS IS CRITICAL:
- Vary sentence length. Some short. Some longer and more rambling.
- Incomplete thoughts are fine. You don't need to wrap everything up neatly.
- Use contractions (don't, isn't, we're, that's)
- Fragments are good. "Finally." or "This." or "Ugh."
- Skip the call-to-action. Not everything needs "What do you think?" at the end.
- Be messy. Real people don't write in perfect parallel structure.

AVOID THESE AI TELLS:
- No "Here's the thing:" or "Hot take:" labels - just say it
- No "I'm excited to share" or "game-changer" or "dive into" or "let's explore"
- No perfect parallel structure in every sentence
- No predictable hook → explanation → question pattern
- Don't acknowledge both sides of everything - just have an opinion
- Don't over-explain. Trust people to get it.

INSTRUCTIONS:
1. Respond to what the article is ACTUALLY about - don't force a workforce angle if it doesn't fit
2. Match the post type - if it's a quick_reaction, keep it to 1-2 sentences max
3. Write like a real person on social media, not a brand account
4. NO hashtags, NO emojis, NO exclamation marks
5. CRITICAL: Maximum 380 characters. End with a complete thought.

Write ONLY the post text - nothing else."""

        # Retry up to 3 times for transient API errors
        max_retries = 3
        for attempt in range(max_retries):
            try:
                message = self.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=400,
                    messages=[{"role": "user", "content": prompt}]
                )
                break
            except anthropic.APIStatusError as e:
                if e.status_code == 529 and attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 10  # 10s, 20s, 30s
                    print(f"API overloaded, retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                else:
                    raise

        post_text = message.content[0].text.strip()

        # Clean up any markdown or extra formatting
        post_text = post_text.replace('**', '').replace('*', '').replace('#', '')

        # Add link at the end
        full_post = f"{post_text}\n\n{article['link']}"

        # Ensure we're under 490 characters total
        if len(full_post) > 490:
            # Calculate max text length (leave room for link + newlines)
            max_text_length = 485 - len(article['link']) - 4

            # Try to find a complete sentence ending
            truncated = post_text[:max_text_length]

            # Look for the last sentence-ending punctuation
            last_period = truncated.rfind('.')
            last_question = truncated.rfind('?')
            last_sentence_end = max(last_period, last_question)

            if last_sentence_end > len(truncated) * 0.5:  # Only use if we keep at least half
                post_text = truncated[:last_sentence_end + 1]
            else:
                # Fall back to word boundary with ellipsis
                post_text = truncated.rsplit(' ', 1)[0] + "..."

            full_post = f"{post_text}\n\n{article['link']}"

        return full_post
