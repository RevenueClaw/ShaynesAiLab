#!/usr/bin/env python3
"""Build blog index HTML from articles.json.

Usage: python3 build_blog_index.py <articles_json_path> <blog_index_html_path>

Replaces the empty-state or existing post-grid with dynamically generated
article cards from the articles JSON.
"""

import json
import re
import sys


def main():
    if len(sys.argv) < 3:
        print("Usage: build_blog_index.py <articles.json> <blog/index.html>", file=sys.stderr)
        sys.exit(1)

    articles_file = sys.argv[1]
    index_file = sys.argv[2]

    with open(articles_file) as f:
        articles = json.load(f)

    if not articles:
        print("No articles, skipping index build")
        return

    cards = []
    for a in articles:
        title = a.get("title", "")
        slug_url = a.get("url", "")
        date = a.get("date", "")
        desc = a.get("description", "")
        cards.append(
            '<article class="post-card card">'
            f'<div class="meta">{date}</div>'
            f'<h3><a href="{slug_url}">{title}</a></h3>'
            f'<p>{desc}</p>'
            "</article>"
        )

    post_html = "\n".join(cards)

    with open(index_file) as f:
        html = f.read()

    # Replace either empty-state or existing post-grid
    html = re.sub(
        r'<div class="empty-state" id="empty-state">.*?</div>|'
        r'<div class="post-grid" id="post-grid">.*?</div>',
        '<div class="post-grid" id="post-grid">' + post_html + '</div>',
        html,
        flags=re.DOTALL,
    )
    html = html.replace('style="display:none;"', "")

    with open(index_file, "w") as f:
        f.write(html)

    print(f"Blog index updated with {len(cards)} articles")


if __name__ == "__main__":
    main()