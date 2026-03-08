#!/usr/bin/env python3
"""
Claude Code usage statusline
Fetches 5-hour and 7-day usage limits from the Anthropic OAuth API.
Refreshes on every call, with a 10-second debounce cache.
"""

import io
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone

# Force UTF-8 output on Windows, use Unix line endings
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", newline="\n")

CACHE_MAX_AGE = 10  # seconds — debounce only, effectively per-call

def get_cache_path():
    # Use temp dir that works cross-platform
    tmp = os.environ.get("TEMP") or os.environ.get("TMP") or "/tmp"
    return os.path.join(tmp, "claude-usage-cache.json")

def get_credentials_path():
    return os.path.join(os.path.expanduser("~"), ".claude", ".credentials.json")

def load_token():
    creds_path = get_credentials_path()
    if not os.path.exists(creds_path):
        return None
    with open(creds_path) as f:
        d = json.load(f)
    return d.get("claudeAiOauth", {}).get("accessToken")

def load_cache():
    cache_path = get_cache_path()
    if not os.path.exists(cache_path):
        return None
    age = time.time() - os.path.getmtime(cache_path)
    if age > CACHE_MAX_AGE:
        return None
    with open(cache_path) as f:
        return json.load(f)

def save_cache(data):
    cache_path = get_cache_path()
    with open(cache_path, "w") as f:
        json.dump(data, f)

def fetch_usage(token):
    req = urllib.request.Request(
        "https://api.anthropic.com/api/oauth/usage",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "anthropic-beta": "oauth-2025-04-20",
            "User-Agent": "claude-code/statusline",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read())
    except Exception:
        return None

def color(pct):
    if pct >= 80:
        return "\033[31m"  # red
    if pct >= 50:
        return "\033[33m"  # yellow
    return "\033[32m"      # green

RESET = "\033[0m"

def time_until(iso_str):
    """Return a compact human-readable string for time remaining until iso_str."""
    if not iso_str:
        return ""
    try:
        reset_at = datetime.fromisoformat(iso_str)
        now = datetime.now(timezone.utc)
        delta = reset_at - now
        secs = int(delta.total_seconds())
        if secs <= 0:
            return "now"
        days, rem = divmod(secs, 86400)
        hours, rem = divmod(rem, 3600)
        minutes = rem // 60
        if days > 0:
            return f"{days}d{hours}h"
        if hours > 0:
            return f"{hours}h{minutes:02d}m"
        return f"{minutes}m"
    except Exception:
        return ""

def format_output(data):
    h = data.get("five_hour") or {}
    w = data.get("seven_day") or {}
    h_pct = h.get("utilization") or 0
    w_pct = w.get("utilization") or 0
    h_reset = time_until(h.get("resets_at"))
    w_reset = time_until(w.get("resets_at"))

    h_reset_str = f" ↺ {h_reset}" if h_reset else ""
    w_reset_str = f" ↺ {w_reset}" if w_reset else ""

    return (
        f"\u26a1 5h {color(h_pct)}{h_pct:.0f}%{RESET}{h_reset_str}"
        f"  7d {color(w_pct)}{w_pct:.0f}%{RESET}{w_reset_str}"
    )

def main():
    # Read and discard stdin (Claude Code sends session JSON)
    sys.stdin.read()

    data = load_cache()
    if data is None:
        token = load_token()
        if not token:
            print("\u26a1 no auth")
            return
        data = fetch_usage(token)
        if data:
            save_cache(data)
        else:
            print("\u26a1 unavailable")
            return

    print(format_output(data))

if __name__ == "__main__":
    main()
