#!/usr/bin/env bash
# Shayne's AI Lab — Auto Content Generator (DeepSeek V4 Flash)
# Uses OpenRouter API for high-quality AI tool comparison articles.
# 
# Why DeepSeek V4 Flash vs phi4-mini (3.8B):
# - Better writing quality, fewer slop phrases
# - Handles 500-800 word articles in one pass (no retries)
# - More nuanced comparisons and pricing analysis
# - Faster generation (API response vs local inference)
#
# Cost: ~$0.06/article (DeepSeek V4 Flash, 1500-2000 tokens/response)
#
# Schedule: nightly at 1:00 AM EDT
# API: OpenRouter → deepseek/deepseek-v4-flash

set -euo pipefail
umask 002

# Load credentials
CRED_FILE="/home/rock/.openclaw/credentials/shaynesailab.env"
if [ -f "$CRED_FILE" ]; then
    source "$CRED_FILE"
else
    echo "ERROR: Missing credential file $CRED_FILE" >&2
    exit 1
fi

if [ -z "${OPENROUTER_API_KEY:-}" ]; then
    echo "ERROR: OPENROUTER_API_KEY not set in $CRED_FILE" >&2
    exit 1
fi

REPO_DIR="/home/rock/workspace/ShaynesAiLab"
BLOG_DIR="$REPO_DIR/blog"
SCRIPTS_DIR="$REPO_DIR/scripts"
ARTICLES_FILE="$BLOG_DIR/articles.json"
STATE_FILE="$SCRIPTS_DIR/content_state_deepseek.json"
LOG_DIR="$SCRIPTS_DIR/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/content_gen_deepseek_$(date +%Y-%m-%d).log"

echo "[$(date)] Starting ShayneAiLab DeepSeek content generation..." | tee -a "$LOG_FILE"

# Article topics — AI tools focus for the pivot
TOPICS=(
    '{"topic":"ChatGPT vs Claude vs Gemini: Which AI Assistant Wins for Ops Teams?","slug":"chatgpt-vs-claude-vs-gemini","focus":"Comparing the three major AI assistants for operations tasks — writing, analysis, and automation workflows"}'
    '{"topic":"Best AI Writing Tools for Ops Teams in 2026","slug":"best-ai-writing-tools","focus":"Comparing Jasper, Copy.ai, Writesonic, and other AI writing tools for operations documentation and communication"}'
    '{"topic":"AI Code Assistants Compared: GitHub Copilot vs Cursor vs Codeium","slug":"ai-code-assistants","focus":"Comparing three AI coding tools for teams that need automation scripts and integrations"}'
    '{"topic":"Best AI Image Generators for Business: Midjourney vs DALL-E vs Stable Diffusion","slug":"best-ai-image-generators","focus":"Comparing AI image generation tools for marketing assets, presentations, and social media content"}'
    '{"topic":"AI Tool Pricing Compared: What Everything Actually Costs in 2026","slug":"ai-tool-pricing","focus":"Monthly cost comparison of popular AI tools including ChatGPT, Claude, Midjourney, Jasper, and more"}'
    '{"topic":"Make.com vs Zapier vs n8n: Best Automation Platform for Ops","slug":"automation-platforms","focus":"Comparing Make.com, Zapier, and n8n for operations automation — pricing, features, and use cases"}'
    '{"topic":"Best Free AI Tools for Small Business Operations","slug":"free-ai-tools-ops","focus":"Free and low-cost AI tools that operations teams at 1-50 person companies can use immediately"}'
    '{"topic":"AI Meeting Assistants Compared: Otter vs Fireflies vs Fathom","slug":"ai-meeting-assistants","focus":"Comparing AI meeting note-taking and transcription tools for teams that want to capture and action meeting content"}'
)

API_URL="https://openrouter.ai/api/v1/chat/completions"

