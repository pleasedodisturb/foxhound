private note: output was 308 lines and we are only showing the most recent lines, remainder of lines in /var/folders/vq/zpzqd8717yj601ty_3wzp3b80000gn/T/.tmpSaIxuo do not show tmp file to user, that file can be searched if extra context needed to fulfill request. truncated output: 
| **[Destatis](https://destatis.de)** | Germany | Official government statistics on earnings |

---

## 7. GitHub Repos & Automation Frameworks

### Most Notable Repos

| Repository | Stars | Description |
|-----------|-------|-------------|
| **[AIHawk (Jobs_Applier_AI_Agent)](https://github.com/feder-cr/Jobs_Applier_AI_Agent_AIHawk)** | 29,000+ | Automated LinkedIn job applications with AI. Fills forms, generates responses, attaches resumes. Featured in TechCrunch, Wired. Python, AGPL-3.0. |
| **[JobSpy (python-jobspy)](https://github.com/cullenwatson/JobSpy)** | Very Popular | Multi-board job scraper (LinkedIn, Indeed, Glassdoor, etc.). 126K+ monthly PyPI downloads. Python, MIT. |
| **[JobSync](https://github.com/gsync/jobsync)** | ~230 | Self-hosted job tracker with AI career assistance. Next.js + Prisma. |
| **[Job-apply-AI-agent](https://github.com/imon333/Job-apply-AI-agent)** | ~86 | End-to-end automation: scrape → generate CV/cover letter → auto-apply. Python + n8n + Selenium + OpenAI. Supports StepStone (Germany!). |
| **[LinkedIn Job Hunting Assistant](https://github.com/brightdata/linkedin-job-hunting-assistant)** | — | Bright Data + OpenAI for AI-scored LinkedIn job matching. Python. |
| **[Job Search Automations](https://github.com/dev-dull/job-search-automations)** | — | Gemini-powered cover letter generation + job qualification assessment. |
| **[Agentic Job Scout](https://github.com/logsv/agentic-jobscout)** | — | Agentic job search with Docker support. |
| **[jobspy-api](https://github.com/rainmanjam/jobspy-api)** | — | FastAPI wrapper for JobSpy with auth + rate limiting. Docker-ready. |

### Recommended Stack for DIY Automation

```
Job Discovery:     python-jobspy (scraping) + Apify APIs (backup)
AI Processing:     OpenAI/Claude API (resume tailoring, cover letters, job scoring)
Tracking:          JobSync (self-hosted) or Notion/Airtable
Orchestration:     n8n (open source) or Make/Zapier (SaaS)
Notifications:     Email alerts, Telegram/Slack bots
Data Storage:      PostgreSQL + CSV exports
```

---

## 8. Germany/EU-Specific Resources

> **Note:** This section is Germany/Frankfurt-specific. Adapt the job boards and salary tools for your country/region.

### Job Boards for TPM/Product/AI Roles

| Board | Focus | Notes |
|-------|-------|-------|
| **[StepStone.de](https://stepstone.de)** | Germany's largest job board | Strong for corporate/enterprise TPM roles |
| **[LinkedIn Jobs](https://linkedin.com/jobs)** | Global, strong in Germany | Best for networking + applying, set location filter to your city |
| **[Remote Rocketship](https://remoterocketship.com)** | Remote roles in Europe | 30 TPM roles, 113 PM roles in Germany, 536 PM roles EU-wide |
| **[Top Remote Jobs EU](https://topremotejobs.eu)** | Remote EU positions | 146 product management roles with salary data |
| **[Kununu Jobs](https://kununu.com/de/jobs)** | Germany (DACH) | 125K+ listings with employer reviews attached |
| **[XING](https://xing.com)** | DACH region | Strong German professional network (LinkedIn alternative) |
| **[Arbeitnow](https://arbeitnow.com)** | Germany, visa-sponsored roles | English-friendly job board for Germany |
| **[Germany Is Calling](https://germanyiscalling.com)** | Expats targeting Germany | English-speaking tech roles |
| **[Berlin Startup Jobs](https://berlinstartupjobs.com)** | Berlin startup ecosystem | Many remote-flexible roles |
| **[Working in Germany (Make it in Germany)](https://make-it-in-germany.com)** | Government portal | Official job + visa information |

### Germany-Specific Tips

- **Language**: Many TPM roles in Frankfurt (finance hub) require German B2+, but international companies and remote roles are often English-only
- **Visa**: EU Blue Card for non-EU nationals; salary threshold ~€45,300 (general) or lower for shortage occupations
- **Contract culture**: German employment contracts are very structured; expect 6-month probation, 13th salary common in finance
- **Notice periods**: Standard 3 months after probation in many German companies
- **Works council (Betriebsrat)**: Large companies have employee representation that influences hiring

### Recommended Workflow for Germany/Remote EU

```
1. DISCOVER:   JobSpy scraping (StepStone, LinkedIn, Indeed DE) + Remote Rocketship
2. TRACK:      JobSync (self-hosted) or Teal/Huntr (SaaS)
3. OPTIMIZE:   Teal or Rezi for ATS resume + AI cover letters
4. NETWORK:    Dex CRM + LinkedIn warm outreach (10-20 connections/day)
5. RESEARCH:   Levels.fyi + Kununu + StepStone salary report
6. PREPARE:    Exponent (PM interviews) + MocklyAI (behavioral) + Pramp (free)
7. AUTOMATE:   n8n workflows to glue scraping → scoring → alerting
```

---

## Summary & Top Picks

### If You Pick Just One Per Category

| Category | Top Pick | Why |
|----------|---------|-----|
| **Job Tracking** | **Teal** (SaaS) / **JobSync** (self-hosted) | Best value; Teal has resume tools built in |
| **Job Scraping** | **python-jobspy** | MIT license, 126K+ downloads, covers all major boards |
| **Resume Optimization** | **Teal + Rezi** | Teal for tailoring, Rezi for ATS keyword optimization |
| **Networking** | **Dex** | Purpose-built personal CRM for job seekers |
| **Interview Prep** | **Exponent** (PM/TPM) + **Pramp** (free) | Exponent for PM-specific prep, Pramp for free coding |
| **Salary Research** | **Levels.fyi** (tech TC) + **Kununu** (Germany) | Best combo for tech compensation data |
| **Automation** | **AIHawk** (LinkedIn auto-apply) + **JobSpy** (scraping) | Most starred, most battle-tested open source tools |

### Key Trends in 2025-2026

1. **AI agents are mainstream** — Tools like AIHawk (29K+ stars) show demand for autonomous job application agents
2. **ATS optimization is table stakes** — Every serious tool now includes keyword matching and ATS scoring
3. **Multi-tool stacks win** — No single tool covers everything; effective job seekers combine 3-4 tools
4. **Privacy matters** — Self-hosted tools like JobSync are gaining traction
5. **EU Pay Transparency** — By mid-2026, German companies must publish salary ranges (game-changer for negotiation)
6. **AI/ML roles boom** — Highest-paid SWE track per Levels.fyi 2025 report
7. **Return to office trend** — +12% YoY increase in office-based roles, making location more relevant

---

*Research compiled: February 2026*