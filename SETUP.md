# Setup Guide — Job Search HQ

Welcome! This is an **AI-native job search system** built with Goose, MCP, and modern tooling.

## 🎯 What This Is

A complete job search operation system that:
- Discovers jobs from multiple sources (JobSpy MCP, German job boards, web search)
- Scores opportunities against your criteria (fuzzy matching, not rigid filters)
- Tracks applications with a Next.js dashboard
- Automates task creation (Linear, TickTick)
- Generates tailored CVs (RenderCV integration)
- Provides Goose/Cursor recipes for repeatable workflows

**This is NOT a spreadsheet.** It's a builder's approach to personal operations.

---

## 📋 Prerequisites

- **Goose** (AI-native command runner) — `brew install block/goose/goose` or see [goose.ai](https://goose.ai)
- **Python 3.11+** with venv
- **Node.js 18+** (for dashboard)
- **Git**
- Optional: Cursor/Claude Desktop for MCP integrations

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/YOUR_USERNAME/job-search-hq.git
cd job-search-hq

# Create Python virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install dashboard dependencies
cd dashboard
npm install
cd ..
```

### 2. Configure Your Profile

**This is the most important step!** The system is only as good as your profile.

```bash
cd profile/

# Edit these files to match YOUR situation:
# 1. README.md — your professional summary
# 2. target-roles.md — your scoring rubric (critical!)
# 3. strengths-summary.md — what you bring
# 4. values.md — what matters to you
```

**Key file: `profile/target-roles.md`**
- Defines how jobs are scored (1-10)
- Company tiers (dream/good/acceptable)
- Remote/location preferences
- Title fuzzy matching rules

**The better your profile, the better the AI scores opportunities.**

### 3. Set Up Tracking

```bash
# Copy the example CSV
cp tracking/applications.csv.example tracking/applications.csv

# This is YOUR application log — never committed to git
# Format: company,role,location,status,score,date_added,url,notes
```

### 4. Configure MCP Integrations (Optional)

If using Cursor or Claude Desktop, configure MCP servers:

```json
// ~/.cursor/mcp.json or ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "jobspy": {
      "command": "uvx",
      "args": ["mcp-server-jobspy"]
    },
    "contextstream": {
      "command": "npx",
      "args": ["-y", "@contextstream/mcp-server@latest"],
      "env": {
        "CONTEXTSTREAM_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

Get API keys:
- **ContextStream**: [contextstream.io](https://contextstream.io) (semantic memory)
- **JobSpy**: No key needed, installed via uvx

### 5. Run Job Discovery

```bash
# Activate venv if not already
source .venv/bin/activate

# Search German job boards
python tools/germany_jobs.py --preset ai --location Frankfurt

# Or use JobSpy MCP through Goose/Cursor
goose session start
# Then ask: "Find AI Product Manager jobs in Germany, remote preferred"
```

### 6. Launch Dashboard

```bash
cd dashboard
npm run dev
# Open http://localhost:3000
```

---

## 🎨 Usage Patterns

### Job Intake Workflow

```bash
goose session start
# In Goose, run the job-intake recipe:
# "Process this job posting: [URL]"
```

The recipe will:
1. Fetch and parse the job posting
2. Score it against your profile (1-10)
3. Add to `tracking/applications.csv`
4. Create Linear issue (if configured)
5. Create TickTick task (if configured)

### Job Discovery Workflow

```bash
# Use the job-discover recipe
goose session start
# "Search for [role] in [location], [requirements]"
```

### Manual Scoring

```bash
python tools/job_scorer.py --job-url "https://..." --verbose
```

---

## 📂 Project Structure

```
job-search-hq/
├── profile/           # YOUR context (scoring rubric, strengths, CV data)
├── tracking/          # Application log (CSV — not committed)
├── tools/             # Python scripts (germany_jobs.py, job_scorer.py)
├── recipes/           # Goose workflows (job-intake, job-discover)
├── dashboard/         # Next.js tracking UI
├── scripts/           # Utility scripts
├── docs/              # Architecture, guides, research
└── worker/            # Background job processors
```

---

## 🔧 Configuration

### Environment Variables

Create `.env` in the root:

```bash
# Optional: API keys for integrations
LINEAR_API_KEY=your_key_here
TICKTICK_API_KEY=your_key_here
BRAVE_API_KEY=your_key_here

# Dashboard
NEXT_PUBLIC_APP_NAME="Job Search HQ"
```

### Goose Configuration

The `.goosehints` file contains context for Goose. Key IDs to update:

```yaml
# Linear team ID (if using Linear)
LINEAR_TEAM_ID: your_team_id_here

# TickTick project ID (if using TickTick)
TICKTICK_PROJECT_ID: your_project_id_here
```

---

## 🎯 Customization

### Adapt the Scoring System

Edit `profile/target-roles.md`:

```markdown
## Dream Company Tiers (floor scores)

**Tier 0 → floor 8:** Your dream companies
**Tier 1 → floor 7:** Great fits
**Tier 2 → score normally:** Good options

## Scoring Modifiers

- Remote at remote-first company: +1.5
- Remote-eligible: +1
- Office in your city: neutral
- Outside your country, not remote: cap at 5
```

### Add Custom Job Sources

Edit `tools/germany_jobs.py` or create new scrapers in `tools/`.

### Customize Dashboard

The dashboard is a standard Next.js app. Edit `dashboard/src/` to:
- Add charts/visualizations
- Integrate with your CRM
- Export to other tools

---

## 🆘 Troubleshooting

### "No results from JobSpy"
- Check your internet connection
- Try different search terms
- JobSpy queries Indeed, LinkedIn, Glassdoor — rate limits may apply

### "Scoring always returns 5"
- Your `profile/target-roles.md` needs more detail
- Add company names to tier lists
- Specify role title variations

### "Dashboard shows no data"
- Ensure `tracking/applications.csv` exists
- Check CSV format matches headers
- Restart dev server

---

## 🤝 Contributing

This is a **personal operations system**, but contributions are welcome!

Ideas:
- New job source integrations
- Better scoring algorithms
- Dashboard improvements
- Documentation enhancements

See `CONTRIBUTING.md` for guidelines.

---

## 📚 Learn More

- **Architecture**: See `ARCHITECTURE.md`
- **Philosophy**: See `PHILOSOPHY.md`
- **Goose**: [goose.ai](https://goose.ai)
- **MCP**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **ContextStream**: [contextstream.io](https://contextstream.io)

---

## 📜 License

MIT — see LICENSE file.

---

**Built by [Your Name]** — a builder exploring AI-native personal operations.

Questions? Open an issue or reach out on [LinkedIn](https://linkedin.com/in/your-profile).