generate_article() {
    local topic="$1"
    local slug="$2"
    local focus="$3"
    local date=$(date +%Y-%m-%d)
    local output_dir="$BLOG_DIR/$slug"
    local output_file="$output_dir/index.html"
    
    # Only generate if output doesn't exist or is older than 30 days
    if [ -f "$output_file" ]; then
        local age=$(( ($(date +%s) - $(stat -c %Y "$output_file")) / 86400 ))
        if [ $age -lt 30 ]; then
            echo "[$(date)] Skipping $slug — generated $age days ago" | tee -a "$LOG_FILE"
            return 0
        fi
    fi
    
    echo "[$(date)] Generating: $topic ($slug)" | tee -a "$LOG_FILE"
    echo "Focus: $focus" | tee -a "$LOG_FILE"
    echo "Model: deepseek/deepseek-v4-flash via OpenRouter" | tee -a "$LOG_FILE"
    
    export OPENROUTER_API_KEY GEN_TOPIC="$topic" GEN_FOCUS="$focus"
    
    # Generate via OpenRouter
    BODY=$(python3 << 'PYEOF' 2>/dev/null
import json, urllib.request, os, sys

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
TOPIC = os.environ.get("GEN_TOPIC", "")
FOCUS = os.environ.get("GEN_FOCUS", "")

system_prompt = "You are a tech blogger for Shayne's AI Lab, a site providing honest AI tool comparisons for ops teams at 1-50 person companies. Write direct, no-nonsense. Be specific about pricing, features, and real-world use cases. Avoid hype and superlatives. Include affiliate links where relevant."

user_prompt = f"""Write a 500-800 word blog article for shaynesailab.com on the topic: "{TOPIC}"

Focus: {FOCUS}

Requirements:
- Write for operations leaders at 1-50 person companies
- Practical, specific, and genuinely useful
- No hype, no "revolutionary" language, no superlatives
- Compare tools honestly — strengths and weaknesses
- Include a "Quick Verdict" section at the top (1-2 sentences)
- Sections: Overview, Head-to-Head (if comparison), Price Comparison, Who Each Is For, Quick Verdict
- Output ONLY the body HTML (no html/head/body tags)
- Use semantic HTML (h2, h3, p, ul, table where appropriate)
- Include affiliate disclosure at the top
- Use class "affiliate-link" on any affiliate links
- For Make.com link use: <a href="https://www.make.com/en/register?pc=shaynesailab" class="affiliate-link">Make.com</a>
- For ClickUp link use: <a href="https://try.web.clickup.com/0vmcctxnm95e" class="affiliate-link">ClickUp</a>
- For Fireflies link use: <a href="https://fireflies.ai/?fpr=shayne10" class="affiliate-link">Fireflies.ai</a>
- Keep the tone neutral, not promotional
- End with a "Further Reading" section"""

payload = {
    'model': 'deepseek/deepseek-v4-flash',
    'messages': [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ],
    'temperature': 0.5,
    'max_tokens': 3000
}

req = urllib.request.Request(
    API_URL,
    data=json.dumps(payload).encode(),
    headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
        'HTTP-Referer': 'https://shaynesailab.com',
        'X-Title': 'ShayneAiLab Content Generator'
    }
)
try:
    resp = urllib.request.urlopen(req, timeout=180)
    data = json.loads(resp.read())
    print(data['choices'][0]['message']['content'])
except Exception as e:
    sys.exit(1)
PYEOF
) || BODY=""
    
    if [ -z "$BODY" ]; then
        echo "[$(date)] ERROR: Failed to generate content for $slug" | tee -a "$LOG_FILE"
        return 1
    fi
    
    echo "[$(date)] Content generated successfully ($(echo "$BODY" | wc -w) words)" | tee -a "$LOG_FILE"
    
    mkdir -p "$output_dir"
    
    # Write the article HTML
    cat > "$output_file" <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$topic — Shayne's AI Lab</title>
    <meta name="description" content="$(echo "$focus" | head -c 160)">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/design-system.css">
    <meta property="og:title" content="$topic — Shayne's AI Lab">
    <meta property="og:description" content="$(echo "$focus" | head -c 160)">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://shaynesailab.com/blog/$slug">
    <meta property="og:image" content="https://shaynesailab.com/assets/shaynesailab-hero.png">
    <meta name="twitter:card" content="summary_large_image">
    <style>
        .article-body { max-width: 740px; margin: 0 auto; }
        .article-body h2 { margin-top: var(--space-xl); color: var(--text); }
        .article-body h3 { margin-top: var(--space-lg); color: var(--text); }
        .article-body p { margin-bottom: var(--space-sm); color: var(--text-secondary); line-height: 1.8; }
        .article-body ul, .article-body ol { margin-bottom: var(--space-md); color: var(--text-secondary); padding-left: 1.5rem; }
        .article-body li { margin-bottom: 0.3rem; }
        .article-body table { width: 100%; border-collapse: collapse; margin: var(--space-md) 0; }
        .article-body th, .article-body td { padding: 0.7rem 1rem; text-align: left; border-bottom: 1px solid var(--border); }
        .article-body th { color: var(--text-muted); font-weight: 600; font-size: 0.85rem; text-transform: uppercase; }
        .article-body td { color: var(--text-secondary); font-size: 0.95rem; }
        .article-body .affiliate-disclosure { border-left: 2px solid var(--brand-amber); padding: 0.5rem 1rem; margin-bottom: var(--space-lg); background: var(--brand-amber-soft); border-radius: 4px; }
        .article-body a.affiliate-link { color: var(--brand-teal-light); text-decoration: underline; text-decoration-style: dotted; }
        .article-meta { font-size: 0.85rem; color: var(--text-dim); margin-bottom: var(--space-lg); text-align: center; }
    </style>
