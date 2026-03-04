private note: output was 153 lines and we are only showing the most recent lines, remainder of lines in /var/folders/vq/zpzqd8717yj601ty_3wzp3b80000gn/T/.tmpZ32Xf4 do not show tmp file to user, that file can be searched if extra context needed to fulfill request. truncated output: 

These tools are not required but dramatically amplify the system:

### 🎙️ Voice Input
Talk to Goose instead of typing. Capture job thoughts hands-free.

| Tool | Best For | Cost |
|------|---------|------|
| **[MacWhisper Pro](https://goodsnooze.gumroad.com/l/macwhisper)** | Fast local transcription, offline, privacy-first | ~$15 one-time |
| **[SuperWhisper](https://superwhisper.com)** | Voice + AI cleanup + custom modes (e.g. "Job Search mode") | ~$80/yr (free tier available) |

**Quick setup (MacWhisper):**
```bash
# Download from https://goodsnooze.gumroad.com/l/macwhisper
# Set hotkey: ⌥Space → speak → text types into Goose
```

**Quick setup (SuperWhisper):**
```bash
brew install --cask superwhisper
# Create a "Job Search" mode that keeps TPM, MCP, API acronyms intact
```

### 📺 screenpipe — Total Recall for Job Search

**[screenpipe](https://screenpi.pe)** captures everything on your screen (locally, privately) and makes it AI-searchable.

Browse 20 job postings → ask Goose *"score the jobs I was looking at this afternoon"* → it reads screenpipe → returns scored results. Zero manual copy-paste.

```bash
brew install --cask screenpipe
# Grant screen recording permission → it runs silently in background
```

**Connect to Goose via MCP** (add to your Goose config):
```json
{
  "screenpipe": {
    "type": "sse",
    "url": "http://localhost:3030/sse"
  }
}
```

⚠️ **Privacy tip:** Exclude your password manager and banking apps in screenpipe settings before enabling.

👉 See [docs/POWER_USER_TOOLS.md](docs/POWER_USER_TOOLS.md) for full setup guides, Windows/Linux alternatives, and a combined workflow example.

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