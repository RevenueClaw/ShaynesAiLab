/**
 * Cloudflare Pages Function: Shayne's AI Lab — AI Starter Kit Delivery
 *
 * POST /api/starter-kit
 * Accepts: { email, firstName }
 * Sends: HTML + plaintext email with AI Starter Kit content
 * Uses: AgentMail API
 */

const FROM_INBOX = 'revenueclaw@agentmail.to';
const AGENTMAIL_BASE = 'https://api.agentmail.to/v0';

const STARTER_KIT_CONTENT = `
# AI Starter Kit
## 8 Tools That Are Actually Useful

---

## Welcome

A curated list of tools that have strong reputations for doing what they claim.

Not 47 tools. Not a "complete AI transformation." Just 8 tools worth knowing about if you're getting started with practical software and AI.

---

### THE 8-TOOL OVERVIEW

**1. ChatGPT (Free tier to start)**
- **What it does:** AI assistant for writing, brainstorming, analysis
- **When to use:** Drafting emails, outlining content, explaining complex topics, brainstorming
- **Pro tip:** The voice feature works well for talking through ideas while mobile
- **Cost:** Free (Plus at $20/mo for priority access and advanced models)

**2. Claude (Free tier)**
- **What it does:** Long-form documents and nuanced analysis
- **When to use:** Analyzing contracts, writing detailed reports, when you need more context than ChatGPT
- **Why it's different:** Larger context window — understands more of your document
- **Cost:** Free

**3. Canva (Free)**
- **What it does:** Graphics, thumbnails, social posts
- **When to use:** Graphics that used to take an hour now take 5 minutes
- **AI features:** Magic Write, Background Remover, Resize
- **Cost:** Free (Pro at $13/mo if you need brand kit)

**4. Perplexity (Free)**
- **What it does:** AI search with real sources
- **When to use:** Research with citations, fact-checking
- **Difference from ChatGPT:** Shows WHERE it got the info
- **Cost:** Free (Pro at $20/mo for more searches)

**5. Notion (Free)**
- **What it does:** Notes, docs, databases, wikis
- **When to use:** Project documentation, team collaboration, linking notes together
- **AI features:** Ask questions about your notes, summarize
- **Cost:** Free (AI features included)

**6. Fireflies.ai (Free tier)**
- **What it does:** Records and transcribes meetings
- **When to use:** Never take meeting notes again, capture customer calls
- **Cost:** Free tier (paid starts at $10/mo for more minutes)

**7. Calendly (Free)**
- **What it does:** Scheduling without the back-and-forth
- **When to use:** Booking calls, eliminating "when works for you?" email chains
- **Savings:** 2-3 emails per meeting
- **Cost:** Free

**8. Cloudflare (Free tier)**
- **What it does:** Website hosting, DNS, security
- **When to use:** Hosting static sites, managing DNS, DDoS protection
- **Cost:** Free tier is enough for most people

---

### TOTAL COST BREAKDOWN

All 8 tools: **$0 to start.** Maybe $20-50/mo if you're using everything heavily.
Compare to: $500+/mo for VAs, designers, assistants.

---

### YOUR FIRST 30 DAYS

**Week 1:** Pick ONE tool that solves your biggest pain point. Use it for one specific task every day.

**Week 2:** Add a second tool once the first feels natural.

**Week 3:** Start connecting them into workflows.

**Week 4:** Review what worked, cut what didn't.

---

### THE HONEST TRUTH

AI won't transform your business overnight. But it will save you 10-15 hours a week if you use it right.

The key: Consistency over complexity. Pick tools. Use them. Build habits. That's it.

---

**Questions?** hello@shaynesailab.com
`;

