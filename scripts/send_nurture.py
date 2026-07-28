#!/usr/bin/env python3
"""Shayne's AI Lab — Nurture Sequence Sender
Cron job that checks leads.json and sends the next nurture email to leads
who haven't received their next step yet.

Schedule: daily at 9:30 AM EDT

Extended sequence: 6 emails over 30 days
- Step 1 (day 3):  Email triage example
- Step 2 (day 7):  Tool overview
- Step 3 (day 14): Tool spotlight — Make.com (affiliate)
- Step 4 (day 21): Blog article push
- Step 5 (day 30): Re-engagement
- Step 6 (day 45): Final check-in
"""

import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path.home() / '.openclaw/workspace/skills/agentmail'))
from agentmail import AgentMail

DATA_FILE = Path(__file__).resolve().parent / 'leads.json'
FROM_INBOX = 'revenueclaw@agentmail.to'

# Telegram alerting
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = '8645083973'

NURTURE_EMAILS = [
    # Step 1 Quick win - day 2
    {
        'step': 1,
        'day_delay': 2,
        'subject': 'One ops problem you can fix in 30 minutes',
        'text': (
            'Hi {first_name},\n\n'
            'The hardest part of ops automation isnt the tools '
            'it is knowing where to start.\n\n'
            'Here is a 30-minute quick win you can set up right now:\n\n'
            'Automate: Form submission to Slack notification\n\n'
            'Free tools: Make.com, Jotform, Slack\n\n'
            'Walkthrough: https://www.make.com/en/register?pc=shaynesailab\n\n'
            'The point isnt this specific flow. '
            'It is proving to yourself that automation takes 30 min.\n\n'
            'Once you have one win, the rest gets easier.\n\n'
            '- Shayne\n'
            'https://shaynesailab.com\n'
        ),
    },
    # Step 2 Email triage case study - day 5
    {
        'step': 2,
        'day_delay': 5,
        'subject': 'Real example: Email triage done well',
        'text': (
            'Hi {first_name},\n\n'
            'Here is a concrete example of how email triage automation works:\n\n'
            'The setup:\n'
            '1. Cron checks inbox every 15 minutes\n'
            '2. AI classifies each email (urgent, important, newsletter, spam)\n'
            '3. Urgent ones trigger Slack notification\n'
            '4. Everything else lands in a daily digest\n\n'
            'Result: 40+ inbox checks/day becomes once-a-day review. '
            'That is 5-8 hours/week saved.\n\n'
            'Build it with Make.com: https://www.make.com/en/register?pc=shaynesailab\n\n'
            'Full comparison: https://shaynesailab.com/blog/email-triage-tools\n\n'
            '- Shayne\n'
        ),
    },
    # Step 3 Make.com affiliate spotlight - day 9 (was day 14)
    {
        'step': 3,
        'day_delay': 9,
        'subject': 'Your first 3 Make.com automations',
        'text': (
            'Hi {first_name},\n\n'
            'Here are 3 automations that take under 30 minutes each '
            'on Make.com (we may earn a commission if you sign up through our link):\n\n'
            '1. Lead capture -> Google Sheets -> Slack\n'
            '2. Weekly report generator (auto-generated, emailed to team)\n'
            '3. Invoice follow-up sequence (wait -> remind -> escalate)\n\n'
            'Start building: https://www.make.com/en/register?pc=shaynesailab\n\n'
            'Free plan covers 1,000 operations/month.\n\n'
            '- Shayne\n'
        ),
    },
    # Step 4 Workflow blueprint - day 15 (new)
    {
        'step': 4,
        'day_delay': 15,
        'subject': 'Workflow blueprint: Lead -> CRM -> Follow-up',
        'text': (
            'Hi {first_name},\n\n'
            'Most ops teams lose leads between form submission and first follow-up.\n\n'
            'The fix (fully automated):\n'
            '1. Lead submits form -> Make.com webhook\n'
            '2. Lead enters CRM (HubSpot, Freshsales, or Sheets)\n'
            '3. Slack notification sent\n'
            '4. Follow-up sequence starts (1h, 24h, 72h)\n\n'
            'Guide: https://shaynesailab.com/blog/lead-capture-jotform-make\n'
            'CRM comparison: https://shaynesailab.com/blog/hubspot-vs-freshsales\n\n'
            '- Shayne\n'
        ),
    },
    # Step 5 Case study / social proof - day 22 (new)
    {
        'step': 5,
        'day_delay': 22,
        'subject': 'How a 5-person team saved 20 hours/week on ops',
        'text': (
            'Hi {first_name},\n\n'
            'A small ops team of 5 automated 4 workflows with Make.com:\n'
            '1. Inbox triage -> AI routing\n'
            '2. Forms -> instant CRM + Slack\n'
            '3. Reports -> auto-generated weekly\n'
            '4. Invoice reminders -> automated sequence\n\n'
            'Result: 20+ hours/week saved. Lead response: 4 hours -> 42 seconds.\n'
            'Late payments dropped 60%.\n\n'
            'Start here: https://www.make.com/en/register?pc=shaynesailab\n'
            'Platform comparison: https://shaynesailab.com/blog/automation-platforms\n\n'
            '- Shayne\n'
        ),
    },
    # Step 6 Final resource + CTA - day 30
    {
        'step': 6,
        'day_delay': 30,
        'subject': 'One last thing: the free ops diagnostic',
        'text': (
            'Hi {first_name},\n\n'
            'This is the last email in this sequence.\n\n'
            'Take the Ops Diagnostic (6 questions, personalized report):\n'
            'https://shaynesailab.com/diagnostic\n\n'
            'Key resources:\n'
            '- Starter Kit: https://shaynesailab.com/starter-kit\n'
            '- Blog: https://shaynesailab.com/blog\n'
            '- Diagnostic: https://shaynesailab.com/diagnostic\n\n'
            'Start with Make.com (free tier): https://www.make.com/en/register?pc=shaynesailab\n\n'
            '- Shayne\n'
        ),
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


def send_email(client, to_email, subject, text):
    return client.inboxes.messages.send(
        inbox_id=FROM_INBOX,
        to=to_email,
        subject=subject,
        text=text,
    )


def send_telegram_alert(message):
    """Send error alert to Telegram when nurture fails."""
    if not TELEGRAM_BOT_TOKEN:
        return
    try:
        url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
        data = json.dumps({
            'chat_id': TELEGRAM_CHAT_ID,
            'text': f'⚠️ Nurture Error: {message}',
            'parse_mode': 'HTML',
        }).encode()
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        pass  # Don't crash if Telegram alert fails


def get_api_key():
    api_key = os.environ.get('AGENTMAIL_API_KEY')
    if api_key:
        return api_key
    # Check workspace .env
    env_file = Path.home() / '.openclaw/workspace/.env'
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if line.startswith('AGENTMAIL_API_KEY='):
                    return line.strip().split('=', 1)[1].strip('\'"')
    # Check credentials directory
    cred_file = Path.home() / '.openclaw/credentials/agentmail.env'
    if cred_file.exists():
        with open(cred_file) as f:
            for line in f:
                if line.startswith('AGENTMAIL_API_KEY=') or line.startswith('export AGENTMAIL_API_KEY='):
                    return line.strip().split('=', 1)[1].replace('export ', '').strip('\'"')
    return None


def main():
    api_key = get_api_key()
    if not api_key:
        msg = "AGENTMAIL_API_KEY not set"
        print(f"ERROR: {msg}")
        send_telegram_alert(msg)
        sys.exit(1)

    os.environ['AGENTMAIL_API_KEY'] = api_key
    client = AgentMail(api_key=api_key)

    leads = load_leads()
    now = datetime.now(timezone.utc)
    sent_count = 0
    errors = []

    for lead in leads:
        email = lead.get('email', '')
        first_name = lead.get('first_name', '') or ''
        signup_date_str = lead.get('signup_date', '')
        nurture_step = lead.get('nurture_step', 0)

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
                text_body = email_def['text'].format(first_name=first_name or 'there')

                print(f"Sending step {step} to {email} ({days_since_signup}d since signup)")
                try:
                    send_email(client, email, email_def['subject'], text_body)
                    lead['nurture_step'] = step
                    lead['nurture_sent_at'] = now.isoformat()
                    sent_count += 1
                    time.sleep(1)
                except Exception as e:
                    err = f"Step {step} to {email}: {e}"
                    print(f"ERROR: {err}")
                    errors.append(err)

    if sent_count > 0:
        save_leads(leads)

    # Alert on errors
    if errors:
        send_telegram_alert(f"{len(errors)} errors in nurture run\n{errors[0][:200]}")

    print(f"Nurture run complete. Sent: {sent_count}, Total leads: {len(leads)}, Errors: {len(errors)}")


if __name__ == '__main__':
    main()