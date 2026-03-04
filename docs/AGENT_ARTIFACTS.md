# Agent Artifacts — Cursor vs Goose Separation

This doc clarifies which files and flows belong to which agent, so you don't mix Cursor-specific and Goose-specific artifacts.

---

## Why AGENT.md vs AGENTS.md?

| File | Convention | Used by |
|------|------------|---------|
| **AGENT.md** | Goose's convention | Goose (and Cursor in this project) |
| **AGENTS.md** | Broader agent ecosystem (Cursor, Copilot, Codex) — [agentsmd.io](https://agentsmd.io) | Cursor, when present |

**This project uses AGENT.md** because:
1. Goose is the primary agent (per README, AGENT.md)
2. Goose recipes explicitly reference `AGENT.md` — see `recipes/job-intake.yaml`, `recipes/job-discover.yaml`
3. Goose docs: "Project-specific hints can be added via `.goosehints` and/or `AGENT.md`"
4. AGENTS.md is in `.gitignore` — kept local-only for Cursor overrides if needed

---

## Artifact Separation

### Cursor-only (do not reference in Goose flows)

| Artifact | Purpose |
|----------|---------|
| `.cursor/` | Rules, MCP config, project settings |
| `.cursor/rules/*.mdc` | Cursor rules (e.g. job-intake-workflow.mdc) |
| `~/.cursor/mcp.json` | Cursor MCP server config |
| `AGENTS.md` | Cursor local overrides (gitignored) |
| `CLAUDE.md`, `GEMINI.md` | Model-specific Cursor instructions (gitignored) |
| `.cursorrules` | Legacy Cursor rules (gitignored) |
| **ContextStream** | `init()`, `context()`, `search()` — Cursor MCP only |
| **ContextStream rules** | `.cursorrules` / ContextStream workspace — Cursor only |

**When in Cursor:** Use ContextStream, .cursor/rules. Do NOT tell the user to "run goose recipe" as the primary path.

---

### Goose-only (do not reference in Cursor flows)

| Artifact | Purpose |
|----------|---------|
| `recipes/*.yaml` | Goose recipe definitions |
| `.goosehints` | Goose project hints (optional; use AGENT.md if shared) |
| `~/.config/goose/` | Goose global config (config.yaml, profiles.yaml) |
| **Goose recipes** | `goose recipe job-intake <url>`, `goose recipe job-discover` |
| **Goose extensions** | MCPs configured in profiles.yaml, not mcp.json |

**When in Goose:** Use recipes, AGENT.md. Do NOT reference ContextStream, .cursor/rules, or init/context/search.

---

### Shared (both agents)

| Artifact | Purpose |
|----------|---------|
| **AGENT.md** | Job intake workflow, scoring, discovery, resume tailoring, safety |
| `profile/target-roles.md` | Target roles, companies, scoring criteria |
| `profile/README.md` | Profile context |
| `tracking/applications.csv` | Application log |
| `docs/PROJECT_STATE.md` | Full project state |

**Shared content:** Top of Mind IDs (Linear, TickTick), scoring rules, safety rules, workflow steps. The *workflow logic* is shared; the *trigger* differs (Cursor: chat; Goose: recipes).

---

## Flow Separation Rules

1. **Cursor:** User chats → agent follows AGENT.md or .cursor/rules → uses Cursor MCPs (Linear, TickTick, ContextStream, etc.)
2. **Goose:** User runs `goose recipe job-intake <url>` → recipe invokes agent with AGENT.md → uses Goose extensions (MCPs in profiles.yaml)
3. **Do not cross-reference:** Cursor instructions should not say "run goose recipe" as the primary path. Goose recipes should not reference ContextStream or .cursor/rules.
4. **AGENT.md** contains the shared workflow. When editing, keep sections agent-agnostic. Agent-specific tool references (e.g. "Use ContextStream" vs "Use Goose Memory") belong in agent-specific docs.

---

## Quick Reference

| I need to... | In Cursor | In Goose |
|--------------|-----------|----------|
| Job intake | Chat with URL; agent follows AGENT.md | `goose recipe job-intake <url>` |
| Job discovery | Ask agent to search; uses tools from AGENT.md | `goose recipe job-discover` |
| Add rules | `.cursor/rules/*.mdc` | AGENT.md or .goosehints |
| Configure MCPs | `~/.cursor/mcp.json` | `~/.config/goose/profiles.yaml` |
| Context/memory | ContextStream | Goose Memory extension |
```
