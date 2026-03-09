# Contributing

Contributions welcome. This is a personal ops system open-sourced for others — improvements that help everyone are great.

---

## Good areas to contribute

**New job sources** — scrapers or API integrations for non-German markets, niche boards (AngelList, YC, ProductHunt jobs), company-specific career pages. Add to `tools/`. See `tools/germany_jobs.py` for reference.

**Better scoring** — ML-based preference learning, salary band estimation, company culture signal detection. Edit `tools/job_scorer.py`.

**Agent workflows** — new workflows for Goose (`recipes/`), Claude Code (`.claude/commands/`), or Cursor. When adding a workflow, provide all agent formats if you can.

**Documentation** — better examples, troubleshooting, use cases.

---

## Development setup

```bash
git clone https://github.com/YOUR_USERNAME/job-search-hq.git
cd job-search-hq
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Code style

**Python:** PEP 8. Type hints where reasonable. `black` formatter if installed.

**Commit messages:** Conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`).

---

## What NOT to contribute

- Personal data (real CSVs, contact info, API keys)
- Features that violate job board ToS (auto-apply, scraping behind auth walls)
- Breaking changes to CSV schema without a migration path

Discuss big changes in an issue first.

---

## Submitting

1. Fork and create a branch (`feature/your-feature`)
2. Make changes, test locally
3. Submit a PR with a clear description

If this project helped you, a star or a note about it is always appreciated.
