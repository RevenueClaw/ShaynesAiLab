# Invoice Follow-Up Blueprint — Setup Guide

## What This Blueprint Does
Tracks outstanding invoices from a spreadsheet or accounting tool, sends escalating reminder emails based on how overdue each invoice is, and stops the sequence when payment is received.

## Quick Setup (10 minutes)

### Prerequisites
- A Make.com account
- A Google Sheet with your invoice data (or QuickBooks/Xero connection)
- A Gmail/Outlook account for sending reminders

### Step 1: Import the Blueprint
1. Log into Make.com
2. Create a new scenario
3. Menu → Import Blueprint
4. Upload `invoice-followup-blueprint.json`

### Step 2: Connect Your Invoice Data
1. Open the Google Sheets module
2. Connect your sheet (columns needed: Invoice ID, Client Email, Amount, Due Date, Status)
3. The blueprint checks daily for invoices past due

### Step 3: Set Up the Reminder Sequence
The blueprint has 3 escalation steps:
- **Step 1** (7 days overdue): Friendly reminder email
- **Step 2** (14 days overdue): More direct follow-up
- **Step 3** (21+ days overdue): Final notice + Slack escalation to your team

### Step 4: Customize Email Templates
Open each Email module and edit the subject line and body to match your brand's tone.

### Step 5: Test
Add a test invoice past due and verify the sequence starts within 24 hours.

## Troubleshooting
- **No reminders sent**: Check the date comparison in the Router module
- **Wrong escalation**: Adjust the day thresholds in each filter
- **Emails not sending**: Verify your email connection is authorized