# 🎯 Job Search HQ

> **An AI-native job search operating system.** Not a job board. Not a spreadsheet. A system.

Built for people who treat their job search like a product — with pipelines, scoring, tracking, and tooling — instead of manually scrolling LinkedIn hoping something good shows up.

---

## 🤔 Should You Use This?

### ✅ This is for you if:

- You're a **senior IC, founding engineer, or technical PM** who's picky about where you work next
- You want **quality over volume** — 5 great applications > 100 spray-and-pray submissions
- You're comfortable with **CLI, Python, and Node.js** (or willing to learn)
- You think **systems beat heroics** — you'd rather build a process than grind manually
- You're **AI-curious** and want to see what AI-native personal ops actually looks like in practice
- You have **specific criteria** (location, compensation, company culture, mission) and want a system that respects them

### ❌ This is NOT for you if:

- You want to apply to 100 jobs a week (use LinkedIn Easy Apply)
- You're entry-level and just need to get your first role
- You're not comfortable running code locally
- You want a SaaS with a nice UI and no setup

---

## 🚀 What It Does

```
You: "Process this job posting: https://company.com/careers/ai-engineer"

Goose:
  ✓ Fetches and parses the job description
  ✓ Scores it 1-10 against your profile and criteria
  ✓ Explains the score ("8/10 — remote-first, AI-native, matches your builder profile")
  ✓ Appends to tracking/applications.csv
  ✓ Creates a Linear issue with priority based on score
  ✓ Creates a TickTick task for follow-up

📋 Acme AI — Senior AI Engineer
📍 Remote (EU)
🎯 Fit Score: 8/10
💡 AI-native product, remote-first, strong builder signals in JD
🔗 https://company.com/careers/ai-engineer
✅ Added to: CSV + Linear (JOB-42) + TickTick
```

---

## 🏗️ System Overview

```
┌─────────────────────────────────────────────────────────┐
│                   YOU (Job Seeker)                       │
│         Natural language commands via Goose              │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              GOOSE (AI Orchestrator)                     │
│   Recipes • Extensions • MCP Tools • .goosehints        │
└────┬──────────────┬──────────────────┬──────────────────┘
     │              │                  │
┌────▼────┐  ┌──────▼──────┐  ┌───────▼──────┐
│  MCPs   │  │Python Tools │  │  Dashboard   │
│JobSpy   │  │germany_jobs │  │  (Next.js)   │
│Linear   │  │job_scorer   │  │  reads CSV   │
│TickTick │  │scraper      │  └──────────────┘
│CVForge  │  └──────┬──────┘
│BraveSearch        │
└────┬──────┘        │
     │               │
┌────▼───────────────▼────────────────────────────────────┐
│                  YOUR DATA (local)                       │
│  profile/          tracking/           docs/             │
│  target-roles.md   applications.csv   decisions          │
│  README.md         action-log.md      research           │
│  strengths         [gitignored]                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| [Goose](https://block.github.io/goose/) | Latest | AI orchestration engine |
| Python | 3.11+ | Job discovery tools |
| Node.js | 18+ | Dashboard |
| Git | Any | Version control |
| A terminal | — | You know how |

**Optional but recommended:**
- [Cursor](https://cursor.sh) or Claude Desktop — for MCP-based integrations
- [Linear](https://linear.app) account — for issue tracking
- [TickTick](https://ticktick.com) account — for task management
- [Brave Search API key](https://brave.com/search/api/) — for web search in Goose

---

## ⚡ Quick Start (15 minutes)

### Step 1 — Clone & install

```bash
git clone https://github.com/YOUR_USERNAME/job-search-hq.git
cd job-search-hq

# Python environment
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Dashboard (optional)
cd dashboard && npm install && cd ..
```

### Step 2 — Set up your profile

This is the most important step. **The system is only as good as the context you give it.**

```bash
# Start with the most important file:
open profile/target-roles.md   # or code/vim/nano
```

Edit these files to describe **you**:

| File | What to fill in |
|------|----------------|
| `profile/target-roles.md` | ⭐ Your scoring rubric — company tiers, role types, location rules |
| `profile/README.md` | Your professional summary and builder identity |
| `profile/cv-scraped.md` | Your CV / work history (raw, unpolished — AI will use it) |
| `profile/strengths-summary.md` | What you're great at |
| `.goosehints` | Quick context for Goose — who you are, what you want |

> 💡 **Tip:** Be specific. "I want a PM role" is useless. "I want a product engineer role at a 10-100 person remote-first AI company where I can ship code and own a product area, paying 130k+ EUR" is excellent.

### Step 3 — Set up tracking

```bash
cp tracking/applications.csv.example tracking/applications.csv
# This file is gitignored — your data stays local
```

### Step 4 — Install Goose

```bash
# macOS (Homebrew)
brew install block/goose/goose

