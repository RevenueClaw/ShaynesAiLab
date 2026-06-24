/**
 * Cloudflare Worker: Shayne's AI Lab — Free Ops Diagnostic Backend
 *
 * Accepted method: POST
 * Expected content-type: application/x-www-form-urlencoded or application/json
 * Origin: https://shaynesailab.com (and preview branches)
 *
 * Behavior:
 * - Parse diagnostic form answers
 * - Map biggest_time_leak to a recommended workflow + kit/custom path
 * - Calculate hours saved / payback based on company size
 * - Generate an HTML email report
 * - Send via AgentMail API from revenueclaw@agentmail.to
 * - Log lead to optional log endpoint (currently stubbed)
 */

const FROM_INBOX = 'revenueclaw@agentmail.to';
const AGENTMAIL_BASE = 'https://api.agentmail.to/v0';

const WORKFLOW_MAP = {
  email_triage: {
    name: 'Email Triage + Routing',
    sentence: 'sort and route incoming emails automatically',
    hasKit: true,
    kitPrice: '$597',
    typicalHours: { '1-10': [3, 5], '11-50': [5, 8], '51-100': [8, 12], '100+': [10, 15] },
    paybackWeeks: { '1-10': [6, 10], '11-50': [4, 8], '51-100': [3, 6], '100+': [3, 5] },
  },
  lead_qualification: {
    name: 'Lead Intake + Qualification',
    sentence: 'score and respond to every new lead automatically',
    hasKit: false,
    typicalHours: { '1-10': [2, 4], '11-50': [4, 6], '51-100': [6, 10], '100+': [8, 12] },
    paybackWeeks: { '1-10': [5, 10], '11-50': [4, 8], '51-100': [3, 6], '100+': [3, 5] },
  },
  support_tickets: {
    name: 'Support Ticket Summarization',
    sentence: 'summarize, route, and suggest answers for support tickets',
    hasKit: false,
    typicalHours: { '1-10': [2, 4], '11-50': [3, 5], '51-100': [5, 8], '100+': [6, 10] },
    paybackWeeks: { '1-10': [6, 12], '11-50': [5, 10], '51-100': [4, 8], '100+': [3, 6] },
  },
  crm_data_entry: {
    name: 'CRM Auto-Population',
    sentence: 'capture contacts and deals from email into your CRM automatically',
    hasKit: false,
    typicalHours: { '1-10': [2, 3], '11-50': [3, 5], '51-100': [5, 8], '100+': [6, 10] },
    paybackWeeks: { '1-10': [6, 12], '11-50': [5, 10], '51-100': [4, 8], '100+': [3, 6] },
  },
  invoicing: {
    name: 'Invoice Follow-Up Automation',
    sentence: 'chase unpaid invoices automatically with escalating reminders',
    hasKit: false,
    typicalHours: { '1-10': [1, 2], '11-50': [2, 3], '51-100': [3, 5], '100+': [4, 6] },
    paybackWeeks: { '1-10': [4, 8], '11-50': [3, 6], '51-100': [2, 4], '100+': [2, 4] },
  },
  meeting_prep: {
    name: 'Meeting Prep Assistant',
    sentence: 'generate briefs for meetings in under 2 minutes',
    hasKit: false,
    typicalHours: { '1-10': [1, 2], '11-50': [2, 3], '51-100': [3, 4], '100+': [3, 5] },
    paybackWeeks: { '1-10': [6, 12], '11-50': [5, 10], '51-100': [4, 8], '100+': [3, 6] },
  },
  content_social: {
    name: 'Social Content Scheduler',
    sentence: 'draft and queue social content from relevant sources',
    hasKit: false,
    typicalHours: { '1-10': [1, 2], '11-50': [2, 4], '51-100': [3, 5], '100+': [4, 6] },
    paybackWeeks: { '1-10': [8, 16], '11-50': [6, 12], '51-100': [5, 10], '100+': [4, 8] },
  },
  other: {
    name: 'Custom Operations Workflow',
    sentence: 'automate the specific operational work draining your team',
    hasKit: false,
    typicalHours: { '1-10': [2, 4], '11-50': [4, 6], '51-100': [6, 8], '100+': [8, 12] },
    paybackWeeks: { '1-10': [6, 12], '11-50': [5, 10], '51-100': [4, 8], '100+': [3, 6] },
  },
};

