# usage-statusline

Displays your Claude API 5-hour and 7-day usage limits live in the Claude Code
statusline — no more typing `/usage`, always visible while you code.

**Example output:**
```
⚡ 5h 20% | 7d 27%
```
Color coding: green below 50%, yellow 50–80%, red above 80%.

---

## How it works

1. Reads your OAuth token from `~/.claude/.credentials.json`
2. Calls `https://api.anthropic.com/api/oauth/usage`
3. Caches the result for 5 minutes
4. Outputs a compact colored string to the Claude Code statusline

The statusline script is invoked automatically by Claude Code after each
response — no background process, no daemon, zero overhead.

---

## Platform support

| Platform | Status |
|----------|--------|
| Windows (Git Bash) | ✅ Supported |
| macOS | 🔜 Planned |
| Linux | 🔜 Planned |

---

## Requirements

- Claude Code CLI (authenticated with a Claude.ai account)
- Python 3.8+
- `curl`
- Git Bash (Windows) or bash (macOS/Linux)

---

## Manual installation

### 1. Clone or copy the files

```bash
# Example: place the tool under ~/tools/claude-tools/
git clone https://github.com/YOUR_USERNAME/claude-tools ~/tools/claude-tools
```

### 2. Make the script executable

```bash
chmod +x ~/tools/claude-tools/usage-statusline/claude-usage.sh
```

### 3. Update `~/.claude/settings.json`

Add (or merge) the following block:

```json
{
  "statusLine": {
    "type": "command",
    "command": "/path/to/claude-tools/usage-statusline/claude-usage.sh",
    "padding": 1
  }
}
```

> **Windows note:** use the Git Bash path format, e.g. `/e/projects/claude-tools/usage-statusline/claude-usage.sh`

### 4. Reload Claude Code

Open a new Claude Code session — the statusline will appear immediately.

---

## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| Cache TTL | 300 s | Edit `CACHE_MAX_AGE` in `claude-usage.py` |
| Color thresholds | 50% / 80% | Edit the `color()` function in `claude-usage.py` |

---

## Roadmap

- [ ] macOS / Linux support
- [ ] `install.sh` script that patches `settings.json` automatically
- [ ] Token auto-refresh on expiry
- [ ] Optional opus usage line (`seven_day_opus`)
