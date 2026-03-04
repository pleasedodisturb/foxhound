# Architecture — Job Search HQ

This document describes the system design, data flow, and decision rationale behind Job Search HQ.

---

## 🎯 Design Principles

1. **AI-Native, Not AI-Augmented**
   - AI is infrastructure, not a feature
   - Goose recipes are the workflow engine
   - Human-in-the-loop for decisions, AI for execution

2. **Context-Rich Operations**
   - Deep profile → better scoring
   - ContextStream for semantic memory
   - Every interaction enriches the system

3. **Composable Tooling**
   - MCP servers for extensibility
   - Python scripts for specific tasks
   - Next.js dashboard for visualization
   - Git for version control of strategy

4. **Data Sovereignty**
   - All data local-first (CSV, markdown)
   - Optional cloud integrations (Linear, TickTick)
   - No vendor lock-in

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER (Job Seeker)                        │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ Natural language commands
                 │
┌────────────────▼────────────────────────────────────────────────┐
│                    GOOSE (Orchestration Layer)                   │
│  • Recipes (job-intake.yaml, job-discover.yaml)                 │
│  • .goosehints (project context)                                 │
│  • Extension system (MCP, tools)                                 │
└────────┬───────────────────────┬────────────────────────────────┘
         │                       │
         │                       │
    ┌────▼─────┐          ┌──────▼──────┐
    │   MCP    │          │   Python    │
    │  Servers │          │   Tools     │
    └────┬─────┘          └──────┬──────┘
         │                       │
         │                       │
┌────────▼───────────────────────▼────────────────────────────────┐
│                      DATA LAYER (Sources)                        │
│                                                                  │
│  Job Sources:              Context:              Integrations:  │
│  • JobSpy MCP              • profile/            • Linear API   │
│  • germany_jobs.py         • AGENT.md            • TickTick API │
│  • Brave Search            • ContextStream       • GitHub       │
│  • Company websites        • .goosehints          • Brave       │
│                                                                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Structured data
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                   STORAGE & TRACKING                             │
│  • tracking/applications.csv — canonical log                     │
│  • profile/ — scoring rubric, strengths, CV data                 │
│  • docs/ — decisions, research, artifacts                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Read by
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                  DASHBOARD (Visualization)                       │
│  • Next.js app                                                   │
│  • Reads tracking/applications.csv                               │
│  • Charts, filters, insights                                     │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow: Job Intake

### 1. Discovery Phase

```
User → Goose → "Find AI Product Manager jobs in Berlin"
                 ↓
              JobSpy MCP
                 ↓
      [5-10 job postings returned]
                 ↓
            For each job:
                 ↓
         Fetch full JD (scrape if needed)
                 ↓
              NEXT PHASE
```

### 2. Scoring Phase

```
Job posting text
    ↓
Parse: title, company, location, description, requirements
    ↓
Load: profile/target-roles.md
    ↓
AI-powered fuzzy matching:
  • Company in tier list? → floor score
  • Remote/location fit? → +/- modifiers
  • Title match (fuzzy)? → base score
  • Required skills present? → adjust
  • Values alignment? → +0.5
    ↓
Final score: 1-10
```

### 3. Tracking Phase

```
Scored job
    ↓
Append to tracking/applications.csv
    ↓
Create Linear issue (optional)
    ↓
Create TickTick task (optional)
    ↓
Return summary to user
```

---

## 🧩 Component Details

### Goose Recipes

**Located:** `recipes/`

Recipes are YAML-defined workflows that Goose executes:

```yaml
# job-intake.yaml
name: Job Intake
description: Process a job posting URL
steps:
  - action: fetch_posting
  - action: score_job
  - action: add_to_csv
  - action: create_tasks
```

**Why recipes?**
- Repeatable workflows
- Version-controlled strategy
- Shareable with others
- AI executes, human approves

### MCP Servers

**JobSpy** (`mcp-server-jobspy`)
- Multi-source job aggregation
- Queries: Indeed, LinkedIn, Glassdoor, Google
- Returns structured job data

**ContextStream** (`@contextstream/mcp-server`)
- Semantic memory across sessions
- Stores decisions, lessons, context
- Enables "recall what we decided about X"

**Future:**
- Linear MCP (issue creation)
- TickTick MCP (task management)
- Custom scrapers (Personio, Greenhouse)

### Python Tools

**`tools/germany_jobs.py`**
- Searches Arbeitsagentur (German federal job board)
- Searches Arbeitnow (English jobs in Germany)
- CLI with presets: `--preset ai`, `--preset builder`
- Outputs JSON for further processing

**`tools/job_scorer.py`**
- Standalone scoring utility
- Takes job URL or text
- Returns 1-10 score with reasoning

**`tools/cv_generator.py`**
- Integrates with RenderCV
- Generates tailored CV per application
- Outputs PDF + Markdown

### Profile System

**`profile/`** is the **brain** of the system:

| File | Purpose |
|------|---------|
| `README.md` | Professional summary, builder identity |
| `target-roles.md` | **Scoring rubric** (most important!) |
| `strengths-summary.md` | What you bring (for cover letters) |
| `values.md` | What matters (company screening) |
| `cv-data.yaml` | Structured CV data for RenderCV |
| `wolt-capability-digest.md` | Evidence of past work (showcase) |

**Why separate from code?**
- Context is data
- Version-controlled strategy
- Easy to update without touching code
- Shareable (with sanitization)

