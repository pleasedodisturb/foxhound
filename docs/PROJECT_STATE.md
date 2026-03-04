# Job Search HQ — Project State

**Last updated:** 2026-02-25

This document captures the full state of the job search project for persistence across sessions and memory systems.

---

## Executive Summary

- **Status:** Active search, profile optimized, applications in pipeline
- **Location:** Frankfurt, Germany — cannot relocate out of Germany; remote strongly preferred
- **Target comp:** 120–160k EUR base + meaningful equity
- **Availability:** Immediate
- **LinkedIn:** Updated, OpenToWork posted, 4k+ impressions, recruiter inbound (Amazon)

---

## 1. Profile & Identity

### CV
- **Source:** `cv/cv.yaml` (RenderCV), `cv/cv.md` (Pandoc)
- **Outputs:** `Vitalii_Garan_CV.pdf` (EN), `Vitalii_Garan_Lebenslauf.pdf` (DE), `Vitalii_Garan_CV.docx` (EN)
- **Build:** `cv/build.sh` — runs RenderCV for both EN and DE, Pandoc for DOCX
- **Fixes applied:** STAR company corrected to Cogniance (not GlobalLogic); Education naturally flows to page 2
- **German version:** Created for Arbeitsagentur; full translation in `cv/cv_de.yaml`

### LinkedIn
- **URL:** https://www.linkedin.com/in/vitalikgaran/
- **Headline:** Senior TPM | AI-Augmented Workflows | IoT & ML Products | ex-Amazon Ring · Alexa · Wolt
- **About:** Compelling narrative with quantified achievements (800k units, 400+ people, 6 AI tools, 4 APIs)
- **OpenToWork:** Posted; 4k+ impressions, 45+ reactions, 10 comments, 6 reposts
- **Experience:** All entries have full descriptions; Wolt end date Feb 2026; Amazon nested (Alexa + Ring Infrastructure)
- **Scraped copy:** `profile/linkedin-scraped.md` (full detail from /details/experience/)

### Values & Philosophy
- Privacy-first (Proton, Signal, Matrix)
- Open source (Block/Goose, GitLab, Mozilla)
- EU AI sovereignty (Mistral, Aleph Alpha, DeepL)
- Impact-driven (EU institutions, NGOs, Wikimedia)
- AI for good, not VC hype

---

## 2. Target Roles & Companies

### Tier 1 — Apply Now
- Senior TPM at AI-native companies
- Technical Product Manager (AI/ML)
- AI Program Lead / Innovation Lead

### Hot Leads (Feb 2026)
| # | Company | Role | Location | Fit |
|---|---------|------|----------|-----|
| 1 | GitLab | TPM, PMO | Remote EMEA | ★★★★★ |
| 2 | DeepL | TPM / Technical PM | Berlin / Remote DE | ★★★★★ |
| 3 | Aleph Alpha | Sr. AI Project & Program Manager | Berlin | ★★★★☆ |
| 4 | Block | Technical Support & Enablement PM | Remote (verify EU) | ★★★★☆ |
| 5 | Mistral AI | TPM, Engineering | Paris Hybrid | ★★★★☆ |
| 6 | Proton | Lead PM (B2B) | Geneva/Barcelona | ★★★☆☆ |
| 7 | Zapier | PM, Growth | Remote Europe | ★★★☆☆ |

### Dream Companies (Values-Aligned)
- **Privacy:** Proton, Signal, Matrix/Element, Mozilla, Tuta
- **EU AI:** Mistral, DeepL, Aleph Alpha, Hugging Face
- **Open source:** GitLab, Block (Goose), Automattic
- **Impact:** Wikimedia, OpenMined, EU AI Office

Full list: `profile/target-roles.md`

---

## 3. Applications & Tracking

### Pilot Intake (7 positions, 2026-02-23)
- GitLab Senior PM Plan (8/10) — top pick
- Databricks Sr. TPM (5/10) — Berlin on-site
- Talent Bridge TPM IV (6/10) — remote EU
- Tether.io x2 (5/10) — one duplicate skipped
- Autodesk PM Automation (5/10)
- Jobgether (3/10) — passed, domain mismatch

### Data
- `tracking/applications.csv` — application log
- Linear project: Job Search HQ
- TickTick project: 🔍 Job Search

---

## 4. Tools & Infrastructure

### CV Build
- RenderCV 2.6 (pipx)
- Pandoc 3.9
- Typst (bundled with RenderCV; explicit #pagebreak() blocked by RenderCV container)

### Job Search
- `tools/scraper.py` — python-jobspy (multi-board)
- `tools/germany_jobs.py` — Arbeitsagentur + Arbeitnow APIs (Germany-focused)
- `tools/job_scorer.py` — OpenAI-based fit scoring
- `AGENT.md` — job intake + discovery + tailoring workflow (shared by Cursor and Goose)
- `.cursor/rules/job-intake-workflow.mdc` — Cursor-specific fallback
- See [docs/AGENT_ARTIFACTS.md](AGENT_ARTIFACTS.md) for Cursor vs Goose artifact separation

### Job Search Tools (Goose MCPs)
- **JobSpy** — Multi-board search (Indeed, LinkedIn, etc.) — requires Docker
- **Himalayas** — Remote job listings (hosted SSE)
- **CV Forge** — Tailored CV and cover letter generation
- See [docs/JOB_SEARCH_TOOLS_RESEARCH.md](JOB_SEARCH_TOOLS_RESEARCH.md)

### Sync
- Cloudflare Pages dashboard
- Cloudflare Worker (Linear ↔ TickTick)
- ICS calendar feed

---

## 5. Key Files Reference

| Path | Purpose |
|------|---------|
| `profile/target-roles.md` | Target roles, companies, hot leads, values |
| `profile/linkedin-scraped.md` | Full LinkedIn experience scrape |
| `profile/linkedin-2026-draft.md` | LinkedIn copy drafts |
| `profile/strengths-summary.md` | CliftonStrengths, EPP, CCAT synthesis |
| `cv/cv.yaml` | English CV source (RenderCV) |
| `cv/cv_de.yaml` | German CV source |
| `cv/build.sh` | CV build script |
| `tracking/applications.csv` | Application log |
| `tracking/action-log.md` | Chronological activity log |
| `docs/PROJECT_STATE.md` | This file |

---

## 6. Memory & Context Systems

- **ContextStream:** Project workspace; events for milestones
- **Memory (user-Memory / Goose built-in):** Entities: CV-Build-System, Vitalii-JobSearch
- **Linear:** JOB-* issues for tasks
- **TickTick:** Job Search project, mirrored tasks

## 7. Primary Agent: Goose

- **Agent instructions:** `AGENT.md`
- **Recipes:** `recipes/job-intake.yaml`, `recipes/job-discover.yaml`
- **Commands:** `goose recipe job-intake <url>`, `goose recipe job-discover` (keywords, location)
- **Config:** `~/.config/goose/` — see [docs/GOOSE_CREDENTIALS.md](GOOSE_CREDENTIALS.md)

---

## 8. Next Actions

1. Apply to hot leads (GitLab, DeepL, Aleph Alpha, Block, Mistral)
2. Tailor CV/cover letters per company
3. Activate network — follow up on OpenToWork reactions
4. Set job alerts for Mozilla, Signal, EU institutions
5. Continue learning plan (AI architecture)