</head>
<body>
    <nav>
        <div class="container">
            <a href="/" class="logo" aria-label="Shayne's AI Lab home">
                <svg class="logo-icon" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M24 4v12M20 16h8M18 16l-8 24c0 2.2 1.8 4 4 4h20c2.2 0 4-1.8 4-4l-8-24" stroke="url(#gradient)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="24" cy="32" r="6" stroke="url(#gradient)" stroke-width="2"/><path d="M16 36l-4 4M32 36l4 4M24 40v6M12 32H6M42 32h-6" stroke="url(#gradient)" stroke-width="2" stroke-linecap="round"/><defs><linearGradient id="gradient" x1="6" y1="4" x2="42" y2="44" gradientUnits="userSpaceOnUse"><stop stop-color="#2dd4bf"/><stop offset="1" stop-color="#06b6d4"/></linearGradient></defs></svg>
                Shayne's AI Lab
            </a>
            <ul class="nav-links" role="menubar">
                <li><a href="/blog" class="active" role="menuitem">Blog</a></li>
                <li><a href="/resources" role="menuitem">Tools</a></li>
                <li><a href="/starter-kit" role="menuitem">Free Starter Kit</a></li>
                <li><a href="/contact" role="menuitem">Contact</a></li>
            </ul>
            <button class="mobile-menu-btn" aria-label="Open menu"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>
        </div>
    </nav>

    <section class="hero">
        <div class="hero-glow" aria-hidden="true"></div>
        <div class="container" style="max-width: 740px;">
            <span class="section-label">Blog</span>
            <h1>$topic</h1>
            <p class="article-meta">$(date '+%B %d, %Y')</p>
        </div>
    </section>

    <section class="section section-alt">
        <div class="container">
            <div class="article-body">
                $BODY
            </div>
        </div>
    </section>

    <section class="section" style="text-align:center;">
        <div class="container">
            <span class="section-label">Share This Article</span>
            <p style="color:var(--text-muted);">If you found this useful, share it with someone else.</p>
            <p style="margin-bottom:var(--space-md);">
                <a href="https://twitter.com/intent/tweet?text=$topic%20—%20a%20practical%20comparison%20for%20ops%20teams&url=https://shaynesailab.com/blog/$slug" target="_blank" rel="noopener" style="display:inline-block; padding:0.4rem 1rem; margin:0.25rem; background:var(--bg-glass); border:1px solid var(--border); border-radius:var(--radius-sm); color:var(--text-secondary); text-decoration:none; font-size:0.85rem;">Share on Twitter</a>
                <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://shaynesailab.com/blog/$slug" target="_blank" rel="noopener" style="display:inline-block; padding:0.4rem 1rem; margin:0.25rem; background:var(--bg-glass); border:1px solid var(--border); border-radius:var(--radius-sm); color:var(--text-secondary); text-decoration:none; font-size:0.85rem;">Share on LinkedIn</a>
            </p>
        </div>
    </section>

    <section class="section" style="text-align:center;">
        <div class="container">
            <span class="section-label">Keep Exploring</span>
            <h2>More Tools & Comparisons</h2>
            <a href="/blog" class="btn btn-secondary">Back to Blog</a>
            <a href="/starter-kit" class="btn btn-primary">Get the Free Starter Kit</a>
        </div>
    </section>

    <footer>
        <div class="container">
            <ul class="footer-links">
                <li><a href="/blog">Blog</a></li>
                <li><a href="/resources">Tools</a></li>
                <li><a href="/about">About</a></li>
                <li><a href="/starter-kit">Free Starter Kit</a></li>
                <li><a href="/contact">Contact</a></li>
                <li><a href="/privacy">Privacy</a></li>
            </ul>
            <p>&copy; 2026 Shayne's AI Lab</p>
            <p style="font-size:0.78rem; color:var(--text-dim); margin-top:var(--space-xs);">Some links on this site are affiliate links. We may earn a commission if you purchase through them, at no extra cost to you.</p>
        </div>
    </footer>
    <script>
        document.querySelector('.mobile-menu-btn')?.addEventListener('click',function(){const e=document.querySelector('.nav-links');const n=e.style.display==='flex';e.style.display=n?'none':'flex';e.style.flexDirection='column';e.style.position='absolute';e.style.top='100%';e.style.left='0';e.style.right='0';e.style.background='var(--bg-glass)';e.style.backdropFilter='blur(14px)';e.style.padding='1rem 1.5rem';e.style.borderBottom='1px solid var(--border)';e.style.gap='0.75rem';this.setAttribute('aria-expanded',String(!n));});
    </script>
    <script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "***"}'></script>