function buildHtmlEmail(firstName) {
  const greeting = firstName ? `Hi ${firstName},` : 'Hi there,';
  const items = STARTER_KIT_CONTENT.split('---').filter(s => s.trim()).map(section => {
    return `<div style="background:#0f172a; border:1px solid #334155; border-radius:12px; padding:20px; margin-bottom:16px;">
      ${section.trim().replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}
    </div>`;
  }).join('');

  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your AI Starter Kit</title>
</head>
<body style="margin:0; padding:0; font-family:Inter, Helvetica, Arial, sans-serif; background:#0f172a; color:#f8fafc;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#0f172a;">
    <tr><td align="center" style="padding:40px 20px;">
      <table role="presentation" width="600" cellspacing="0" cellpadding="0" style="background:#1e293b; border:1px solid #334155; border-radius:16px; overflow:hidden;">
        <tr><td style="padding:32px;">
          <h1 style="margin:0 0 8px; font-size:24px; color:#f8fafc;">Your AI Starter Kit</h1>
          <p style="margin:0 0 24px; color:#94a3b8; font-size:15px;">${greeting}</p>
          
          <p style="color:#f8fafc; line-height:1.6; margin-bottom:24px;">
            A curated list of 8 tools that have strong reputations for doing what they claim. Not 47 tools. Not a "complete AI transformation."
            Just 8 tools worth knowing about if you're getting started with practical software and AI.
          </p>

          ${items}

          <hr style="border:0; border-top:1px solid #334155; margin:24px 0;">
          <p style="margin:0; color:#64748b; font-size:13px; line-height:1.5;">
            Want more? Check out the <a href="https://shaynesailab.com/diagnostic" style="color:#2dd4bf;">Free Ops Diagnostic</a> — 6 questions, 5 minutes, personalized report.<br><br>
            — Shayne<br>
            <a href="https://shaynesailab.com" style="color:#2dd4bf; text-decoration:none;">Shayne's AI Lab</a>
          </p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>`;
}

function buildPlaintextEmail(firstName) {
  const greeting = firstName ? `Hi ${firstName},` : 'Hi there,';
  return `${greeting}

A curated list of 8 tools that have strong reputations for doing what they claim. Not 47 tools. Not a "complete AI transformation." Just 8 tools worth knowing about if you're getting started with practical software and AI.

${STARTER_KIT_CONTENT}

Want more? Check out the Free Ops Diagnostic: https://shaynesailab.com/diagnostic

— Shayne
Shayne's AI Lab
https://shaynesailab.com`;
}

async function sendStarterKit(data, env) {
  const apiKey = env.AGENTMAIL_API_KEY;
  if (!apiKey) {
    throw new Error('AGENTMAIL_API_KEY not configured');
  }

  const html = buildHtmlEmail(data.firstName);
  const text = buildPlaintextEmail(data.firstName);

  const encodedInbox = encodeURIComponent(FROM_INBOX);
  const response = await fetch(`${AGENTMAIL_BASE}/inboxes/${encodedInbox}/messages/send`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      to: [data.email],
      subject: 'Your AI Starter Kit — 8 Tools That Actually Save Time',
      text,
      html,
      reply_to: 'hello@shaynesailab.com',
    }),
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`AgentMail send failed: ${response.status} ${err}`);
  }

  return (await response.json()).message_id;
}

function allowOrigin(origin) {
  if (!origin) return 'https://shaynesailab.com';
  if (origin.includes('shaynesailab.pages.dev') || origin.includes('shaynesailab.com')) {
    return origin;
  }
  return 'https://shaynesailab.com';
}

export async function onRequestPost(context) {
  const { request, env } = context;
  const origin = request.headers.get('origin');
  const corsOrigin = allowOrigin(origin);

  try {
    const data = await request.json();

    if (!data.email || !data.email.includes('@')) {
      return new Response(JSON.stringify({
        success: false,
        error: 'Valid email is required',
      }), {
        status: 400,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': corsOrigin,
        },
      });
    }

    const messageId = await sendStarterKit(data, env);

    return new Response(JSON.stringify({
      success: true,
      message_id: messageId,
    }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': corsOrigin,
      },
    });
  } catch (error) {
    console.error('Starter kit error:', error);
    return new Response(JSON.stringify({
      success: false,
      error: error.message,
    }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': corsOrigin,
      },
    });
  }
}

export async function onRequestOptions(context) {
  const request = context.request;
  const origin = request.headers.get('origin');
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': allowOrigin(origin),
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  });
}