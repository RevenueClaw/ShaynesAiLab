#!/usr/bin/env python3
"""monitor-shaynesailab.py — Health checks for Shayne's AI Lab funnel.
Alerts via Telegram if pages or API endpoints fail.

Checks every run:
- Key landing pages return 200
- Lead capture API endpoints return 200
- Cloudflare tunnel endpoints are reachable
- Product landing pages return 200
- Stripe payment links return 200

Intended for cron: */5 * * * *
"""
import os
import sys
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "8645083973")

STATE_FILE = Path("/tmp/shaynesailab_health_state.json")

PAGE_CHECKS = [
    ("GET", "https://shaynesailab.com/", 200, "homepage"),
    ("GET", "https://shaynesailab.com/products/", 200, "products"),
    ("GET", "https://shaynesailab.com/products/supportbot/", 200, "supportbot"),
    ("GET", "https://shaynesailab.com/products/contentcrew/", 200, "contentcrew"),
    ("GET", "https://shaynesailab.com/products/leadmagnet/", 200, "leadmagnet"),
    ("GET", "https://shaynesailab.com/products/bundle/", 200, "bundle"),
    ("GET", "https://shaynesailab.com/services/", 200, "services"),
    ("GET", "https://shaynesailab.com/diagnostic/", 200, "diagnostic"),
    ("GET", "https://shaynesailab.com/ai-starter-kit/", 200, "ai-starter-kit"),
    ("GET", "https://shaynesailab.com/blog/", 200, "blog"),
]

API_CHECKS = [
    ("GET", "https://api.shaynesailab.com/api/health", 200, "lead-api-health", None),
    ("POST", "https://api.shaynesailab.com/api/nurture-fire", 200, "nurture-fire-api", b""),
    ("POST", "https://api.shaynesailab.com/api/sequence-fire", 200, "sequence-fire-api", b""),
]

# Optional: deeper endpoint checks that submit real forms. Disabled by default to avoid polluting lead stores.
# API_FORM_CHECKS = [
#     ...
# ]

STRIPE_CHECKS = [
    ("GET", "https://buy.stripe.com/28E14o6A3fDq0TVbL71RC00", 200, "stripe-supportbot"),
    ("GET", "https://buy.stripe.com/28E8wQ8Ib62QdGH16tRC01", 200, "stripe-contentcrew"),
    ("GET", "https://buy.stripe.com/4gMcN66A34YMdGHg1n1RC02", 200, "stripe-leadmagnet"),
    ("GET", "https://buy.stripe.com/14A7sM8Ibaj6dGH16t1RC03", 200, "stripe-bundle"),
]


def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except json.JSONDecodeError:
            pass
    return {"alerts": {}, "last_ok": None, "runs": 0}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def send_telegram(message):
    if not TELEGRAM_BOT_TOKEN:
        print("TELEGRAM_BOT_TOKEN not set; skipping alert")
        return False
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = json.dumps({
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
        }).encode()
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(req, timeout=10)
        print("Telegram alert sent")
        return True
    except Exception as e:
        print(f"Telegram alert failed: {e}")
        return False


def check_url(method, url, expected_status, name, body=None):
    start_time = time.time()
    try:
        req = urllib.request.Request(url, data=body, method=method)
        req.add_header("User-Agent", "shaynesailab-health-monitor/1.0")
        if method == "POST" and body and body.startswith(b"{"):
            req.add_header("Content-Type", "application/json")
        elif method == "POST" and body:
            req.add_header("Content-Type", "application/x-www-form-urlencoded")
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.getcode()
            elapsed = int((time.time() - start_time) * 1000)
            ok = status == expected_status
            return name, ok, status, elapsed, None
    except Exception as e:
        elapsed = int((time.time() - start_time) * 1000)
        return name, False, None, elapsed, str(e)


def run_checks():
    results = []
    failures = []

    for method, url, expected, name in PAGE_CHECKS:
        name, ok, status, elapsed, err = check_url(method, url, expected, name)
        results.append({"name": name, "ok": ok, "status": status, "elapsed_ms": elapsed, "error": err})
        if not ok:
            failures.append((name, status, err))

    for method, url, expected, name, body in API_CHECKS:
        name, ok, status, elapsed, err = check_url(method, url, expected, name, body)
        results.append({"name": name, "ok": ok, "status": status, "elapsed_ms": elapsed, "error": err})
        if not ok:
            failures.append((name, status, err))

    for method, url, expected, name in STRIPE_CHECKS:
        name, ok, status, elapsed, err = check_url(method, url, expected, name)
        results.append({"name": name, "ok": ok, "status": status, "elapsed_ms": elapsed, "error": err})
        if not ok:
            failures.append((name, status, err))

    return results, failures


def main():
    state = load_state()
    state["runs"] += 1

    results, failures = run_checks()
    now = datetime.now(timezone.utc).isoformat()

    summary = {"time": now, "total": len(results), "failed": len(failures), "results": results}
    print(json.dumps(summary, indent=2))

    # Only alert if there are failures, and throttle repeated alerts for same failing checks
    if failures:
        failing_names = sorted(name for name, _, _ in failures)
        alert_key = ",".join(failing_names)
        last_alert = state["alerts"].get(alert_key)

        # Throttle: only alert once per hour for the same failure pattern
        should_alert = True
        if last_alert:
            last_time = datetime.fromisoformat(last_alert)
            if (datetime.now(timezone.utc) - last_time).total_seconds() < 3600:
                should_alert = False

        if should_alert:
            lines = [f"🚨 <b>shaynesailab.com Funnel Alert</b> ({now[:19].replace('T',' ')} UTC)"]
            for name, status, err in failures:
                detail = f"status={status}" if status else f"error={err[:120]}"
                lines.append(f"• <b>{name}</b>: {detail}")
            lines.append("\nCheck <code>/tmp/shaynesailab_health_state.json</code> for full results.")
            send_telegram("\n".join(lines))
            state["alerts"][alert_key] = now
        else:
            print("Alert throttled (same failure pattern within 1 hour)")
    else:
        state["last_ok"] = now
        # Clear old alerts on success
        state["alerts"] = {}

    save_state(state)

    # Exit with non-zero on failure so cron logs show it
    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
