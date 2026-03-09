# Profile — Your Context Library

This directory is the brain of the scoring system. Everything here helps the AI understand who you are, what you want, and what you won't settle for. The richer your profile, the better the scoring — and the more authentic your cover letters.

This is not a résumé folder. It's a context library.

---

## The one file you must fill in

**`target-roles.md`** — your scoring rubric. Company tiers, role types, location rules, deal-breakers, dream companies. This is what the AI scores every job against. Without it, scores are generic guesses. With it, they match your gut.

Everything else in this directory is optional but high-leverage.

---

## What to put here

Add anything that helps the AI understand you as a professional and as a person. There are no wrong formats — markdown, PDFs, images, audio transcripts, whatever you have. The categories below are suggestions, not requirements.

### Professional identity

Write a 1-page document about who you are professionally. Not your CV — the honest version. What you bring, what you want, what environments make you thrive, what environments kill you.

Example file: `identity.md`

### Personality and cognitive assessments

If you've taken any of these, drop the results here. They give the AI remarkably useful signal for scoring cultural fit and writing in your voice.

| Assessment | What it measures | Where to take it |
|------------|-----------------|------------------|
| [CliftonStrengths](https://www.gallup.com/cliftonstrengths/) | Top strengths (out of 34) | $20-50 via Gallup |
| [16Personalities](https://www.16personalities.com/) | MBTI-style personality type | Free |
| [Big Five / OCEAN](https://bigfive-test.com/) | Openness, conscientiousness, extraversion, agreeableness, neuroticism | Free |
| [DISC](https://www.discprofile.com/) | Communication and work style | Various providers |
| [Criteria Corp (CCAT, EPP)](https://www.criteriacorp.com/) | Cognitive aptitude + personality | Often taken during hiring processes |
| [Hogan Assessment](https://www.hoganassessments.com/) | Personality, values, derailers | Usually employer-provided |
| [StrengthsFinder 2.0](https://www.gallup.com/cliftonstrengths/) | Same as CliftonStrengths (older name) | Book + online code |

You don't need all of these. Even one assessment adds meaningful context. If you've taken something during a past hiring process, that counts — dig up the results PDF.

Example files: `strengths-gallup.md`, `personality-16p.md`, `cognitive-ccat.pdf`

### Career narrative

Your story. Not bullet points — the narrative. What happened at your last job, why you left (or were let go), what you learned, what you're looking for now. The AI uses this to write cover letters that sound like you, not like a template.

Be honest. If you got fired, say so. If you burned out, say so. The AI doesn't judge — it just needs context to represent you accurately.

Example file: `narrative.md`

### Writing samples

Emails, Slack messages, documents, blog posts, internal memos — anything that shows how you actually communicate. The AI learns your voice patterns from these.

The more natural the better. A Slack thread where you explained a technical decision is more useful than a polished blog post.

Example files: `writing-slack-samples.md`, `writing-blog-posts.md`

### Project artifacts

Evidence of what you've built. This makes cover letters specific instead of generic.

- Screenshots of dashboards, tools, or products you built
- Architecture diagrams
- Code snippets (especially if you're targeting technical roles)
- Demo videos or recordings
- Presentation slides
- Conference talks (links or transcripts)

Example files: `project-crm-migration.md`, `project-ai-pipeline.md`, `demo-screenshot.png`

### Professional profiles

- LinkedIn export (you can request your data from LinkedIn settings)
- Portfolio site content
- GitHub profile README
- Conference speaker bio

Example files: `linkedin-export.md`, `portfolio.md`

### Values and priorities

What matters to you beyond compensation and title. Privacy? Open source? Climate? Diversity? European sovereignty? This helps the scoring system weight companies that align with your values.

Also: what you won't do. Companies you'd never work for, industries that are deal-breakers, environments you know are toxic for you.

Example file: `values.md`

### Anything else

The system can use anything you throw at it:

- Feedback from managers or peers
- Performance review snippets
- Whiteboard photos from brainstorming sessions
- Audio transcripts (meetings, voice notes about what you want)
- Photos of things you've built
- Interview prep notes (what questions you ask, what you look for)

The principle: **if it helps someone understand who you are and what you've done, it helps the AI too.**

---

## Profile depth = scoring quality

| Profile quality | What happens |
|----------------|-------------|
| **Empty** (just target-roles.md) | Scores are 5-7 for everything. The AI is guessing. |
| **Basic** (identity + target-roles + narrative) | Scores spread to 3-9. Reasonable accuracy. |
| **Deep** (5+ documents, assessments, writing samples) | Scores match your gut. Cover letters sound like you. |

Investing an afternoon in your profile pays off across every job you score and every application you write. It's the highest-leverage time you'll spend with this system.

---

## File naming

No strict convention. Just be descriptive:

```
profile/
├── target-roles.md          # required — scoring rubric
├── identity.md              # who you are
├── narrative.md             # your career story
├── values.md                # what matters to you
├── strengths-gallup.md      # CliftonStrengths results
├── personality-16p.md       # 16Personalities results
├── writing-samples.md       # how you communicate
├── project-ai-pipeline.md   # evidence of what you built
└── linkedin-export.md       # professional profile
```

---

## Privacy note

This directory is committed to git by default (so your AI agent can read it). If your repo is public, think about what you're comfortable sharing. You can:

- Keep the repo private
- Add sensitive files to `.gitignore`
- Use a separate private repo for profile/ and symlink it
- Keep only the rubric (`target-roles.md`) committed and load the rest locally
