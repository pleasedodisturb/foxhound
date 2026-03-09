# Detailed Setup Guide

The [README](../README.md) gets you running in 5 minutes. This guide covers everything else — per-agent MCP configuration, optional integrations, batch scoring, and the CV pipeline.

---

## Prerequisites

- Python 3.11+ (`python3 --version`)
- git
- An AI agent: [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Goose](https://block.github.io/goose/), [Cursor](https://cursor.sh), or any LLM
- Node.js 18+ (for MCP servers that use `npx`)
- Docker (optional, for JobSpy MCP)

---

## 1. Clone and install

```bash
git clone https://github.com/YOUR_USERNAME/job-search-hq.git
cd job-search-hq
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 2. Configure your profile

This is the most important step. Scoring quality is directly proportional to profile depth.

```bash
# Edit your scoring rubric:
open profile/target-roles.md

# Read the full guide for what to add:
open profile/README.md
```

Fill out every `<!-- CUSTOMIZE -->` section in `profile/target-roles.md`. Then add context documents to `profile/` — identity statement, career narrative, assessments, writing samples. See [profile/README.md](../profile/README.md) for the full list with links to assessment tools.

---

## 3. Set up tracking

```bash
cp tracking/applications.csv.example tracking/applications.csv
```

This file is gitignored — your application data stays local.

---

## 4. Pick your agent

### Claude Code

Claude Code reads `CLAUDE.md` automatically when you open the project.

**MCP setup:**
```bash
cp .mcp.json.example .mcp.json
# Edit .mcp.json — update all /path/to/your/... entries
```

Claude Code reads `.mcp.json` from the project root. MCP servers start automatically when Claude Code opens the project.

**Slash commands** (if using Claude Code's command feature):
- `.claude/commands/` contains workflow shortcuts
- Use them via `/job-intake`, `/job-discover`, etc.

### Goose

Goose reads `.goosehints` automatically from the project root.

**MCP setup** — add servers to your Goose config (`~/.config/goose/config.yaml`):
```yaml
mcp:
  memory:
    command: /path/to/your/project/.venv/bin/memory
    args: ["server"]
    env:
      MCP_MEMORY_STORAGE_BACKEND: sqlite_vec
      MCP_MEMORY_SQLITE_PATH: /path/to/your/.mcp_memory/memory.db
  context7:
    command: npx
    args: ["-y", "@upstash/context7-mcp"]
```

Then: `goose session start` from the project root.

### Cursor

Cursor reads `.cursorrules` automatically when you open the project folder.

**MCP setup** — add servers to `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "memory": {
      "command": "/path/to/your/project/.venv/bin/memory",
      "args": ["server"],
      "env": {
        "MCP_MEMORY_STORAGE_BACKEND": "sqlite_vec",
        "MCP_MEMORY_SQLITE_PATH": "/path/to/your/.mcp_memory/memory.db"
      }
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

### Any other agent

Paste the contents of [AGENT.md](../AGENT.md) into your agent's system prompt. That gives it the full workflow logic — intake, scoring, discovery, application prep, safety rules.

---

## 5. MCP servers (optional)

All MCP servers are optional. The Python tools work standalone without any MCP server running.

### memory (mcp-memory-service)

Local semantic memory using SQLite-vec. Lets your agent remember context across sessions.

```bash
# Install in project venv:
source .venv/bin/activate
pip install mcp-memory-service
```

Config is in `.mcp.json.example`. The `memory` entry points to your venv's `memory` binary.

### JobSpy

Multi-board job search (Indeed, LinkedIn, Glassdoor). Requires Docker.

```bash
# Pull and run:
docker pull ghcr.io/isidrok/mcp-server-jobspy:latest

# Or build from source:
git clone https://github.com/isidrok/mcp-server-jobspy
cd mcp-server-jobspy && docker build -t jobspy .
```

Add the JobSpy entry from `.mcp.json.example` to your `.mcp.json`.

**Alternative:** Use `tools/scraper.py` directly without Docker — it uses `python-jobspy` (same underlying library).

### Linear (issue tracking)

```bash
# Get API key from https://linear.app/settings/api
export LINEAR_API_KEY=your_key_here
```

Add the Linear entry from `.mcp.json.example` to your `.mcp.json`. Replace `your_linear_api_key_here` with your actual key.

### TickTick (task management)

```bash
# Install the MCP server:
pip install ticktick-mcp-server

# Set up OAuth credentials — see https://github.com/felores/ticktick-mcp-server
```

Add the TickTick entry from `.mcp.json.example` to your `.mcp.json`.

### context7 (documentation lookup)

No setup needed. Just add the entry from `.mcp.json.example`:
```json
"context7": {
  "command": "npx",
  "args": ["-y", "@upstash/context7-mcp"]
}
```

### Himalayas (remote jobs)

No API key needed:
```json
"himalayas": {
  "command": "npx",
  "args": ["-y", "mcp-remote", "https://mcp.himalayas.app/sse"]
}
```

---

## 6. Batch scoring (optional)

Score a CSV of scraped jobs in bulk using GPT-4o-mini:

```bash
export OPENAI_API_KEY=your_key_here
.venv/bin/python tools/job_scorer.py tracking/scraped_jobs.csv --limit 20
```

This adds 6 columns: `fit_score`, `fit_reasoning`, `estimated_salary`, `effort_flag`, `prep_level`, `prep_notes`.

**Customize scoring criteria:** Edit the `PROFILE_CRITERIA` variable in `tools/job_scorer.py` to match your `profile/target-roles.md`. The TODO comments show what to change.

**Cost:** ~$0.01-0.02 per job scored with GPT-4o-mini.

---

## 7. CV pipeline (optional)

### Install RenderCV

```bash
pip install rendercv
```

### Build your base CV

```bash
# Edit your CV source:
open cv/cv.yaml

# Build PDF:
cd cv && rendercv render cv.yaml
```

This generates a typeset PDF from YAML. All facts (education, dates, experience) come from `cv/cv.yaml` — never invent or hallucinate data.

### Generate tailored CVs

```bash
# Edit roles in the script:
open tools/render_tailored_cvs.py

# Run:
.venv/bin/python tools/render_tailored_cvs.py
```

Each role gets a tailored summary paragraph while keeping all facts from the base CV.

### Generate cover letter PDFs

```bash
# Write cover letter markdown:
mkdir -p cv/applications/company-role
# Write cv/applications/company-role/cover-letter.md

# Generate PDF:
.venv/bin/python tools/md_to_pdf_cover_letter.py
```

---

## 8. Verify it works

Open the project in your agent and try:

> "Process this job posting: https://some-company.com/careers/ai-engineer"

The agent should:
1. Parse the job description
2. Score it against your `profile/target-roles.md`
3. Estimate salary + prep level
4. Add a row to `tracking/applications.csv`
5. Show you a summary with score, salary estimate, and prep rating

If that works, you're set. Browse [AGENT.md](../AGENT.md) for the full list of workflows.

---

## Troubleshooting

**MCP server won't start:** Check paths in `.mcp.json`. All `/path/to/your/...` entries must be absolute paths to your actual installation.

**JobSpy scraping fails:** LinkedIn and Indeed block aggressive scraping. Use `--limit 10` and add delays. Or use `tools/germany_jobs.py` which hits free government APIs.

**Scoring seems random:** Your `profile/target-roles.md` is probably too vague. Be specific about what you want. See the calibration guide in the [README](../README.md#calibration).

**RenderCV fails:** Make sure you're in the `cv/` directory and your `.venv` is activated. Check that `cv/cv.yaml` is valid YAML.