function formatName(email) {
  const local = email.split('@')[0] || 'there';
  const clean = local.replace(/[._-]/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
  return clean;
}

function hoursRange(companySize, workflow) {
  const range = workflow.typicalHours[companySize] || workflow.typicalHours['11-50'];
  return `${range[0]}–${range[1]}`;
}

function paybackRange(companySize, workflow) {
  const range = workflow.paybackWeeks[companySize] || workflow.paybackWeeks['11-50'];
  return `${range[0]}–${range[1]}`;
}

function monthlyValue(companySize, workflow) {
  const range = workflow.typicalHours[companySize] || workflow.typicalHours['11-50'];
  const midpoint = (range[0] + range[1]) / 2;
  const monthly = Math.round(midpoint * 35 * 4.3);
  return `$${monthly.toLocaleString()}`;
}

function buildReportHtml(data, workflow) {
  const name = formatName(data.email);
  const tools = Array.isArray(data.tools) && data.tools.length
    ? data.tools.join(', ')
    : 'Email / common ops tools';

  const ctaKit = workflow.hasKit
    ? `<p style="margin: 24px 0;">
        <strong>Start with the self-install kit.</strong><br>
        The ${workflow.name} Kit costs ${workflow.kitPrice}. If you're comfortable editing a config file, you can install it in one afternoon and start saving hours this week.
      </p>
      <p style="margin: 18px 0;">
        <a href="https://shaynesailab.com/templates/email-triage-kit" style="display:inline-block; background:#2dd4bf; color:#0f172a; padding:12px 24px; border-radius:8px; text-decoration:none; font-weight:600;">View the Kit</a>
      </p>`
    : `<p style="margin: 24px 0;">
        <strong>Request a custom build.</strong><br>
        The ${workflow.name} is best built around your exact tools (like ${tools}). I can scope it, quote a fixed price, and deliver it in 1–2 weeks.
      </p>
      <p style="margin: 18px 0;">
        <a href="mailto:hello@shaynesailab.com?subject=Custom%20workflow%20scoping%20for%20${encodeURIComponent(data.role || 'ops')}" style="display:inline-block; background:#2dd4bf; color:#0f172a; padding:12px 24px; border-radius:8px; text-decoration:none; font-weight:600;">Request a Custom Build</a>
      </p>`;

  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your AI Ops Diagnostic Report</title>
</head>
<body style="margin:0; padding:0; font-family:Inter, Helvetica, Arial, sans-serif; background:#0f172a; color:#f8fafc;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#0f172a;">
    <tr><td align="center" style="padding:40px 20px;">
      <table role="presentation" width="600" cellspacing="0" cellpadding="0" style="background:#1e293b; border:1px solid #334155; border-radius:16px; overflow:hidden;">
        <tr><td style="padding:32px;">
          <h1 style="margin:0 0 8px; font-size:24px; color:#f8fafc;">Your AI Ops Diagnostic Report</h1>
          <p style="margin:0 0 24px; color:#94a3b8; font-size:15px;">For ${name}, ${data.company_size} people</p>
          
          <h2 style="font-size:18px; color:#2dd4bf; margin-bottom:12px;">Your biggest time leak</h2>
          <p style="margin:0 0 24px; color:#f8fafc; line-height:1.6;">
            Based on your answers, the work draining the most time is <strong style="color:#2dd4bf;">${workflow.name}</strong>.
            This is the work of ${workflow.sentence}.
          </p>
          
          <h2 style="font-size:18px; color:#2dd4bf; margin-bottom:12px;">Recommended first workflow</h2>
          <p style="margin:0 0 24px; color:#f8fafc; line-height:1.6;">
            <strong>${workflow.name}</strong><br>
            A team your size typically saves <strong>${hoursRange(data.company_size, workflow)} hours per week</strong> with this workflow.
            At $35/hour, that's about <strong>${monthlyValue(data.company_size, workflow)} per month</strong> in reclaimed time.
            Most teams see payback in <strong>${paybackRange(data.companySize, workflow)} weeks</strong>.
          </p>
          
          <div style="background:#0f172a; border:1px solid #334155; border-radius:12px; padding:20px; margin-bottom:24px;">
            <h3 style="margin:0 0 12px; font-size:16px; color:#f8fafc;">Your best next step</h3>
            ${ctaKit}
          </div>
          
          <p style="color:#94a3b8; font-size:14px; line-height:1.6;">
            Not ready to decide? Just reply to this email with your #1 question and I'll answer personally.
          </p>
          
          <hr style="border:0; border-top:1px solid #334155; margin:24px 0;">
          <p style="margin:0; color:#64748b; font-size:13px;">
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

function buildReportText(data, workflow) {
  const name = formatName(data.email);
  const nextStep = workflow.hasKit
    ? `Start with the self-install kit.\nThe ${workflow.name} Kit costs ${workflow.kitPrice}. View it here: https://shaynesailab.com/templates/email-triage-kit`
    : `Request a custom build.\nThe ${workflow.name} is best built around your exact setup. Email me to scope it: hello@shaynesailab.com`;

  return `Your AI Ops Diagnostic Report

Hi ${name},

Your biggest time leak: ${workflow.name}
This is the work of ${workflow.sentence}.

Recommended first workflow: ${workflow.name}
Typical time saved: ${hoursRange(data.company_size, workflow)} hours per week
Estimated monthly value: ${monthlyValue(data.company_size, workflow)}
Typical payback: ${paybackRange(data.company_size, workflow)} weeks

Your best next step:
${nextStep}

Not ready to decide? Reply to this email with your #1 question and I'll answer personally.

— Shayne
Shayne's AI Lab
https://shaynesailab.com
`;
}

function parseFormData(request, env) {
  const contentType = request.headers.get('content-type') || '';
  if (contentType.includes('application/json')) {
    return request.json();
  }
  return request.formData().then(fd => {
    const obj = {};
    for (const [key, value] of fd.entries()) {
      if (key === 'tools') {
        obj[key] = obj[key] || [];
        obj[key].push(value);
      } else {
        obj[key] = value;
      }
    }
    return obj;
  });
}

async function sendReport(data, env) {
  const leakKey = data.biggest_time_leak || 'other';
  const workflow = WORKFLOW_MAP[leakKey] || WORKFLOW_MAP.other;
  const html = buildReportHtml(data, workflow);
  const text = buildReportText(data, workflow);

  const apiKey = env.AGENTMAIL_API_KEY;
  if (!apiKey) {
    throw new Error('AGENTMAIL_API_KEY not configured');
  }

  const encodedInbox = encodeURIComponent(FROM_INBOX);
  const response = await fetch(`${AGENTMAIL_BASE}/inboxes/${encodedInbox}/messages/send`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      to: [data.email],
      subject: `Your AI Ops Diagnostic Report — ${workflow.name}`,
      text,
      html,
      reply_to: 'hello@shaynesailab.com',
    }),
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`AgentMail send failed: ${response.status} ${err}`);
  }

  return { message_id: (await response.json()).message_id, workflow: workflow.name };
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
  return handleDiagnostic(request, env);
}

export async function onRequestOptions(context) {
  const request = context.request;
  const origin = request.headers.get('origin');
  const corsOrigin = allowOrigin(origin);
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': corsOrigin,
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  });
}

async function handleDiagnostic(request, env) {
  const origin = request.headers.get('origin');
  const corsOrigin = allowOrigin(origin);

  if (request.method !== 'POST') {
    return new Response('Method not allowed', { status: 405 });
  }

  try {
    const data = await parseFormData(request);
    const result = await sendReport(data, env);

    return new Response(JSON.stringify({
      success: true,
      message_id: result.message_id,
      recommended_workflow: result.workflow,
    }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': corsOrigin,
      },
    });
  } catch (error) {
    console.error('Diagnostic error:', error);
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
