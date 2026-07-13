#!/usr/bin/env bash
# Shayne's AI Lab — Auto Content Generator
# Runs as part of the overnight batch pipeline.
# Generates comparison articles and tool roundups with affiliate links.
# Articles are saved as static HTML in blog/ directory.
#
# Schedule: nightly at 1:00 AM EDT
# Model: ollama-omen-cpu/mistral-small (CPU, precise enough for structured output)

set -euo pipefail
umask 002

REPO_DIR="/home/rock/workspace/ShaynesAiLab"
BLOG_DIR="$REPO_DIR/blog"
SCRIPTS_DIR="$REPO_DIR/scripts"
ARTICLES_FILE="$BLOG_DIR/articles.json"
STATE_FILE="$SCRIPTS_DIR/content_state.json"
LOG_DIR="$SCRIPTS_DIR/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/content_gen_$(date +%Y-%m-%d).log"

echo "[$(date)] Starting ShayneAiLab content generation..." | tee -a "$LOG_FILE"

# Article generation config — one per run, rotates through topics
TOPICS=(
    '{"topic":"Notion vs ClickUp for Ops Teams","slug":"notion-vs-clickup","focus":"task and project management for operations"}'
    '{"topic":"Make.com vs Zapier: Which Automation Platform Wins?","slug":"make-vs-zapier","focus":"automation workflows for small teams"}'
    '{"topic":"Best AI Writing Assistants for Ops Teams in 2026","slug":"best-ai-writing","focus":"ChatGPT, Claude, Jasper compared for ops docs"}'
    '{"topic":"Canva vs Alternatives: Best Design Tool for Ops","slug":"canva-alternatives","focus":"graphic design for non-designers in operations"}'
    '{"topic":"HubSpot vs Free CRM Options for Small Teams","slug":"hubspot-vs-free-crm","focus":"CRM for 1-50 person ops teams"}'
    '{"topic":"5 Free Tools Every Ops Team Should Know About","slug":"5-free-ops-tools","focus":"productivity tools under $0/mo"}'
    '{"topic":"Automating Email Triage: Tools and Techniques","slug":"automate-email-triage","focus":"email management with AI and automation"}'
    '{"topic":"Notion Templates for Operations Management","slug":"notion-ops-templates","focus":"Notion setup guides for ops workflows"}'
)

# Affiliate links — replace TODO once Shayne provides them
NOTION_AFF="TODO:NOTION_AFFILIATE_LINK"
MAKE_AFF="https://www.make.com/en/register?pc=shaynesailab"
HUBSPOT_AFF="TODO:HUBSPOT_AFFILIATE_LINK"
CANVA_AFF="TODO:CANVA_AFFILIATE_LINK"
AMAZON_AFF="shaynesailab-20"

