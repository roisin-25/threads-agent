# NEOMA THREADS AGENT - VOICE & CONTENT UPDATES

## 🎯 What Changed

### 1. **Brand Voice Implementation (insight_generator.py)**

Added three distinct voice variations that rotate randomly:

#### PROVOCATEUR
- **Persona**: The challenger who questions conventional wisdom
- **Style**: Sharp, contrarian, calls out what others won't say
- **When it shines**: Challenging weak assumptions, pointing out blind spots, pushing back on hype
- **Example**: "Another article claiming upskilling fails. Funny how they never measure programs that actually last longer than 8 weeks."

#### OPTIMISTIC BUILDER
- **Persona**: The solutions-focused practitioner building the future
- **Style**: Constructive, energizing, shows what works
- **When it shines**: Highlighting wins, showing the path forward, connecting to Neoma's solutions
- **Example**: "The best talent strategy isn't hiring more people. It's seeing what your people can become."

#### INDUSTRY INSIDER
- **Persona**: The voice from the trenches sharing what's really happening
- **Style**: Behind-the-scenes insights, real client experiences, non-obvious patterns
- **When it shines**: Connecting news to actual implementation, revealing what's working in practice
- **Example**: "We're seeing this play out with our enterprise clients right now - the bottleneck isn't skills, it's internal mobility processes."

### 2. **Content Filtering Upgrades (news_scraper.py + config.py)**

#### Relevance Scoring System
Articles now get scored based on:
- **Australian context** (+3 points per match): Australian policy, companies, locations
- **Strategic signals** (+2 points per match): enterprise transformation, workforce planning, ROI, business case
- **Keyword matches** (+1 point per match): AI, upskilling, talent, etc.

The agent now selects the most relevant article, not just the most recent.

#### Enhanced News Sources
Added Australian sources:
- SMH Technology
- AFR Technology  
- InnovationAus

Kept global sources for international context:
- TechCrunch
- The Verge
- Wired
- Hacker News

#### Expanded Keywords
Now captures broader workforce transformation content:
- Added: layoffs, redundancies, redeployment, career transition
- Added: skills gap, recruitment, hiring trends, tech careers

### 3. **Neoma's Mission Integration**

The AI now understands and uses Neoma's core beliefs:
- ✅ Companies should invest in existing workforce, not replace them
- ✅ "Talent shortages" often mask poor internal capability assessment  
- ✅ Alternative hiring pathways create better outcomes
- ✅ Workforce transformation needs data, not just good intentions
- ✅ ROI and business outcomes matter - pragmatic, not idealistic

**The agent will challenge OR amplify based on alignment with these principles.**

### 4. **Technical Updates**
- Character limit: 500 → 490
- Better logging: Shows voice type, relevance score, character count
- Improved post formatting: Removes markdown artifacts, cleaner output

---

## 🧪 Testing Your New Voice

### Quick Test (Without Posting)
```bash
python test_voices.py
```

This will:
1. Fetch a real article
2. Generate 3 different voice variations
3. Show you character counts
4. Let you compare approaches

### Full Test (With Posting - Be Careful!)
```bash
python main.py
```

This will immediately generate and post one article, then wait for the 9 AM daily schedule.

**Pro tip**: Comment out the `self.run_daily_post()` line in `main.py` if you want to wait for the scheduled time instead of posting immediately.

---

## 📝 Example Output Comparison

**Same article, three different voices:**

### Article
*"Microsoft announces new AI-powered HR analytics tool"*

### Provocateur
"Everyone's launching 'AI-powered HR tools.' How many actually solve for internal capability assessment vs just adding another dashboard?"

### Optimistic Builder  
"This is the direction we need - turning workforce data into action. The question now: who's building the frameworks to use these insights for actual transformation?"

### Industry Insider
"Interesting. Three clients asked us about exactly this type of tool last month. The gap we keep seeing? Integration with existing learning systems."

---

## 🎚️ Fine-Tuning Options

If after testing you want to adjust:

### Make One Voice More Prominent
In `insight_generator.py`, change:
```python
voice_type = random.choice(self.voices)
```

To weighted selection:
```python
voice_type = random.choices(
    self.voices, 
    weights=[0.2, 0.5, 0.3]  # [provocateur, builder, insider]
)[0]
```

### Adjust Australian Preference
In `config.py`, change the scoring multipliers:
```python
score += australian_matches * 5  # Increase from 3
score += relevance_matches * 2   # Keep same
score += keyword_matches          # Keep same
```

### Add More Voice Examples
In `insight_generator.py`, add more examples to each voice's `examples` list to further guide the style.

### Change Posting Time
In `main.py`, change:
```python
schedule.every().day.at("09:00").do(self.run_daily_post)
```

To your preferred time (24-hour format).

---

## 📊 Monitoring Your Posts

The agent now logs:
- Relevance score of selected article
- Character count of generated post
- Voice type used (visible in logs if you add print statement)
- Success/failure status

Consider tracking over time:
- Which voice gets more engagement
- Australian vs. international content performance
- Topic categories that resonate

---

## ⚠️ Important Notes

1. **Voice Variety**: The agent randomly selects a voice each time. Over a week, you'll see a natural mix.

2. **Challenge vs. Amplify**: The AI decides whether to push back on or amplify the article based on alignment with Neoma's mission. You might see both types.

3. **Australian Context**: Articles with Australian indicators get boosted in selection, but global news that impacts Australians will still appear.

4. **Character Limit**: Now 490 (was 500) to ensure the full post with link fits comfortably.

5. **No Hashtags/Emojis**: Following your preference for intelligent, professional content without typical social media markers.

---

## 🚀 Next Steps

1. **Run test_voices.py** to see the variations
2. **Review** the generated posts - do they sound like Neoma?
3. **Adjust** voice examples if needed
4. **Deploy** when satisfied

Remember: You can always refine the voice prompts further based on what you see. The examples in each voice definition are what guide the AI's tone most directly.