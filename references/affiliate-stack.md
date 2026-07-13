# ShayneAiLab Affiliate Stack — Complete Reference

**Generated:** 2026-07-13
**Site:** shaynesailab.com → operations leaders, teams of 1-50 people

## Quick Links

| Program | Signup URL | Commission | Fit |
|---------|-----------|------------|-----|
| Notion | notion.partnerstack.com | $50 + 20% yr-1 rev | Docs, wikis, project mgmt |
| Make.com | make.com/en/affiliate | ~30% recurring 12mo | No-code automation |
| HubSpot | hubspot.com/partners | 30% recurring 12mo | CRM + marketing ops |
| Canva | canva.com/en_gb/help/canva-affiliate-marketing-program/ | ~30% recurring | Design for non-designers |
| ClickUp | clickup.com/partners | 30% recurring 12mo | All-in-one PM |
| Cal.com | cal.com/affiliate-program | 20% recurring 12mo | Open source scheduling |
| Jotform | jotform.com/partnership/affiliate/ | 30% recurring | Forms + automation |
| Miro | miro.com/affiliates/join-our-program/ | $10-83 CPL | Whiteboarding |
| Reclaim.ai | reclaim.ai/affiliate-program | 40% recurring 12mo | Smart calendar AI |
| MailerLite | mailerlite.com/affiliate | 30% lifetime rec. | Email marketing |
| Kit (ConvertKit) | kit.com/affiliates (search) | 30-50% rec. 12mo | Email for creators |
| Typeform | typeform.com/partners | 15-20% rec. + $20 | Surveys + forms |
| Loom | loom.com/creators | 15-20% rec. 1yr | Video messaging |
| Amazon | Already set up ✅ | Variable | Books, hardware |

## TIER 1: Must Join (Your Time First)

These are the highest-leverage programs for our ops audience.

### 1. Notion (PartnerStack)
- **Commission:** $50 per activated signup + 20% of year-one revenue
- **Cookie:** Last-click, 180 days
- **Why:** Every ops team uses Notion. Our articles naturally compare Notion vs. alternatives.
- **Signup:** https://notion.partnerstack.com
- **Status:** ⏳ TODO

### 2. Make.com
- **Commission:** ~30% recurring for 12 months
- **Cookie:** 90 days
- **Why:** "Anyone can become an affiliate." Automation is the core ops conversation.
- **Signup:** https://www.make.com/en/affiliate
- **Status:** ⏳ TODO — may be instant approval

### 3. HubSpot (Impact)
- **Commission:** 30% recurring for 12 months on ALL products
- **Cookie:** 180 days
- **Why:** CRM + marketing + sales ops. High price point = high absolute commission.
- **Signup:** https://www.hubspot.com/partners
- **Status:** ⏳ TODO

## TIER 2: Strong Adds (When You Have 10 More Minutes)

### 4. Jotform
- **Commission:** 30% recurring
- **Why:** Forms are universal in ops. Easy approval. "Apply in minutes."
- **Signup:** https://www.jotform.com/partnership/affiliate/
- **Status:** ⏳ TODO

### 5. ClickUp
- **Commission:** 30% recurring 12 months
- **Cookie:** 90 days
- **Why:** Direct Notion competitor — comparison articles perform great.
- **Signup:** https://clickup.com/partners (search for affiliate program)
- **Status:** ⏳ TODO

### 6. Cal.com
- **Commission:** 20% recurring 12 months (bonus: referrals get 20% off too)
- **Why:** Calendly has NO affiliate program. Cal.com is the open source alternative with one. Our readers get a scheduling tool AND a discount.
- **Signup:** https://cal.com/affiliate-program
- **Status:** ⏳ TODO

### 7. Reclaim.ai
- **Commission:** 40% recurring 12mo + $1/workplace signup bonus
- **Why:** Highest commission rate on this list. Smart calendar assistant is a compelling ops story.
- **Signup:** https://reclaim.ai/affiliate-program
- **Status:** ⏳ TODO

## TIER 3: Nice To Have (Fill In Later)

### 8. Miro (PartnerStack)
- **Commission:** $10-83 per business signup (tiered by region)
- **Why:** Whiteboarding is essential for planning. 90M+ users.
- **Signup:** https://miro.com/affiliates/join-our-program/
- **Status:** ⏳ TODO

### 9. MailerLite
- **Commission:** 30% lifetime recurring
- **Why:** Email marketing is ops-adjacent. 30% forever is excellent.
- **Signup:** https://www.mailerlite.com/affiliate
- **Status:** ⏳ TODO

### 10. Kit (formerly ConvertKit)
- **Commission:** 30-50% recurring first 12 months, 10-20% lifetime beyond
- **Why:** Best commission structure on the list. Great for creator/ops crossover content.
- **Signup:** Search "Kit affiliate program" or check convertkit.com
- **Status:** ⏳ TODO

### 11. Typeform
- **Commission:** $20 instant + 15-20% recurring
- **Why:** Surveys and forms. Lower commission but excellent conversion.
- **Signup:** https://typeform.com/partners
- **Status:** ⏳ TODO

### 12. Canva
- **Commission:** ~30% recurring (Canvassador program)
- **Why:** Universal appeal but requires Canvassador application. Lower priority.
- **Signup:** https://www.canva.com/en_gb/help/canva-affiliate-marketing-program/
- **Status:** ⏳ TODO

### 13. Loom
- **Commission:** 15-20% recurring first year
- **Why:** Video messaging for async teams. Lower commission but broad appeal.
- **Signup:** https://loom.com/creators
- **Status:** ⏳ TODO

## Already Handled ✅

### Amazon Associates
- **Tag:** `shaynesailab-20`
- **Store ID:** vhicklegar011-20
- **Use for:** Operations books, USB hubs, monitors, ergonomic gear, Raspberry Pi hardware
- **Status:** ✅ LIVE

## Skipped (No Affiliate Program)

| Tool | Why Skip |
|------|----------|
| Calendly | "We do not currently have an affiliate program" (official) |
| Slack | $100 one-time commission only — not worthwhile for recurring model |
| Airtable | $10 credit per referral — effectively nothing |
| GoHighLevel | 40% lifetime is tempting, but audience is agencies — wrong fit for shaynesailab.com |

## Content Strategy Per Tool

Once links are live, the overnight content generator will produce articles that naturally drop in these affiliate links:

| Article Topic | Tools Featured |
|--------------|---------------|
| Notion vs ClickUp | Notion affiliate, ClickUp affiliate |
| Best Automation Platform | Make.com affiliate, alternatives |
| Scheduling Tools Compared | Cal.com affiliate (vs Calendly) |
| Form Builders for Ops | Jotform affiliate, Typeform affiliate |
| Calendar AI for Teams | Reclaim.ai affiliate |
| Free Ops Stack | MailerLite, Miro, Canva |
| Best Design Tool for Ops | Canva affiliate |
| Whiteboarding Showdown | Miro affiliate |

## TODO Search/Replace List

When you have all the referral links, send them to me and I'll run:

```bash
for f in functions/api/starter-kit/index.js functions/api/diagnostic/index.js \
         resources/index.html blog/*.html scripts/overnight/generate_content.sh; do
  sed -i "s|TODO:NOTION_AFFILIATE_LINK|$NOTION_LINK|g" "$f"
  sed -i "s|TODO:MAKE_AFFILIATE_LINK|$MAKE_LINK|g" "$f"
  # ... etc
done
```