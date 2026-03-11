# Foxhound — Claude Code Instructions

## Who

[Your Name]. [Your City, Country]. [Relocation constraints].
Target: [salary range + equity expectations]. [Availability].
Roles: [your target role types, e.g. Senior TPM, Product Engineer, AI Program Lead].
[One-line builder identity — what makes you different].

## Key IDs

- **Linear team:** YOUR_LINEAR_TEAM_ID (optional — only if using Linear MCP)
- **TickTick project:** YOUR_TICKTICK_PROJECT_ID (optional — only if using TickTick MCP)
- **GitHub repo:** YOUR_GITHUB_USERNAME/foxhound

## Workflows

**Read `AGENT.md` before any job-related task.** It contains all shared workflow logic (intake, scoring, discovery, application prep). This file only has Claude Code-specific settings.

Before writing cover letters, read all docs in `profile/` — identity, narrative, assessments, writing samples. The more context, the more authentic the output.

Write in your authentic voice — direct, specific, no corporate fluff. Every claim backed by a specific story.

## Available MCPs

**Always-on (in `.mcp.json`):**

| MCP | Purpose |
|-----|---------|
| memory | doobidoo/mcp-memory-service — local semantic memory (SQLite-vec) |
| jobspy | Multi-board job search (Indeed, LinkedIn, Glassdoor) |
| context7 | Documentation lookup |

**On-demand (copy into `.mcp.json` when needed, remove after):**

| MCP | Purpose | When |
|-----|---------|------|
| ticktick | Task management (felores/ticktick-mcp-server) | Task sessions |
| himalayas | Remote job listings (SSE endpoint) | Job discovery |
| cv-forge | Parse job requirements, draft applications | Application writing |
| browsermcp | Browser automation | Web scraping |
| linear | Job tracking issues (JOB-* prefix) | Issue tracking |

Use `gh` CLI for GitHub operations (authenticate via `gh auth login`).
Use built-in `WebSearch` for web searches.

## Safety Rules

- NEVER delete or overwrite `tracking/applications.csv` without explicit confirmation
- NEVER modify `profile/target-roles.md` without approval
- Ask before any bulk or destructive operation
- All secrets via environment variables or secret manager — zero plaintext in config files

## Session Persistence

- **Memory:** Use `store_memory` after significant actions (intake, scoring, application updates, decisions)
- **Git:** Commit regularly during active work. Descriptive messages.

## Python

- Use `.venv/bin/python` (project venv at root)
- Never install packages globally

## Key Files

| Path | Purpose |
|------|---------|
| `AGENT.md` | Job intake, scoring, discovery workflows |
| `profile/` | Identity, voice, target roles, strengths |
| `tracking/applications.csv` | Application log (canonical) |
| `tools/germany_jobs.py` | Regional job board search (adapt to your market) |
| `tools/scraper.py` | Multi-board scrape |
| `tools/job_scorer.py` | AI-based fit scoring |

## Scoring Quick Reference

- Remote-first: +1.5
- Builder signals: +1
- AI-native company: +1
- Dream tier companies: floor 8
- Your city / remote: neutral. Your country: -0.5. Outside country: cap 5.
- Full rubric in AGENT.md

## Slash Commands

Claude Code slash commands are in `.claude/commands/`:
- `/job-intake <url or text>` — Process a single job posting
- `/job-discover [keywords]` — Multi-source job search
- `/weekly-scan [min_score]` — Automated weekly discovery digest
