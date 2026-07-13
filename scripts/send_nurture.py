#!/usr/bin/env python3
"""Shayne's AI Lab — Nurture Sequence Sender
Cron job that checks leads.json and sends the next nurture email to leads
who haven't received their next step yet.

Schedule: daily at 9:00 AM EDT
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# AgentMail SDK
sys.path.insert(0, str(Path.home() / '.openclaw/workspace/skills/agentmail'))
from agentmail import AgentMail

DATA_DIR = Path(__file__).resolve().parent / '..'
DATA_FILE = DATA_DIR / 'scripts' / 'leads.json'
STATE_FILE = DATA_DIR / 'scripts' / 'nurture_state.json'

AGENTMAIL_API_KEY = os.environ.get('AGENTMAIL_API_KEY', '')
FROM_INBOX = 'revenueclaw@agentmail.to'

NURTURE_EMAILS = [
    # Step 0: Already sent the starter kit (handled by Cloudflare function)
    # Step 1: Day 3 — Case study
    {
        'step': 1,
        'day_delay': 3,
        'subject': 'How I went from 40 inbox checks/day to 1',
        'text': """Hi {first_name},

A few days ago you grabbed the AI Starter Kit — hope it's been useful.

I wanted to share something concrete: here's exactly how my Email Triage workflow works.

The setup is simple:
1. A cron job checks my inbox every 15 minutes
2. Each email gets classified by AI: urgent, important, newsletter, spam
3. Urgent ones hit my Telegram immediately
4. Everything else lands in a daily digest I review once

The result: I used to check email 40+ times a day. Now I check it once. That's 5-8 hours back per week.

If you'd like to see the exact code/config I use, I wrote it up here:
https://shaynesailab.com/workflows

Questions? Just reply to this email.

— Shayne
""",
        'html': None,
    },
    # Step 2: Day 7 — Resources page + free tools
    {
        'step': 2,
        'day_delay': 7,
        'subject': 'The 8 tools I actually use (no fluff)',
        'text': """Hi {first_name},

You asked for tools that work, so here's my honest list:

1. **ChatGPT** — Free tier. Drafting, brainstorming, getting past writer's block.
2. **Claude** — Free. Long documents, contract review.
3. **Canva** — Free. Graphics in 5 minutes (used to take me an hour).
4. **Perplexity** — Free. Research with real sources you can verify.
5. **Notion** — Free. Where my entire business lives.
6. **Fireflies.ai** — Free tier. Never take meeting notes again.
7. **Calendly** — Free. Kills the "when works?" email ping-pong.
8. **Cloudflare** — Free tier. Hosts all my sites.

Full details with cost breakdowns and use cases:
https://shaynesailab.com/resources

The honest truth: I run custom automations that took months to build. But these 8 tools? They just work. Start here.

— Shayne
""",
        'html': None,
    },
]


def load_leads():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE) as f:
        return json.load(f)


def save_leads(leads):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(leads, f, indent=2)


def send_email(client, to_email, subject, text, html=None):
    """Send via AgentMail SDK."""
    payload = {
        'to': [to_email],
        'subject': subject,
        'text': text,
    }
    if html:
        payload['html'] = html
    
    return client.inboxes.messages.send(
        inbox=FROM_INBOX,
        **payload,
    )


def main():
    api_key = os.environ.get('AGENTMAIL_API_KEY') or AGENTMAIL_API_KEY
    if not api_key:
        # Try reading from env file
        env_file = Path.home() / '.openclaw/workspace/.env'
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.startswith('AGENTMAIL_API_KEY='):
                        api_key = line.strip().split('=', 1)[1]
                        break
    
    if not api_key:
        print("ERROR: AGENTMAIL_API_KEY not set")
        sys.exit(1)
    
    os.environ['AGENTMAIL_API_KEY'] = api_key
    client = AgentMail(api_key=api_key)
    
    leads = load_leads()
    now = datetime.now(timezone.utc)
    sent_count = 0
    
    for lead in leads:
        email = lead.get('email', '')
        first_name = lead.get('first_name', '') or ''
        signup_date_str = lead.get('signup_date', '')
        nurture_step = lead.get('nurture_step', 0)
        nurture_sent_at = lead.get('nurture_sent_at')
        
        if not email:
            continue
        
        try:
            signup_date = datetime.fromisoformat(signup_date_str)
        except (ValueError, TypeError):
            signup_date = now
        
        days_since_signup = (now - signup_date).days
        
        for email_def in NURTURE_EMAILS:
            step = email_def['step']
            day_delay = email_def['day_delay']
            
            if nurture_step < step and days_since_signup >= day_delay:
                print(f"Sending step {step} to {email} ({days_since_signup}d since signup)")
                
                try:
                    greeting = f"Hi {first_name}," if first_name else "Hi there,"
                    text_body = email_def['text'].format(first_name=first_name or 'there')
                    
                    send_email(client, email, email_def['subject'], text_body)
                    
                    lead['nurture_step'] = step
                    lead['nurture_sent_at'] = now.isoformat()
                    sent_count += 1
                    
                    # Rate limit between sends
                    time.sleep(1)
                except Exception as e:
                    print(f"ERROR sending step {step} to {email}: {e}")
    
    if sent_count > 0:
        save_leads(leads)
    
    print(f"Nurture run complete. Sent: {sent_count}, Total leads: {len(leads)}")


if __name__ == '__main__':
    main()
