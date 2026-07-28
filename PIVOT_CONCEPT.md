# Practical Ops — Full Pivot Concept v2
## Shayne's AI Lab re:Monetization
*2026-07-28 | Research-backed | Shayne-approved draft*

---

## The Model in One Sentence

**We sell ops automation that actually works.** Free downloads build trust. Paid blueprints and workshops generate automated income. Custom builds deliver the high-ticket revenue. Zero affiliate network approvals needed.

---

## What We Actually Own (Inventory)

### 8 Production-Ready Workflows

These are already built, tested, and documented in `/home/rock/workspace/shaynesailab-workflows/workflows/`:

| # | Workflow | What It Does | Sell As |
|---|----------|-------------|---------|
| 1 | **Email Triage + Routing** | Read inbox, classify (AI), route, reply, escalate humans | Blueprint ($19) + Workshop ($47) |
| 2 | **Lead Intake Auto-Respond** | Parse web forms, qualify via LLM, add to CRM, email sequences | Blueprint ($19) + Consulting ($2K) |
| 3 | **Support Summarization** | Summarize tickets, match KB, suggest articles, route/escalate | Consulting ($2K-5K) |
| 4 | **Social Content Scheduler** | Scrape RSS, score via LLM, draft posts, queue for review | Blueprint ($19) + Workshop ($47) |
| 5 | **Meeting Prep Assistant** | Generate pre-meeting briefs from calendar invites | Blueprint ($19) |
| 6 | **Invoice Follow-Up** | Track invoices, escalating email reminders | Blueprint ($19) + Workshop ($47) |
| 7 | **CRM Auto-Population** | Create/update CRM records from email signals | Consulting ($2K-5K) |
| 8 | **Newsletter Pipeline** | Curate RSS + products into weekly newsletter | Consulting ($2K-5K) |

### 3 Blueprints Already Ready

From the archive — actual importable Make.com JSON files:
- Lead Capture Pipeline (5-module flow)
- Email Triage System (3-module flow)
- Invoice Follow-Up (4-module flow)

These are sellable *today*. Just need a payment link and a delivery mechanism.

---

## Pricing Strategy (Research-Backed)

### Market Data
| Category | What Others Charge | Our Price | Reasoning |
|----------|-------------------|-----------|-----------|
| Single Make.com template (Etsy/Gumroad) | $5-15 | **$19** | Ours include setup guide + video + support — premium positioning |
| Bulk template bundle (50-250 templates) | $19-47 | **$39** | 3 tested, production-ready blueprints > 50 generic ones |
| Recorded workshop/masterclass | $47-97 | **$47** | Industry standard, low friction for first purchase |
| Full ops bundle (blueprints + workshop) | — | **$79** | Bundle value: bundle of 3 blueprints + workshop recording |
| AI automation consulting | $150-500/hr or $500-2K/workflow | **$2K/workflow** | Premium but justifiable — these are production, not prompts |
| Suite (3 workflows) | — | **$5K** | Saves client ~$1K vs buying separately |
| Monthly retainer | $2-5K/mo | **$2K/mo** | Competitive for ongoing ops automation |

### The $47 Sweet Spot
Per the research, **$47** is the standard price for "skill masterclass with a clear transformation." That's what our workshops are. At 25 sales/month = $1,175/month. At 100 sales/month = $4,700/month.

---

## Product Tiers

```
FREE (Value Builder)                PAID ($19-79)                        PREMIUM ($2K-5K)
┌─────────────────────┐            ┌──────────────────────┐             ┌─────────────────────┐
│ Blog articles        │           │ Blueprint: Email      │            │ Custom workflow      │
│ Free blueprint DL    │  ───>     │   Triage      $19     │   ───>     │   (single)    $2K   │
│ Mini email course    │           │ Blueprint: Lead       │            │ Ops suite           │
│ Free workshop replay │           │   Capture      $19    │            │   (3 flows)   $5K   │
│                      │           │ Blueprint: Invoice    │            │ Monthly retainer    │
│ Email list growth    │           │   Follow-Up    $19    │            │   $2K/mo            │
│                      │           │ Bundle (all 3) $39    │            │                     │
│                      │           │ Workshop: Email       │            │                     │
│                      │           │   Triage      $47    │            │                     │
│                      │           │ Full Bundle:          │            │                     │
│                      │           │   Blueprints +        │            │                     │
│                      │           │   Workshop    $79    │            │                     │
└─────────────────────┘            └──────────────────────┘             └─────────────────────┘
```

Each tier feeds the next. The free blueprint proves we're real. The paid blueprint solves their problem. The consulting handles what they can't DIY.

---

## Webinar/Workshop Strategy

**Format:** Pre-recorded, evergreen. Delivered via email after purchase (or gated behind email for free version). Hosted on YouTube unlisted or Vimeo. Low cost, high leverage.

**Free workshop (lead magnet):**
- "Automate Your Inbox in 30 Minutes" — record once, captures emails forever
- Uses the Email Triage Blueprint as the demo
- At the end: "Want the full blueprint with setup guide? Get it here ($19)"
- And: "Need this customized for your team? Book a call"

