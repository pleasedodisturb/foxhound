# Power User Tools

These tools are **not required** but dramatically improve the experience. Think of them as the "hardware upgrades" for this system.

---

## 🎙️ Voice Input — Stop Typing, Start Talking

One of the most underrated productivity boosts for job searching: **voice-to-text your thoughts directly into Goose**.

Instead of typing:
> "Score this job and add it to tracking"

You just say it. While walking. While cooking. While commuting.

---

### Option A: MacWhisper Pro (macOS, recommended for quality)

**[MacWhisper](https://goodsnooze.gumroad.com/l/macwhisper)** — local Whisper transcription, no cloud, fast.

**Why it's great for job search:**
- Dictate job descriptions directly into Goose chat
- Voice-type cover letter ideas while reviewing a JD
- Capture "why I liked this company" notes hands-free
- Works fully offline — your thoughts stay private

**Setup:**
```bash
# Install via Homebrew (unofficial cask) or download directly
brew install --cask macwhisper

# Or download from:
# https://goodsnooze.gumroad.com/l/macwhisper
```

**Recommended settings:**
- Model: Whisper Large v3 (best accuracy, ~3GB download)
- Hotkey: ⌥Space (global push-to-talk)
- Output: "Type into active app" mode — transcribes directly into wherever your cursor is
- Language: Auto-detect (handles English + German seamlessly)

**Job search workflow:**
1. Open Goose
2. Hold ⌥Space → speak your command or paste URL + say "process this"
3. Release → text appears → hit Enter
4. Done

**Cost:** ~$15 one-time (Pro unlocks larger models + features)

---

### Option B: SuperWhisper (macOS, best UX + AI post-processing)

**[SuperWhisper](https://superwhisper.com)** — Whisper + AI cleanup + global hotkey magic.

**What makes it different from MacWhisper:**
- AI post-processing: fixes grammar, punctuation, formatting after transcription
- "Modes" — you can set a mode like "Technical dictation" that knows to keep acronyms like TPM, MCP, API intact
- Prompt injection: prefix your transcription with a system prompt
- Clipboard + type modes

**Why it's great for job search:**
- Set a "Job Search" mode that outputs clean, formatted notes
- Dictate your initial take on a company ("Mistral: AI-first, remote, my kind of place, score this high")
- Voice-type long cover letter drafts that AI then cleans up
- Capture post-interview notes immediately while memory is fresh

**Setup:**
```bash
# Download from:
# https://superwhisper.com

# Or Mac App Store
```

**Recommended config:**
- Global hotkey: ⌘⌥Space (distinct from MacWhisper if you run both)
- Default mode: "Technical writing" or create a custom "Job Search" mode
- Model: Cloud (faster) or local Large v3 (private)

**Custom "Job Search" mode prompt:**
```
You are transcribing notes for a technical job search. 
Keep acronyms intact: TPM, PM, AI, ML, MCP, API, SaaS, ARR, OKR, FAANG.
Format output as clean prose with proper punctuation.
If the speaker gives a score like "8 out of 10" format it as "8/10".
```

**Cost:** ~$10/month or ~$80/year (has free tier with limits)

---

### MacWhisper vs SuperWhisper — Which to Choose?

| | MacWhisper Pro | SuperWhisper |
|---|---|---|
| **Best for** | Pure transcription speed | AI-cleaned output + modes |
| **Privacy** | 100% local | Local or cloud (your choice) |
| **Languages** | All Whisper languages | All Whisper languages |
| **AI cleanup** | No | Yes (fixes grammar/formatting) |
| **Custom modes** | No | Yes |
| **Price** | ~$15 one-time | ~$80/year |
| **Verdict** | 🏆 If you just want fast, accurate voice input | 🏆 If you want smarter output |

**Recommendation:** Start with MacWhisper Pro. Add SuperWhisper if you find yourself editing transcriptions a lot.

---

## 📺 screenpipe — Continuous Context Capture

**[screenpipe](https://screenpi.pe)** — 24/7 local screen + audio recording with AI search.

Think of it as **total recall for your job search**. Every job posting you looked at, every Goose conversation, every LinkedIn profile you visited — all searchable, all local, all private.

### Why This Changes Job Search

Without screenpipe:
- "What was that company I saw three days ago?"
- "What did Goose say about that role before I dismissed it?"
- "What were those specific phrases in that JD I liked?"

→ Gone. Unrecoverable.

With screenpipe:
- Search "Mistral" → see every time you looked at anything Mistral-related
- Search "founding engineer remote" → surfaces every job post you browsed
- Search "interview prep" → finds that tab you had open for 5 minutes last Tuesday

### Key Features for Job Searching

- **Screen OCR** — captures text from everything you see, even non-copyable PDFs
- **Audio transcription** — records and transcribes system audio + mic (useful for interview notes)
- **AI search** — semantic search across everything captured
- **Local-first** — nothing leaves your machine
- **MCP server included** — plug directly into Goose/Cursor for context injection

### Setup

```bash
# Install via Homebrew
brew install --cask screenpipe

# Or download from:
# https://screenpi.pe
```

**First run:**
1. Grant screen recording permission (System Settings → Privacy → Screen Recording)
2. Grant microphone permission (optional, for audio capture)
3. It starts running silently in the background

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
