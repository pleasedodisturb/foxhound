# Architecture

How the system works, what talks to what, and why it's built this way.

---

## Three layers

```
┌──────────────────────────────────────────────────────────────┐
│  LAYER 1: YOU + YOUR AI AGENT                                │
│                                                              │
│  "Process this job: https://..."    "Find AI PM jobs in DE"  │
│                                                              │
│  Claude Code │ Goose │ Cursor │ Any LLM                      │
│  CLAUDE.md   │ .goosehints │ .cursorrules │ paste AGENT.md   │
└──────────────────────┬───────────────────────────────────────┘
                       │ natural language
                       ▼
┌──────────────────────────────────────────────────────────────┐
│  LAYER 2: WORKFLOW ENGINE                                    │
│                                                              │
│  AGENT.md (shared brain)                                     │
│  ├── Job intake workflow (parse → score → track)             │
│  ├── Job discovery workflow (search → score → rank)          │
│  ├── Application prep workflow (CV + cover letter)           │
│  ├── Scoring rubric pointer → profile/target-roles.md        │
│  └── Safety rules (never delete CSV, always confirm)         │
│                                                              │
│  Agent configs are thin wrappers that point here.            │
└────────┬──────────────────────────────┬──────────────────────┘
         │                              │
         ▼                              ▼
┌─────────────────────┐  ┌─────────────────────────────────────┐
│  MCP SERVERS         │  │  PYTHON TOOLS                       │
│  (optional)          │  │  (standalone, no agent required)    │
│                      │  │                                     │
│  JobSpy → multi-board│  │  germany_jobs.py → regional boards  │
│  memory → persistence│  │  job_scorer.py  → batch scoring     │
│  Linear → kanban     │  │  scraper.py     → multi-board       │
│  TickTick → tasks    │  │  render_tailored_cvs.py → CVs       │
│  Himalayas → remote  │  │  md_to_pdf_cover_letter.py → PDFs   │
└────────┬────────────┘  └──────────────┬──────────────────────┘
         │                              │
         ▼                              ▼
┌──────────────────────────────────────────────────────────────┐
│  LAYER 3: YOUR DATA (all local)                              │
│                                                              │
│  profile/               tracking/              cv/           │
│  ├── target-roles.md    ├── applications.csv   ├── cv.yaml   │
│  ├── identity.md        │   (gitignored)       ├── build.sh  │
│  ├── narrative.md       │                      └── apps/     │
│  └── [your docs]        └── action-log.md          [co]/     │
│                                                              │
│  Everything is markdown, CSV, or YAML. No database.          │
│  Git tracks strategy. CSV tracks applications.               │
└──────────────────────────────────────────────────────────────┘
```

---

## Scoring flow

This is the core logic. Everything else is plumbing.

```
Job posting (URL, markdown, or pasted text)
│
├─ 1. PARSE
│  Extract: company, role title, location, remote status,
│  requirements, salary (if mentioned), description summary
│
├─ 2. LOAD RUBRIC
│  Read profile/target-roles.md:
│  - Company tier lists (dream → good → normal)
│  - Role type targets (tier 1, 2, 3)
│  - Scoring modifiers (remote, AI, builder signals, values)
│  - Location rules and salary floor
│  - Anti-patterns and deal-breakers
│
├─ 3. BASE SCORE
│  How well does this role match your tier 1/2/3 targets?
│  AI uses fuzzy matching — reads intent, not just title keywords
│  "Product Engineer" can match "Technical PM" if JD is PM work
│
├─ 4. APPLY MODIFIERS
│  +1.5 remote-first │ +1 AI-native │ +1 builder signals
│  +1 early-stage │ +0.5 values-aligned │ -0.5 wrong city
│  -2 anti-patterns │ cap 5 if outside country + not remote
│
├─ 5. APPLY COMPANY TIER FLOOR
│  Dream company (tier 0)? Score starts at 8 minimum.
│  Great fit (tier 1)? Score starts at 7 minimum.
│
├─ 5b. ESTIMATE SALARY
│  If not posted: estimate from market bands in target-roles.md
│  Flag effort level: sweet-spot / moderate / high-intensity
│
├─ 5c. RATE PREP LEVEL (1-5)
│  How much interview prep does this role demand?
│  Prep 4+: apply scoring penalty (-0.5 to -1.0)
│
├─ 6. FINAL OUTPUT
│  Score (1-10) + reasoning + salary estimate + effort flag
│  + prep level (1-5) + prep notes
│
└─ 7. DECISION BAND
   8-10: Apply now, tailored cover letter
   6-7:  Apply, standard tailoring
   4-5:  Apply only if pipeline is thin
   1-3:  Skip
```

