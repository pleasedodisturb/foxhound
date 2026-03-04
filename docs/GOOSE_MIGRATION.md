# Cursor to Goose Migration Log

Migration of Job Search HQ from Cursor IDE to Block's Goose AI agent. Plan reference: Cursor to Goose Migration Plan (cursor_to_goose_migration).

---

## Completed

### Phase 1: Install and Configure Goose

- **1.1** Install: `brew install --cask block-goose` (user runs manually)
- **1.2** Config dir: `~/.config/goose/` (exists)
- **1.3** Config templates: `docs/goose-config/config.yaml.template`, `docs/goose-config/profiles.yaml.template`. If you had existing `~/.config/goose/` config, restore from `config.yaml.bak` / merge extensions as needed.
- **1.4** Credentials: [docs/GOOSE_CREDENTIALS.md](GOOSE_CREDENTIALS.md) — Proton Pass + pass-cli wrapper for TickTick, ContextStream, GitHub, Brave Search

### Phase 2: Project Hints and Rules

- **2.1** [AGENT.md](../AGENT.md) — job intake workflow, scoring, CSV format, Linear/TickTick IDs, input formats
- **2.2** [recipes/job-intake.yaml](../recipes/job-intake.yaml) — Goose recipe for job intake. For discovery: run from project root or set `GOOSE_RECIPE_PATH` to include `recipes/`

### Phase 3: MCP Migration

| MCP        | Status | Notes |
|-----------|--------|-------|
| Linear    | Check registry | Add to profiles.yaml if MCP available |
| TickTick  | Template in docs | pass-cli wrapper; Felores or ticktick-sdk |
| ContextStream | Template in docs | pass-cli wrapper |
| Memory    | Built-in | Goose has Memory extension |
| browsermcp | Computer Controller | Use built-in for web scraping |
| Brave Search | Template in docs | pass-cli wrapper |
| GitHub    | Template in docs | pass-cli wrapper |

### Phase 4: External Systems

- No changes — Cloudflare Worker, Dashboard, tracking files unchanged
- Same API keys and project IDs (Linear: `YOUR_LINEAR_TEAM_ID`, TickTick: `YOUR_TICKTICK_PROJECT_ID`)

### Phase 5: Documentation

- This file
- [GOOSE_CREDENTIALS.md](GOOSE_CREDENTIALS.md)
- [PROJECT_STATE.md](PROJECT_STATE.md) — "Primary agent: Goose" section
- `.gitignore` — `.goosehints` only if it contains secrets (AGENT.md committed)

### Phase 6: Cutover

- README.md updated: Goose as primary agent

---

## Validation Checklist

- [ ] Goose installs and runs
- [ ] All MCPs load (no startup errors)
- [ ] Job intake: URL → parse → score → CSV → Linear → TickTick
- [ ] LinkedIn scrape: Computer Controller or browsermcp
- [ ] Memory: create/update entity
- [ ] ContextStream: create event
- [ ] Git commit and push from Goose

---

## Rollback

- Keep `~/.cursor/mcp.json` and `.cursor/rules/` until Goose is validated
- To restore Cursor: use existing mcp.json; rules remain in `.cursor/rules/`

---

## File Summary

| Action | File |
|--------|------|
| Create | `AGENT.md` |
| Create | `docs/GOOSE_MIGRATION.md` |
| Create | `docs/GOOSE_CREDENTIALS.md` |
| Create | `docs/goose-config/config.yaml.template` |
| Create | `docs/goose-config/profiles.yaml.template` |
| Create | `recipes/job-intake.yaml` |
| Update | `docs/PROJECT_STATE.md` |
| Update | `README.md` |
| Preserve | `.cursor/` |
```