# Or download from: https://block.github.io/goose/
```

Configure Goose with your AI provider:
```bash
goose configure
# Follow the prompts to set your LLM provider (Anthropic, OpenAI, etc.)
```

### Step 5 — Run your first job intake

```bash
cd job-search-hq
goose session start

# In the Goose session:
# "Process this job posting: https://some-company.com/jobs/ai-engineer"
```

That's it. Goose will score it, track it, and optionally create tasks — all in one shot.

---

## 🔌 MCP Integrations

MCPs (Model Context Protocol servers) extend what your AI agent can do. Here's what this system supports and how to set each one up.

### What is MCP?

MCP is an open protocol (by Anthropic) that lets AI assistants connect to external tools and data sources in a standardized way. Think of it like plugins — but for AI agents. [Learn more →](https://modelcontextprotocol.io)

---

### 🔍 JobSpy MCP (Job Discovery)

Searches Indeed, LinkedIn, Glassdoor, and Google Jobs simultaneously.

**Install:**
```bash
# Requires uvx (install via pipx or brew)
brew install uv
uvx mcp-server-jobspy --help  # verify it works
```

**Configure in Goose** (`~/.config/goose/config.yaml`):
```yaml
extensions:
  jobspy:
    type: sse
    cmd: uvx
    args: ["mcp-server-jobspy"]
    enabled: true
```

**Configure in Cursor/Claude Desktop** (`~/.cursor/mcp.json` or `~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "jobspy": {
      "command": "uvx",
      "args": ["mcp-server-jobspy"]
    }
  }
}
```

**Usage in Goose:**
```
"Search for AI Product Manager jobs in Berlin, remote preferred, last 7 days"
```

---

### 🧠 ContextStream MCP (Semantic Memory)

Gives your AI persistent memory across sessions — decisions, lessons, preferences, context.

**Why use it:** Without this, Goose forgets everything between sessions. With it, it remembers your scoring decisions, lessons learned, and context about companies you've researched.

**Install:**
```bash
npm install -g @contextstream/mcp-server@latest
```

**Get API key:** [contextstream.io](https://contextstream.io) (free tier available)

**Configure in Goose:**
```yaml
extensions:
  contextstream:
    type: sse
    cmd: npx
    args: ["-y", "@contextstream/mcp-server@latest"]
    env:
      CONTEXTSTREAM_API_KEY: "your_key_here"
    enabled: true
```

**Configure in Cursor/Claude:**
```json
{
  "mcpServers": {
    "contextstream": {
      "command": "npx",
      "args": ["-y", "@contextstream/mcp-server@latest"],
      "env": {
        "CONTEXTSTREAM_API_KEY": "your_key_here"
      }
    }
  }
}
```

---

### 📋 Linear MCP (Issue Tracking)

Creates issues in Linear automatically when you add a job. Gives you a Kanban board for your job search pipeline.

**Why use it:** Great if you already use Linear. Each job becomes an issue with priority based on score. You can move it through: Backlog → Researching → Applied → Interviewing → Offer.

**Get API key:** Linear → Settings → API → Personal API keys

**Configure in Cursor/Claude:**
```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@linear/mcp-server@latest"],
      "env": {
        "LINEAR_API_KEY": "your_key_here"
      }
    }
  }
}
```

**Setup:**
1. Create a team in Linear called "Job Search" (or whatever you like)
2. Copy the team ID from: Linear → Settings → Team → ID
3. Update `AGENT.md`: replace `YOUR_LINEAR_TEAM_ID` with your actual team ID
4. Update `.goosehints` similarly

---

### ✅ TickTick MCP (Task Management)

Creates tasks in TickTick automatically. Good if you prefer a personal task manager over a project board.

**Why use it:** Each scored job becomes a task with due dates and priority. Keeps your job search in your existing task workflow.

**Get credentials:** TickTick → Settings → Integrations (OAuth flow)

**Configure:**
```json
{
  "mcpServers": {
    "ticktick": {
      "command": "uvx",
      "args": ["mcp-server-ticktick"],
      "env": {
        "TICKTICK_CLIENT_ID": "your_client_id",
        "TICKTICK_CLIENT_SECRET": "your_client_secret"
      }
    }
  }
}
```

**Setup:**
1. Create a project in TickTick called "Job Search"
2. Copy the project ID from the URL when viewing the project
3. Update `AGENT.md` and `.goosehints` with `YOUR_TICKTICK_PROJECT_ID`

---

### 🌐 Brave Search MCP (Web Search)

Lets Goose search the web for job postings, company research, and career pages.

**Get API key:** [brave.com/search/api](https://brave.com/search/api/) (free tier: 2000 queries/month)

**Configure in Goose:**
```yaml
extensions:
  brave-search:
    type: sse
    cmd: npx
    args: ["-y", "@modelcontextprotocol/server-brave-search"]
    env:
      BRAVE_API_KEY: "your_key_here"
    enabled: true
