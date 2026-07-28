# Lead Capture Blueprint — Setup Guide

## What This Blueprint Does
Automatically captures leads from web forms, adds them to your CRM or spreadsheet, sends a Slack notification, and starts a follow-up email sequence.

## Quick Setup (15 minutes)

### Prerequisites
- A Make.com account
- A web form (Jotform, Typeform, Google Forms, or custom HTML form)
- A Google Sheet or CRM (HubSpot, Freshsales)
- A Slack workspace (optional)

### Step 1: Import the Blueprint
1. Log into Make.com
2. Create a new scenario
3. Menu → Import Blueprint
4. Upload `lead-capture-blueprint.json`

### Step 2: Configure the Webhook
1. Open the Webhook module
2. Copy the webhook URL
3. Add it as the form action URL in your form builder

### Step 3: Connect Your CRM
1. Open the Google Sheets or CRM module
2. Authorize Make.com to access your account
3. Map the form fields to the correct columns

### Step 4: Set Up Notifications
1. Open the Slack module
2. Connect your Slack workspace
3. Choose the channel for lead notifications

### Step 5: Test
Submit a test form entry and verify it appears in your CRM within 60 seconds.

## Troubleshooting
- **No leads captured**: Verify the webhook URL is correct in your form
- **Wrong data in CRM**: Check the field mappings in the Google Sheets module
- **Slack not sending**: Verify the Slack connection is authorized