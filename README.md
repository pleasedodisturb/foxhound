# foxhound

**Track by scent, not by scroll.**

A job search operating system for people who'd rather build a process than refresh LinkedIn hoping something shows up. Local-first, AI-native, agent-agnostic. You define what you want once — foxhound does the filtering, scoring, and busywork.

Not a job board. Not a SaaS. A system you own and run.

> *No relation to Kojima, Konami, or Metal Gear Solid. But if you know, you know — and it forever lives in our hearts.*

---

## The problem

Job search is an operations problem disguised as a discovery problem.

There are plenty of jobs out there. The hard part is figuring out which ones are actually worth your time — and then not losing track of them in a sea of browser tabs, half-finished applications, and "I'll get to it later."

Most tools optimize for volume. LinkedIn wants you to scroll more. Easy Apply wants you to click more. Nobody helps you think: *"Is this actually good for me?"*

I needed a system, not a spreadsheet. So I built one — with AI scoring against my actual preferences, automated tracking, and a CV pipeline that generates tailored applications in minutes instead of hours. This repo is that system, open-sourced and templatized so you can fork it and make it yours.

---

## How it works

Foxhound is a **breed engineered to find things.** Relentless, methodical, nose to the ground. That's the operating model:

```
                    YOUR PROFILE
                   (target-roles.md)
                         │
                    defines scent
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
    ▼                    ▼                    ▼
 DISCOVER             SCORE               TRACK
 ─────────           ─────────           ─────────
 JobSpy MCP          1-10 fit score      applications.csv
 germany_jobs.py     salary estimate     Linear issues
 Arbeitsagentur      prep level 1-5      TickTick tasks
 Himalayas           effort flag
 web search          fuzzy matching
    │                    │                    │
    └────────────────────┼────────────────────┘
                         │
                         ▼
                      APPLY
                   ─────────────
                   tailored CV (RenderCV)
                   cover letter → PDF
                   per-company output
```

### Job intake — share a posting, the AI does the rest

```
You: "Process this job posting: https://company.com/careers/ai-engineer"

Foxhound:
  → Fetches and parses the job description
  → Scores it 7/10 against your profile
    ("remote-first, AI-native, but role skews too junior")
  → Appends to tracking/applications.csv
  → Optionally creates Linear issue + TickTick task
```

### Job discovery — search across multiple sources at once

```
You: "Find AI Product Manager jobs in Germany, remote preferred, last 7 days"

Foxhound:
  → Searches Indeed, LinkedIn, Glassdoor via JobSpy
  → Searches Arbeitsagentur + Arbeitnow via germany_jobs.py
  → Scores all results against your profile
  → Presents ranked table, skips duplicates
```

### Application prep — tailored CVs and cover letters

```
You: "Generate a tailored application for this role"

Foxhound:
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

**Not** for you if:
- You want to apply to 100 jobs a week (use LinkedIn Easy Apply)
- You're entry-level and just need your first role (this is overkill)
- You want a polished UI with no setup
- You're not comfortable running code locally

---

## Get started (5 minutes)

### 1. Clone and install

```bash
git clone https://github.com/pleasedodisturb/foxhound.git
cd foxhound
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Define your profile

This is the most important step. The system is only as good as the context you give it.

```bash
open profile/target-roles.md
```

Edit `profile/target-roles.md` with your scoring rubric: company tiers, role types, location rules, deal-breakers. Be specific. "I want a PM role" is useless. "Product engineer at a 10-100 person remote-first AI company, 130k+ EUR, where I ship code and own a product area" is excellent.

Then add context documents to `profile/` — identity statement, career narrative, assessment results, writing samples. The more context the AI has, the better it scores and writes. See `profile/README.md` for a full guide with links to assessment tools.

### 3. Set up tracking

```bash
cp tracking/applications.csv.example tracking/applications.csv
# This file is gitignored — your data stays local
```

For detailed per-agent setup, MCP configuration, and optional integrations, see [docs/SETUP.md](docs/SETUP.md).

### 4. Run your first job intake

Open the project in your AI agent of choice and tell it:

> "Process this job posting: https://some-company.com/careers/ai-engineer"

That's it. The agent reads `AGENT.md`, scores the job against your profile, and tracks it.

---

## Pick your agent

Foxhound works with any AI agent that can read markdown files. Three have first-class support:

