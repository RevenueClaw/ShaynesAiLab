# LeadMagnet Setup Guide

## What You're Getting
LeadMagnet is an AI-powered lead qualification and follow-up automation system that scores, segments, and nurtures your leads automatically.

## What's Included
- **Qualifying Questions** — 7-question scoring flow + logic
- **Follow-Up Sequences** — 4-email nurture series
- **Conversation Scripts** — Chatbot flow with branching logic
- **CRM Templates** — HubSpot, Airtable, Notion imports

## Quick Setup (60 minutes)

### Step 1: Define Your ICP
Before configuring LeadMagnet, document:
- Who is your ideal customer? (Industry, role, company size)
- What's their budget range? (Set price_range variable)
- What problem do you solve for them?
- What signals show they're ready to buy?

### Step 2: Configure Scoring
Edit the qualifying questions:
1. Open `leadmagnet-template.json`
2. Adjust questions for your industry
3. Set score values per answer
4. Define your qualification thresholds (45+/70 = qualified)

### Step 3: Set Up Your Platform
**Option A: Chatbot (ChatGPT/Claude)**
- Create a Custom GPT with the conversation script
- Deploy on your landing page
- Capture leads automatically

**Option B: CRM Integration**
- Import the lead scoring fields
- Set up automated email sequences
- Configure lead routing rules

**Option C: Automation (Make.com / n8n)**
- Connect form → scoring → CRM → email
- Build the full pipeline

### Step 4: Test & Iterate
1. Submit 5 test leads through your form
2. Check their scores against your expectations
3. Adjust question weights if needed
4. Run the email sequence on a test email
5. Review and refine weekly