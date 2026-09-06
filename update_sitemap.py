#!/usr/bin/env python3
"""Add blogs.html, category pages, and all 101 article pages to sitemap.xml."""
import re, os, glob

BASE = "https://lipon.pro.bd"
SITEMAP = "sitemap.xml"

# Read existing sitemap
with open(SITEMAP, "r", encoding="utf-8") as f:
    content = f.read()

# Collect existing locs
existing = set(re.findall(r"<loc>(.*?)</loc>", content))

# Build new entries
new_entries = []

def add(loc, lastmod="2026-09-06", freq="weekly", prio="0.7"):
    if loc not in existing:
        new_entries.append((loc, lastmod, freq, prio))
        existing.add(loc)

# blogs.html
add(f"{BASE}/blogs.html", "2026-09-06", "daily", "0.9")

# category pages
for cat in ["guides", "game-lists", "gaming-culture"]:
    add(f"{BASE}/blogs/category/{cat}.html", "2026-09-06", "weekly", "0.8")

# all 101 articles
slugs = sorted(glob.glob("blogs/*.html"))
for p in slugs:
    slug = os.path.basename(p)[:-5]
    add(f"{BASE}/blogs/{slug}.html", "2026-09-06", "weekly", "0.7")

# Rebuild sitemap: keep original order for existing, append new
# Parse original url blocks in order
url_blocks = re.findall(r"<url>.*?</url>", content, re.DOTALL)
existing_locs_in_order = []
for b in url_blocks:
    m = re.search(r"<loc>(.*?)</loc>", b)
    if m:
        existing_locs_in_order.append(m.group(1))

# Build final ordered list: original order + new entries (not already present)
final_locs = list(existing_locs_in_order)
final_set = set(final_locs)
for loc, lastmod, changefreq, prio in new_entries:
    if loc not in final_set:
        final_locs.append(loc)
        final_set.add(loc)

def block(loc, lastmod, changefreq, prio):
    return f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{prio}</priority>
  </url>"""

# Map loc -> (lastmod, changefreq, prio) for new entries
meta = {loc: (lm, cf, pr) for loc, lm, cf, pr in new_entries}

# For existing locs, preserve their original metadata by re-parsing
orig_meta = {}
for b in url_blocks:
    m = re.search(r"<loc>(.*?)</loc>", b)
    if not m:
        continue
    loc = m.group(1)
    lm = re.search(r"<lastmod>(.*?)</lastmod>", b)
    cf = re.search(r"<changefreq>(.*?)</changefreq>", b)
    pr = re.search(r"<priority>(.*?)</priority>", b)
    orig_meta[loc] = (lm.group(1) if lm else "2026-09-05",
                      cf.group(1) if cf else "weekly",
                      pr.group(1) if pr else "0.7")

blocks = []
for loc in final_locs:
    if loc in orig_meta:
        lm, cf, pr = orig_meta[loc]
    else:
        lm, cf, pr = meta[loc]
    blocks.append(block(loc, lm, cf, pr))

header = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
footer = "</urlset>\n"
with open(SITEMAP, "w", encoding="utf-8") as f:
    f.write(header)
    f.write("\n".join(blocks))
    f.write("\n" + footer)

print(f"Total URLs in sitemap: {len(final_locs)}")
print(f"Blog article URLs: {sum(1 for l in final_locs if '/blogs/' in l and '/category/' not in l)}")
print(f"Category URLs: {sum(1 for l in final_locs if '/blogs/category/' in l)}")
print(f"blogs.html present: {'https://lipon.pro.bd/blogs.html' in final_locs}")