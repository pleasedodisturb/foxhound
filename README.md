private note: output was 108 lines and we are only showing the most recent lines, remainder of lines in /var/folders/vq/zpzqd8717yj601ty_3wzp3b80000gn/T/.tmpm5bRlY do not show tmp file to user, that file can be searched if extra context needed to fulfill request. truncated output: 
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


**Q: Can I use voice input?**
Yes — and it's highly recommended. [MacWhisper Pro](https://goodsnooze.gumroad.com/l/macwhisper) (~$15) or [SuperWhisper](https://superwhisper.com) let you dictate job commands and notes directly into Goose. See [docs/POWER_USER_TOOLS.md](docs/POWER_USER_TOOLS.md).

**Q: Can Goose see jobs I was browsing without me saving them?**
Yes, with [screenpipe](https://screenpi.pe). It runs locally in the background, captures your screen (privately, no cloud), and exposes an MCP server. Ask Goose: *"score the jobs I was browsing this afternoon"* — it reads your screen history and processes them automatically.

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