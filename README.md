# claude-tools

A collection of small, focused utilities that enhance the Claude Code workflow.
Each tool lives in its own subfolder and is independently installable.

## Tools

| Tool | Description | Windows | macOS |
|------|-------------|---------|-------|
| [usage-statusline](./usage-statusline/) | Live 5h & 7d usage limits in your Claude Code statusline | ✅ | 🔜 |

## Philosophy

- **One tool, one folder** — each utility is self-contained
- **Zero workflow impact** — tools integrate silently into existing Claude Code features
- **Cross-platform** — Windows and macOS support for every tool

## Roadmap

- [ ] macOS support for all tools
- [ ] Per-tool install scripts (`install.sh`)
- [ ] Single global installer for the whole collection

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI
- Python 3.8+
- Git Bash (Windows) or bash (macOS/Linux)