**Paid workshop ($47):**
- "Build Your Ops Stack: 3 Automations in 90 Minutes" — deeper dive
- Includes email triage, lead capture, invoice follow-up
- Comes with all 3 blueprints + step-by-step video
- Recorded, evergreen, delivered after purchase

**Webinar platform:** Loom (free tier for recording) + YouTube unlisted (hosting) + Gumroad (payment + delivery). Total cost: $0/month until we outgrow it.

---

## Delivery Infrastructure

**Recommendation: Gumroad for MVP (shipping this week)**

| Feature | Stripe-Only | Gumroad |
|---------|-------------|---------|
| Time to first sale | 4-6 hours build | 30 minutes setup |
| Hosted storefront | Build from scratch | Built-in |
| Payment processing | Need to build checkout | Built-in (Stripe behind scenes) |
| Digital delivery | Build custom flow | Auto-deliver on payment |
| Tax compliance | Handle manually | Auto-handled |
| Fee on $19 sale | $0.85 (2.9% + $0.30) | ~$2.85 (10% + $0.50 + Stripe) |
| Fee on $47 sale | $1.66 | ~$5.70 |
| Migration path | — | Can migrate to Stripe later |

**For speed-to-market, Gumroad wins.** The $3-6/sale premium is worth getting live this week instead of next month. When volume justifies it, we can move to self-hosted Stripe.

---

## What Changes on the Site (Minimal)

The site mostly stays the same. Changes:

1. **Homepage hero** — Replace current messaging with "Operations automation that actually works. Blueprints, workshops, and custom builds."
2. **New `/products/` page** — Gumroad embeds for 5 products (3 blueprints, bundle, workshop)
3. **Consulting page** — Revive from git commit 8cab746 (old design was solid)
4. **Blog CTAs** — Already have email capture. Add: "Try the free blueprint" and "Buy the full blueprint"
5. **Remove affiliate-heavy links** — Keep Make.com/Amazon/Jotform as passive sidebar items, not primary CTA

That's it. Everything else (lead capture, nurture sequence, tunnel, content pipeline) stays as-is.

---

## The Big Question: Brand Name

You own **shaynesailab.com** and **nexusautomationsolutions.com**.

**shaynesailab.com** pros:
- Personal, trustworthy
- Existing content, traffic, infrastructure
- "Lab" implies experimentation and building — fits the model

**nexusautomationsolutions.com** pros:
- No personal brand dependency
- Sounds like a real company (better for B2B consulting)
- "Nexus" = connection hub, fits automation

**My recommendation: Keep shaynesailab.com.** Here's why:
- We already have 18 posts indexed, traffic flowing, and infrastructure connected
- For B2B services (consulting), "Shayne's AI Lab" is actually **more** trustworthy than a generic corporate name — it's a real person
- The domain is already on the lead magnet, nurture emails, and blog
- Changing now means starting over on SEO and brand recognition
- **If** the product side (Gumroad) takes off, we can always spin it under a separate brand later

But if you hate the "personal brand" angle and want purely corporate B2B positioning for the consulting side, Nexus Automation Solutions could test better for that specific audience.

---

## Where We Need Your Input

1. **Gumroad account** — Need you to create one (or I walk you through it). Then I can set up products and delivery in ~30 min.
2. **Workshop recording** — Need you to record the first free workshop ("Automate Your Inbox"). I'll script it; you deliver it. 20-30 minutes, straight to the point, no fluff.
3. **First consulting client** — Anyone in mind? Or do we let the funnel generate one naturally?
4. **Product names** — Ops Starter Pack? Practical Ops Bundle? Something else?

---

## 60-Day Execution Timeline

| Week | Focus | Key Deliverable |
|------|-------|-----------------|
| 1 | Ship | Gumroad account → 5 product pages → free blueprint available for download |
| 2 | Record | Script + record free workshop → paid workshop → update site |
| 3 | Launch | Consulting page live → all 3 blueprints for sale → nurture sequence updated |
| 4 | Grow | 4 new blog posts (tutorials linking to products) → email campaign to existing list |
| 5-6 | Optimize | Review sales data → adjust pricing → improve conversion |
| 7-8 | Evaluate | Review against kill switch → decide scale or pivot |

---

## The Honest Numbers

This won't replace a full-time income in month one. But it's a **real business** — not a traffic-for-pennies affiliate hustle:

| Target | Monthly Revenue | Requires |
|--------|----------------|----------|
| Conservative (Month 2) | ~$1,000 | 15 bundle sales + 5 workshop sales + 1 consulting lead |
| Realistic (Month 4) | ~$2,500 | 25 bundle + 10 workshop + 1 consulting engagement (quarterly) |
| Aspirational (Month 6) | ~$5,000 | 50 bundle + 20 workshop + 1 retainer client |

At $5K/month we're making real money. At $2K/month we're covering costs and growing. The model is sustainable from day one because there are zero gatekeepers.

---

*File: PIVOT_CONCEPT.md in the ShaynesAiLab repo — easy to find and edit.*