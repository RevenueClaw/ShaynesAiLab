#!/usr/bin/env python3
"""
ShayneSAI Lab — Weekly Performance Report
Sends a summary of traffic, leads, nurture, and costs to Telegram + email.

Run: python3 scripts/weekly_report.py
Schedule: Sunday 10:00 AM EDT
"""

import json
import os
import sys
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path.home() / '.openclaw/workspace/skills/agentmail'))
from agentmail import AgentMail

DATA_FILE = Path(__file__).resolve().parent / 'leads.json'
NURTURE_LOG = Path(__file__).resolve().parent / 'logs' / 'nurture.log'

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = '8645083973'

def get_leads_summary():
    if not DATA_FILE.exists():
        return "0 leads"
    with open(DATA_FILE) as f:
        leads = json.load(f)
    
    total = len(leads)
    new_this_week = 0
    nurtured = 0
    now = datetime.now(timezone.utc)
    week_ago = now - timedelta(days=7)
    
    for l in leads:
        signup = l.get('signup_date', '')
        step = l.get('nurture_step', 0)
        if signup:
            try:
                sd = datetime.fromisoformat(signup)
                if sd > week_ago:
                    new_this_week += 1
            except:
                pass
        if step > 0:
            nurtured += 1
    
    return f"{total} total, {new_this_week} new this week, {nurtured} nurtured"

def get_nurture_summary():
    if not NURTURE_LOG.exists():
        return "No nurture log"
    with open(NURTURE_LOG) as f:
        lines = f.readlines()
    sent_count = sum(1 for l in lines if 'Sending step' in l)
    errors = sum(1 for l in lines if 'ERROR' in l)
    last_run = ''
    for l in reversed(lines):
        if 'complete' in l:
            last_run = l.strip()
            break
    return f"{sent_count} emails sent, {errors} errors. Last: {last_run[:80]}"

def send_telegram(msg):
    if not TELEGRAM_BOT_TOKEN:
        return
    try:
        url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
        data = json.dumps({
            'chat_id': TELEGRAM_CHAT_ID,
            'text': f' ShynSi Lab Weekly Report\n\n{msg}',
            'parse_mode': 'HTML',
        }).encode()
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=10)
        print("Telegram alert sent")
    except Exception as e:
        print(f"Telegram send failed: {e}")

def send_email_report():
    api_key = os.environ.get('AGENTMAIL_API_KEY')
    if not api_key:
        print("No AGENTMAIL_API_KEY, skipping email")
        return
    try:
        client = AgentMail(api_key=api_key)
        leads_summary = get_leads_summary()
        report = (
            f"ShyneSAI Lab - Weekly Report\n"
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            f"Leads: {leads_summary}\n"
            f"Nurture: {get_nurture_summary()}\n\n"
            f"Kill switch check:\n"
            f"- Traffic: Check Cloudflare Analytics\n"
            f"- Leads: Check leads.json\n"
            f"- Affiliate clicks: Check Make.com dashboard\n"
            f"- Cost: Check OpenRouter usage\n"
        )
        client.inboxes.messages.send(
            inbox_id='revenueclaw@agentmail.to',
            to='revenueclaw@gmail.com',
            subject=f'ShyneSAI Lab Weekly Report - {datetime.now().strftime("%b %d, %Y")}',
            text=report,
        )
        print("Email report sent")
    except Exception as e:
        print(f"Email failed: {e}")

def main():
    leads = get_leads_summary()
    nurture = get_nurture_summary()
    
    msg = (
        f"Leads: {leads}\n"
        f"Nurture: {nurture}\n\n"
        f"Check Cloudflare Analytics for traffic numbers."
    )
    
    send_telegram(msg)
    send_email_report()
    print("Report complete")

if __name__ == '__main__':
    main()
