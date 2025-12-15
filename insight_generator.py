import anthropic
import random
import time
from config import Config

class InsightGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.voices = ['provocateur', 'optimistic_builder', 'industry_insider']

    def get_voice_context(self, voice_type):
        """Return the persona and style for each voice type"""

        contexts = {
            'provocateur': {
                'persona': 'the challenger who questions conventional wisdom',
                'style': 'Push back on assumptions. Be sharp and contrarian. Call out what others won\'t say. Ask the question nobody else is asking.',
                'examples': [
                    'Everyone\'s debating whether Australia\'s social media ban is good policy. Almost nobody\'s asking: why are social media companies allowed to build software deemed too dangerous for kids in the first place?',
                    '"Talent shortage" is code for "we haven\'t looked internally yet."',
                    'Everyone\'s hiring AI engineers. Nobody\'s asking who on their team could become one.'
                ]
            },
            'optimistic_builder': {
                'persona': 'the solutions-focused thinker who sees opportunity in challenges',
                'style': 'Focus on what\'s possible. Find the opportunity for positive change. Ask how we can make things better.',
                'examples': [
                    'Australia\'s teen social media ban is a forcing function for platforms to rethink engagement models. How can they pivot so the perception shifts from net-negative to net-positive?',
                    'The best talent strategy isn\'t hiring more people. It\'s seeing what your people can become.',
                    'Love seeing this: companies realizing their existing team has untapped potential. That\'s the unlock.'
                ]
            },
            'industry_insider': {
                'persona': 'the informed observer connecting dots others miss',
                'style': 'Share non-obvious insights. Connect this news to broader patterns. Reveal what\'s really at stake.',
                'examples': [
                    'Australia\'s moving first on under-16 social media bans while the rest of the world watches. The interesting question isn\'t whether it\'ll work - it\'s what happens when tech companies are forced to verify age at scale.',
                    'This is the third major policy shift this quarter signaling the same thing: the era of "move fast and break things" is over.',
                    'Interesting timing. This aligns with a pattern we\'re seeing across the industry.'
                ]
            }
        }

        return contexts[voice_type]

    def generate_insight(self, article):
        """Generate an insightful take on a news article using Neoma's brand voice"""

        # Randomly select a voice for variety
        voice_type = random.choice(self.voices)
        voice_context = self.get_voice_context(voice_type)

        prompt = f"""You are writing a Threads post for Neoma AI, an Australian company focused on workforce transformation and helping people reach their potential.

NEOMA'S CORE VALUES:
- We care about people and positively impacting the world
- We believe in driving innovation while finding opportunities for business growth
- We think companies should invest in their people, not just replace them
- We're pragmatic about business outcomes, but never lose sight of the human element

TARGET AUDIENCE:
Leaders in tech, AI, HR, and talent strategy who care about the future of work, technology's impact on society, and business innovation

VOICE FOR THIS POST: {voice_type.upper()}
Persona: You are {voice_context['persona']}
Style: {voice_context['style']}

Examples of this voice:
{chr(10).join('- ' + ex for ex in voice_context['examples'])}

ARTICLE:
Title: {article['title']}
Summary: {article['summary'][:600]}
Link: {article['link']}

INSTRUCTIONS:
1. Respond to what the article is ACTUALLY about - don't force a workforce/upskilling angle if it doesn't fit
2. Find the most interesting angle: policy implications, business opportunity, human impact, or what everyone's missing
3. If workforce transformation IS genuinely relevant, weave it in naturally
4. Write in Neoma's voice: witty, intelligent, relevant, NOT corporate
5. Make it feel human - use contractions, conversational flow
6. NO hashtags, NO emojis, NO exclamation marks unless truly warranted
7. End with a thought-provoking question OR a clear takeaway (not both)
8. CRITICAL: Maximum 380 characters. End with a complete thought.

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
