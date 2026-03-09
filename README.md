# Job Search HQ

A system for people who'd rather build a process than scroll LinkedIn hoping something shows up.

Job Search HQ turns your job search into an operations pipeline — with AI-powered scoring, multi-source discovery, application tracking, and tailored CV generation. You define what you want once, then let your AI agent do the filtering, scoring, and busywork.

Not a job board. Not a SaaS. A local-first system you own and run.

---

## Why this exists

Job search is an operations problem disguised as a discovery problem. There are plenty of jobs out there. The hard part is figuring out which ones are actually worth your time — and then not losing track of them in a sea of browser tabs and half-forgotten bookmarks.

Most tools optimize for volume. LinkedIn wants you to scroll more. Easy Apply wants you to click more. Nobody helps you think: "Is this actually good for me?"

I got fired from Wolt. I needed a system, not a spreadsheet. So I built one — with AI scoring against my actual preferences, automated tracking, and a CV pipeline that generates tailored applications in minutes instead of hours. This repo is that system, open-sourced and templatized so you can fork it and make it yours.

It's also a portfolio piece. I build and iterate whether it's for the job or for finding a job. This is what that looks like in practice.

---

## What it does

**Job intake** — you share a posting, the AI does the rest:

```
You: "Process this job posting: https://company.com/careers/ai-engineer"

Agent:
  → Fetches and parses the job description
  → Scores it 7/10 against your profile
    ("remote-first, AI-native, but role skews too junior")
  → Appends to tracking/applications.csv
  → Optionally creates Linear issue + TickTick task
```

**Job discovery** — search across multiple sources at once:

```
You: "Find AI Product Manager jobs in Germany, remote preferred, last 7 days"

Agent:
  → Searches Indeed, LinkedIn, Glassdoor via JobSpy
  → Searches Arbeitsagentur + Arbeitnow via germany_jobs.py
  → Scores all results against your profile
  → Presents ranked table, skips duplicates
```

**Application prep** — tailored CVs and cover letters from a single source:

```
You: "Generate a tailored application for this role"

Agent:
  → Reads your cv.yaml (single source of truth)
  → Generates role-specific CV via RenderCV → PDF
  → Drafts cover letter in your voice → PDF
  → Saves everything to cv/applications/[company-role]/
```

---

## Who this is for

- Senior ICs, founding engineers, technical PMs who are picky about where they work next
- People who want 5 great applications, not 100 spray-and-pray submissions
- Comfortable with CLI and Python (or willing to learn)
- AI-curious — you want to see what AI-native personal ops looks like
- You have specific criteria (location, comp, culture, mission) and want a system that respects them

This is **not** for you if:
- You want to apply to 100 jobs a week (use LinkedIn Easy Apply)
- You're entry-level and just need your first role (this is overkill)
- You want a polished UI with no setup
- You're not comfortable running code locally

---

## Get started (5 minutes)

### 1. Clone and install

```bash
git clone https://github.com/YOUR_USERNAME/job-search-hq.git
cd job-search-hq
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Define your profile

This is the most important step. The system is only as good as the context you give it.

```bash
# Start here — this is the brain of the scoring system:
open profile/target-roles.md
```

Edit `profile/target-roles.md` with your scoring rubric: company tiers, role types, location rules, deal-breakers. Be specific. "I want a PM role" is useless. "Product engineer at a 10-100 person remote-first AI company, 130k+ EUR, where I ship code and own a product area" is excellent.

Then add context documents to `profile/` — identity statement, career narrative, assessment results, writing samples, project artifacts. The more context the AI has, the better it scores and writes. See `profile/README.md` for a full guide with links to assessment tools.

### 3. Set up tracking

```bash
cp tracking/applications.csv.example tracking/applications.csv
# This file is gitignored — your data stays local
```

### 4. Run your first job intake

Open the project in your AI agent of choice and tell it:

> "Process this job posting: https://some-company.com/careers/ai-engineer"

That's it. The agent reads `AGENT.md`, scores the job against your profile, and tracks it.

---

## Pick your agent

This system works with any AI agent that can read markdown files. Three have first-class support:

| Agent | Config file | Workflows | How to run |
|-------|-------------|-----------|------------|
| **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** | `CLAUDE.md` | `.claude/commands/` (slash commands) | Open in VS Code, use `/job-intake`, `/job-discover`, `/weekly-scan` |
| **[Goose](https://block.github.io/goose/)** | `.goosehints` | `recipes/` (YAML) | `goose session start` from project root |
| **[Cursor](https://cursor.sh)** | `.cursorrules` | Chat-based | Open project, chat with agent |
| **Any LLM** | — | — | Paste `AGENT.md` into system prompt, start chatting |

**`AGENT.md` is the shared brain.** It contains all workflow logic — intake, scoring, discovery, application prep, safety rules. The agent config files (CLAUDE.md, .goosehints, .cursorrules) are thin wrappers that point to it.

Adding support for a new agent: create its config file at project root pointing to AGENT.md. That's it.

---

## The scoring system

This is the core of the system. Every job gets a 1–10 score against your `profile/target-roles.md`. It replaces gut-feel scrolling with a structured, repeatable rubric.

### How it works

There are two ways to score:

**Agent-driven scoring** (primary) — you share a job posting with your AI agent. The agent reads `AGENT.md` and your `profile/target-roles.md`, parses the job description, applies your rubric, and returns a score with reasoning. This is the main workflow.

**Automated batch scoring** (`tools/job_scorer.py`) — feed it a CSV of scraped jobs, and it runs each one through GPT-4o-mini with your scoring criteria. Adds `fit_score` and `fit_reasoning` columns. Good for processing 50+ jobs from a discovery run.

### The scoring pipeline

```
Job posting (URL, text, or markdown)
  → Parse: title, company, location, requirements, description
  → Load your rubric: profile/target-roles.md
  → Base score: how well does the role match your tier 1/2/3 targets? (1-10)
  → Apply modifiers: remote? AI-native? builder signals? values-aligned?
  → Apply company tier floor: dream companies start at 7-8 regardless
  → Apply location rules: outside your country + not remote = cap at 5
  → Estimate salary range (if not posted, use market bands from rubric)
  → Rate interview prep level (1-5, how much study this role demands)
  → Final output: score + reasoning + salary estimate + effort flag + prep level
