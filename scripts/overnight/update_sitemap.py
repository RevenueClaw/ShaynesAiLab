#!/usr/bin/env python3
"""Update sitemap.xml with static pages and blog articles.

Usage: python3 update_sitemap.py <articles.json> <sitemap.xml> <repo_dir>
"""

import json
import sys


def main():
    if len(sys.argv) < 4:
        print("Usage: update_sitemap.py <articles.json> <sitemap.xml> <repo_dir>",
              file=sys.stderr)
        sys.exit(1)

    articles_file = sys.argv[1]
    sitemap_file = sys.argv[2]
    repo_dir = sys.argv[3]

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
        with open(articles_file) as f:
            articles = json.load(f)
        for a in articles:
            pages.append({
                "loc": "https://shaynesailab.com" + a["url"],
                "priority": "0.8",
                "changefreq": "monthly"
            })
    except Exception as e:
        print(f"Warning: Could not load articles: {e}", file=sys.stderr)

    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>',
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in pages:
        xml_lines.append("  <url>")
        xml_lines.append(f'    <loc>{p["loc"]}</loc>')
        xml_lines.append(f'    <priority>{p["priority"]}</priority>')
        xml_lines.append(f'    <changefreq>{p["changefreq"]}</changefreq>')
        xml_lines.append("  </url>")
    xml_lines.append("</urlset>")

    with open(sitemap_file, "w") as f:
        f.write("\n".join(xml_lines) + "\n")

    print(f"[sitemap] Updated with {len(pages)} URLs")


if __name__ == "__main__":
    main()