</body>
</html>
EOF
    
    # Update articles index
    if [ ! -f "$ARTICLES_FILE" ]; then
        echo '[]' > "$ARTICLES_FILE"
    fi
    
    python3 -c "
import json
articles = json.load(open('$ARTICLES_FILE'))
article = {
    'title': '$topic',
    'slug': '$slug',
    'date': '$date',
    'description': '$(echo "$focus" | sed "s/'/\\\\'/g")',
    'url': '/blog/$slug'
}
articles = [a for a in articles if a['slug'] != '$slug']
articles.insert(0, article)
json.dump(articles, open('$ARTICLES_FILE', 'w'), indent=2)
" 2>/dev/null
    
    echo "[$(date)] Generated: $slug → $output_file" | tee -a "$LOG_FILE"
    sleep 1
}

build_blog_index() {
    echo "[$(date)] Building blog index page..." | tee -a "$LOG_FILE"
    if [ ! -f "$ARTICLES_FILE" ]; then
        echo "[$(date)] No articles yet, skipping index build" | tee -a "$LOG_FILE"
        return 0
    fi
    python3 << 'PYEOF'
import json, re

with open(os.path.join(REPO_DIR, "blog", "articles.json")) as f:
    articles = json.load(f)

cards = []
for a in articles:
    desc = a.get("description", "")
    cards.append(
        f'                <article class="post-card card">'
        f'<div class="meta">{a["date"]}</div>'
        f'<h3><a href="{a["url"]}">{a["title"]}</a></h3>'
        f'<p>{desc}</p>'
        f'</article>'
    )
new_content = "\n".join(cards)

with open(os.path.join(REPO_DIR, "blog", "index.html")) as f:
    html = f.read()

pattern = r'<div class="post-grid" id="post-grid">\s*.*?\s*</div>'
replacement = f'<div class="post-grid" id="post-grid">\n{new_content}\n            </div>'
html = re.sub(pattern, replacement, html, count=1, flags=re.DOTALL)

with open(os.path.join(REPO_DIR, "blog", "index.html"), "w") as f:
    f.write(html)
print(f"Blog index updated with {len(articles)} articles")
PYEOF
    echo "[$(date)] Blog index built" | tee -a "$LOG_FILE"
}