```

### Modifiers (customize these in `profile/target-roles.md`)

| Condition | Modifier |
|-----------|----------|
| Remote-first company | +1.5 |
| Remote-eligible | +1 |
| AI-native product | +1 |
| Builder signals in JD (shipping, building, tools) | +1 |
| Early stage / founding team | +1 |
| Values-aligned (privacy, open source, etc.) | +0.5 |
| Your city office | 0 |
| Other city, office-only | -0.5 |
| Outside your country, not remote | cap at 5 |

### Company tiers

Define floor scores for dream companies — so even a non-obvious role gets considered:

```
Tier 0 (floor 8): Your absolute dream companies — any builder role considered
Tier 1 (floor 7): Great fits — strong preference
Tier 2: Score normally against rubric
```

### Decision bands

| Score | What to do |
|-------|-----------|
| 8-10 | Apply immediately. Prioritize. Write tailored cover letter. |
| 6-7 | Apply with standard tailoring. |
| 4-5 | Apply only if pipeline is thin. |
| 1-3 | Skip or archive. |

### Salary estimation + prep scoring

Two bonus dimensions beyond the 1-10 fit score:

**Salary estimation** — if the posting doesn't list comp, the system estimates from market bands you define in your rubric. Helps you skip roles that are likely below your floor before you invest time.

**Prep level (1-5)** — rates how much interview preparation a role demands relative to your current skills. A dream role that requires 3 months of study scores differently than one you can walk into. The system applies small penalties for high-prep roles so your pipeline naturally surfaces quick wins.

### Fuzzy matching

The scorer doesn't require title exact matches. A role called "Product Engineer" can score as high as "Technical Product Manager" if the JD is 90% PM work. The AI reads intent, not just keywords.

### Calibration

Your rubric needs tuning. Here's how:

1. **Test with known-good jobs.** Score 5 jobs you know are great fits and 5 you know are terrible. Do the scores match your gut?
2. **Adjust modifiers.** If everything scores 7+, your modifiers are too generous. If nothing scores above 6, your requirements are too strict.
3. **Common mistakes:**
   - Too many +1 bonuses → everything clusters at 8-9
   - No deal-breakers or caps → nothing drops below 5
   - Vague rubric → AI guesses, scores are random
4. **Update as you learn.** After scoring 20-30 jobs, you'll spot patterns. Refine the rubric.

### Profile depth = scoring quality

| Profile quality | Scoring behavior |
|----------------|-----------------|
| Empty (just target-roles.md with minimal detail) | Scores cluster at 5-7. The AI is guessing. |
| Basic (rubric + identity doc + narrative) | Scores spread to 3-9. Reasonable accuracy. |
| Deep (5+ profile docs, assessments, writing samples) | Scores match your gut. Cover letters sound like you. |

Investing an afternoon in your profile pays off across every job you score. See `profile/README.md` for what to add.

---

## Tools

Python scripts in `tools/` — all runnable standalone, no AI agent required.

| Script | What it does |
|--------|-------------|
| `germany_jobs.py` | Searches Arbeitsagentur + Arbeitnow. Presets: `--preset ai`, `--preset builder`, `--preset all`. Adapt for your market. |
| `job_scorer.py` | Standalone scoring via OpenAI. Takes a URL or file, returns 1-10 with reasoning. |
| `scraper.py` | Multi-board scraper via python-jobspy (Indeed, LinkedIn, Glassdoor). |
| `render_tailored_cvs.py` | Generates per-role tailored CVs from `cv/cv.yaml` via RenderCV. |
| `md_to_pdf_cover_letter.py` | Converts markdown cover letters to formatted PDFs via fpdf2. |
| `_filter_jobs.py` | Utility filter for job results. |
| `weekly-scan.sh` | Shell script for automated weekly discovery runs. |

```bash
# Examples
.venv/bin/python tools/germany_jobs.py --preset ai --location Berlin
.venv/bin/python tools/job_scorer.py --url "https://company.com/job"
```

---

## MCP integrations (all optional)

MCPs extend what your AI agent can do. None are required — the core loop works without them.

### Core MCPs

| Server | Purpose | Setup |
|--------|---------|-------|
| **JobSpy** | Multi-board job search (Indeed, LinkedIn, Glassdoor, Google) | See `.mcp.json.example` |
| **memory** ([mcp-memory-service](https://github.com/doobidoo/mcp-memory-service)) | Semantic memory across sessions. Local SQLite-vec, no cloud, no API key. | See `.mcp.json.example` |
| **context7** | Documentation lookup for libraries | `npx -y @upstash/context7-mcp` |

### Nice-to-have MCPs

| Server | Purpose |
|--------|---------|
| **Linear** | Kanban board for your job pipeline (issues auto-created per job) |
| **TickTick** | Personal task management (tasks auto-created per job) |
| **CV Forge** | JD parsing and email draft generation |
| **Himalayas** | Remote-only job listings |
| **browsermcp** | Browser automation for scraping login-walled pages |

See `.mcp.json.example` for config templates. Copy to `.mcp.json` and update paths.

### Storing secrets

Use whatever secret manager you already use: environment variables, macOS Keychain, Bitwarden, 1Password, Proton Pass, or a gitignored `.env` file. Just don't commit API keys.

---

## CV and application pipeline

### CV generation

Source of truth: `cv/cv.yaml` (RenderCV format). One YAML file for all your facts — education, experience, skills. Never duplicated, never invented.

```bash
# Build base CV
cd cv && rendercv render cv.yaml

