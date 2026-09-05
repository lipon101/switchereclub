#!/usr/bin/env python3
# Regenerate all game pages with rich, natural, policy-safe SEO.
import json, re, os, html, datetime

with open("games.js","r") as f:
    js = f.read()
m = re.search(r'window\.GAME_CATALOG\s*=\s*(\[[\s\S]*\]);', js)
games = json.loads(m.group(1))

SITE = "https://lipon.pro.bd"
BRAND = "Switchere Club"
TODAY = datetime.date.today().isoformat()
PUB = "2025-10-01T09:00:00+00:00"

def slug_title(t):
    return t.strip()

def intro_for(title):
    t = html.escape(title)
    return (f"Play <strong>{t}</strong> online for free at {BRAND} — no download, no sign-up, "
            f"just instant browser gameplay. It's fast, fun, safe for all ages, and works right in your browser.")

def howto_for(title):
    t = html.escape(title)
    return (f"<strong>{t}</strong> loads instantly in your browser — just press play and go. "
            f"No installation or account needed. It works on desktop and mobile, so you can jump in anywhere.")

def faq_for(title):
    t = html.escape(title)
    return [
        {"q": f"Is {t} free to play?", "a": f"Yes — {t} is 100% free to play on {BRAND}. No download or sign-up is required."},
        {"q": f"Can I play {t} on mobile?", "a": f"Yes, {t} runs in your browser and works on both phone and desktop."},
        {"q": f"Do I need to install anything?", "a": f"No. {t} plays directly in your browser — no installation needed."},
    ]

def related(index, n=4):
    out = []
    i = 1
    while len(out) < n and i <= len(games):
        g = games[(index + i) % len(games)]
        if g["file"] != games[index]["file"]:
            out.append(g)
        i += 1
    return out

def img_or_none(g):
    imp = g.get("img") or ""
    return imp if imp else "images/social-preview.png"

