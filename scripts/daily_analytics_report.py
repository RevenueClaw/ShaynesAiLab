#!/usr/bin/env python3
"""
Daily analytics report for Shayne's AI Lab.

Runs analytics_report.py for the last 24 hours and sends the text summary
to Telegram. Intended to run from cron once per day.

Usage:
    python3 scripts/daily_analytics_report.py
"""
import os
import subprocess
import sys
from pathlib import Path
import urllib.request
import urllib.parse
import json


TELEGRAM_BOT_TOKEN = (
    os.environ.get("TELEGRAM_BOT_TOKEN", "")
    or os.environ.get("CHIPRADAR_TELEGRAM_BOT_TOKEN", "")
    or os.environ.get("TG_BOT", "")
)
TELEGRAM_CHAT_ID = (
    os.environ.get("TELEGRAM_CHAT_ID", "8645083973")
    or os.environ.get("CHIPRADAR_TELEGRAM_CHAT_ID", "8645083973")
    or os.environ.get("TG_CHAT", "8645083973")
)

ENV_FILE = Path("/home/rock/.openclaw/credentials/chipradar.env")


def _load_env_file(path: Path):
    """Load KEY=value pairs from an env file that may contain unquoted values."""
    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key:
                os.environ.setdefault(key, value)


_load_env_file(ENV_FILE)

# Re-evaluate after loading env file
TELEGRAM_BOT_TOKEN = (
    os.environ.get("TELEGRAM_BOT_TOKEN", "")
    or os.environ.get("CHIPRADAR_TELEGRAM_BOT_TOKEN", "")
    or os.environ.get("TG_BOT", "")
)
TELEGRAM_CHAT_ID = (
    os.environ.get("TELEGRAM_CHAT_ID", "8645083973")
    or os.environ.get("CHIPRADAR_TELEGRAM_CHAT_ID", "8645083973")
    or os.environ.get("TG_CHAT", "8645083973")
)

REPO_DIR = Path(__file__).resolve().parent.parent
REPORT_SCRIPT = REPO_DIR / "scripts" / "analytics_report.py"


def send_telegram(message: str) -> bool:
    if not TELEGRAM_BOT_TOKEN:
        print("TELEGRAM_BOT_TOKEN not set; skipping send")
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp.read()
        return True
    except Exception as e:
        print(f"Telegram send failed: {e}", file=sys.stderr)
        return False


def main():
    result = subprocess.run(
        [sys.executable, str(REPORT_SCRIPT), "--hours", "24", "--format", "text"],
        capture_output=True,
        text=True,
        cwd=str(REPO_DIR),
    )
    if result.returncode != 0:
        error_msg = f"Daily analytics report failed:\n{result.stderr or result.stdout}"
        print(error_msg, file=sys.stderr)
        send_telegram(f"⚠️ Daily analytics report failed\n```\n{result.stderr[:400]}\n```")
        sys.exit(1)

    report = result.stdout.strip()
    if not report:
        report = "No analytics events in the last 24 hours."

    header = "📊 *Shayne's AI Lab — Daily Analytics Report*"
    message = f"{header}\n\n```\n{report}\n```"

    # Telegram message limit is 4096 characters
    if len(message) > 4000:
        message = message[:3997] + "\n```"

    if send_telegram(message):
        print("Daily analytics report sent to Telegram")
    else:
        print(report)


if __name__ == "__main__":
    main()
