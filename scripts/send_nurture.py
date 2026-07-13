#!/usr/bin/env python3
"""Shayne's AI Lab — Nurture Sequence Sender
Cron job that checks leads.json and sends the next nurture email to leads
who haven't received their next step yet.

Schedule: daily at 9:30 AM EDT
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path.home() / '.openclaw/workspace/skills/agentmail'))
from agentmail import AgentMail

DATA_FILE = Path(__file__).resolve().parent / 'leads.json'
FROM_INBOX = 'revenueclaw@agentmail.to'

NURTURE_EMAILS = [
    {
        'step': 1,
        'day_delay': 3,
        'subject': 'Real example: Email triage done well',
        'text': (
            'Hi {first_name},\n\n'
            'A few days ago you grabbed the AI Starter Kit \u2014 hope you found it useful.\n\n'
            'Here\u2019s a concrete example of how email triage automation works in practice:\n\n'
            'The setup:\n'
            '1. A cron job checks the inbox every 15 minutes\n'
            '2. Each email gets classified by AI: urgent, important, newsletter, spam\n'
            '3. Urgent ones trigger an instant notification\n'
            '4. Everything else lands in a daily digest for review\n\n'
            'The result: 40+ inbox checks a day becomes once-a-day review. '
            'That\u2019s 5-8 hours per week saved for most teams.\n\n'
            'Interested in the technical details? The workflows page has more information:\n'
            'https://shaynesailab.com/workflows\n\n'
            'Questions? Just reply to this email.\n\n'
            '\u2014 Shayne\n'
        ),
    },
    {
        'step': 2,
        'day_delay': 7,
        'subject': '8 tools worth knowing about',
        'text': (
            'Hi {first_name},\n\n'
            'Following up on the AI Starter Kit \u2014 here\u2019s a quick overview of 8 tools '
            'that have strong reputations in their categories:\n\n'
            '1. ChatGPT \u2014 Free tier. Drafting, brainstorming, getting past writer\u2019s block.\n'
            '2. Claude \u2014 Free. Long documents, contract review.\n'
            '3. Canva \u2014 Free. Graphics in minutes instead of hours.\n'
            '4. Perplexity \u2014 Free. Research with real sources you can verify.\n'
            '5. Notion \u2014 Free. Notes, docs, wikis, project management in one place.\n'
            '6. Fireflies.ai \u2014 Free tier. Meeting transcription and search.\n'
            '7. Calendly \u2014 Free. Kills the "when works?" email ping-pong.\n'
            '8. Cloudflare \u2014 Free tier. DNS, CDN, hosting.\n\n'
            'Full details with cost breakdowns and use cases:\n'
            'https://shaynesailab.com/resources\n\n'
            'Note: Every business is different. These are worth evaluating for your own needs, '
            'not endorsements. Do your own research and pick what fits your workflow.\n\n'
            '\u2014 Shayne\n'
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
        inbox=FROM_INBOX,
        to=[to_email],
        subject=subject,
        text=text,
    )


def get_api_key():
    api_key = os.environ.get('AGENTMAIL_API_KEY')
    if api_key:
        return api_key
    env_file = Path.home() / '.openclaw/workspace/.env'
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if line.startswith('AGENTMAIL_API_KEY='):
                    return line.strip().split('=', 1)[1].strip('\'"')
    return None


def main():
    api_key = get_api_key()
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
                greeting = f"Hi {first_name}," if first_name else "Hi there,"
                text_body = email_def['text'].format(first_name=first_name or 'there')

                print(f"Sending step {step} to {email} ({days_since_signup}d since signup)")
                try:
                    send_email(client, email, email_def['subject'], text_body)
                    lead['nurture_step'] = step
                    lead['nurture_sent_at'] = now.isoformat()
                    sent_count += 1
                    time.sleep(1)
                except Exception as e:
                    print(f"ERROR sending step {step} to {email}: {e}")

    if sent_count > 0:
        save_leads(leads)

    print(f"Nurture run complete. Sent: {sent_count}, Total leads: {len(leads)}")


if __name__ == '__main__':
    main()