### Tracking System

**`tracking/applications.csv`** is the **canonical source of truth**:

```csv
company,role,location,status,score,date_added,url,notes
Mistral AI,AI Product Manager,Paris (Remote),interested,9,2024-01-15,https://...,Dream company
```

**Why CSV?**
- Simple, portable, future-proof
- Git-friendly (text diffs)
- Works with any tool (Excel, Pandas, SQL)
- No database overhead

**Status values:**
- `interested` — scored, not yet applied
- `applied` — application submitted
- `interviewing` — in process
- `offered` — job offer received
- `rejected` — not selected
- `withdrawn` — you withdrew

### Dashboard

**Tech stack:**
- Next.js 14 (App Router)
- React + TypeScript
- Tailwind CSS
- Recharts for visualizations

**Features:**
- Application list with filters
- Score distribution chart
- Status pipeline view
- Company tier breakdown
- Timeline view

**Why Next.js?**
- Fast to build
- Easy to deploy (Vercel, Netlify)
- Can add API routes later (webhooks, integrations)
- Modern, maintainable

---

## 🔐 Security & Privacy

### Local-First

All sensitive data stays local:
- `tracking/applications.csv` never leaves your machine
- Profile data is yours
- Git ignores sensitive files

### Optional Cloud

Cloud integrations are opt-in:
- Linear (task tracking)
- TickTick (personal tasks)
- ContextStream (semantic memory)

**You control what goes where.**

### Sanitization

The `scripts/create_public_version.sh` script:
- Strips personal info from profile
- Creates example CSV (no real data)
- Removes API keys
- Produces shareable version

---

## 🚀 Scaling Considerations

### Current: Single User

- Local CSV (< 1000 entries)
- Manual Goose invocations
- Dashboard reads file directly

### Future: Power User

- SQLite for tracking (faster queries)
- Background workers (automated discovery)
- Webhook integrations (auto-notify)
- Browser extension (one-click intake)

### Future: Team/Service

- PostgreSQL for multi-user
- API server (FastAPI)
- Authentication
- Shared company knowledge base

**But start simple.** CSV is fine for 95% of job searches.

---

## 🧪 Testing Strategy

### Current

- Manual QA (run recipes, check CSV)
- Profile validation (scoring makes sense?)
- Dashboard renders correctly

### Recommended

- Unit tests for `job_scorer.py`
- Integration tests for Goose recipes
- Schema validation for CSV
- Snapshot tests for dashboard

### Philosophy

This is **personal infrastructure**, not production software.
- Optimize for iteration speed
- Test what breaks often
- Document edge cases
- Trust but verify AI outputs

---

## 🤔 Design Decisions

### Why Goose, Not Custom Scripts?

**Goose pros:**
- Natural language interface
- Built-in AI orchestration
- MCP ecosystem
- Session management

**Goose cons:**
- Less control than code
- Debugging is harder
- Depends on external service

**Decision:** Use Goose for workflows, Python for logic. Best of both worlds.

### Why CSV, Not Database?

**CSV pros:**
- Simple, portable, human-readable
- Git-friendly
- Works with everything
- No migration hell

**CSV cons:**
- No relations
- No transactions
- Manual locking

**Decision:** Start with CSV. Migrate to SQLite if > 500 entries or need speed.

### Why Next.js, Not CLI?

**Next.js pros:**
- Visual is better for tracking
- Easy to share (deploy link)
- Can add features (webhooks, exports)

**Next.js cons:**
- Overkill for basic tracking
- Requires Node.js

**Decision:** Dashboard is optional. CSV + CLI works too.

### Why MCP, Not Direct APIs?

**MCP pros:**
- Standardized interface
- Composable
- AI-native
- Growing ecosystem

**MCP cons:**
- New protocol (less mature)
- Limited servers available
- Abstraction overhead

**Decision:** Use MCP where available, direct APIs otherwise.

---

## 📊 Metrics & Observability

### What to Track

- Jobs discovered per week
- Score distribution (are you too picky?)
- Time from interest → application
- Interview conversion rate
- Offer conversion rate

### How to Track

- Dashboard charts (built-in)
- CSV exports to Google Sheets
- Manual journaling
- ContextStream (decision log)

### Key Question

**"Is the system making me faster or just busier?"**

If you're processing 100 jobs/week but applying to 0, the system failed.
The goal is **better decisions**, not more data.

---

## 🔮 Future Enhancements

### Short-Term (Next 3 Months)

- [ ] Browser extension (one-click job intake)
- [ ] Email integration (alert on high-score matches)
- [ ] LinkedIn auto-apply integration
- [ ] Cover letter generator (from profile + job)

### Medium-Term (6 Months)

- [ ] Interview prep mode (company research, Q&A)
- [ ] Offer comparison tool (comp, equity, growth)
- [ ] Network graph (who works where?)
- [ ] Automated follow-ups (email templates)

### Long-Term (1 Year)

- [ ] Job market analytics (trends, demand)
- [ ] Skill gap analysis (what to learn)
- [ ] Salary negotiation assistant
- [ ] Referral network automation

---

## 🤝 Contributing

See `CONTRIBUTING.md` for:
- How to add new job sources
- How to improve scoring
- Dashboard contribution guide
- Code style (linting, formatting)

---

**Questions?** Open an issue or discussion on GitHub.
