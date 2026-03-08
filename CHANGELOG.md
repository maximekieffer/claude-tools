# Changelog

All notable changes to this project will be documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Planned
- macOS support for `usage-statusline`
- Per-tool `install.sh` scripts
- Global installer for the full collection

---

## [0.1.0] - 2026-03-08

### Added
- `usage-statusline` tool — displays live 5-hour and 7-day Claude API usage limits
  directly in the Claude Code statusline
- 5-minute result caching to avoid hammering the API
- Color-coded output (green / yellow / red) based on utilization
- Windows support via Git Bash + Python 3
