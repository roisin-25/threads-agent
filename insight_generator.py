import anthropic
import random
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
                'style': 'Push back on assumptions. Be sharp and contrarian. Call out what others won\'t say.',
                'examples': [
                    '"Talent shortage" is code for "we haven\'t looked internally yet."',
                    'Another article claiming upskilling fails. Funny how they never measure programs that actually last longer than 8 weeks.',
                    'Everyone\'s hiring AI engineers. Nobody\'s asking who on their team could become one.'
                ]
            },
            'optimistic_builder': {
                'persona': 'the solutions-focused practitioner building the future',
                'style': 'Focus on what works and what\'s possible. Show the path forward. Be constructive and energizing.',
                'examples': [
                    'This is exactly why we built our capability assessment framework - you can\'t transform what you can\'t measure.',
                    'Love seeing this: companies realizing their existing team has untapped potential. That\'s the unlock.',
                    'The best talent strategy isn\'t hiring more people. It\'s seeing what your people can become.'
                ]
            },
            'industry_insider': {
                'persona': 'the voice from the trenches sharing what\'s really happening',
                'style': 'Share behind-the-scenes insights. Connect to real client experiences. Reveal non-obvious patterns.',
                'examples': [
                    'We\'re seeing this play out with our enterprise clients right now - the bottleneck isn\'t skills, it\'s internal mobility processes.',
                    'Interesting timing. Three clients asked us about this exact challenge last month.',
                    'This aligns with what we discovered building our workforce intelligence platform - companies have the data, they just don\'t know how to action it.'
                ]
            }
        }

        return contexts[voice_type]

    def generate_insight(self, article):
        """Generate an insightful take on a news article using Neoma's brand voice"""

        # Randomly select a voice for variety
        voice_type = random.choice(self.voices)
        voice_context = self.get_voice_context(voice_type)

        prompt = f"""You are writing a Threads post for Neoma AI, an Australian workforce transformation company that helps organizations reskill existing employees into tech roles (rather than pursuing layoffs or external hiring).

NEOMA'S MISSION & VIEWPOINTS:
- Companies should invest in their existing workforce, not replace them
- "Talent shortages" often mask poor internal capability assessment
- Alternative hiring pathways (like reskilling) create better outcomes than traditional hiring
- Workforce transformation needs data, not just good intentions
- ROI and business outcomes matter - we're pragmatic, not idealistic

TARGET AUDIENCE:
Leaders in tech, AI, HR, and talent strategy who care about workforce trends and the future of tech careers

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
1. Read the article and decide: does it align with or contradict Neoma's mission?
2. If it aligns: Amplify it, add your angle, show why it matters
3. If it contradicts: Challenge it, but intelligently - point out what's missing or misframed
4. Write in Neoma's voice: witty, intelligent, relevant, NOT corporate or overly professional
5. Make it feel human - use contractions, incomplete sentences if natural, conversational flow
6. NO hashtags, NO emojis, NO exclamation marks unless truly warranted
7. End with a thought-provoking question OR a clear takeaway (not both)
8. If Australian context is relevant, weave it in naturally
9. Maximum 440 characters for your insight (leaves room for link)

Write ONLY the post text - nothing else."""

        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )

        post_text = message.content[0].text.strip()

        # Clean up any markdown or extra formatting
        post_text = post_text.replace('**', '').replace('*', '').replace('#', '')

        # Add link at the end
        full_post = f"{post_text}\n\n{article['link']}"

        # Ensure we're under 490 characters total
        if len(full_post) > 490:
            # Trim the insight, keep the link
            max_text_length = 485 - len(article['link']) - 2
            post_text = post_text[:max_text_length].rsplit(' ', 1)[0] + "..."
            full_post = f"{post_text}\n\n{article['link']}"

        return full_post