generate_article() {
    local topic="$1"
    local slug="$2"
    local focus="$3"
    local date=$(date +%Y-%m-%d)
    local output_file="$BLOG_DIR/$slug.html"
    
    # Only generate if output doesn't exist or is older than 30 days
    if [ -f "$output_file" ]; then
        local age=$(( ($(date +%s) - $(stat -c %Y "$output_file")) / 86400 ))
        if [ $age -lt 30 ]; then
            echo "[$(date)] Skipping $slug — generated $age days ago" | tee -a "$LOG_FILE"
            return 0
        fi
    fi
    
    echo "[$(date)] Generating: $topic ($slug)" | tee -a "$LOG_FILE"
    
    PROMPT=$(cat <<-END
Write a 500-800 word blog article for shaynesailab.com on the topic: "$topic".

Focus: $focus

Requirements:
- Write for operations leaders at 1-50 person companies
- Practical, specific, and genuinely useful
- No hype, no "revolutionary" language, no superlatives
- Compare tools honestly — strengths and weaknesses
- Include a "Quick Verdict" section at the top (1-2 sentences)
- Sections: Overview, Head-to-Head (if comparison), Price Comparison, Who Each Is For, Quick Verdict
- Output ONLY the body HTML (no html/head/body tags)
- Use semantic HTML (h2, h3, p, ul, table where appropriate)
- Include affiliate disclosure at the top: "<p class="affiliate-disclosure" style="font-size:0.82rem;color:#64748b;">Some links below are affiliate links. We may earn a commission if you purchase through them, at no extra cost to you.</p>"
- Use class "affiliate-link" on any link that is an affiliate link
- For affiliate links use this format: <a href="https://notion.com?ref=TODO" class="affiliate-link">Notion</a> (replace TODO with link placeholder)
- Keep the tone neutral, not promotional
- End with a "Further Reading" section linking to relevant tools
END
)
    
    # Generate via Ollama on Omen CPU
    # Using curl to ollama-omen-cpu:11435 with mistral-small for quality
    BODY=$(curl -s http://192.168.4.108:11435/api/generate \
        -d "{\"model\":\"mistral-small\",\"prompt\":\"$PROMPT\",\"stream\":false,\"options\":{\"temperature\":0.3,\"max_tokens\":3000}}" | \
        python3 -c "import sys,json; print(json.load(sys.stdin).get('response',''))" 2>/dev/null) || BODY=""
    
    if [ -z "$BODY" ]; then
        echo "[$(date)] ERROR: Failed to generate content for $slug" | tee -a "$LOG_FILE"
        return 1
    fi
    
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
            <p class="article-meta">$(date +%B %d, %Y)</p>
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
# Remove existing entry if present
articles = [a for a in articles if a['slug'] != '$slug']
articles.insert(0, article)
json.dump(articles, open('$ARTICLES_FILE', 'w'), indent=2)
" 2>/dev/null
    
    echo "[$(date)] Generated: $slug" | tee -a "$LOG_FILE"
    
    # Rate limit
    sleep 2
}

build_blog_index() {
    echo "[$(date)] Building blog index page..." | tee -a "$LOG_FILE"
    
    if [ ! -f "$ARTICLES_FILE" ]; then
        echo "[$(date)] No articles yet, skipping index build" | tee -a "$LOG_FILE"
        return 0
    fi
    
    INDEX_FILE="$BLOG_DIR/index.html"
    
    # Generate post cards HTML
    POSTS_HTML=$(python3 -c "
import json
articles = json.load(open('$ARTICLES_FILE'))
if not articles:
    print('')
else:
    cards = []
    for a in articles:
        cards.append(f'<article class=\"post-card card\">'
            f'<div class=\"meta\">{a[\"date\"]}</div>'
            f'<h3><a href=\"{a[\"url\"]}\">{a[\"title\"]}</a></h3>'
            f'<p>{a[\"description\"]}</p>'
            f'</article>')
    print('\\n'.join(cards))
" 2>/dev/null)
    
    if [ -n "$POSTS_HTML" ]; then
        # Update the blog index - hide empty state, show posts
        sed -i "s|<div class=\"empty-state\" id=\"empty-state\">.*|<div class=\"post-grid\" id=\"post-grid\">$POSTS_HTML</div>|" "$INDEX_FILE"
        sed -i 's|style="display:none;"||g' "$INDEX_FILE"
        echo "[$(date)] Blog index updated with $(echo "$POSTS_HTML" | grep -c 'post-card') articles" | tee -a "$LOG_FILE"
    fi
}

# Main
# Generate one article per run (rotates)
STATE=$(cat "$STATE_FILE" 2>/dev/null || echo '{"index":0}')
INDEX=$(echo "$STATE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('index',0))" 2>/dev/null)
TOTAL=${#TOPICS[@]}

TOPIC_DATA=$(echo "${TOPICS[$INDEX]}" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['topic']);print(d['slug']);print(d['focus'])" 2>/dev/null)

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

echo "[$(date)] Content generation complete. Next topic index: $NEXT_INDEX" | tee -a "$LOG_FILE"