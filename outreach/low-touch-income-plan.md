# Low-Touch Income Plan — Shayne's AI Lab
*Built: 2026-10-15 | Goal: Replace lost Mercor income with a low-touch revenue layer while outreach converts retainer clients*

## The Numbers

Lost Mercor income: **~$2,000–3,200/week ≈ $8,000–13,000/month**.

This plan builds a **low-touch layer** designed to generate **$500–1,500/month within 90 days**, independent of retainer sales:

| Layer | 30-Day Target | 90-Day Target |
|-------|--------------|---------------|
| AgentKit digital products | $200–400 | $500–1,000 |
| Affiliate background streams | $100–200 | $150–300 |
| Strategy sessions from nurture | $250–500 | $500–1,000 |
| **Total low-touch** | **$550–1,100** | **$1,150–2,300** |

Retainer outreach runs in parallel. One Growth ($1,500/mo) or Enterprise ($3,500/mo) client per month replaces the bulk of the Mercor gap.

---

## 1. AgentKit Digital Products ($47–$247 Tier)

**Current state:** 12 products live, **$0 sales**.

Root causes and fixes:

### 1.1 Pricing Fix
- Most products are priced too low ($7–$47) or bundled awkwardly.
- New price anchors:
  - **Lead magnet:** free — `AI Starter Kit`
  - **Entry toolkit:** $47 — single workflow template (Notion/Sheets + prompt pack)
  - **System kit:** $97 — multi-step workflow with setup video
  - **Done-with-you blueprint:** $197–247 — template + 30-min setup call
- Bundles: create a `$247 Agency Operations Bundle` with the top 4 templates.

### 1.2 Landing Page Fix
- Every product needs its own focused landing page, not just the products grid.
- Required elements on each page:
  - Specific outcome headline ("Get 10+ hours back per week")
  - Who it's for (niche + pain)
  - What's inside (3–5 bullets)
  - Price + guarantee
  - Stripe buy button (tested, live keys verified)
  - Email capture fallback for non-buyers
- Start with the **highest-leverage products**:
  1. Email Triage Workflow
  2. Lead Qualification Agent
  3. Invoice Follow-Up System
  4. Support Summarization Agent

### 1.3 Email Capture Fix
- Add a lead-magnet gate before the sale on every product page:
  - "Enter your email to get the first chapter free"
  - Drops into the same AgentMail nurture sequence as the main lead magnet
- Exit-intent popup on `/products` with the free AI Starter Kit.

### 1.4 One Launch Promo
- Run a 7-day "Agency Ops Automation Week" launch:
  - Day 1: announce on LinkedIn + email list
  - Day 2–4: one product deep-dive per day
  - Day 5: case study / result from your own swarm
  - Day 6: bundle deal ($247 → $197)
  - Day 7: final call, price goes back up
- Promotion delivered via AgentMail broadcast to nurture list.
- Target: first 3–5 product sales + 50+ new email subscribers.

---

## 2. Lead Magnet Nurture (Workflow 9)

**Current state:** 3-email AgentMail sequence, cron every 6 hours, live at `api.shaynesailab.com`.

Sequence:
1. **Email 1 (immediate):** deliver AI Starter Kit + quick win
2. **Email 2 (+2 days):** diagnose the inbox/time leak
3. **Email 3 (+5 days):** offer the Ops Diagnostic call or entry product

Improvements to make:
- Add explicit product pitch in Email 3 (link to `$47 Email Triage Toolkit`)
- Split test subject lines using AgentMail tags
- Add post-sequence tag for non-buyers → weekly newsletter
- Track `lead_source` per submission to know which pages convert

Verification rhythm:
- After each test lead, confirm: form → API → email queued → nurture fires.
- Check automation run history for failures and fix within 24 hours.

---

## 3. Affiliate Background Streams

These run in the background and provide low-volatility base income.

### 3.1 worthitgoods.com
- Affiliate deal site with real traffic (78–285 pageviews/day).
- Current state: comparison articles publish on scheduled cadence.
- Optimization levers:
  - Add 1 new comparison per week
  - Update top 10 articles with current prices every 30 days
  - Add a "Shayne's AI Lab" cross-link in footer / resources page
- 90-day target: **$50–150/month** from Amazon PAAPI commissions.

### 3.2 chipradar.io
- Premium subscription site + affiliate board listings.
- Current state: 1 active $8/mo subscriber, real human traffic ~30–50 visits/day.
- Optimization levers:
  - Push SEO content pipeline (already running nightly)
  - Add premium-gated vendor pricing comparison tables
  - Test a $47 one-time "Deal Alert Bundle" via Stripe
- 90-day target: **$100–150/month** from subs + affiliate clicks.

Combined background target: **$150–300/month within 90 days**.

---

## 4. Content / SEO Cadence

Organic traffic is the cheapest long-term acquisition channel.

### Weekly Rhythm
- **1 long-form article** on shaynesailab.com blog: ops automation case study or how-to
- **1 LinkedIn post** showing a real behind-the-scenes workflow result
- **1 WorthItGoods comparison** (automated via existing pipeline)
- **1 ChipRadar SEO article** (automated via existing pipeline)

### Distribution
- Every new article → LinkedIn + email broadcast
- Every product page → link from 2–3 relevant blog posts
- Lead magnet embedded in top 50% of articles

---

## 5. 90-Day Action Roadmap

| Week | Focus | Key Deliverable |
|------|-------|-----------------|
| 1–2 | Product page fixes + lead capture | 4 product landing pages live, email gates added |
| 2–3 | Outreach starts | 25 agency prospects in CSV, 10 DMs/day |
| 3–4 | Launch promo | Agency Ops Automation Week campaign |
| 5–8 | Optimize conversions | A/B subject lines, pricing tests, bundle experiments |
| 9–12 | Scale what works | Retarget nurture non-buyers, double down on winning channel |

---

## 6. Success Metrics

Track weekly:
- **Leads captured** (form submissions)
- **Nurture sequence completions**
- **Product page → checkout conversion**
- **Outreach replies and booked calls**
- **Retainer proposals sent and closed**
- **Affiliate revenue** (WorthItGoods + ChipRadar)

Primary goal: **low-touch layer hits $500–1,500/mo by January 15, 2027**, with retainer outreach closing the rest of the Mercor gap.