# Build tailored CVs (per-role summaries)
.venv/bin/python tools/render_tailored_cvs.py
```

### Cover letters

Write in markdown at `cv/applications/[company-role]/cover-letter.md`, convert to PDF:

```bash
.venv/bin/python tools/md_to_pdf_cover_letter.py
```

### Per-application output

```
cv/applications/acme-ai-engineer/
├── cover-letter.md        # you write this
├── cover-letter.pdf       # generated
└── your-name-acme-cv.pdf  # generated (tailored)
```

---

## Project structure

```
job-search-hq/
├── AGENT.md                 # shared agent brain (all workflow logic)
├── CLAUDE.md                # Claude Code config
├── .goosehints              # Goose config
├── .cursorrules             # Cursor config
├── CONTRIBUTING.md
├── requirements.txt
│
├── profile/                 # YOUR context — the brain of scoring
│   ├── target-roles.md      # scoring rubric (customize first!)
│   ├── README.md            # guide: what to add + assessment links
│   └── [your docs]          # identity, narrative, assessments, writing samples
│
├── tracking/                # application log (gitignored)
│   ├── applications.csv     # your data (not committed)
│   └── applications.csv.example
│
├── tools/                   # Python scripts
│   ├── germany_jobs.py      # regional job board search
│   ├── job_scorer.py        # standalone AI scoring
│   ├── scraper.py           # multi-board scraper
│   ├── render_tailored_cvs.py
│   ├── md_to_pdf_cover_letter.py
│   └── weekly-scan.sh
│
├── cv/                      # CV pipeline
│   ├── cv.yaml.example      # RenderCV template
│   ├── build.sh             # build script
│   └── applications/        # per-company output
│
├── recipes/                 # Goose YAML workflows
├── .claude/commands/        # Claude Code slash commands
├── .mcp.json.example        # MCP config template
└── docs/                    # architecture, research
```

---

## FAQ

**Do I need any MCP servers to start?**
No. The core loop (score → track) works with just your AI agent, `AGENT.md`, and the Python tools. MCPs are additive.

**Do I need a specific AI agent?**
No. Claude Code, Goose, and Cursor have first-class configs. Any LLM that can read `AGENT.md` works.

**What LLM works best?**
Any modern LLM: Claude (recommended), GPT-4o, Gemini. Larger models score better. Claude Sonnet is a good quality/cost balance.

**How much does it cost?**
~$0.01–0.05 per job intake depending on JD length and your LLM. A heavy week (50 intakes) runs ~$1–2.

**The scoring seems wrong for everything.**
Your `profile/target-roles.md` needs more specificity. Test: paste 5 jobs you know are great and 5 you know are terrible. Adjust until scores match your gut.

**Can I use this without Python?**
Barely. You need `pip install` and basic CLI. If that's a stretch, the setup cost may not be worth it.

**This is Germany-focused. What about other countries?**
The `germany_jobs.py` script searches German job boards. Everything else is global. Add your country's boards to `tools/` and update your profile. The scoring system and pipeline are location-agnostic.

---

## License

MIT — do whatever you want with it.

If this helps you land a great role, I'd genuinely love to hear about it.

---

Built by [Vitalii Garan](https://github.com/pleasedodisturb). Builder, not just process. Systems over heroics.
