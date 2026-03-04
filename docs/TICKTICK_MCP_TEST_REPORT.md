# TickTick MCP Test Report

**Date:** 2026-02-23  
**Status:** Both servers configured; live testing blocked by auth/network

---

## Current Status

| Server | Cursor Config | Loaded in Cursor | Status |
|--------|---------------|------------------|--------|
| **felores** (`ticktick`) | `~/.cursor/mcp.json` | ❌ Not in available list | Not loaded (likely failing at startup) |
| **ticktick-sdk** | `~/.cursor/mcp.json` | ✅ `user-ticktick-sdk` | **Errored** – server fails to initialize |

**Note:** `STATUS.md` reports ticktick-sdk as errored. Felores does not appear in the MCP server list, so it may be failing before tools are advertised.

---

## Feature Comparison (from source code)

### Felores (ticktick-mcp-server) – 24 tools

**Auth:** OAuth2 only (client_id, client_secret, stored access token)

| Category | Tools |
|----------|-------|
| **Projects** | `get_projects`, `get_project`, `get_project_tasks`, `create_project`, `delete_project` |
| **Tasks** | `get_task`, `create_task`, `update_task`, `complete_task`, `delete_task` |
| **Batch / GTD** | `batch_create_tasks`, `create_subtask` |
| **Filters** | `get_all_tasks`, `get_tasks_by_priority`, `get_tasks_due_today`, `get_tasks_due_tomorrow`, `get_tasks_due_in_days`, `get_tasks_due_this_week`, `get_overdue_tasks` |
| **Search** | `search_tasks` |
| **GTD helpers** | `get_engaged_tasks`, `get_next_tasks` |

**Strengths:** OAuth2-only, GTD-style filters (engaged/next), batch create, subtasks.

---

### TickTick-SDK – 43 tools

**Auth:** V1 (OAuth2) + V2 (username/password) – both required

| Category | Tools |
|----------|-------|
| **Tasks** | `ticktick_create_tasks`, `ticktick_get_task`, `ticktick_list_tasks`, `ticktick_update_tasks`, `ticktick_complete_tasks`, `ticktick_delete_tasks`, `ticktick_move_tasks`, `ticktick_set_task_parents`, `ticktick_unparent_tasks`, `ticktick_search_tasks`, `ticktick_pin_tasks` |
| **Projects** | `ticktick_list_projects`, `ticktick_get_project`, `ticktick_create_project`, `ticktick_update_project`, `ticktick_delete_project` |
| **Folders** | `ticktick_list_folders`, `ticktick_create_folder`, `ticktick_rename_folder`, `ticktick_delete_folder` |
| **Kanban** | `ticktick_list_columns`, `ticktick_create_column`, `ticktick_update_column`, `ticktick_delete_column` |
| **Tags** | `ticktick_list_tags`, `ticktick_create_tag`, `ticktick_update_tag`, `ticktick_delete_tag`, `ticktick_merge_tags` |
| **User** | `ticktick_get_profile`, `ticktick_get_status`, `ticktick_get_statistics`, `ticktick_get_preferences` |
| **Focus** | `ticktick_focus_heatmap`, `ticktick_focus_by_tag` |
| **Habits** | `ticktick_habits`, `ticktick_habit`, `ticktick_habit_sections`, `ticktick_create_habit`, `ticktick_update_habit`, `ticktick_delete_habit`, `ticktick_checkin_habits`, `ticktick_habit_checkins` |

**Strengths:** Habits, tags, folders, kanban columns, focus/pomodoro, user stats, batch operations, markdown/JSON output.

---

## Differences Summary

| Feature | Felores | TickTick-SDK |
|---------|---------|--------------|
| Auth | OAuth2 only | OAuth2 + session (both required) |
| Habits | ❌ | ✅ |
| Tags CRUD | ❌ | ✅ |
| Folders | ❌ | ✅ |
| Kanban columns | ❌ | ✅ |
| Focus / Pomodoro | ❌ | ✅ |
| User stats | ❌ | ✅ |
| GTD filters (engaged/next) | ✅ | ❌ (use list_tasks filters) |
| Batch create | ✅ | ✅ |
| Subtasks | ✅ | ✅ (via set_task_parents) |
| Tool count | 24 | 43 |

---

## How to Test (when credentials are valid)

### 1. Verify credentials

**Felores:**
- `~/.config/ticktick-mcp/credentials.json` exists and has valid access token
- `TICKTICK_CLIENT_ID` and `TICKTICK_CLIENT_SECRET` in `mcp.json` (not `REPLACE_ME`)

**TickTick-SDK:**
- `~/.config/ticktick-sdk/credentials.json` exists
- `TICKTICK_USERNAME` and `TICKTICK_PASSWORD` in `mcp.json` (not `REPLACE_ME`)

### 2. Restart Cursor

Restart Cursor so both MCP servers reload. Check **Settings → MCP** for status.

### 3. Manual tool test

In a Cursor chat, ask the AI to:
- **Felores:** "List my TickTick projects" (uses `get_projects`)
- **TickTick-SDK:** "List my TickTick projects" (uses `ticktick_list_projects`)

### 4. CLI smoke test (optional)

```bash
# Felores – list tools (requires network + valid token)
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | \
  /path/to/your/job-search-hq/.venv/bin/ticktick-mcp-server run 2>/dev/null | head -200

# TickTick-SDK – list tools (requires network + valid credentials)
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | \
  TICKTICK_CREDENTIALS_PATH="$HOME/.config/ticktick-sdk/credentials.json" \
  TICKTICK_USERNAME="your@email.com" TICKTICK_PASSWORD="yourpassword" \
  /path/to/your/job-search-hq/ticktick-sdk/.venv/bin/ticktick-sdk server 2>/dev/null | head -500
```

---

## Recommendations

1. **Fix ticktick-sdk auth** – Ensure `TICKTICK_USERNAME` and `TICKTICK_PASSWORD` in `mcp.json` are real values (or that credentials file is valid). The server needs both V1 and V2 auth.
2. **Fix felores loading** – If you want felores, ensure `TICKTICK_CLIENT_ID` and `TICKTICK_CLIENT_SECRET` are set and the OAuth flow has been run (`ticktick-mcp-server auth`).
3. **Choose one for daily use** – TickTick-SDK has more features (habits, tags, focus). Felores is simpler and OAuth-only. Run both in parallel only if you need both feature sets.
4. **Optional:** Use `TICKTICK_ENABLED_TOOLS` with ticktick-sdk to limit tools and reduce context usage.
```