```

---

### 📄 CV Forge MCP (Resume Generation)

Parses job requirements and generates tailored CVs and cover letters from your profile data.

**Configure:**
```json
{
  "mcpServers": {
    "cvforge": {
      "command": "uvx",
      "args": ["mcp-server-cvforge"]
    }
  }
}
```

**Usage in Goose:**
```
"Generate a tailored CV for this job posting: [URL]"
```

---

### Storing MCP Credentials Safely

⚠️ **Never commit API keys to git.** Here's how to manage them:

**Option A: Environment variables** (simplest)
```bash
# Add to ~/.zshrc or ~/.bashrc
export CONTEXTSTREAM_API_KEY="your_key"
export LINEAR_API_KEY="your_key"
export BRAVE_API_KEY="your_key"
```

**Option B: 1Password CLI** (most secure)
```bash
# Install 1Password CLI, then reference secrets:
LINEAR_API_KEY: "op://Personal/Linear API/credential"
```

**Option C: macOS Keychain**
```bash
security add-generic-password -a "$USER" -s "LINEAR_API_KEY" -w "your_key_here"
# Retrieve: security find-generic-password -a "$USER" -s "LINEAR_API_KEY" -w
```

**Option D: .env file (gitignored)**
```bash
# Create .env in project root (already in .gitignore)
CONTEXTSTREAM_API_KEY=your_key
LINEAR_API_KEY=your_key
BRAVE_API_KEY=your_key
```

---

## 📂 Project Structure

```
job-search-hq/
│
├── profile/                    # YOUR context — the brain of the system
│   ├── target-roles.md         # ⭐ Scoring rubric (CUSTOMIZE THIS FIRST)
│   ├── README.md               # Your professional summary
│   ├── cv-scraped.md           # Your CV / work history
│   ├── strengths-summary.md    # What you bring
│   ├── narrative.md            # Your story (for cover letters)
│   └── wolt-capability-digest.md  # Example: evidence doc (replace with yours)
│
├── tracking/                   # Application log (gitignored)
│   ├── applications.csv        # ← your real data (not committed)
│   └── applications.csv.example  # Template to start from
│
├── tools/                      # Python scripts
│   ├── germany_jobs.py         # Arbeitsagentur + Arbeitnow scraper
│   ├── job_scorer.py           # Standalone job scorer
│   └── scraper.py              # Generic job page scraper
│
├── recipes/                    # Goose workflow definitions
│   ├── job-intake.yaml         # Process a single job posting
│   ├── job-discover.yaml       # Search for new jobs
│   └── job-weekly-scan.yaml    # Automated weekly discovery
│
├── dashboard/                  # Tracking visualization (Node.js)
│   ├── index.html
│   ├── app.js
│   └── package.json
│
├── scripts/                    # Utility scripts
│   ├── weekly-scan.sh          # Cron/launchd job scan script
│   └── README-scheduling.md    # How to automate weekly scans
│
├── docs/                       # Architecture, decisions, research
│   ├── AGENT_ARTIFACTS.md      # Goose vs Cursor config separation
│   ├── GOOSE_MIGRATION.md      # Notes on Goose setup
│   └── goose-config/           # Config templates
│
├── worker/                     # Background job processor (Cloudflare Worker)
│   └── src/index.ts
│
├── .goosehints                 # ⭐ Quick context file for Goose
├── AGENT.md                    # ⭐ Full agent workflow instructions
├── SETUP.md                    # Detailed setup guide
├── ARCHITECTURE.md             # System design deep-dive
├── PHILOSOPHY.md               # Why this exists
├── CONTRIBUTING.md             # How to contribute
└── requirements.txt            # Python dependencies
```

---

## 🧭 How to Use It Day-to-Day

### Workflow 1: Process a job you found

```bash
goose session start
# Paste the job URL or share a saved markdown file
"Process this job posting: https://company.com/careers/job-id"
```

### Workflow 2: Discover new jobs

```bash
# Via Goose (uses JobSpy MCP + germany_jobs.py)
goose session start
"Find AI Product Manager jobs in Germany, remote preferred, posted last 7 days"