---

## Data flow: end to end

```
DISCOVERY                  SCORING                 TRACKING              APPLICATION
                                                                         PREP
JobSpy MCP ──┐
germany_jobs ─┤            profile/                tracking/             cv/cv.yaml
scraper.py ───┤  jobs ──→  target-roles.md  ──→    applications.csv  ──→ render_tailored
web search ───┘            + AGENT.md rubric       (append row)         _cvs.py
                           = score 1-10                                  ↓
                                                   Linear issue         tailored CV PDF
                                                   (optional)           + cover letter
                                                   TickTick task        PDF in
                                                   (optional)           cv/applications/
```

---

## What file talks to what

```
CLAUDE.md ─────────────┐
.goosehints ───────────┤──→ AGENT.md (shared workflow logic)
.cursorrules ──────────┘         │
                                 ├──→ profile/target-roles.md (scoring rubric)
                                 ├──→ profile/* (context for cover letters)
                                 ├──→ tracking/applications.csv (append rows)
                                 └──→ tools/* (execute scripts)

tools/job_scorer.py ──→ OpenAI API (GPT-4o-mini) + internal criteria
tools/germany_jobs.py ──→ Arbeitsagentur API + Arbeitnow API
tools/scraper.py ──→ python-jobspy (Indeed, LinkedIn, Glassdoor)
tools/render_tailored_cvs.py ──→ cv/cv.yaml ──→ RenderCV ──→ PDF
tools/md_to_pdf_cover_letter.py ──→ cv/applications/*/cover-letter.md ──→ PDF

.mcp.json ──→ MCP servers (JobSpy, memory, Linear, TickTick, etc.)
```

---

## Design principles

**AI-native** — AI is infrastructure (scoring engine, orchestration layer, memory), not a chatbot wrapper bolted onto a spreadsheet.

**Context-rich** — Deep profile enables fuzzy scoring. A role called "Product Engineer" can score 8/10 because the AI understands your intent, not just your keywords.

**Local-first** — CSV, markdown, YAML, git. Your data stays on your machine. Cloud integrations (Linear, TickTick) are opt-in. No database, no server, no vendor lock-in.

**Human decides, AI executes** — AI discovers, scores, and drafts. You approve, override, and apply. This is high-stakes (your career), so the AI accelerates rather than automates.

**Agent-agnostic** — AGENT.md contains all workflow logic in plain markdown any LLM can follow. Agent configs (CLAUDE.md, .goosehints, .cursorrules) are thin wrappers. Adding a new agent = one file.

---

## Key design decisions

**Why CSV, not a database?**
Simple, portable, git-friendly, human-readable, works with pandas/Excel/any tool. No migration hell. Migrate to SQLite if you hit 500+ entries.

**Why AGENT.md as shared brain?**
Each AI tool (Claude Code, Goose, Cursor) reads its config differently. Duplicating workflow logic across three files means three things to maintain and three things to get out of sync. AGENT.md is the single source of truth.

**Why MCP?**
Standardized protocol for AI tool integrations. Composable, growing ecosystem. But nothing depends on it — the Python tools work standalone without any MCP server running.

**Why local-first?**
Job search data is sensitive (companies, contacts, salary negotiations) and permanent (you'll want it in 5 years). Local files + git history beats any SaaS for longevity and control.
