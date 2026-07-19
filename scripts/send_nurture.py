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
            'Want to build this yourself? This is exactly the kind of workflow '
            'Make.com handles well: https://www.make.com/en/register?pc=shaynesailab\n\n'
            'Questions? Just reply to this email.\n\n'
            '\u2014 Shayne\n'
            'Shayne\u2019s AI Lab\n'
            'https://shaynesailab.com\n'
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
            'Shayne\u2019s AI Lab\n'
            'https://shaynesailab.com\n'
        ),
    },
    {
        'step': 3,
        'day_delay': 14,
        'subject': 'Tool spotlight: Make.com for automation',
        'text': (
            'Hi {first_name},\n\n'
            'If you\u2019re still figuring out which automation tools to invest time in, '
            'here\u2019s one worth evaluating: Make.com.\n\n'
            'Why it stands out for ops teams:\n'
            '- Pricing is usage-based, not per-seat (much cheaper for teams)\n'
            '- Visual builder means you can see the logic flow\n'
            '- Integrates with 1,000+ apps without needing to code\n'
            '- Handles complex logic: conditions, routers, iterators, webhooks\n\n'
            'Common ops automations people build with it:\n'
            '  \u2022 Email triage and routing\n'
            '  \u2022 Lead capture from forms \u2192 CRM\n'
            '  \u2022 Slack notifications for specific triggers\n'
            '  \u2022 Weekly report generation\n'
            '  \u2022 Invoice follow-up reminders\n\n'
            'We\u2019ve compared it side-by-side with alternatives here:\n'
            'https://shaynesailab.com/blog/email-triage-tools\n\n'
            'If you want to try it:\n'
            'https://www.make.com/en/register?pc=shaynesailab\n\n'
            '(We may earn a commission if you sign up through that link. '
            'It\u2019s how we keep the site running.)\n\n'
            '\u2014 Shayne\n'
        ),
    },
    {
        'step': 4,
        'day_delay': 21,
        'subject': 'New: Email triage tools comparison',
        'text': (
            'Hi {first_name},\n\n'
            'We just published a detailed comparison of email triage tools '
            'for operations teams. Thought you might find it useful:\n\n'
            'https://shaynesailab.com/blog/email-triage-tools\n\n'
            'It covers:\n'
            '- Dedicated email clients (Superhuman, Missive, Spike)\n'
            '- Automation platforms (Make.com)\n'
            '- AI-powered assistants (SaneBox, Shortwave)\n'
            '- Pricing comparisons and which approach fits which team size\n\n'
            'No sponsored content, no hype \u2014 just what we found.\n\n'
            '\u2014 Shayne\n'
        ),
    },
    {
        'step': 5,
        'day_delay': 30,
        'subject': 'Still evaluating tools? Here\u2019s a recap',
        'text': (
            'Hi {first_name},\n\n'
            'It\u2019s been about a month since you grabbed the AI Starter Kit. '
            'Wanted to leave you with a quick recap of the key resources:\n\n'
            '1. Free AI Starter Kit \u2014 8 tools with cost breakdowns\n'
            '   https://shaynesailab.com/starter-kit\n\n'
            '2. Free Ops Diagnostic \u2014 6 questions, personalized report\n'
            '   https://shaynesailab.com/diagnostic\n\n'
            '3. Tool Comparisons \u2014 Honest head-to-heads\n'
            '   https://shaynesailab.com/blog\n\n'
            '4. Tools Reference \u2014 Curated list of ops tools\n'
            '   https://shaynesailab.com/resources\n\n'
            'No pressure. The resources are here whenever you need them.\n\n'
            'If you have questions about any of the tools, just reply to this email.\n\n'
            '\u2014 Shayne\n'
        ),
    },
    {
        'step': 6,
        'day_delay': 45,
        'subject': 'Quick question about your ops setup',
        'text': (
            'Hi {first_name},\n\n'
            'Quick question: what\u2019s the one ops task you wish would just run itself?\n\n'
            'Reply to this email if you feel like sharing \u2014 I read every response.\n\n'
            'In the meantime, the tools and resources are still here:\n'
            'https://shaynesailab.com\n\n'
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