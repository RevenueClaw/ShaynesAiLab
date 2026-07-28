#!/usr/bin/env python3
"""
Shayne's AI Lab — Affiliate Link Retrofit Script
Phase 1.2: Adds working affiliate links to all 18 existing blog posts.
Also adds affiliate disclosure where missing.

Run: python3 scripts/retrofit_affiliate_links.py
"""

import os
import re
import shutil

# ── Configuration ──
BLOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "blog")

# Confirmed working affiliate links
AFFILIATE_LINKS = {
    "make.com": {
        "url": "https://www.make.com/en/register?pc=shaynesailab",
        "label": "Make.com",
        "class": "affiliate-link",
    },
    "clickup": {
        "url": "https://try.web.clickup.com/0vmcctxnm95e",
        "label": "ClickUp",
        "class": "affiliate-link",
    },
    "fireflies": {
        "url": "https://fireflies.ai/?fpr=shayne10",
        "label": "Fireflies.ai",
        "class": "affiliate-link",
    },
    "fireflies.ai": {
        "url": "https://fireflies.ai/?fpr=shayne10",
        "label": "Fireflies.ai",
        "class": "affiliate-link",
    },
    "jotform": {
        "url": "https://www.jotform.com/?partner=revenueclaw",
        "label": "Jotform",
        "class": "affiliate-link",
    },
}

# Amazon tag — any amazon.com link with shaynesailab-20
AMAZON_TAG = "shaynesailab-20"
AMAZON_AFF_FORMAT = "https://www.amazon.com/s?k={query}&tag={tag}"

# Post-to-affiliate mapping: which affiliate links should appear in each post
POST_AFFILIATE_MAP = {
    "systemeio-vs-clickfunnels": ["jotform"],  # Systeme.io doesn't have aff program
    "systemeio-pricing": ["jotform"],
    "notion-vs-clickup": [],  # Already has 21 links — verified
    "hubspot-vs-freshsales": ["jotform"],
    "automation-platforms": ["make.com"],
    "chatgpt-vs-claude-vs-gemini": [],  # No direct affiliate programs for these
    "free-ai-tools-ops": ["fireflies", "make.com", "jotform"],
    "best-ai-writing-tools": [],  # Jasper/Copy.ai — no aff links yet
    "best-ai-image-generators": [],  # Canva/Midjourney — no aff links yet
    "ai-tool-pricing": ["make.com", "jotform", "fireflies"],
    "ai-meeting-assistants": ["fireflies"],
    "ai-code-assistants": [],  # Copilot/Cursor/Codeium — no aff links
    "systemeio-funnel-setup": ["jotform"],
    "lead-capture-jotform-make": ["jotform", "make.com"],
    "ergonomic-ops-desk-setup": [],  # Amazon links — handled separately
    "email-triage-tools": ["make.com"],
    "free-form-builders-ops": ["jotform"],
    "make-automations-ops": ["make.com"],
}

# Tool name → affiliate key mapping (for text replacement)
# More specific matches first to avoid partial matches
TOOL_TEXT_MAP = [
    (r'\bFireflies\.ai\b', 'fireflies.ai', 'Fireflies.ai'),
    (r'\bFireflies\b(?!\.ai)', 'fireflies', 'Fireflies.ai'),
    (r'\bMake\.com\b', 'make.com', 'Make.com'),
    (r'\bClickUp\b', 'clickup', 'ClickUp'),
    (r'\bJotform\b', 'jotform', 'Jotform'),
]

AFFILIATE_DISCLOSURE = (
    '<p class="affiliate-disclosure">Some links in this article are affiliate links. '
    'We may earn a commission if you purchase through them, at no extra cost to you.</p>'
)


def has_affiliate_disclosure(html):
    """Check if the article already has an affiliate disclosure."""
    return 'affiliate-disclosure' in html


def ensure_affiliate_disclosure(html):
    """Add affiliate disclosure at the top of the article body if missing."""
    if has_affiliate_disclosure(html):
        return html
    
    # Find the article-body div content start
    body_match = re.search(r'<div class="article-body">\s*\n', html)
    if body_match:
        insert_pos = body_match.end()
        # Check if there's already a disclosure
        if 'affiliate' in html[insert_pos:insert_pos + 500].lower():
            return html
        html = html[:insert_pos] + '\n' + AFFILIATE_DISCLOSURE + '\n' + html[insert_pos:]
        print("  + Added affiliate disclosure")
    return html


def wrap_tool_in_affiliate_link(html, tool_pattern, aff_key, tool_display):
    """Wrap standalone tool name mentions with affiliate links, avoiding double-wrapping."""
    aff = AFFILIATE_LINKS.get(aff_key)
    if not aff:
        return html
    
    url = aff["url"]
    css_class = aff.get("class", "")
    class_attr = f' class="{css_class}"' if css_class else ""
    
    # Don't wrap if already inside an <a> tag
    def replace_match(m):
        full_match = m.group(0)
        # Find position in original string
        start = m.start()
        # Check if we're already inside an <a> tag (backward search)
        before = html[max(0, start - 200):start]
        if re.search(r'<a\s[^>]*href=[\'"]', before) and '</a>' not in before[before.rfind('<a'):]:
            return full_match  # Already inside an anchor tag, skip
        # Don't replace if already an affiliate link
        if f'class="affiliate-link"' in before[max(0, len(before) - 100):]:
            return full_match
        return f'<a href="{url}"{class_attr}>{full_match}</a>'
    
    return re.sub(tool_pattern, replace_match, html)