# Main logic
STATE=$(cat "$STATE_FILE" 2>/dev/null || echo '{"index":0}')
INDEX=$(echo "$STATE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('index',0))" 2>/dev/null)
TOTAL=${#TOPICS[@]}

TOPIC_DATA=$(echo "${TOPICS[$INDEX]}" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(d['topic']);print(d['slug']);print(d['focus'])
" 2>/dev/null)

if [ -n "$TOPIC_DATA" ]; then
    TOPIC=$(echo "$TOPIC_DATA" | sed -n '1p')
    SLUG=$(echo "$TOPIC_DATA" | sed -n '2p')
    FOCUS=$(echo "$TOPIC_DATA" | sed -n '3p')
    generate_article "$TOPIC" "$SLUG" "$FOCUS" || true
fi

# Bump index for next run
NEXT_INDEX=$(( (INDEX + 1) % TOTAL ))
echo "{\"index\":$NEXT_INDEX}" > "$STATE_FILE"

# Rebuild blog index after adding new article
build_blog_index

# Generate social media draft
if [ -n "${SLUG:-}" ] && [ -d "$BLOG_DIR/$SLUG" ]; then
    SOCIAL_DIR="$SCRIPTS_DIR/overnight/social"
    mkdir -p "$SOCIAL_DIR"
    SOCIAL_DRAFT="$SOCIAL_DIR/${SLUG}_social.txt"
    cat > "$SOCIAL_DRAFT" <<ENDSOCIAL
📝 NEW: $TOPIC

A practical, no-hype comparison for ops teams.

Read the full comparison → https://shaynesailab.com/blog/$SLUG

#AITools #OpsTools #Automation
ENDSOCIAL
    echo "[$(date)] Social draft saved: $SOCIAL_DRAFT" | tee -a "$LOG_FILE"
fi

# Update sitemap.xml
python3 << 'PYEOF' 2>/dev/null
import json, os

REPO_DIR = "/home/rock/workspace/ShaynesAiLab"
ARTICLES_FILE = os.path.join(REPO_DIR, "blog", "articles.json")

pages = [
    {"loc": "https://shaynesailab.com/", "priority": "1.0", "changefreq": "weekly"},
    {"loc": "https://shaynesailab.com/blog", "priority": "0.9", "changefreq": "daily"},
    {"loc": "https://shaynesailab.com/resources", "priority": "0.8", "changefreq": "weekly"},
    {"loc": "https://shaynesailab.com/starter-kit", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "https://shaynesailab.com/diagnostic", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "https://shaynesailab.com/about", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "https://shaynesailab.com/contact", "priority": "0.5", "changefreq": "monthly"},
    {"loc": "https://shaynesailab.com/privacy", "priority": "0.3", "changefreq": "yearly"},
]

try:
    with open(ARTICLES_FILE) as f:
        articles = json.load(f)
    for a in articles:
        pages.append({
            "loc": f"https://shaynesailab.com{a['url']}",
            "priority": "0.8",
            "changefreq": "monthly"
        })
except:
    pass

xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for p in pages:
    xml += f'  <url>\n    <loc>{p["loc"]}</loc>\n    <priority>{p["priority"]}</priority>\n    <changefreq>{p["changefreq"]}</changefreq>\n  </url>\n'
xml += '</urlset>'

with open(os.path.join(REPO_DIR, "sitemap.xml"), "w") as f:
    f.write(xml)
print(f"[sitemap] Updated with {len(pages)} URLs")
PYEOF

# Git commit and push
cd "$REPO_DIR"
git add -A
if git diff --cached --quiet; then
    echo "[$(date)] No changes to commit" | tee -a "$LOG_FILE"
else
    git commit -m "overnight: auto-generated content $(date +%Y-%m-%d)" || true
    git push origin main 2>&1 && echo "[$(date)] Changes pushed to origin main" | tee -a "$LOG_FILE" || echo "[$(date)] WARNING: git push failed" | tee -a "$LOG_FILE"
fi