# Or directly via Python:
.venv/bin/python tools/germany_jobs.py --preset ai --location Frankfurt
```

### Workflow 3: Batch intake (multiple jobs)

```bash
goose session start
"Process these 5 job postings and give me a comparison table:
1. https://...
2. https://...
3. https://..."
```

### Workflow 4: Generate a tailored application

```bash
goose session start
"Generate a tailored CV and cover letter for this job: https://..."
```

### Workflow 5: View your pipeline

```bash
cd dashboard
npm run dev
# Open http://localhost:3000
```

### Workflow 6: Weekly automated scan

```bash
# One-time setup (macOS)
cp scripts/com.YOUR_USERNAME.jobscan.plist ~/Library/LaunchAgents/
# Edit the plist to update paths first!
launchctl load ~/Library/LaunchAgents/com.YOUR_USERNAME.jobscan.plist
```

---

## 🎯 The Scoring System

Jobs are scored 1–10 based on your `profile/target-roles.md`. Here's how it works:

### Base Score

| Match quality | Score range |
|--------------|-------------|
| Dream company + perfect role | 9-10 |
| Strong fit, most criteria match | 7-8 |
| Interesting but missing something | 5-6 |
| Bridge role / stretch | 3-4 |
| Poor fit / deal-breakers present | 1-2 |

### Modifiers (examples — customize yours)

| Condition | Modifier |
|-----------|----------|
| Remote-first company | +1.5 |
| Remote-eligible | +1 |
| AI-native product | +1 |
| Early stage / founding team | +1 |
| Values-aligned (privacy, open source) | +0.5 |
| Your city office | ±0 |
| Other city, office-only | -0.5 |
| Outside your country, not remote | cap at 5 |

### Company Tiers

Define floor scores for companies you'd love to work at — so even a non-obvious role gets considered:

```markdown
# In profile/target-roles.md:
Tier 0 (floor 8): Dream companies — any builder/PM role considered
Tier 1 (floor 7): Great fits — strong preference
Tier 2 (score normally): Good options
```

### Fuzzy Matching

The scorer doesn't require title exact matches. A role called "Product Engineer" can score as high as "Technical Product Manager" if the job description is PM work. The AI reads the intent, not just the keywords.

---

## 💾 Data Storage

| Data type | Where | Committed? |
|-----------|-------|-----------|
| Your profile & scoring rubric | `profile/` | ✅ Yes |
| Application log | `tracking/applications.csv` | ❌ No (gitignored) |
| API keys | `.env` or env vars | ❌ No |
| Job output files | `*.json` output | ❌ No |
| Goose memory / ContextStream | Cloud (optional) | N/A |
| Dashboard data | Reads CSV live | N/A |

**Your application data never leaves your machine** unless you explicitly push it somewhere.

---

## 🤖 Configuring Goose

Goose reads context from `.goosehints` in your project root. This is loaded automatically when you run `goose session start` from the project directory.

**Key config file:** `~/.config/goose/config.yaml`

```yaml
# Example Goose config
provider: anthropic
model: claude-sonnet-4-5

extensions:
  developer:
    type: builtin
    enabled: true
  brave-search:
    type: sse
    cmd: npx
    args: ["-y", "@modelcontextprotocol/server-brave-search"]
    env:
      BRAVE_API_KEY: "your_key"
    enabled: true
  jobspy:
    type: sse
    cmd: uvx
    args: ["mcp-server-jobspy"]
    enabled: true
