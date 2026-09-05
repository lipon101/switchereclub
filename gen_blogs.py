#!/usr/bin/env python3
# Regenerate the Blogs listing page (blogs.html) and every article page (blogs/{slug}.html).
# Content lives in blog_data.py. Run:  python3 gen_blogs.py
import os, html, datetime
from blog_data import ARTICLES
from blog_enrich import enrich_all

SITE = "https://lipon.pro.bd"
BRAND = "Switchere Club"
TODAY = "2026-09-05"

# ---------- shared head / header / footer ----------
def head(title, desc, canonical, og_type="article"):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{canonical}" />
  <link rel="icon" href="/classroom.png" type="image/png" />
  <meta name="theme-color" content="#0e1420" />
  <meta property="og:type" content="{og_type}" />
  <meta property="og:site_name" content="{BRAND}" />
  <meta property="og:title" content="{html.escape(title)}" />
  <meta property="og:description" content="{html.escape(desc)}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{SITE}/images/social-preview.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:site" content="@switchereclub" />
  <meta name="twitter:title" content="{html.escape(title)}" />
  <meta name="twitter:description" content="{html.escape(desc)}" />
  <meta name="twitter:image" content="{SITE}/images/social-preview.png" />
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-64NJRHCT9P"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-64NJRHCT9P');</script>
  <link href="https://fonts.googleapis.com/css2?family=Bungee&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet" />
  <style>
    :root{{--bg:#0e1420;--panel:#151d2c;--card:#1a2334;--border:#263048;--txt:#e6e9ef;--muted:#8b96a8;--accent:#22c55e;--accent2:#4facfe;}}
    *{{margin:0;padding:0;box-sizing:border-box;}}
    body{{background:var(--bg);color:var(--txt);font-family:'Inter',system-ui,sans-serif;line-height:1.7;min-height:100vh;}}
    a{{color:inherit;text-decoration:none;}}
    .wrap{{max-width:1200px;margin:0 auto;padding:0 16px;}}
    header.site{{position:sticky;top:0;z-index:50;background:rgba(14,20,32,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--border);}}
    .nav{{display:flex;align-items:center;gap:14px;padding:12px 0;flex-wrap:wrap;}}
    .brand{{font-family:'Bungee',system-ui;font-size:1.25rem;color:#fff;letter-spacing:.5px;}}
    .brand span{{color:var(--accent);}}
    .nav-links{{display:flex;gap:6px;margin-left:auto;flex-wrap:wrap;}}
    .nav-links a{{padding:7px 13px;border-radius:9px;color:var(--muted);font-weight:600;font-size:.9rem;transition:.2s;}}
    .nav-links a:hover,.nav-links a.active{{background:var(--card);color:#fff;}}
    .page-head{{text-align:center;padding:46px 0 10px;}}
    .page-head h1{{font-size:clamp(1.8rem,4vw,2.6rem);font-weight:800;letter-spacing:-.5px;line-height:1.15;}}
    .page-head h1 .grad{{background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;background-clip:text;color:transparent;}}
    .page-head p{{color:var(--muted);max-width:680px;margin:12px auto 0;font-size:1.05rem;}}
    .ad-slot{{margin:16px auto;display:block;text-align:center;min-height:90px;border:none;background:transparent;}}
    .blog-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px;padding:20px 0 30px;}}
    .bcard{{display:flex;flex-direction:column;border-radius:14px;background:var(--card);border:1px solid var(--border);overflow:hidden;transition:.18s;}}
    .bcard:hover{{transform:translateY(-4px);border-color:var(--accent);box-shadow:0 12px 26px rgba(34,197,94,.15);}}
    .bcard .bcat{{font-size:.72rem;font-weight:700;letter-spacing:.6px;text-transform:uppercase;color:var(--accent);padding:16px 18px 0;}}
    .bcard h3{{font-size:1.12rem;font-weight:700;line-height:1.35;padding:8px 18px 0;}}
    .bcard h3 a:hover{{color:var(--accent);}}
    .bcard p{{color:var(--muted);font-size:.92rem;padding:8px 18px 0;flex:1;}}
    .bcard .bmeta{{color:var(--muted);font-size:.78rem;padding:10px 18px 0;}}
    .bcard .readmore{{display:inline-block;margin:14px 18px 18px;padding:9px 16px;border-radius:9px;background:var(--accent);color:#fff;font-weight:700;font-size:.88rem;align-self:flex-start;transition:.15s;}}
    .bcard .readmore:hover{{filter:brightness(1.1);}}
    .cat-bar{{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:18px 0 6px;}}
    .cat-bar a{{padding:7px 15px;border-radius:20px;background:var(--card);border:1px solid var(--border);color:var(--muted);font-weight:600;font-size:.85rem;transition:.15s;}}
    .cat-bar a:hover,.cat-bar a.active{{background:var(--accent);color:#fff;border-color:var(--accent);}}
    .search-wrap{{max-width:520px;margin:18px auto 4px;}}
    .search-wrap input{{width:100%;padding:12px 16px;border-radius:10px;border:1px solid var(--border);background:var(--card);color:var(--txt);font-size:.95rem;outline:none;}}
    .search-wrap input:focus{{border-color:var(--accent);}}
    .filter-row{{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:12px 0 4px;}}
    .filter-btn{{padding:7px 15px;border-radius:20px;background:var(--card);border:1px solid var(--border);color:var(--muted);font-weight:600;font-size:.85rem;cursor:pointer;transition:.15s;font-family:inherit;}}
    .filter-btn:hover,.filter-btn.active{{background:var(--accent);color:#fff;border-color:var(--accent);}}
    .no-results{{display:none;text-align:center;color:var(--muted);padding:30px 0;}}
    .article{{max-width:760px;margin:0 auto;padding:30px 0 40px;}}
    .article .crumb{{color:var(--muted);font-size:.85rem;margin-bottom:14px;}}
    .article .crumb a:hover{{color:var(--accent);}}
    .article h1{{font-size:clamp(1.7rem,4vw,2.4rem);font-weight:800;letter-spacing:-.5px;line-height:1.2;}}
    .article .ameta{{color:var(--muted);font-size:.85rem;margin:12px 0 6px;}}
    .article .acat{{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.6px;text-transform:uppercase;color:var(--accent);margin-bottom:10px;}}
    .article h2{{font-size:1.35rem;font-weight:700;margin:30px 0 10px;color:#fff;}}
    .article h3{{font-size:1.1rem;font-weight:700;margin:22px 0 8px;color:#fff;}}
    .article p{{margin:12px 0;color:var(--txt);}}
    .article ul,.article ol{{margin:12px 0 12px 22px;}}
    .article li{{margin:6px 0;}}
    .article strong{{color:#fff;}}
    .article .tip{{background:var(--card);border-left:3px solid var(--accent);border-radius:8px;padding:14px 16px;margin:16px 0;}}
    .article .tip strong{{color:var(--accent);}}
    .article .toc{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:16px 20px;margin:20px 0;}}
    .article .toc h3{{margin:0 0 8px;font-size:1rem;}}
    .article .toc a{{display:block;color:var(--muted);font-size:.9rem;padding:3px 0;}}
    .article .toc a:hover{{color:var(--accent);}}
    .article .related{{margin-top:34px;border-top:1px solid var(--border);padding-top:20px;}}
    .article .related h3{{margin-bottom:10px;}}
    .article .related a{{display:block;color:var(--accent);padding:4px 0;font-weight:600;}}
    .article .related a:hover{{text-decoration:underline;}}
    footer.site{{border-top:1px solid var(--border);margin-top:30px;padding:30px 0 20px;background:var(--panel);}}
    footer .cols{{display:flex;flex-wrap:wrap;gap:30px;justify-content:space-between;}}
    footer h4{{font-size:.95rem;margin-bottom:10px;color:#fff;}}
    footer a{{display:block;color:var(--muted);font-size:.9rem;padding:3px 0;}}
    footer a:hover{{color:var(--accent);}}
    .disclaimer{{color:var(--muted);font-size:.8rem;margin-top:20px;border-top:1px solid var(--border);padding-top:14px;}}
    .bcard .bimg{{width:100%;height:170px;object-fit:cover;display:block;background:var(--panel);}}
    .bcard .bimg-wrap{{position:relative;overflow:hidden;}}
    .bcard .bimg-wrap::after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 55%,rgba(14,20,32,.55));pointer-events:none;}}
    .bcard .bcat{{padding-top:14px;}}
    .bcard .bimg-wrap .bcat{{position:absolute;top:10px;left:12px;z-index:2;padding:4px 10px;border-radius:20px;background:rgba(14,20,32,.75);backdrop-filter:blur(4px);font-size:.68rem;font-weight:700;letter-spacing:.6px;text-transform:uppercase;color:var(--accent);}}
    .article .hero{{width:100%;max-height:420px;object-fit:cover;border-radius:14px;margin:18px 0 6px;display:block;border:1px solid var(--border);}}
    .article .fig{{margin:22px 0;}}
    .article .fig img{{width:100%;border-radius:12px;display:block;border:1px solid var(--border);}}
    .article .fig figcaption{{color:var(--muted);font-size:.8rem;margin-top:8px;text-align:center;}}
    .article .inbody{{margin:22px 0;}}
    .article .inbody img{{width:100%;border-radius:12px;display:block;border:1px solid var(--border);}}
    .article .inbody figcaption{{color:var(--muted);font-size:.8rem;margin-top:8px;text-align:center;}}
    .article a{{color:var(--accent2);}}
    .article a:hover{{text-decoration:underline;}}
    .backtop{{position:fixed;bottom:26px;right:26px;z-index:90;width:46px;height:46px;border-radius:50%;background:var(--accent);color:#fff;border:none;font-size:1.3rem;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 20px rgba(34,197,94,.35);opacity:0;visibility:hidden;transform:translateY(12px);transition:.25s;}}
    .backtop.show{{opacity:1;visibility:visible;transform:translateY(0);}}
    .backtop:hover{{filter:brightness(1.1);}}
    @keyframes fadeUp{{from{{opacity:0;transform:translateY(14px);}}to{{opacity:1;transform:translateY(0);}}}}
    .bcard{{animation:fadeUp .5s ease both;}}
    .bcard:hover{{transform:translateY(-6px);border-color:var(--accent);box-shadow:0 16px 34px rgba(34,197,94,.18);}}
    @media(max-width:600px){{.blog-grid{{grid-template-columns:1fr;}}}}
  </style>
</head>
"""

def header(active):
    links = [
        ("/", "Games", active == "games"),
        ("/tools.html", "Tools", active == "tools"),
        ("/security.html", "Security", active == "security"),
        ("/blogs.html", "Blogs", active == "blogs"),
        ("/privacypolicy.html", "Privacy", active == "privacy"),
    ]
    nav = "".join(
        '<a href="{}"{}>{}</a>'.format(href, ' class="active"' if act else "", label)
        for href, label, act in links
    )
    return f'<header class="site"><div class="wrap nav"><div class="brand">Switchere<span>Club</span></div><nav class="nav-links">{nav}</nav></div></header>'

def footer():
    return f"""<footer class="site"><div class="wrap">
    <div class="cols">
      <div><h4>Switchere Club</h4><a href="/">Free Online Games</a><a href="/tools.html">Free Online Tools</a><a href="/security.html">Security Tools</a><a href="/blogs.html">Blog &amp; Guides</a></div>
      <div><h4>Company</h4><a href="/privacypolicy.html">Privacy Policy</a><a href="/clearai.html">Support</a><a href="mailto:sales@lipon.pro.bd">Contact</a></div>
      <div><h4>Popular</h4><a href="/geometrydash.html">Geometry Dash</a><a href="/slope.html">Slope</a><a href="/moto-x3m.html">Moto X3M</a><a href="/amongus.html">Among Us</a></div>
    </div>
    <p class="disclaimer">We link to third-party games (we don't host them). Cookies &amp; ads keep Switchere Club free. <a href="/privacypolicy.html" style="display:inline;color:var(--accent);">Privacy Policy</a>.</p>
  </div></footer>
  <button class="backtop" id="backTop" aria-label="Back to top">&uarr;</button>
  <script>
    (function(){{
      var bt = document.getElementById('backTop');
      if (bt) {{
        window.addEventListener('scroll', function () {{
          if (window.scrollY > 300) bt.classList.add('show');
          else bt.classList.remove('show');
        }});
        bt.addEventListener('click', function () {{
          window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }});
      }}
    }})();
  </script>
  <script src="/ads.js"></script>
</body>
</html>"""

# ---------- category helpers ----------
def category_slug(cat):
    return cat.lower().replace(" ", "-")

def categories():
    seen = []
    for a in ARTICLES:
        if a["category"] not in seen:
            seen.append(a["category"])
    return seen

# ---------- build listing page ----------
def build_listing():
    cards = []
    for a in ARTICLES:
        cover = a.get("cover_image") or ""
        cover_html = ""
        if cover:
            cover_html = f'<div class="bimg-wrap"><img class="bimg" src="{cover}" alt="{html.escape(a["title"])}" loading="lazy" /><div class="bcat">{html.escape(a["category"])}</div></div>'
        else:
            cover_html = f'<div class="bcat">{html.escape(a["category"])}</div>'
        cards.append(f"""<article class="bcard" data-cat="{html.escape(a['category'])}" data-title="{html.escape(a['title'].lower())}" data-desc="{html.escape(a['description'].lower())}">
      {cover_html}
      <h3><a href="/blogs/{a["slug"]}.html">{html.escape(a["title"])}</a></h3>
      <p>{html.escape(a["description"])}</p>
      <div class="bmeta">{a["date"]} &middot; {a["read_time"]} min read</div>
      <a class="readmore" href="/blogs/{a['slug']}.html">Read More</a>
    </article>""")
    cat_links = "".join(
        f'<a href="/blogs/category/{category_slug(c)}.html">{html.escape(c)}</a>'
        for c in categories()
    )
    filter_btns = "".join(
        f'<button class="filter-btn" data-filter="{html.escape(c)}">{html.escape(c)}</button>'
        for c in categories()
    )
    body = f"""<main class="wrap">
    <section class="page-head">
      <h1>Blog &amp; <span class="grad">Gaming Guides</span></h1>
      <p>Tips, tricks, walkthroughs and honest guides for the games you love. Written by people who actually play them.</p>
    </section>
    <div class="cat-bar">{cat_links}</div>
    <div class="search-wrap"><input type="text" id="blogSearch" placeholder="Search articles, games, topics..." aria-label="Search articles" /></div>
    <div class="filter-row"><button class="filter-btn active" data-filter="all">All</button>{filter_btns}</div>
    <div class="ad-slot" data-adsterra data-key="8988dbb524d00a156bcd9b13090236d8" data-w="300" data-h="250" style="max-width:340px;margin-left:auto;margin-right:auto;"></div>
    <div class="blog-grid" id="blogGrid">
    {''.join(cards)}
    </div>
    <div class="no-results" id="noResults">No articles match your search. Try a different keyword or category.</div>
  </main>
  <script>
    (function(){{
      var grid = document.getElementById('blogGrid');
      var cards = Array.prototype.slice.call(grid.querySelectorAll('.bcard'));
      var search = document.getElementById('blogSearch');
      var noResults = document.getElementById('noResults');
      var activeCat = 'all';
      function apply() {{
        var q = (search.value || '').toLowerCase().trim();
        var shown = 0;
        cards.forEach(function (card) {{
          var cat = card.getAttribute('data-cat').toLowerCase();
          var title = card.getAttribute('data-title') || '';
          var desc = card.getAttribute('data-desc') || '';
          var matchCat = activeCat === 'all' || cat === activeCat.toLowerCase();
          var matchQ = !q || title.indexOf(q) !== -1 || desc.indexOf(q) !== -1 || cat.indexOf(q) !== -1;
          var show = matchCat && matchQ;
          card.style.display = show ? '' : 'none';
          if (show) shown++;
        }});
        noResults.style.display = shown ? 'none' : 'block';
      }}
      search.addEventListener('input', apply);
      var btns = document.querySelectorAll('.filter-btn');
      btns.forEach(function (btn) {{
        btn.addEventListener('click', function () {{
          btns.forEach(function (b) {{ b.classList.remove('active'); }});
          btn.classList.add('active');
          activeCat = btn.getAttribute('data-filter');
          apply();
        }});
      }});
    }})();
  </script>"""
    page = head(f"Blog &amp; Gaming Guides \u2014 {BRAND}",
                "Gaming tips, guides, walkthroughs and honest advice written by real players. Free, useful and easy to read.",
                f"{SITE}/blogs.html", og_type="website")
    page += header("blogs") + body + footer()
    return page

# ---------- build category page ----------
def build_category(cat):
    slug = category_slug(cat)
    cards = []
    for a in ARTICLES:
        if a["category"] != cat:
            continue
        cover = a.get("cover_image") or ""
        cover_html = ""
        if cover:
            cover_html = f'<div class="bimg-wrap"><img class="bimg" src="{cover}" alt="{html.escape(a["title"])}" loading="lazy" /><div class="bcat">{html.escape(a["category"])}</div></div>'
        else:
            cover_html = f'<div class="bcat">{html.escape(a["category"])}</div>'
        cards.append(f"""
            <article class="bcard">
      {cover_html}
      <h3><a href="/blogs/{a["slug"]}.html">{html.escape(a["title"])}</a></h3>
      <p>{html.escape(a["description"])}</p>
      <div class="bmeta">{a["date"]} &middot; {a["read_time"]} min read</div>
      <a class="readmore" href="/blogs/{a['slug']}.html">Read More</a>
    </article>""")
    cat_links = "".join(
        '<a href="/blogs/category/{}.html"{}>{}</a>'.format(
            category_slug(c), ' class="active"' if c == cat else "", html.escape(c)
        )
        for c in categories()
    )
    body = f"""<main class="wrap">
    <section class="page-head">
      <h1><span class="grad">{html.escape(cat)}</span></h1>
      <p>All {html.escape(cat)} articles on {BRAND}. Browse the full collection below.</p>
    </section>
    <div class="cat-bar">{cat_links}</div>
    <div class="ad-slot" data-adsterra data-key="8988aab52420d00a156bcd9b13090236d8" data-w="300" data-h="250" style="max-width:340px;margin-left:auto;margin-right:auto;"></div>
    <div class="blog-grid">
    {''.join(cards)}
    </div>
    <p style="text-align:center;margin:10px 0 30px;"><a href="/blogs.html" style="color:var(--accent);font-weight:600;">&larr; Back to all articles</a></p>
  </main>"""
    page = head(f"{html.escape(cat)} \u2014 {BRAND}",
                f"All {html.escape(cat)} articles on {BRAND}. Tips, guides and honest advice written by real players.",
                f"{SITE}/blogs/category/{slug}.html", og_type="website")
    page += header("blogs") + body + footer()
    return page

# ---------- build article page ----------
def build_article(a):
    related = [x for x in ARTICLES if x["category"] == a["category"] and x["slug"] != a["slug"]][:4]
    if len(related) < 3:
        for x in ARTICLES:
            if x["slug"] != a["slug"] and x not in related:
                related.append(x)
            if len(related) >= 3:
                break
    rel_html = "".join(f'<a href="/blogs/{r["slug"]}.html">{html.escape(r["title"])}</a>' for r in related[:3])
    # hero + in-body images
    hero_html = ""
    if a.get("cover_image"):
        hero_html = f'<img class="hero" src="{a["cover_image"]}" alt="{html.escape(a["title"])}" loading="lazy" />'
    inbody_html = ""
    for img in (a.get("images") or [])[:2]:
        inbody_html += f'<figure class="inbody"><img src="{img["url"]}" alt="{html.escape(img.get("alt", a["title"]))}" loading="lazy" /><figcaption>{html.escape(img.get("alt", ""))}</figcaption></figure>'
    # internal + external links block
    links_html = ""
    ints = a.get("internal_links") or []
    ext = a.get("external_link")
    if ints or ext:
        parts = []
        for target_slug, anchor in ints[:2]:
            parts.append(f'<a href="/blogs/{target_slug}.html">{html.escape(anchor)}</a>')
        if ext:
            parts.append(f'<a href="{ext}" target="_blank" rel="noopener nofollow">Learn more about this game</a>')
        links_html = '<div class="related"><h3>Related reading</h3>' + "".join(parts) + "</div>"
    schema = f"""<script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": {json.dumps(a["title"])},
  "description": {json.dumps(a["description"])},
  "datePublished": "{a['date']}T09:00:00+00:00",
  "dateModified": "{a['date']}T09:00:00+00:00",
  "author": {{"@type": "Organization", "name": "{BRAND}"}},
  "publisher": {{"@type": "Organization", "name": "{BRAND}"}},
  "mainEntityOfPage": "{SITE}/blogs/{a['slug']}.html"
}}</script>"""
    body = f"""
  <main class="wrap">
    <article class="article">
      <div class="crumb"><a href="/">Home</a> &rsaquo; <a href="/blogs.html">Blog</a> &rsaquo; {html.escape(a["category"])}</div>
      <div class="acat">{html.escape(a["category"])}</div>
      <h1>{html.escape(a["title"])}</h1>
      <div class="ameta">{a["date"]} &middot; {a["read_time"]} min read</div>
      {hero_html}
      <div class="ad-slot" data-adsterra data-key="793d8bb524d00a156bcd9b13090236d8" data-w="300" data-h="250" style="max-width:340px;margin:18px auto;"></div>
      {a["body"]}
      {inbody_html}
      {links_html}
      <div class="related">
        <h3>Keep reading</h3>
        {rel_html}
      </div>
    </article>
  </main>"""
    page = head(f'{a["title"]} \u2014 {BRAND}', a["description"], f"{SITE}/blogs/{a['slug']}.html")
    page += schema + header("blogs") + body + footer()
    return page

# ---------- main ----------
def main():
    global ARTICLES
    ARTICLES = enrich_all(ARTICLES)
    os.makedirs("blogs", exist_ok=True)
    os.makedirs("blogs/category", exist_ok=True)
    with open("blogs.html", "w") as f:
        f.write(build_listing())
    for a in ARTICLES:
        with open(f"blogs/{a['slug']}.html", "w") as f:
            f.write(build_article(a))
    for c in categories():
        with open(f"blogs/category/{category_slug(c)}.html", "w") as f:
            f.write(build_category(c))
    print(f"Generated blogs.html + {len(ARTICLES)} article pages + {len(categories())} category pages in blogs/")

if __name__ == "__main__":
    import json
    main()