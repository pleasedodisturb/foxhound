# Foxhound — Project State

**Last updated:** [date]

This document captures the full state of your job search project for persistence across sessions and memory systems. Fill it in as your search progresses — it helps AI agents pick up where you left off.

---

## Executive Summary

- **Status:** [Active search / Passive / Paused]
- **Location:** [Your city, country] — [relocation constraints]
- **Target comp:** [Range in currency] + [equity preference]
- **Availability:** [Immediate / X weeks notice]
- **LinkedIn:** [Status — updated? OpenToWork?]

---

## 1. Profile & Identity

### CV
- **Source:** `cv/cv.yaml` (RenderCV)
- **Build:** `cv/build.sh`
- **Languages:** [EN / DE / other]

### LinkedIn
- **URL:** [your LinkedIn URL]
- **Headline:** [current headline]

### Values
<!-- What matters to you beyond comp and title -->
- [Value 1]
- [Value 2]
- [Value 3]

---

## 2. Target Roles & Companies

### Tier 1 — Apply Now
- [Role type 1]
- [Role type 2]
- [Role type 3]

### Hot Leads
<!-- Update this table as you discover high-fit roles -->
| # | Company | Role | Location | Fit |
|---|---------|------|----------|-----|
| 1 | | | | /10 |
| 2 | | | | /10 |
| 3 | | | | /10 |

### Dream Companies
- [Company list by category]

Full rubric: `profile/target-roles.md`

---

## 3. Applications & Tracking

- `tracking/applications.csv` — application log (gitignored)
- Linear project (optional): [project name]
- TickTick project (optional): [project name]

---

## 4. Tools & Infrastructure

### CV Build
- RenderCV (`pip install rendercv`)
- `cv/cv.yaml` → `cv/build.sh` → PDF

### Job Search
- `tools/scraper.py` — python-jobspy (multi-board)
- `tools/germany_jobs.py` — regional APIs (adapt to your market)
- `tools/job_scorer.py` — OpenAI-based fit scoring (6-field output)
- `AGENT.md` — shared workflow logic

### MCP Servers (optional)
- See `.mcp.json.example` for available integrations
- See [docs/SETUP.md](SETUP.md) for installation instructions

---

## 5. Key Files

| Path | Purpose |
|------|---------|
| `profile/target-roles.md` | Scoring rubric, company tiers, role targets |
| `profile/README.md` | Guide to adding profile context |
| `cv/cv.yaml` | CV source (RenderCV) |
| `cv/build.sh` | CV build script |
| `tracking/applications.csv` | Application log (gitignored) |
| `AGENT.md` | Shared agent workflow logic |
| `docs/architecture.md` | System architecture and scoring flow |
| `docs/SETUP.md` | Detailed setup guide |
| `docs/PROJECT_STATE.md` | This file |

---

## 6. Next Actions

<!-- Update as your search progresses -->
1. [Action 1]
2. [Action 2]
3. [Action 3]
