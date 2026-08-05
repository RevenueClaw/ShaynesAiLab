# SupportBot Setup Guide

## What You're Getting
SupportBot is a ready-to-use AI customer support agent template. It includes system prompts, response templates, and escalation workflows that work with ChatGPT, Claude, or any major AI platform.

## What's Included
- **System Prompt** — Defines the agent's role, tone, and boundaries
- **Response Templates** — Greetings, escalations, follow-ups
- **Workflows** — Refund handling, technical support, general inquiries
- **Integration Guide** — How to set up on ChatGPT, Claude, or your platform

## Quick Setup (30 minutes)

### Step 1: Gather Your Knowledge Base
Before setting up SupportBot, collect:
- FAQ documents
- Product manuals or specs
- Common customer issues and solutions
- Your company policies (refunds, returns, shipping)
- Brand voice guidelines

### Step 2: Choose Your Platform

**Option A: ChatGPT Custom GPT (easiest)**
1. Open ChatGPT → Explore → Create a GPT
2. Paste the system prompt into "Instructions"
3. Upload your knowledge base files in "Knowledge"
4. Add response templates as conversation starters
5. Save and share the link

**Option B: Claude Project**
1. Create a new Project in Claude
2. Add the system prompt as Project Instructions
3. Upload templates and knowledge base files
4. Configure custom instructions

**Option C: Custom Integration**
Use OpenClaw or your own agent framework
- Configure the agent with the system prompt
- Set up escalation triggers
- Integrate with your support ticketing system

### Step 3: Configure Variables
Edit these in the system prompt:
- `company_name` — Your business name
- `refund_threshold` — Maximum automatic refund amount
- `response_timeframe` — Expected response time for escalations

### Step 4: Test & Launch
1. Test with 5 real customer scenarios
2. Review tone and accuracy
3. Adjust escalation rules as needed
4. Deploy to your support channel
5. Monitor first week and iterate

## Files Included
- `supportbot-template.json` — Complete prompt templates
- `SupportBot_System_Prompt.txt` — Ready to paste
- `SupportBot_Templates.json` — Response templates
- `Knowledge_Base_Guide.md` — How to organize your KB
- Quick Reference Card (PDF)