# AI Job Search & Resume Agent Research

> **Date:** 2026-03-11
> **Purpose:** Survey open-source AI job search agents, resume matchers, and automation tools. Extract patterns and implementation ideas applicable to Job Search HQ.

---

## Table of Contents

1. [Landscape Overview](#landscape-overview)
2. [Job Search & Orchestration Agents](#job-search--orchestration-agents)
3. [Resume/CV Matching & Tailoring](#resumecv-matching--tailoring)
4. [Tracking, UX & Automation](#tracking-ux--automation)
5. [Cross-Project Synthesis](#cross-project-synthesis)
6. [Implementation Roadmap for Job Search HQ](#implementation-roadmap-for-job-search-hq)

---

## Landscape Overview

| Project | Stars | Focus | Stack | Key Innovation |
|---------|-------|-------|-------|----------------|
| **AIHawk** (feder-cr) | ~29,400 | Auto-apply | Python, Selenium | Battle-tested LinkedIn automation, resume facade pattern |
| **Resume-Matcher** (srbhr) | ~24,000 | ATS matching | Python, Ollama | Master resume concept, keyword extraction via textacy |
| **Jobber** (sentient-eng) | ~667 | CLI auto-apply | Python, OpenAI | FSM for agent flows, dual architecture |
| **ApplyPilot** (Pickle-Pixel) | ~619 | Full pipeline | Python, JobSpy, Gemini | 6-stage gated pipeline, dry-run mode |
| **JobSync** (Gsync) | ~281 | Tracker/CRM | Next.js, Prisma, Docker | Rich data model, automation run tracking |
| **resume-job-matcher** (sliday) | ~262 | Scoring | Python, Claude/GPT | Weighted composite scoring, red flag detection |
| **genai-job-agents** (touhi99) | ~60 | Multi-agent search | Python, LangGraph | Supervisor pattern, retry with alt keywords |
| **cv-agents** (0xrushi) | ~26 | Resume tailoring | Python, CrewAI | Adversarial multi-agent refinement loop |
| **JobSearch-Agent** (sreekar2858) | ~18 | Scrape + CV gen | Python, Playwright | SQLite dedup, prompt isolation, anti-detection |
| **VibeHired AI** (ganainy) | — | Full tracker | React, Node, MongoDB | Gmail scanning for auto status updates |
| **job-application-assistant** (dinakajoy) | — | Full-stack | Next.js, Express | Hybrid embedding+LLM scoring, function calling |

---

## Job Search & Orchestration Agents

### 1. AIHawk / Jobs_Applier_AI_Agent

**Repo:** https://github.com/feder-cr/Jobs_Applier_AI_Agent_AIHawk (~29,400 stars)

The dominant open-source job application automation project. Media coverage from TechCrunch, Business Insider, The Verge.

**Architecture:**
- Selenium-based LinkedIn automation with Chrome/Chromium
- YAML-driven config: `secrets.yaml`, `work_preferences.yaml`, plain-text resume
- **Suitability scoring gateway:** `JOB_SUITABILITY_SCORE` threshold (default 7) — jobs below are skipped
- **Rate limiting:** `MINIMUM_WAIT_TIME_IN_SECONDS` (60s), `JOB_MAX_APPLICATIONS` (5) per session
- **Resume builder** uses Facade pattern (`resume_facade.py`) with dynamic module loading, template system, style management
- **LLM Manager** abstracts OpenAI/Ollama/Gemini behind unified interface

**Key patterns:**
- Facade pattern for resume generation — clean API hiding template selection, style management, LLM calls, PDF rendering
- Dynamic module loading (`module_loader.py`) — runtime plugin architecture
- Job dataclass with `formatted_job_information()` producing markdown for LLM consumption
- Suitability score as a pipeline gate

**Worth borrowing:**
- Score-gated pipeline (only 7+ proceeds to application)
- LLM provider abstraction layer
- YAML config separation (credentials vs preferences vs resume)

---

### 2. genai-job-agents (LangChain/LangGraph)

**Repo:** https://github.com/touhi99/genai-job-agents (~60 stars)

**Architecture:**
- **Supervisor multi-agent pattern** from LangGraph: one supervisor routes work among 3 workers
- Workers: Analyzer (resume parsing), Searcher (job search), Generator (cover letters)
- `AgentState` TypedDict with accumulating messages via `operator.add`
- Conditional edge routing — supervisor uses LLM function-calling to pick next agent or `FINISH`

**Graph flow:**
```
START → Supervisor → [Analyzer | Searcher | Generator] → Supervisor → ... → FINISH
```

**Key patterns:**
- Supervisor evaluates after each worker whether the query is satisfied
- Worker results returned as HumanMessage so supervisor sees full conversation context
- **Retry logic in Searcher prompt** — instructed to retry with alternative keywords up to 3x
- Multi-LLM support (OpenAI vs Groq/Llama3) with provider-specific token wrappers

**Worth borrowing:**
- Supervisor multi-agent graph — easily extensible (adding a Scorer agent = add node + register)
- `AgentState` TypedDict with accumulating messages
- Prompt retry strategy (try alternative keywords on failure)

---

### 3. JobSearch-Agent (Google ADK / Gemini)

**Repo:** https://github.com/sreekar2858/JobSearch-Agent (~18 stars)

**Architecture:**
- Dual-mode: synchronous CLI (`main.py`) + async FastAPI (`main_api.py`), sharing core pipeline
- **Playwright for scraping** (not Selenium) — advanced anti-detection: random user agents, timezone/language randomization, WebGL/Canvas/WebRTC fingerprint blocking, proxy support, rate limiting
- **SQLite-first storage** with automatic deduplication before downstream processing
- Separate agents for CV writing, cover letter, JD parsing in `src/agents/`
- **Prompt isolation:** All prompts in `src/prompts/`, separate from agent logic

**Module structure:**
```
src/
  agents/          # CV writer, cover letter, JD parser
  prompts/         # Prompt templates (isolated)
  scraper/         # Playwright-based scraping
  tools/           # Utilities
  utils/
    job_search_pipeline.py   # Core orchestrator
    job_database.py          # SQLite + dedup
```

**Worth borrowing:**
- YAML config splitting scraper / AI agent / file configs
- SQLite dedup before any downstream processing
- Prompt isolation pattern (prompts/ directory separate from logic)
- Playwright anti-detection setup

---

### 4. ApplyPilot

**Repo:** https://github.com/Pickle-Pixel/ApplyPilot (~619 stars)

**Architecture:**
- 6-stage pipeline: **Discover → Enrich → Score (1-10) → Tailor Resume → Cover Letter → Auto-Apply**
- Uses JobSpy for discovery, Playwright MCP for browser automation
- Scoring gates: only 7+ proceeds to tailoring stage
- **Dry-run mode** — essential safety pattern for auto-apply

**Key patterns:**
- Explicit scoring gates between pipeline stages
- Resume facts preserved exactly (no fabrication constraint)
- Graceful CAPTCHA degradation
- Lenient/strict validation modes

**Worth borrowing:**
- 6-stage gated pipeline architecture
- Dry-run mode for any automation
- No-fabrication constraint as a first-class concern

---

## Resume/CV Matching & Tailoring

### 5. CV-Matcher (eristavi) — fork of srbhr/Resume-Matcher

**Repo:** https://github.com/eristavi/CV-Matcher

**Scoring approach:**
- **Cohere embeddings** (4096-dim vectors) for keyword extraction
- **Qdrant vector DB** as similarity engine — cosine distance on extracted keywords
- Keywords extracted via Textacy, then embedded (not raw text → focused on skills signal)
- Star graph visualization (NetworkX + Plotly) showing keyword-resume connections

**Worth borrowing:**
- **Keywords-as-vectors, not raw text** — embedding extracted keywords focuses similarity on skills/requirements, not filler
- Qdrant as a pluggable similarity backend
- Visual keyword-resume connection graphs for explainability

---

### 6. JobSensei / resume-matcher (11a55an)

**Repo:** https://github.com/11a55an/resume-matcher (11 stars)

The most detailed scoring rubric found across all projects.

**Dual-score system:**

| Score One: Resume-Job Match | Weight |
|-|--------|
| Keywords & Skills | 30% |
| Experience & Abilities | 25% |
| Requirements & Qualifications | 25% |
| ATS Best Practices | 10% |
| Word Count | 5% |
| Measurable Results | 2.5% |
| Action Verbs | 2.5% |

| Score Two: Qualifications Match | Weight |
|-|--------|
| Skills | 40% |
| Experience/Expertise | 40% |
| Requirements/Qualifications | 20% |

**Key innovation — evidence-mandatory scoring:**
- Each factor produces: `score` (0-100), `weight`, `feedback`, `evidence` (quotes from resume), `missing` (gaps)
- Rubric anchors in prompts: "100%: 5+ distinct quantified achievements; 0%: No numbers mentioned"
- LLM must cite specific resume excerpts — prevents hallucinated scores

**Pydantic model hierarchy:**
```
ResumeSchema > Experience/Education/Project
ScoringFactor > score, weight, feedback, evidence[], missing[]
ScoreOneReport / ScoreTwoReport > ScoringFactor[]
JobSenseiAnalysis > wraps everything
```

**Worth borrowing:**
- Dual-score separation (presentation match vs actual qualification)
- Evidence-based scoring with mandatory citation extraction
- Explicit rubric anchors in prompts for LLM scoring consistency
- Clean Pydantic model hierarchy

---

### 7. smart-agentic-ats-resume (CrewAI)

**Repo:** https://github.com/unikill066/smart-agentic-ats-resume (4 stars)

**Architecture:**
- **CrewAI** with 4 agents: Tech Job Researcher, Personal Profiler, Resume Strategist, Interview Preparer
- Dual interface: Streamlit + CLI
- **GitHub profile as input signal** — pulls real project data to substantiate resume claims

**Worth borrowing:**
- Agent-per-concern separation (research, profile, tailor, interview prep)
- GitHub profile mining for authentic evidence
- History tracking of past tailored resumes with DB persistence
- "Refuses to generate false information" as a prompt-level constraint

---

### 8. Resume Screening App (LangGraph)

**Repo:** https://github.com/haroon-sajid/Resume-Screening-App (3 stars)

**LangGraph DAG with parallel execution:**
```
Resume_agent ──┬──> JD_agent ──────┬──> Recruiter_agent ──> END
               └──> Redflag_agent ─┘
```
- Resume and JD agents run in **parallel**, then converge for final scoring
- Auto-generates Mermaid workflow diagram

**Scoring rubric:**
| Category | Points |
|----------|--------|
| Skills Match | 30 |
| Experience Match | 50 |
| Education Match | 10 |
| Extras (certs, awards) | 10 |

Decision thresholds: >75 = Recommend, 50-75 = Entry-level, <50 = Reject.

**Red Flag Detection (dedicated agent):**
- Frequent job switching (<1 year)
- Employment gaps
- Skill claims without evidence
- Missing education
- Irrelevant experience
- Spelling/grammar issues

**Worth borrowing:**
- Parallel LangGraph execution converging for scoring
- **Red flag agent as a separate concern** (missing from most tools)
- Visual workflow generation via Mermaid
- Fresher vs experienced scoring bifurcation

---

### 9. Resume-Optimizer (naveennk045)

**Repo:** https://github.com/naveennk045/Resume-Optimizer

**Key innovation — prompt template for ATS optimization:**
1. Section ordering: Name > Contact > Summary > Skills > Experience > Education > Projects > Certs
2. Relevance rules: Prioritize JD-matching skills, rearrange bullets for keyword alignment
3. ATS formatting rules: Simple Markdown only, no tables, consistent headings
4. Achievement quantification guidance
5. **Markdown as intermediate format** — clean, portable, easy to diff between raw and optimized

**Worth borrowing:**
- Markdown as the manipulation format between PDF input and PDF output
- Structured ATS formatting rules in prompts
- WeasyPrint for lightweight PDF generation (vs LaTeX)

---

### 10. resume-job-matcher (sliday)

**Repo:** https://github.com/sliday/resume-job-matcher (~262 stars)

**Weighted composite scoring:**
- **AI Match Score (75% weight)** — LLM evaluates content relevance
- **Resume Quality Score (25% weight)** — evaluates presentation quality
- Formula: `(AI_Score × 0.75) + (Quality_Score × 0.25)`, clamped 0-100
- Includes **red flag detection** for critical disqualifiers

**Key patterns:**
- Runtime API selection (Anthropic vs OpenAI)
- Batch processing with progress bars and statistical reporting (mean, median, stddev)
- Can fetch candidate info from personal websites via BeautifulSoup
- Outputs: Markdown and PDF with configurable font presets

**Worth borrowing:**
- Separating content match from presentation quality
- Red flag detection as separate binary concern
- Statistical reporting across batch of applications (mean/median/stddev of match scores)

---

### 11. job-application-assistant (dinakajoy)

**Repo:** https://github.com/dinakajoy/job-application-assistant

**Most architecturally interesting scoring approach — hybrid embedding + LLM:**
1. **Embedding score:** OpenAI `text-embedding-3-small` for both resume and JD → cosine similarity (no vector DB needed)
2. **Score-conditional LLM analysis:** If similarity ≥70% → "why is this a match?"; if <70% → "why is this NOT a match?"
3. Returns `{ score: number, explanation: string }`

**5 service functions (complete pipeline):**
1. `jobDescriptionAnalyzer` — OpenAI function calling with JSON schema → `{skills[], responsibilities[], experience[]}`
2. `resumeForJobDescriptionAnalyzer` — Hybrid embedding + LLM scoring
3. `getResumeImprovements` — Function calling → `{missing_skills[], formatting_tips[], keyword_optimization[]}`
4. `getRewrittenResume` — Structured rewrite with `{summary, skills_section, experience_section, improvements_applied}`
5. `getCoverLetter` / `getEmailContent` — Generation with low temperature (0.5)

**Testing patterns (Jest + Supertest):**
- OpenAI client mocked via `jest.mock("openai")` with `mockImplementation`
- Tests verify both success paths and error handling

**Worth borrowing:**
- **Direct cosine similarity without vector DB** — simplest possible embedding comparison
- **Score-conditional prompting** — different analysis prompts based on numerical threshold
- **Function calling for structured extraction** — schema-enforced output over "return JSON" instructions
- Full pipeline coverage: JD analysis → matching → improvements → rewriting → cover letter → email
- Zustand for lightweight state management

---

## Tracking, UX & Automation

### 12. JobSync

**Repo:** https://github.com/Gsync/jobsync (~281 stars)

**Rich Prisma data model:**
- **Job** — core entity with `statusId` → **JobStatus** lookup table (configurable pipeline stages, not hardcoded enums)
- Fields: `jobUrl`, `description`, `jobType`, `applied`, `appliedDate`, `dueDate`, `matchScore`, `matchData`, `discoveryStatus`, `discoveredAt`
- Relations: Company, JobTitle, JobSource, Location, Interview, Resume, Note, Tag
- **Resume/Profile** — structured sections: ContactInfo, WorkExperience, Education, Certifications
- **Activity/Task** — time tracking with startTime/endTime/duration
- **Automation** — discovery config with `matchThreshold` (default 80), scheduled runs, per-board keywords/location
- **AutomationRun** — execution metrics: jobsSearched, jobsDeduplicated, jobsProcessed, jobsMatched, jobsSaved, status, errorMessage

**Deployment:** Single `docker compose up`. Self-hosted, full data ownership.

**Worth borrowing:**
- **Automation + AutomationRun pattern** — separate schedule definition from execution history with dedup/match metrics
- **matchScore/matchData stored on Job** — scoring as first-class persistent property
- **JobStatus as configurable lookup table** — flexible pipeline stages
- Execution metrics tracking (searched, deduped, processed, matched, saved)

---

### 13. Jobber (Sentient Engineering)

**Repo:** https://github.com/sentient-engineering/jobber (~667 stars)

**Dual architecture:**
1. **`jobber/`** — Multi-agent conversation (planner + browser control). Simpler, more LLM providers.
2. **`jobber_fsm/`** — Finite state machine. States and transitions define workflow. More scalable but requires structured outputs.

**Key patterns:**
- **FSM for long-running agent flows** — models application workflows as explicit state transitions. Agent can only move through valid states (implicit guardrail).
- LangSmith integration for tracing agent decisions
- User preferences in plain text

**Worth borrowing:**
- FSM pattern for any multi-step autonomous flow
- Dual architecture approach: simple version first, FSM when you need reliability
- LangSmith-style observability for agent tracing

---

### 14. cv-agents (0xrushi)

**Repo:** https://github.com/0xrushi/cv-agents (~26 stars)

**Multi-agent adversarial refinement loop:**
1. **Hiring Manager Agent** — critically evaluates resume against JD
2. **CV Editor Agent** — refines formatting, language, content
3. **Job Seeker Agent** — strategizes positioning, selects relevant experiences

Agents loop until resume achieves "top-tier rating." Adversarial pattern: hiring manager creates pressure, editor responds, strategist optimizes.

**Output:** Tailored PDF + **before/after diff PDF** (trust-building UX pattern).

**Worth borrowing:**
- **Multi-agent adversarial refinement** — critic + creator produces higher quality than single-pass generation
- **Diff visualization** — before/after comparison for transparency
- **No-fabrication constraint** — selects and enhances real experiences, never invents

---

### 15. VibeHired AI

**Repo:** https://github.com/ganainy/VibeHired-ai

**Standout feature — Gmail inbox scanning:**
- Auto-detects status changes from emails every 15 minutes
- Surfaces salary info, prep advice, calendar events as independent actions
- **Nothing applied until user confirms** — maintains control while automating detection

Also has: Kanban board, ATS scoring, AI-tailored CVs/cover letters, work logging with voice commands, portfolio builder.

**Worth borrowing:**
- Gmail integration for automatic status updates
- "Detection then confirmation" pattern
- Kanban-style pipeline visualization

---

## Cross-Project Synthesis

### Top Patterns by Category

#### Scoring & Matching
| Pattern | Source | Impact |
|---------|--------|--------|
| Dual-score (match vs qualification) | JobSensei | Distinguish presentation from actual fit |
| Evidence-mandatory scoring with citation | JobSensei | Prevent hallucinated scores |
| Weighted rubric with explicit anchors in prompts | JobSensei | Dramatically improve LLM consistency |
| Hybrid embedding + LLM scoring | job-application-assistant | Fast numerical score + conditional explanation |
| Red flag detection as separate concern | Resume Screening App, resume-job-matcher | Binary disqualifiers checked independently |
| Score-conditional prompting | job-application-assistant | Better explanations when LLM knows direction |
| Statistical reporting (mean/median/stddev) | resume-job-matcher | Insight into targeting accuracy |

#### Architecture & Orchestration
| Pattern | Source | Impact |
|---------|--------|--------|
| Score-gated pipeline stages | AIHawk, ApplyPilot | Only qualified jobs proceed downstream |
| Supervisor multi-agent graph | genai-job-agents | Extensible worker orchestration |
| FSM for long-running flows | Jobber | Prevents invalid state transitions |
| LangGraph DAG with parallel execution | Resume Screening App | Concurrent analysis that converges |
| Adversarial multi-agent refinement | cv-agents | Higher quality than single-pass |
| Prompt isolation directory | JobSearch-Agent | Clean separation of concerns |
| SQLite dedup before processing | JobSearch-Agent | Prevent re-processing |
| Automation + AutomationRun tracking | JobSync | Pipeline health visibility |

#### Resume & Cover Letter Generation
| Pattern | Source | Impact |
|---------|--------|--------|
| Markdown as intermediate format | Resume-Optimizer | Clean, diffable, portable |
| ATS formatting rules in prompts | Resume-Optimizer | Better pass-through rates |
| GitHub profile as input signal | smart-agentic-ats-resume | Authentic evidence |
| Before/after diff visualization | cv-agents | Trust and transparency |
| Master resume + per-application tailoring | Resume-Matcher (srbhr) | Canonical source → variations |
| Function calling for structured extraction | job-application-assistant | Schema-enforced output |
| No-fabrication constraint in prompts | cv-agents, ApplyPilot | Safety and integrity |

#### UX & Data
| Pattern | Source | Impact |
|---------|--------|--------|
| JobStatus as configurable lookup | JobSync | Flexible pipeline stages |
| Gmail scanning for status auto-detection | VibeHired | Pipeline stays current |
| Execution metrics on automation runs | JobSync | Debugging and visibility |
| Dry-run mode | ApplyPilot | Safe testing of automation |
| LangSmith-style observability | Jobber | Agent decision tracing |

---

## Implementation Roadmap for Job Search HQ

Based on the research above, here are the highest-impact improvements organized by effort and value.

### Phase 1: Quick Wins (enhance existing tools)

#### 1.1 Evidence-Based Scoring Upgrade
**Inspired by:** JobSensei, Resume Screening App
**File:** `tools/job_scorer.py`

Current scorer uses GPT-4o-mini with a simple prompt. Upgrade to:
- **Weighted rubric with explicit anchors** in the scoring prompt
- **Evidence extraction** — force the LLM to cite specific JD/profile excerpts for each score dimension
- **Red flag detection** as a separate check (anti-patterns: "native German required", PMBOK-heavy, etc.)
- **Structured output** via Pydantic models or function calling instead of free-text parsing

```python
# Proposed scoring dimensions (adapt weights to profile)
SCORING_RUBRIC = {
    "role_alignment": {"weight": 0.30, "anchors": {"10": "exact match to target roles", "5": "adjacent role", "1": "unrelated"}},
    "tech_stack_fit": {"weight": 0.20, "anchors": {"10": "daily use of listed tools", "5": "some overlap", "1": "no overlap"}},
    "builder_signals": {"weight": 0.15, "anchors": {"10": "shipping, building, 0-to-1", "5": "some building", "1": "pure process"}},
    "company_signals": {"weight": 0.15, "anchors": {"10": "AI-native, remote-first, dream tier", "5": "tech company", "1": "legacy/agency"}},
    "location_remote": {"weight": 0.10, "anchors": {"10": "remote-first", "5": "hybrid/local", "1": "relocation required, wrong country"}},
    "growth_ceiling":  {"weight": 0.10, "anchors": {"10": "leadership path clear", "5": "standard IC", "1": "dead-end role"}},
}
```

#### 1.2 Prompt Isolation
**Inspired by:** JobSearch-Agent
**Current:** Prompts embedded in tool scripts. **Proposed:** Move to `prompts/` directory.

```
prompts/
  scoring_system.md      # System prompt for job scoring
  scoring_rubric.md      # Rubric with anchors
  cover_letter_system.md # System prompt for cover letter generation
  cv_tailor_system.md    # System prompt for CV tailoring
  jd_extraction.md       # Job description structured extraction
```

Benefits: Easier iteration on prompts without touching Python code. Version control on prompt changes. Reusable across different LLM providers.

#### 1.3 Structured JD Extraction
**Inspired by:** job-application-assistant (function calling), JobSensei (Pydantic)

Add a JD extraction step to intake that produces structured data:
```python
class JobDescription(BaseModel):
    title: str
    company: str
    location: str
    remote_policy: Literal["remote-first", "hybrid", "onsite", "unspecified"]
    salary_range: Optional[str]
    skills_required: list[str]
    skills_nice_to_have: list[str]
    experience_years: Optional[str]
    responsibilities: list[str]
    red_flags: list[str]  # anti-patterns detected
    builder_signals: list[str]  # shipping/building/0-to-1 indicators
    company_stage: Optional[str]  # startup/scaleup/enterprise
```

Use Claude function calling or tool_use for structured extraction instead of parsing free text.

### Phase 2: Medium Effort (new capabilities)

#### 2.1 Discovery Pipeline Metrics
**Inspired by:** JobSync (AutomationRun model)

Track execution metrics for each discovery run:
```
tracking/discovery-runs.csv
date,source,keywords,jobs_searched,jobs_deduped,jobs_scored,jobs_above_threshold,new_jobs,duration_sec
```

This gives visibility into pipeline health: Are we searching enough? Is dedup working? What's our hit rate?

#### 2.2 Hybrid Scoring (Embedding + LLM)
**Inspired by:** job-application-assistant, CV-Matcher

Add a fast pre-filter before expensive LLM scoring:
1. Embed profile summary + JD text using a local embedding model (or Claude embeddings API)
2. Compute cosine similarity → fast 0-100 score
3. Only send jobs above embedding threshold (e.g., 50%) to LLM for detailed scoring
4. LLM scoring uses evidence-based rubric from Phase 1

Benefits: 10x faster batch scoring, lower API costs, same quality for top candidates.

#### 2.3 Score-Conditional Analysis
**Inspired by:** job-application-assistant

When presenting scored jobs, generate different analysis based on score:
- **8-10:** "Here's why this is a strong match: [evidence]" + immediate action items
- **5-7:** "Potential fit with gaps: [missing skills/experience]. Worth applying if [conditions]."
- **1-4:** "Poor fit because: [reasons]. Skip unless [specific circumstances]."

#### 2.4 Application Diff Visualization
**Inspired by:** cv-agents

When generating tailored CVs, produce a before/after comparison showing:
- What was emphasized (moved up, expanded)
- What was de-emphasized (moved down, condensed)
- What was added (relevant projects/skills highlighted)
- What was unchanged (core facts preserved)

Output as a markdown diff or side-by-side comparison.

### Phase 3: Ambitious (new architecture patterns)

#### 3.1 Multi-Agent Refinement for Cover Letters
**Inspired by:** cv-agents (adversarial refinement)

Instead of single-pass cover letter generation:
1. **Drafter Agent** — writes initial cover letter from profile + JD
2. **Hiring Manager Agent** — critiques: "Would this make me want to interview this person?"
3. **Editor Agent** — revises based on critique, preserving authentic voice
4. Loop until quality threshold met (max 3 iterations)

Can be implemented within Claude Code's agent framework without external libraries.

#### 3.2 SQLite Job Database
**Inspired by:** JobSearch-Agent, JobSync

Graduate from CSV to SQLite for job tracking:
```sql
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    url TEXT UNIQUE,
    source TEXT,
    status TEXT DEFAULT 'discovered',
    fit_score REAL,
    score_evidence TEXT,  -- JSON: {dimension: {score, evidence, missing}}
    embedding BLOB,       -- for fast similarity search
    jd_structured TEXT,   -- JSON: structured JD extraction
    red_flags TEXT,       -- JSON: list of detected issues
    discovered_at TEXT,
    applied_at TEXT,
    notes TEXT
);

CREATE TABLE discovery_runs (
    id INTEGER PRIMARY KEY,
    run_date TEXT,
    source TEXT,
    keywords TEXT,
    jobs_found INTEGER,
    jobs_new INTEGER,
    jobs_above_threshold INTEGER,
    duration_sec REAL
);

CREATE TABLE score_history (
    id INTEGER PRIMARY KEY,
    job_id INTEGER REFERENCES jobs(id),
    scored_at TEXT,
    scorer_version TEXT,
    score REAL,
    evidence TEXT
);
```

Benefits: Proper dedup by URL, query jobs by status/score/date, track score changes over time, JOIN with discovery runs for analytics. CSV export still available for backwards compat.

#### 3.3 FSM for Application Workflow
**Inspired by:** Jobber

Model the application lifecycle as explicit state transitions:
```
discovered → interested → preparing → applied → interviewing → offer → accepted/rejected
                                                    ↓
                                                screening → technical → final → offer
```

Each transition has:
- **Guards** (pre-conditions): e.g., can't move to "applied" without cover letter + CV
- **Actions** (side-effects): e.g., moving to "applied" updates CSV, creates calendar reminder
- **Timestamps**: every transition logged

Prevents skipping steps or entering invalid states.

#### 3.4 Gmail/Email Status Detection
**Inspired by:** VibeHired AI

If user grants Gmail access (via MCP or OAuth):
- Scan inbox for application-related emails (rejection, interview invite, follow-up)
- Surface detected status changes as **suggestions** (never auto-apply)
- Pattern: "Detected email from [Company] that looks like [interview invite]. Update status?"

### Phase 4: Long-term Vision

#### 4.1 Observability Layer
**Inspired by:** Jobber (LangSmith)

Add tracing for agent decisions:
- Log every scoring decision with inputs, rubric applied, evidence cited
- Track time and cost per operation
- Dashboard: scoring accuracy over time, cost per application, pipeline funnel metrics

#### 4.2 Batch Statistical Reporting
**Inspired by:** resume-job-matcher

After weekly scans, generate statistical summary:
- Distribution of scores (histogram)
- Mean/median/stddev of fit scores
- Score trends over time (are you targeting better?)
- Source effectiveness (which boards produce highest-scoring jobs?)
- Keyword effectiveness (which search terms yield best results?)

---

## Appendix: Project Links

| Project | URL |
|---------|-----|
| AIHawk | https://github.com/feder-cr/Jobs_Applier_AI_Agent_AIHawk |
| Resume-Matcher (srbhr) | https://github.com/srbhr/Resume-Matcher |
| Jobber | https://github.com/sentient-engineering/jobber |
| ApplyPilot | https://github.com/Pickle-Pixel/ApplyPilot |
| JobSync | https://github.com/Gsync/jobsync |
| resume-job-matcher | https://github.com/sliday/resume-job-matcher |
| genai-job-agents | https://github.com/touhi99/genai-job-agents |
| cv-agents | https://github.com/0xrushi/cv-agents |
| JobSearch-Agent | https://github.com/sreekar2858/JobSearch-Agent |
| VibeHired AI | https://github.com/ganainy/VibeHired-ai |
| job-application-assistant | https://github.com/dinakajoy/job-application-assistant |
| CV-Matcher | https://github.com/eristavi/CV-Matcher |
| JobSensei (resume-matcher) | https://github.com/11a55an/resume-matcher |
| smart-agentic-ats-resume | https://github.com/unikill066/smart-agentic-ats-resume |
| Resume Screening App | https://github.com/haroon-sajid/Resume-Screening-App |
| Resume-Optimizer | https://github.com/naveennk045/Resume-Optimizer |
| chapagain/ai-job-apply-agent | https://github.com/chapagain/ai-job-apply-agent |