def fix_amazon_links(html):
    """Add Amazon affiliate tag to any amazon.com links that don't have a tag."""
    # Find amazon.com links without tag parameter
    def add_tag(m):
        link = m.group(0)
        if 'tag=' in link:
            return link  # Already has a tag
        if '?' in link:
            return link + f'&tag={AMAZON_TAG}'
        else:
            return link + f'?tag={AMAZON_TAG}'
    
    html = re.sub(r'https?://(?:www\.)?amazon\.com[^\s"\'<>)]+', add_tag, html)
    return html


def insert_affiliate_section(html, slug):
    """Add targeted affiliate recommendations section near the end of articles that have affiliate links."""
    aff_keys = POST_AFFILIATE_MAP.get(slug, [])
    if not aff_keys:
        return html
    
    # Check if we already added this section
    if 'affiliate-recommendations' in html:
        return html
    
    # Build recommendations HTML
    items = []
    for key in aff_keys:
        aff = AFFILIATE_LINKS.get(key)
        if aff:
            items.append(f'<li><a href="{aff["url"]}" class="affiliate-link" rel="nofollow">{aff["label"]}</a> — {get_tool_blurb(key)}</li>')
    
    if not items:
        return html
    
    section = (
        '\n<h3>Tools mentioned in this article</h3>\n'
        '<ul class="affiliate-recommendations">\n'
        + '\n'.join(items) +
        '\n</ul>\n'
    )
    
    # Insert before "Further Reading" section or at end of article body
    further_reading = re.search(r'<h2?>Further Reading</h2?>', html, re.IGNORECASE)
    if further_reading:
        insert_pos = further_reading.start()
        html = html[:insert_pos] + section + html[insert_pos:]
    else:
        article_body_end = html.rfind('</div>')
        if article_body_end > 0:
            html = html[:article_body_end] + section + html[article_body_end:]
    
    return html


def get_tool_blurb(key):
    """Short description for tool recommendation section."""
    blurbs = {
        "make.com": "Build automations without code — email triage, lead routing, and custom workflows",
        "jotform": "Forms, automation, and payment collection — great for lead capture and intake forms",
        "fireflies": "AI meeting notes and transcription that integrates with your calendar",
        "clickup": "Project management platform with AI features for ops teams",
    }
    return blurbs.get(key, "")


def process_post(slug):
    """Process a single blog post to add affiliate links."""
    post_dir = os.path.join(BLOG_DIR, slug)
    index_file = os.path.join(post_dir, "index.html")
    
    if not os.path.exists(index_file):
        print(f"  SKIP: {slug} — no index.html found")
        return False
    
    # Backup
    backup_file = index_file + ".bak"
    shutil.copy2(index_file, backup_file)
    
    with open(index_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original = html
    changes = []
    
    # 1. Ensure affiliate disclosure is present
    html = ensure_affiliate_disclosure(html)
    if html != original:
        changes.append("disclosure")
    
    # 2. Fix Amazon links
    html_before = html
    html = fix_amazon_links(html)
    if html != html_before:
        changes.append("amazon-tags")
    
    # 3. Wrap tool names with affiliate links
    for pattern, aff_key, tool_display in TOOL_TEXT_MAP:
        # Only wrap if this post is mapped to have this affiliate
        if aff_key in POST_AFFILIATE_MAP.get(slug, []) or aff_key == 'amazon':
            html_before = html
            html = wrap_tool_in_affiliate_link(html, pattern, aff_key, tool_display)
            if html != html_before:
                changes.append(f"affiliate-{aff_key}")
    
    # 4. Add affiliate recommendations section
    html_before = html
    html = insert_affiliate_section(html, slug)
    if html != html_before:
        changes.append("recommendations-section")
    
    # Write if changed
    if html != original:
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  ✅ {slug}: {', '.join(changes)}")
        return True
    else:
        print(f"  ➖ {slug}: no changes needed")
        return False


def main():
    print("=" * 60)
    print("Shayne's AI Lab — Affiliate Link Retrofit")
    print("=" * 60)
    
    # Get all blog post directories (exclude non-post dirs)
    post_slugs = []
    for item in sorted(os.listdir(BLOG_DIR)):
        item_path = os.path.join(BLOG_DIR, item)
        if os.path.isdir(item_path) and item != 'content' and not item.startswith('.'):
            post_slugs.append(item)
    
    # Also process standalone HTML files in blog root
    standalone_posts = []
    for f in sorted(os.listdir(BLOG_DIR)):
        if f.endswith('.html') and f != 'index.html' and os.path.isfile(os.path.join(BLOG_DIR, f)):
            standalone_posts.append(f)
    
    total_modified = 0
    total_skipped = 0
    
    print(f"\n📁 Processing {len(post_slugs)} blog post directories...\n")
    for slug in post_slugs:
        if process_post(slug):
            total_modified += 1
        else:
            total_skipped += 1
    
    print(f"\n📄 Processing {len(standalone_posts)} standalone HTML files...\n")
    for fname in standalone_posts:
        slug = fname.replace('.html', '')
        if process_post(slug):
            total_modified += 1
        else:
            total_skipped += 1
    
    print(f"\n{'=' * 60}")
    print(f"Done! Modified: {total_modified} | Skipped: {total_skipped}")
    print(f"Backups saved as .bak files alongside originals")
    print(f"Don't forget: git add, commit, and push to deploy!")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()