def build_page(g, index):
    title = slug_title(g["title"])
    desc = (f"Play {title} free online at {BRAND}. Instant browser gameplay — no download, no sign-up. "
            f"Works on mobile & desktop. Safe for all ages.")
    file = g["file"]
    url = f"{SITE}/{file}"
    img = img_or_none(g)

    intro = intro_for(title)
    howto = howto_for(title)
    faqs = faq_for(title)
    rels = related(index, 4)

    # FAQPage JSON-LD
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{
            "@type": "Question",
            "name": f["q"],
            "acceptedAnswer": {"@type": "Answer", "text": f["a"]}
        } for f in faqs]
    }

    game_ld = {
        "@context": "https://schema.org",
        "@type": "VideoGame",
        "name": title,
        "url": url,
        "applicationCategory": "Game",
        "operatingSystem": "Web",
        "playMode": "SinglePlayer",
        "gamePlatform": "Web Browser",
        "inLanguage": "en",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "publisher": {"@type": "Organization", "name": BRAND, "url": SITE + "/"},
        "aggregateRating": None,  # no fake ratings
        "datePublished": PUB,
        "dateModified": PUB,
    }
    # remove None
    game_ld = {k:v for k,v in game_ld.items() if v is not None}

    breadcrumb_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
            {"@type":"ListItem","position":2,"name":"Games","item":SITE+"/"},
            {"@type":"ListItem","position":3,"name":title,"item":url},
        ]
    }

    rel_links = "".join(
        f'            <a class="rel-card" href="/{r["file"]}">{html.escape(r["title"])}</a>' for r in rels
    )

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — Play Free Online | {BRAND}</title>
  <meta name="description" content="{html.escape(desc)}" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <link rel="canonical" href="{url}" />
  <meta property="article:published_time" content="{PUB}" />
  <meta property="article:modified_time" content="{PUB}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="{BRAND}" />
  <meta property="og:title" content="{title} — Play Free Online at {BRAND}" />
  <meta property="og:description" content="{html.escape(desc)}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{SITE}/{img}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:site" content="@switchereclub" />
  <meta name="twitter:title" content="{title} — Play Free Online at {BRAND}" />
  <meta name="twitter:description" content="{html.escape(desc)}" />
  <meta name="twitter:image" content="{SITE}/{img}" />
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-64NJRHCT9P"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-64NJRHCT9P');</script>
  <script type="application/ld+json">{json.dumps(game_ld, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(breadcrumb_ld, ensure_ascii=False)}</script>
  <style>
    body, html {{ margin:0; padding:0; width:100%; background:#0e1420; font-family:'Inter',system-ui,sans-serif; color:#e6e9ef; }}
    #main-content {{ max-width:1100px; margin:0 auto; padding:10px 8px 30px; }}
    .topbar {{ display:flex; align-items:center; gap:12px; padding:6px 4px 12px; }}
    .brand {{ flex:1; font-weight:800; letter-spacing:-.5px; font-size:1.05rem; }}
    .brand a {{ color:#e6e9ef; text-decoration:none; }} .brand a span {{ color:#22c55e; }}
    .home-button {{ background:linear-gradient(135deg,#22c55e,#16a34a); color:#fff; border:none; padding:9px 16px; border-radius:9px; font-weight:700; cursor:pointer; font-size:.9rem; text-decoration:none; display:inline-block; }}
    .content {{ position:relative; width:100%; aspect-ratio:16/9; max-height:72vh; background:#000; border-radius:14px; overflow:hidden; border:1px solid #263048; }}
    iframe {{ width:100%; height:100%; border:none; display:block; }}
    .fullscreen-button {{ position:absolute; bottom:12px; right:12px; background:rgba(0,0,0,.55); color:#fff; border:1px solid rgba(255,255,255,.25); padding:8px 14px; border-radius:9px; cursor:pointer; font-size:.85rem; z-index:2; }}
    .fullscreen-button:hover {{ background:rgba(0,0,0,.75); }}
    h1 {{ font-size:1.5rem; margin:18px 4px 6px; color:#fff; letter-spacing:-.5px; }}
    .seo {{ margin:6px 4px 4px; color:#cbd2e0; font-size:.95rem; line-height:1.6; max-width:72ch; }}
    .seo p {{ margin:0 0 10px; }}
    .rel {{ margin:22px 4px 4px; }}
    .rel h2 {{ font-size:1.05rem; color:#fff; margin-bottom:10px; }}
    .rel-grid {{ display:flex; flex-wrap:wrap; gap:8px; }}
    .rel-card {{ background:var(--card,#1a2334); border:1px solid #263048; border-radius:10px; padding:10px 14px; color:#e6e9ef; text-decoration:none; font-size:.88rem; font-weight:600; transition:border-color .15s, transform .15s; }}
    .rel-card:hover {{ border-color:#22c55e; transform:translateY(-1px); }}
    .sc-adwrap {{ margin:16px auto 0; text-align:center; min-height:100px; }}
  </style>
</head>
<body>
  <div id="main-content">
    <div class="topbar">
      <div class="brand"><a href="/">Switchere<span>Club</span></a></div>
      <button class="home-button" onclick="goToHomePage()">Home</button>
    </div>
    <div class="content">
      <iframe id="gameFrame" src="{g["src"]}" allow="fullscreen; autoplay; gamepad" allowfullscreen onload="focusGame()" title="Play {title} online free"></iframe>
      <button class="fullscreen-button" onclick="toggleFullScreen()">⛶ Fullscreen</button>
    </div>
    <div class="sc-adwrap" data-adsterra data-key="793d8bb524d00a156bcd9b13090236d8" data-w="300" data-h="250" style="text-align:center;margin:16px auto 0;min-height:250px;"></div>
    <h1>{title}</h1>
    <div class="seo">
      <p>{intro}</p>
      <p>{howto}</p>
    </div>
    <div class="rel">
      <h2>More Free Games</h2>
      <div class="rel-grid">
{rel_links}
      </div>
    </div>
  </div>
  <script>
    function toggleFullScreen() {{
      var iframe = document.getElementById('gameFrame');
      if (iframe.requestFullscreen) iframe.requestFullscreen();
      else if (iframe.mozRequestFullScreen) iframe.mozRequestFullScreen();
      else if (iframe.webkitRequestFullscreen) iframe.webkitRequestFullscreen();
      else if (iframe.msRequestFullscreen) iframe.msRequestFullscreen();
      iframe.focus();
    }}
    function focusGame() {{ var i = document.getElementById('gameFrame'); if (i) i.focus(); }}
    function goToHomePage() {{ window.location.href = '/'; }}
  </script>
  <script src="/ads.js"></script>
</body>
</html>
'''

n = 0
for i, g in enumerate(games):
    try:
        page = build_page(g, i)
        with open(g["file"], "w") as f:
            f.write(page)
        n += 1
    except Exception as e:
        print("ERROR", g["file"], e)

print(f"Regenerated {n} game pages with SEO.")
