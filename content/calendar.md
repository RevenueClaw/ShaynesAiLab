# Shayne's AI Lab — Content Calendar

_Last updated: 2026-10-15_

## Goal
Publish 1–2 SEO-focused ops-automation articles per week to drive organic traffic to the product pages and lead magnets.

## Content Pillars
1. **AI tools & comparisons** — practical evaluations for ops teams
2. **Workflow tutorials** — step-by-step automation guides
3. **Use-case spotlights** — email triage, lead capture, support, content
4. **Strategy & planning** — how to choose/build/deploy AI agents

## Upcoming Articles

| Week | Target Keyword / Topic | Status | URL Slug |
|------|------------------------|--------|----------|
| 2026-10-20 | AI agents for small business: 5 workflows to deploy this week | ✅ published | `blog/ai-agents-small-business` |
| 2026-10-20 | How to choose an AI agent platform (no-code vs custom vs managed) | ✅ published | `blog/choose-ai-agent-platform` |
| 2026-10-27 | AI customer service automation: setup guide + tools | ⚪ planned | `blog/ai-customer-service-automation` |
| 2026-11-03 | Lead qualification automation: from form to CRM to follow-up | ⚪ planned | `blog/lead-qualification-automation` |
| 2026-11-10 | Building an AI SDR: prompts, tools, and guardrails | ⚪ planned | `blog/ai-sdr-setup` |
| 2026-11-17 | AI project management: automating status updates and reports | ⚪ planned | `blog/ai-project-management` |

## Production Workflow
1. Write brief in `content/briefs/{slug}.md`
2. Generate draft with `scripts/generate_blog_post.py`
3. Human review / edit
4. Add to `blog/{slug}/index.html`
5. Update `articles.json`, `sitemap.xml`, `blog/index.html`
6. Publish via git push

## Distribution Checklist
- [ ] Post to Telegram (@RockLobsterClaw_Bot)
- [ ] Post to LinkedIn (personal + company if available)
- [ ] Add to newsletter queue
- [ ] Submit updated sitemap to Bing