| Agent | Config file | Workflows | How to run |
|-------|-------------|-----------|------------|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | `CLAUDE.md` | `.claude/commands/` (slash commands) | Open in VS Code, use `/job-intake`, `/job-discover`, `/weekly-scan` |
| [Goose](https://block.github.io/goose/) | `.goosehints` | `recipes/` (YAML) | `goose session start` from project root |
| [Cursor](https://cursor.sh) | `.cursorrules` | Chat-based | Open project, chat with agent |
| Any LLM | — | — | Paste `AGENT.md` into system prompt, start chatting |

**`AGENT.md` is the shared brain.** All workflow logic lives there — intake, scoring, discovery, application prep, safety rules. Agent config files are thin wrappers that point to it. Adding support for a new agent = one file.

---

## The scoring system

Every job gets a 1-10 score against your `profile/target-roles.md`. It replaces gut-feel scrolling with a structured, repeatable rubric.

### Two ways to score

**Agent-driven scoring** (primary) — share a job posting with your AI agent. It reads `AGENT.md` and your profile, parses the JD, applies your rubric, returns a score with reasoning.

**Automated batch scoring** (`tools/job_scorer.py`) — feed it a CSV of scraped jobs, runs each through GPT-4o-mini with your scoring criteria. Good for processing 50+ jobs from a discovery run.

### The pipeline

```
Job posting (URL, text, or markdown)
  → Parse: title, company, location, requirements, description
  → Load rubric: profile/target-roles.md
  → Base score: role match against tier 1/2/3 targets (1-10)
  → Modifiers: remote? AI-native? builder signals? values-aligned?
  → Company tier floor: dream companies start at 7-8 regardless
  → Location rules: outside your country + not remote = cap at 5
  → Estimate salary (if not posted, use market bands from rubric)
  → Rate interview prep level (1-5)
  → Final: score + reasoning + salary estimate + effort flag + prep level
```

### Modifiers (customize in `profile/target-roles.md`)

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

### Decision bands

| Score | Action |
|-------|--------|
| 8-10 | Apply immediately. Prioritize. Write tailored cover letter. |
| 6-7 | Apply with standard tailoring. |
| 4-5 | Apply only if pipeline is thin. |
| 1-3 | Skip or archive. |

### Profile depth = scoring quality

| Profile quality | Scoring behavior |
|----------------|-----------------|
| Empty (minimal target-roles.md) | Scores cluster at 5-7. The AI is guessing. |
| Basic (rubric + identity + narrative) | Scores spread to 3-9. Reasonable accuracy. |
| Deep (5+ profile docs, assessments, writing samples) | Scores match your gut. Cover letters sound like you. |

Investing an afternoon in your profile pays off across every job you score.

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
| **JobSpy** | Multi-board search (Indeed, LinkedIn, Glassdoor, Google) | See `.mcp.json.example` |
| **memory** ([mcp-memory-service](https://github.com/doobidoo/mcp-memory-service)) | Semantic memory across sessions. Local SQLite-vec, no cloud. | See `.mcp.json.example` |
| **context7** | Documentation lookup for libraries | `npx -y @upstash/context7-mcp` |

### Nice-to-have MCPs

| Server | Purpose |
|--------|---------|
| **Linear** | Kanban board for your pipeline (issues auto-created per job) |
| **TickTick** | Personal task management (tasks auto-created per job) |
| **CV Forge** | JD parsing and email draft generation |
| **Himalayas** | Remote-only job listings |
| **browsermcp** | Browser automation for scraping login-walled pages |

See `.mcp.json.example` for config templates. Copy to `.mcp.json` and update paths.

---

## CV and application pipeline

### CV generation

Source of truth: `cv/cv.yaml` (RenderCV format). One YAML file for all your facts — education, experience, skills. Never duplicated, never invented.

```bash
cd cv && rendercv render cv.yaml         # base CV
.venv/bin/python tools/render_tailored_cvs.py  # per-role tailored CVs
```

### Cover letters

Write in markdown, convert to PDF:

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
foxhound/
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
│   └── [your docs]          # identity, narrative, assessments, samples
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
└── docs/                    # architecture, setup, research
```

---

## Real-world examples

### "Find me AI roles in Germany"

```
You: "Search for AI Product Manager and AI Engineer jobs in Berlin, remote OK, last 7 days"

Foxhound:
  → Runs germany_jobs.py --preset ai --location Berlin
    Found 23 roles from Arbeitsagentur
    Found 8 roles from Arbeitnow

  → Runs JobSpy MCP: Indeed + LinkedIn + Glassdoor
    Found 41 roles (17 deduplicated)

  → Scores all 55 unique jobs against profile/target-roles.md

  Results:
  ┌────┬───────────────────────┬──────────────────────────┬───────┬──────────┐
  │ #  │ Company               │ Role                     │ Score │ Salary   │
  ├────┼───────────────────────┼──────────────────────────┼───────┼──────────┤
  │ 1  │ Mistral AI            │ Product Engineer          │ 9/10  │ 130-160k │
  │ 2  │ DeepL                 │ AI Product Manager        │ 8/10  │ 110-140k │
  │ 3  │ Hugging Face          │ Solutions Engineer        │ 8/10  │ 120-150k │
  │ 4  │ [startup]             │ Founding Engineer         │ 7/10  │ 90-120k  │
  │ ...│ 51 more scored and ranked                                            │
  └────┴───────────────────────┴──────────────────────────┴───────┴──────────┘

  "Want me to run intake on #1-3?"
```

### "Process this LinkedIn posting"

```
You: share a LinkedIn URL or paste JD text

Foxhound:
  → Parses: "Senior Technical Program Manager — Datadog (Remote EU)"
  → Scores: 7/10
    ✓ Remote-first (+1.5)
    ✓ Observability/AI platform (+1)
    ✗ Title is TPM, not builder role (-0.5)
    ✗ Large org, less autonomy (-0.5)
  → Salary estimate: 140-170k EUR (not posted, estimated from market bands)
  → Prep level: 2/5 (brush up on observability domain)
  → Effort: sweet-spot
  → Added to tracking CSV, Linear issue created

  "Score 7/10. Solid match — remote + AI platform.
   Main risk: could be process-heavy at this org size.
   Worth applying with standard tailoring."
```

### "Run a weekly scan"

```
You: /weekly-scan 6

Foxhound:
  → Searches all sources with your stored keywords
  → Filters: only roles scoring 6+
  → Deduplicates against tracking/applications.csv (skips already-seen)
  → Generates digest:

  Weekly Scan — March 11, 2026
  ────────────────────────────
  New roles found: 12 (above threshold 6/10)
  Sources: Arbeitsagentur (4), Indeed (3), LinkedIn (3), Arbeitnow (2)

  Top picks:
  1. Linear — Product Engineer (9/10) — remote, dream company
  2. Proton — AI Privacy Engineer (8/10) — Geneva, values-aligned
  3. Block — Technical PM, AI (8/10) — remote US/EU

  Already tracked: 7 roles skipped (seen before)
```

### "Generate a tailored application"

```
You: "Create a full application package for the Linear Product Engineer role"

Foxhound:
  → Fetches full JD from Linear's careers page
  → Reads all profile/ docs for voice and context
  → Reads cv/cv.yaml for facts

  Generated:
  cv/applications/linear-product-engineer/
  ├── cover-letter.md     ← drafted in your voice, references your specific projects
  ├── cover-letter.pdf    ← formatted PDF
  └── your-name-linear-cv.pdf  ← tailored CV with role-specific summary

  "Cover letter highlights your [specific project] and [specific skill].
   CV summary reframed for product engineering focus.
   Review the cover letter — I drafted it, you own it."
```

---

## FAQ

**Do I need any MCP servers to start?**
No. The core loop (score, track) works with just your AI agent, `AGENT.md`, and the Python tools.

**Do I need a specific AI agent?**
No. Claude Code, Goose, and Cursor have first-class configs. Any LLM that can read `AGENT.md` works.

**What LLM works best?**
Any modern LLM: Claude (recommended), GPT-4o, Gemini. Larger models score better.

**How much does it cost?**
~$0.01-0.05 per job intake depending on JD length and your LLM. A heavy week (50 intakes) runs ~$1-2.

**The scoring seems wrong for everything.**
Your `profile/target-roles.md` needs more specificity. Test with 5 jobs you know are great and 5 you know are terrible. Adjust until scores match your gut.

**Can I use this without Python?**
Barely. You need `pip install` and basic CLI.

**This is Germany-focused. What about other countries?**
`germany_jobs.py` searches German job boards. Everything else is global. Add your country's boards to `tools/` and update your profile. The scoring system and pipeline are location-agnostic.

---

## License

MIT — do whatever you want with it.

If this helps you land a great role, I'd genuinely love to hear about it.

---

Built by [pleasedodisturb](https://github.com/pleasedodisturb). Systems over heroics.
