#!/bin/bash
# Claude Code usage statusline - wrapper script
# Delegates to claude-usage.py for cross-platform compatibility

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/claude-usage.py"
