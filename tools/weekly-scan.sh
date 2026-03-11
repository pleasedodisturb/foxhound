### scripts/weekly-scan.sh
```bash
#!/bin/bash
# Weekly job scan — runs goose recipe job-weekly-scan headlessly
# Designed for launchd scheduling on macOS
# 
# To install: see scripts/README-scheduling.md

set -euo pipefail

JOBS_DIR="$(dirname "$0")/.."
LOG_DIR="$JOBS_DIR/logs"
GOOSE_BIN="/Applications/Goose.app/Contents/Resources/bin/goosed"

mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/weekly-scan-$TIMESTAMP.log"

echo "=== Weekly Job Scan: $TIMESTAMP ===" | tee "$LOG_FILE"
echo "Working dir: $JOBS_DIR" | tee -a "$LOG_FILE"

cd "$JOBS_DIR"

# Note: goosed runs the agent server, not recipes directly.
# Until goose CLI supports headless recipe execution, this runs germany_jobs.py
# as a standalone scan and prints the digest location.

echo "Running Germany API scan..." | tee -a "$LOG_FILE"
.venv/bin/python tools/germany_jobs.py --preset all --limit 25 --output json \
  > "tracking/weekly-raw-$TIMESTAMP.json" 2>>"$LOG_FILE" || true

echo "Germany scan complete. Raw results: tracking/weekly-raw-$TIMESTAMP.json" | tee -a "$LOG_FILE"
echo "Open Goose and run: goose recipe job-weekly-scan" | tee -a "$LOG_FILE"
echo "=== Done ===" | tee -a "$LOG_FILE"

