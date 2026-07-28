# Email Triage Blueprint — Setup Guide

## What This Blueprint Does
Automatically reads your email inbox, classifies each email (urgent, important, newsletter, spam), and routes them to the right place. Urgent emails trigger instant notifications. Everything else lands in a daily digest.

## Quick Setup (10 minutes)

### Prerequisites
- A Make.com account (free tier works for up to 1,000 operations/month)
- A Gmail or Outlook email account
- (Optional) A Slack workspace for notifications

### Step 1: Import the Blueprint
1. Log into your Make.com account
2. Click "Create a new scenario"
3. Click the menu icon (three dots) in the scenario editor
4. Select "Import Blueprint"
5. Choose the `email-triage-blueprint.json` file

### Step 2: Configure Connections
The blueprint uses these modules. You'll need to connect each one:

1. **Scheduler** — Sets the check interval (default: every 15 minutes)
2. **Gmail / Outlook** — Connect your email account
3. **Router** — Classifies based on your rules (sender, subject, keywords)
4. **Slack / Email** — Set where notifications go

### Step 3: Customize the Rules
Open the Router module and set your classification rules:

- **Urgent**: Emails from specific senders or with keywords (e.g., "urgent", "ASAP", "deadline")
- **Important**: Emails from known contacts or with actionable subjects
- **Newsletter**: Bulk senders, marketing emails
- **Spam**: Known spam patterns

### Step 4: Test
Send yourself a test email and verify it appears in the right bucket within 15 minutes.

## Troubleshooting
- **No emails processed**: Check your email connection is authorized
- **Wrong classification**: Adjust the Router module's filter rules
- **Slack not sending**: Verify the Slack webhook URL is correct

## Support
Reply to your purchase email or contact hello@shaynesailab.com