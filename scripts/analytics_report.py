#!/usr/bin/env python3
"""
Simple analytics report for Shayne's AI Lab self-hosted tracking.

Reads workflows/state/analytics_events.jsonl and produces summaries
by event type, page, source, and daily/hourly buckets.

Usage:
    python3 scripts/analytics_report.py
    python3 scripts/analytics_report.py --hours 24 --format json
    python3 scripts/analytics_report.py --output /tmp/report.html
"""
import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path


DEFAULT_EVENTS_PATH = Path(__file__).resolve().parent.parent / ".." / "shaynesailab-workflows" / "workflows" / "state" / "analytics_events.jsonl"
DEFAULT_EVENTS_PATH = DEFAULT_EVENTS_PATH.resolve()


def parse_args():
    p = argparse.ArgumentParser(description="Generate analytics reports from event log")
    p.add_argument("--events", type=Path, default=DEFAULT_EVENTS_PATH, help="Path to analytics_events.jsonl")
    p.add_argument("--hours", type=int, default=168, help="Report window in hours (default: 7 days)")
    p.add_argument("--format", choices=["text", "json", "html"], default="text", help="Output format")
    p.add_argument("--output", type=Path, default=None, help="Write output to file instead of stdout")
    return p.parse_args()


def load_events(path, cutoff):
    events = []
    if not path.exists():
        return events
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                evt = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts_str = evt.get("ts", "")
            try:
                ts = datetime.fromisoformat(ts_str)
            except (ValueError, TypeError):
                continue
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            if ts >= cutoff:
                events.append(evt)
    return events


def summarize(events):
    total = len(events)
    by_event = Counter(e.get("event", "unknown") for e in events)
    by_page = Counter(e.get("page", "unknown") for e in events)
    by_source = Counter(e.get("source", "unknown") for e in events)
    by_target = Counter(e.get("target", "") for e in events if e.get("target"))

    # Daily buckets
    daily = defaultdict(int)
    hourly = defaultdict(int)
    for e in events:
        ts_str = e.get("ts", "")
        try:
            ts = datetime.fromisoformat(ts_str)
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            daily[ts.strftime("%Y-%m-%d")] += 1
            hourly[ts.strftime("%Y-%m-%d %H:00")] += 1
        except (ValueError, TypeError):
            continue

    # Conversion funnel approximation
    pageviews = by_event.get("pageview", 0)
    email_captures = by_event.get("email_capture", 0)
    cta_clicks = by_event.get("cta_click", 0)
    buy_clicks = by_event.get("buy_click", 0)
    capture_rate = round(email_captures / pageviews * 100, 2) if pageviews else 0.0
    cta_rate = round(cta_clicks / pageviews * 100, 2) if pageviews else 0.0
    buy_rate = round(buy_clicks / pageviews * 100, 2) if pageviews else 0.0

    return {
        "total": total,
        "window_hours": None,  # filled later
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "by_event": dict(by_event.most_common()),
        "by_page": dict(by_page.most_common(20)),
        "by_source": dict(by_source.most_common(20)),
        "by_target": dict(by_target.most_common(20)),
        "daily": dict(sorted(daily.items())),
        "hourly": dict(sorted(hourly.items())),
        "funnel": {
            "pageviews": pageviews,
            "email_captures": email_captures,
            "cta_clicks": cta_clicks,
            "buy_clicks": buy_clicks,
            "capture_rate_pct": capture_rate,
            "cta_rate_pct": cta_rate,
            "buy_rate_pct": buy_rate,
        },
    }


def format_text(report):
    lines = []
    lines.append("=" * 60)
    lines.append("Shayne's AI Lab — Analytics Report")
    lines.append(f"Generated: {report['generated_at']}")
    lines.append(f"Window: last {report['window_hours']} hours")
    lines.append(f"Total events: {report['total']}")
    lines.append("=" * 60)

    lines.append("\n--- Events by type ---")
    for k, v in report["by_event"].items():
        lines.append(f"  {k}: {v}")

    lines.append("\n--- Top pages ---")
    for k, v in report["by_page"].items():
        lines.append(f"  {k}: {v}")

    lines.append("\n--- Top sources ---")
    for k, v in report["by_source"].items():
        lines.append(f"  {k}: {v}")

    if report["by_target"]:
        lines.append("\n--- Top targets ---")
        for k, v in report["by_target"].items():
            lines.append(f"  {k}: {v}")

    lines.append("\n--- Funnel ---")
    f = report["funnel"]
    lines.append(f"  Pageviews:       {f['pageviews']}")
    lines.append(f"  Email captures:  {f['email_captures']} ({f['capture_rate_pct']}%)")
    lines.append(f"  CTA clicks:      {f['cta_clicks']} ({f['cta_rate_pct']}%)")
    lines.append(f"  Buy clicks:      {f['buy_clicks']} ({f['buy_rate_pct']}%)")

    lines.append("\n--- Daily ---")
    for k, v in report["daily"].items():
        lines.append(f"  {k}: {v}")

    return "\n".join(lines)


def format_html(report):
    title = "Shayne's AI Lab — Analytics Report"
    rows_event = "\n".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in report["by_event"].items())
    rows_page = "\n".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in report["by_page"].items())
    rows_source = "\n".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in report["by_source"].items())
    rows_daily = "\n".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in report["daily"].items())
    f = report["funnel"]

    def tbl(caption, rows):
        return f"""<h3>{caption}</h3>
<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;margin-bottom:1.5rem;">
<thead><tr><th>Item</th><th>Count</th></tr></thead>
<tbody>{rows}</tbody>
</table>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
body {{ font-family: Inter, system-ui, sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; color: #111; }}
h1 {{ font-size: 1.6rem; }}
h3 {{ font-size: 1.1rem; margin-top: 1.5rem; }}
table {{ width: 100%; max-width: 600px; }}
th {{ background: #f3f4f6; text-align: left; }}
.metric {{ display: inline-block; margin-right: 1.5rem; margin-bottom: 1rem; }}
.metric strong {{ display: block; font-size: 1.4rem; }}
</style>
</head>
<body>
<h1>{title}</h1>
<p>Generated: {report['generated_at']} | Window: last {report['window_hours']} hours | Total events: {report['total']}</p>

<div class="metrics">
<div class="metric"><strong>{f['pageviews']}</strong>Pageviews</div>
<div class="metric"><strong>{f['email_captures']}</strong>Email Captures ({f['capture_rate_pct']}%)</div>
<div class="metric"><strong>{f['cta_clicks']}</strong>CTA Clicks ({f['cta_rate_pct']}%)</div>
<div class="metric"><strong>{f['buy_clicks']}</strong>Buy Clicks ({f['buy_rate_pct']}%)</div>
</div>

{tbl('Events by type', rows_event)}
{tbl('Top pages', rows_page)}
{tbl('Top sources', rows_source)}
{tbl('Daily', rows_daily)}

</body>
</html>"""


def main():
    args = parse_args()
    cutoff = datetime.now(timezone.utc) - timedelta(hours=args.hours)
    events = load_events(args.events, cutoff)
    report = summarize(events)
    report["window_hours"] = args.hours

    if args.format == "json":
        output = json.dumps(report, indent=2)
    elif args.format == "html":
        output = format_html(report)
    else:
        output = format_text(report)

    if args.output:
        args.output.write_text(output, encoding="utf-8")
        print(f"Report written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
