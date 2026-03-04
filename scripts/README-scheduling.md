# Scheduling — Job Search Automation

## What Can Be Scheduled

### ✅ Fully automated (no Goose session needed)
- `scripts/weekly-scan.sh` — runs germany_jobs.py, saves raw JSON
- Can run via launchd on macOS

### ⚠️ Requires Goose session (semi-automated)
- `goose recipe job-weekly-scan` — full AI-scored weekly digest
- `goose recipe job-discover` — interactive discovery session
- `goose recipe job-intake <url>` — intake a specific posting

Goose Desktop (Electron app) doesn't currently support headless/scheduled recipe execution.
The `goosed` binary runs the agent server, not recipes directly.

**Workaround**: Use launchd to run the lightweight shell script, then open Goose manually
to run the AI-scored digest when you want the full scored output.

## macOS launchd Setup (weekly-scan.sh)

### 1. Create the plist

Save to ~/Library/LaunchAgents/com.YOUR_USERNAME.jobscan.plist:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.YOUR_USERNAME.jobscan</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/path/to/your/job-search-hq/scripts/weekly-scan.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/path/to/your/job-search-hq/logs/launchd-stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/your/job-search-hq/logs/launchd-stderr.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
```

### 2. Install it

```bash
# Make script executable
chmod +x /path/to/your/job-search-hq/scripts/weekly-scan.sh

# Copy plist
cp scripts/com.YOUR_USERNAME.jobscan.plist ~/Library/LaunchAgents/

# Load it
launchctl load ~/Library/LaunchAgents/com.YOUR_USERNAME.jobscan.plist

# Verify
launchctl list | grep jobscan

# Test run immediately
launchctl start com.YOUR_USERNAME.jobscan
```

### 3. Uninstall if needed

```bash
launchctl unload ~/Library/LaunchAgents/com.YOUR_USERNAME.jobscan.plist
```

## Full AI Scan (manual, weekly habit)

Every Monday morning, open Goose and run:
```
goose recipe job-weekly-scan
```

This runs the full scored digest with all sources (JobSpy + Germany APIs + Himalayas).
Takes 3-5 minutes. Review digest, then run `goose recipe job-intake <url>` for anything interesting.

## Recommended Weekly Rhythm

| Day | Action |
|-----|--------|
| Monday AM | Open Goose → run job-discover or job-weekly-scan |
| Mon-Wed | Process interesting roles via job-intake |
| Thu | Follow up on any applications sent |
| Fri | Review tracking/applications.csv status |