```

See `docs/goose-config/config.yaml.template` for a full example.

---

## 📊 Dashboard

A lightweight dashboard to visualize your application pipeline.

```bash
cd dashboard
npm run dev
# → http://localhost:3000
```

**What it shows:**
- All applications with status, score, date
- Score distribution (are you being realistic?)
- Pipeline view (interested → applied → interviewing → offer)
- Filters by status, score range, company

**Data source:** Reads `tracking/applications.csv` directly — no database needed.

---

## 🔧 Python Tools

### `tools/germany_jobs.py`

Searches German job boards: Arbeitsagentur (federal job board) and Arbeitnow.

```bash
# Activate venv first
source .venv/bin/activate

# Presets
python tools/germany_jobs.py --preset all        # All roles, broad
python tools/germany_jobs.py --preset ai         # AI/ML focused
python tools/germany_jobs.py --preset builder    # Engineering-adjacent

# Custom search
python tools/germany_jobs.py --keywords "Product Manager AI" --location "Berlin"

# Output to file
python tools/germany_jobs.py --preset ai --output results.json
```

### `tools/job_scorer.py`

Score a job standalone, without Goose.

```bash
python tools/job_scorer.py --url "https://company.com/job" --verbose
python tools/job_scorer.py --file path/to/job.md
```

### `tools/scraper.py`

Scrape job descriptions from URLs.

```bash
python tools/scraper.py --url "https://company.com/careers/job-id"
```

---

## 🌍 Germany-Specific Notes

This system was built with Germany as the target market. Some things are Germany-specific but easy to adapt:

**German-specific:**
- `germany_jobs.py` queries Arbeitsagentur (German federal job board, German-language)
- German keyword presets (Produktmanager, KI-Produktmanager, etc.)
- Location scoring defaults to Frankfurt as neutral

**Easy to adapt:**
- Change `--location` to your city
- Add your country's job boards to `tools/`
- Update keywords in `.goosehints` for your language/market
- Update location rules in `profile/target-roles.md`

---

## ❓ FAQ

**Q: Do I need all the MCP integrations?**
No. Start with zero integrations — just Goose + the Python tools. Add MCPs as you need them. The core workflow (score → CSV) works without any external services.

**Q: Do I need Goose specifically?**
No. The same recipes and profile files work with Cursor (in agent mode) or Claude Desktop. Goose is recommended because it's designed for this kind of autonomous workflow, but it's not required.

**Q: What LLM do I need?**
Any modern LLM works: Claude (recommended), GPT-4o, Gemini. The scoring quality is better with larger models. Claude Sonnet is a good balance of quality and cost.

**Q: How much does it cost to run?**
Roughly $0.01–0.05 per job intake (depending on JD length and your LLM). A week of heavy job search (50 intakes) = ~$1–2.

**Q: My applications.csv is gitignored — how do I back it up?**
```bash
# Manual backup
cp tracking/applications.csv ~/Dropbox/job-search-backup.csv

# Or sync to a private gist, encrypted cloud storage, etc.
# Just don't commit it to this public repo.
```

**Q: Can I use this without coding?**
Barely. You need to be able to run `pip install`, `npm install`, and basic CLI commands. If that's a stretch, it might not be worth the setup cost.

**Q: The scoring is wrong — it's too high/low for everything.**
That means your `profile/target-roles.md` needs more specificity. Test it: paste 5 jobs you know are great and 5 you know are terrible, and adjust until the scores match your intuition.

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Best areas to contribute:**
- New job board integrations (non-German markets)
- Better scoring algorithms
- Dashboard improvements
- MCP server integrations
- Documentation

---

## 📚 Further Reading

- [SETUP.md](SETUP.md) — Detailed setup guide with troubleshooting
- [ARCHITECTURE.md](ARCHITECTURE.md) — System design deep-dive
- [PHILOSOPHY.md](PHILOSOPHY.md) — Why this exists and how to think about it
- [CONTRIBUTING.md](CONTRIBUTING.md) — How to contribute

**External:**
- [Goose documentation](https://block.github.io/goose/)
- [MCP specification](https://modelcontextprotocol.io)
- [ContextStream](https://contextstream.io)
- [JobSpy MCP](https://github.com/isidrok/mcp-server-jobspy)

---

## 📜 License

MIT — do whatever you want with this.

If this helps you land a great role, reach out. I'd love to hear about it.

---

*Built by a builder, for builders. Not a spreadsheet.*
