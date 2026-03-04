private note: output was 252 lines and we are only showing the most recent lines, remainder of lines in /var/folders/vq/zpzqd8717yj601ty_3wzp3b80000gn/T/.tmpQK8De1 do not show tmp file to user, that file can be searched if extra context needed to fulfill request. truncated output: 
**Connect screenpipe to Goose via MCP:**
```json
// Add to your Goose MCP config (~/.config/goose/config.yaml or mcp.json)
{
  "screenpipe": {
    "type": "sse",
    "url": "http://localhost:3030/sse"
  }
}
```

Then in Goose you can ask:
> "What job postings did I look at in the last 3 days?"
> "Find the JD for that AI engineer role I was reading this morning"
> "What did I say about [company] last week?"

### Privacy Considerations

screenpipe captures **everything** on your screen. Before enabling:

- ✅ **Safe:** It's 100% local. Nothing is uploaded.
- ✅ **Safe:** You can exclude apps (e.g. banking, password managers)
- ⚠️ **Be careful:** Exclude your password manager, banking apps, anything with sensitive creds
- ⚠️ **Be careful:** Disable before screen sharing in meetings

**Exclusion config:**
```bash
# In screenpipe settings, add to excluded apps:
# - 1Password
# - Bitwarden  
# - Proton Pass
# - Banking apps
# - Any app with credentials
```

### screenpipe MCP in Practice

Once connected to Goose, a powerful workflow becomes:

1. Browse job postings on LinkedIn (screenpipe captures it all)
2. Ask Goose: *"Based on what I've been browsing today, which roles look like the best fit?"*
3. Goose queries screenpipe, gets the raw screen captures, scores them against your profile
4. You get a ranked list of jobs you *already looked at* — no re-browsing needed

**Cost:** Free (open source). Pro plan available for cloud sync + team features.

---

## 🔗 Combining All Three

The ultimate job search setup:

```
screenpipe (background)     → captures everything you see/hear
      ↓
MacWhisper/SuperWhisper     → voice input for quick commands
      ↓
Goose + MCP                 → orchestrates everything
      ↓
Job Search HQ               → scores, tracks, creates tasks
```

**Example power workflow:**

1. You browse LinkedIn for 20 minutes (screenpipe captures everything)
2. You spot 3 interesting roles but don't click "save"
3. Later, you tell Goose via voice (MacWhisper): *"Score the jobs I was looking at on LinkedIn this afternoon"*
4. Goose queries screenpipe → extracts the JDs → scores them → adds top ones to tracking
5. Total manual effort: 10 seconds of talking

---

## 📦 Quick Install Summary

```bash
# MacWhisper Pro
# → https://goodsnooze.gumroad.com/l/macwhisper (~$15)

# SuperWhisper  
# → https://superwhisper.com (~$80/yr, has free tier)
brew install --cask superwhisper  # if available

# screenpipe
brew install --cask screenpipe
# Or: https://screenpi.pe (free, open source)
```

---

## 🪟 Windows / Linux Alternatives

| Tool | Windows | Linux |
|------|---------|-------|
| Voice input | Windows Speech Recognition (built-in) | [Whisper.cpp](https://github.com/ggerganov/whisper.cpp) + [wtype](https://github.com/atx/wtype) |
| SuperWhisper-like | [Whisper Anywhere](https://github.com/htoooth/WhisperAnywhere) | Same |
| screenpipe | ✅ screenpipe works on Windows | ✅ screenpipe works on Linux |

---

*These are tools the original author uses. No affiliate links. No sponsorships. Just things that work.*