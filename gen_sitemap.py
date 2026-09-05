import json, re, datetime, os

with open("games.js","r") as f:
    js = f.read()
m = re.search(r'window\.GAME_CATALOG\s*=\s*(\[[\s\S]*\]);', js)
games = json.loads(m.group(1))

SITE = "https://lipon.pro.bd"
TODAY = datetime.date.today().isoformat()

urls = [
    ("/", "1.0", "daily"),
    ("/tools.html", "0.8", "weekly"),
    ("/security.html", "0.8", "weekly"),
    ("/privacypolicy.html", "0.5", "monthly"),
]
for g in games:
    urls.append((f"/{g['file']}", "0.7", "weekly"))

lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path, prio, freq in urls:
    lines.append("  <url>")
    lines.append(f"    <loc>{SITE}{path}</loc>")
    lines.append(f"    <lastmod>{TODAY}</lastmod>")
    lines.append(f"    <changefreq>{freq}</changefreq>")
    lines.append(f"    <priority>{prio}</priority>")
    lines.append("  </url>")
lines.append("</urlset>")

with open("sitemap.xml","w") as f:
    f.write("\n".join(lines) + "\n")

print(f"sitemap.xml: {len(urls)} URLs")
