#!/usr/bin/env bash
# Loads the newest handoff and the board summary into every new session.
cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}" || exit 0
latest=$(ls -1 vault/handoffs/*.md 2>/dev/null | grep -v '/README.md$' | sort | tail -n 1)
if [ -n "$latest" ]; then
  echo "Latest handoff ($latest):"
  head -n 80 "$latest"
else
  echo "No handoff yet. If this is a new project, the owner should run /kickoff."
fi
echo
python3 tools/board.py show --brief 2>/dev/null || true
