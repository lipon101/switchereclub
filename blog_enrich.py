#!/usr/bin/env python3
# Enrichment module: adds cover images, in-body images, and internal/external links
# to every article. Imported by gen_blogs.py so regeneration is deterministic.
# Data sources: accurate local game images (/images) + curated Wikimedia Commons URLs.

# ---------- 1. Local game images (accurate, same-origin) ----------
LOCAL = {
 'geometry-dash-tips-for-beginners':'geometrydash.png','slope-game-high-score-tips':'slope.png',
 'moto-x3m-all-levels-guide':'motox3m.png','what-is-2048-game-rules':'2048.png',
 'among-us-tips-to-win':'amongus.png','geometry-dash-hardest-levels':'geometrydash.png',
 'how-to-play-1v1-lol':'1v1.lol.png','how-to-get-better-at-1v1-lol':'1v1.lol.png',
 'how-to-beat-2048-every-time':'2048.png','geometry-dash-practice-mode-guide':'geometrydash.png',
 'how-to-play-chess-online':'chess.png','how-to-beat-the-impossible-quiz':'theimpossiblequiz.png',
 'tetris-high-score-strategy':'tetris.png','how-to-play-pac-man':'pacman.png',
 'how-to-get-better-at-minecraft':'minecraft.png','fireboy-and-watergirl-co-op-guide':'fireboyandwatergirl.png',
 'games-like-geometry-dash':'geometrydash.png','how-to-play-flappy-bird':'flappybird.png',
 'how-to-play-snake':'googlesnake.png','games-like-among-us':'amongus.png',
 'how-to-play-temple-run-2':'templerun2.png','how-to-play-crossy-road':'crossyroad.png',
 'how-to-play-helix-jump':'helixjump.png','how-to-play-cut-the-rope':'cuttherope.png',
 'how-to-play-snake-io':'snakeio.png','how-to-play-paper-io':'paper.io2.png',
 'how-to-play-run-3':'run3.png','how-to-play-stickman-hook':'stickmanhook.png',
 'how-to-play-little-alchemy':'littlealchemy.png','how-to-play-tiny-fishing':'tinyfishing.png',
 'how-to-play-2048-cupcakes':'2048cupcake.png','how-to-play-basketball-legends':'basketballlegends.png',
 'how-to-play-basketball-stars':'basketballstars.png','how-to-play-vex-3':'vex3.png',
 'how-to-play-vex-4':'vex4.png','how-to-play-vex-5':'vex5.png','how-to-play-vex-6':'vex6.png',
 'how-to-play-vex-7':'vex7.png','how-to-play-moto-x3m-2':'motox3m2.png',
 'how-to-play-moto-x3m-3':'motox3m3.png','how-to-play-moto-x3m-pool':'motox3mpool.jpg',
 'how-to-play-moto-x3m-spooky':'moto3mspooky.jpeg','how-to-play-moto-x3m-winter':'motox3mwinter.jpeg',
 'best-games-like-minecraft':'minecraft.png','how-to-get-better-at-chess':'chess.png',
 'how-to-play-chess-online-with-friends':'chess.png','how-to-play-chess-for-beginners':'chess.png',
 'how-to-play-chess-online-for-free':'chess.png',
}

# ---------- 2. Curated Wikimedia Commons picks (real verified URLs) ----------
from blog_images import WM

# ---------- 3. External authoritative links (slug/title keyword -> URL) ----------
EXTERNAL = {
    "geometry-dash": "https://en.wikipedia.org/wiki/Geometry_Dash",
    "slope": "https://slope-game.io/",
    "moto-x3m": "https://poki.com/en/g/moto-x3m",
    "2048": "https://en.wikipedia.org/wiki/2048_(video_game)",
    "among-us": "https://en.wikipedia.org/wiki/Among_Us",
    "1v1-lol": "https://1v1.lol/",
    "tetris": "https://en.wikipedia.org/wiki/Tetris",
    "pac-man": "https://en.wikipedia.org/wiki/Pac-Man",
    "minecraft": "https://en.wikipedia.org/wiki/Minecraft",
    "fireboy": "https://en.wikipedia.org/wiki/Fireboy_and_Watergirl",
    "flappy-bird": "https://en.wikipedia.org/wiki/Flappy_Bird",
    "snake": "https://en.wikipedia.org/wiki/Snake_(video_game_genre)",
    "chess": "https://en.wikipedia.org/wiki/Chess",
    "temple-run": "https://en.wikipedia.org/wiki/Temple_Run",
    "crossy-road": "https://en.wikipedia.org/wiki/Crossy_Road",
    "helix-jump": "https://www.helixjump.io/",
    "cut-the-rope": "https://en.wikipedia.org/wiki/Cut_the_Rope",
    "agar": "https://en.wikipedia.org/wiki/Agar.io",
    "slither": "https://en.wikipedia.org/wiki/Slither.io",
    "vex": "https://www.vex4.io/",
    "subway-surfers": "https://en.wikipedia.org/wiki/Subway_Surfers",
    "fortnite": "https://en.wikipedia.org/wiki/Fortnite",
    "roblox": "https://en.wikipedia.org/wiki/Roblox",
    "steam": "https://en.wikipedia.org/wiki/Steam_(service)",
    "solitaire": "https://en.wikipedia.org/wiki/Klondike_(solitaire)",
    "basketball": "https://en.wikipedia.org/wiki/Basketball",
    "gaming-pc": "https://en.wikipedia.org/wiki/Gaming_computer",
    "gaming-laptop": "https://en.wikipedia.org/wiki/Gaming_laptop",
    "gaming-keyboard": "https://en.wikipedia.org/wiki/Computer_keyboard",
    "gaming-mouse": "https://en.wikipedia.org/wiki/Computer_mouse",
    "chromebook": "https://en.wikipedia.org/wiki/Chromebook",
    "stream": "https://en.wikipedia.org/wiki/Video_game_live_streaming",
    "esports": "https://en.wikipedia.org/wiki/Esports",
    "browser-games": "https://en.wikipedia.org/wiki/Browser_game",
    "reaction-time": "https://en.wikipedia.org/wiki/Mental_chronometry",
    "typing": "https://en.wikipedia.org/wiki/Typing",
    "fps": "https://en.wikipedia.org/wiki/First-person_shooter",
    "retro": "https://en.wikipedia.org/wiki/Retro_gaming",
    "puzzle": "https://en.wikipedia.org/wiki/Puzzle_video_game",
    "idle": "https://en.wikipedia.org/wiki/Incremental_game",
    "tower-defense": "https://en.wikipedia.org/wiki/Tower_defense",
    "io-games": "https://en.wikipedia.org/wiki/.io_games",
    "zombie": "https://en.wikipedia.org/wiki/Zombie_(fiction)",
    "cooking": "https://en.wikipedia.org/wiki/Cooking",
    "racing": "https://en.wikipedia.org/wiki/Racing_video_game",
    "sports": "https://en.wikipedia.org/wiki/Sports_video_game",
    "action": "https://en.wikipedia.org/wiki/Action_game",
    "multiplayer": "https://en.wikipedia.org/wiki/Multiplayer_video_game",
    "2-player": "https://en.wikipedia.org/wiki/Multiplayer_video_game",
    "kids": "https://en.wikipedia.org/wiki/Children%27s_game",
    "low-end": "https://en.wikipedia.org/wiki/Computer",
    "phone": "https://en.wikipedia.org/wiki/Mobile_game",
    "laptop": "https://en.wikipedia.org/wiki/Laptop",
    "work": "https://en.wikipedia.org/wiki/Office",
    "bored": "https://en.wikipedia.org/wiki/Boredom",
    "quick-break": "https://en.wikipedia.org/wiki/Break_(work)",
    "hands": "https://en.wikipedia.org/wiki/Hand_game",
    "class": "https://en.wikipedia.org/wiki/Classroom",
    "friends": "https://en.wikipedia.org/wiki/Friendship",
    "school": "https://en.wikipedia.org/wiki/School",
    "record": "https://en.wikipedia.org/wiki/Screen_recording",
    "aim": "https://en.wikipedia.org/wiki/First-person_shooter",
    "gaming": "https://en.wikipedia.org/wiki/Video_game",
    "history": "https://en.wikipedia.org/wiki/History_of_video_games",
    "stickman": "https://en.wikipedia.org/wiki/Stick_figure",
    "run-3": "https://run3.io/",
    "paper-io": "https://en.wikipedia.org/wiki/Paper.io",
    "snake-io": "https://en.wikipedia.org/wiki/Snake.io",
    "impossible-quiz": "https://en.wikipedia.org/wiki/The_Impossible_Quiz",
    "little-alchemy": "https://littlealchemy.com/",
    "tiny-fishing": "https://en.wikipedia.org/wiki/Fishing",
    "2048-cupcakes": "https://en.wikipedia.org/wiki/2048_(video_game)",
    "basketball-legends": "https://en.wikipedia.org/wiki/Basketball",
    "basketball-stars": "https://en.wikipedia.org/wiki/Basketball",
    "vex-3": "https://en.wikipedia.org/wiki/Vex_(video_game)",
    "vex-4": "https://en.wikipedia.org/wiki/Vex_(video_game)",
    "vex-5": "https://en.wikipedia.org/wiki/Vex_(video_game)",
    "vex-6": "https://en.wikipedia.org/wiki/Vex_(video_game)",
    "vex-7": "https://en.wikipedia.org/wiki/Vex_(video_game)",
    "moto-x3m-2": "https://en.wikipedia.org/wiki/Moto_X3M",
    "moto-x3m-3": "https://en.wikipedia.org/wiki/Moto_X3M",
    "moto-x3m-pool": "https://en.wikipedia.org/wiki/Moto_X3M",
    "moto-x3m-spooky": "https://en.wikipedia.org/wiki/Moto_X3M",
    "moto-x3m-winter": "https://en.wikipedia.org/wiki/Moto_X3M",
    "temple-run-2": "https://en.wikipedia.org/wiki/Temple_Run",
    "crossy-road": "https://en.wikipedia.org/wiki/Crossy_Road",
    "helix-jump": "https://www.helixjump.io/",
    "cut-the-rope": "https://en.wikipedia.org/wiki/Cut_the_Rope",
    "agar-io": "https://en.wikipedia.org/wiki/Agar.io",
    "slither-io": "https://en.wikipedia.org/wiki/Slither.io",
    "snake-io": "https://en.wikipedia.org/wiki/Snake.io",
    "paper-io": "https://en.wikipedia.org/wiki/Paper.io",
    "run-3": "https://run3.io/",
    "stickman-hook": "https://en.wikipedia.org/wiki/Stick_figure",
    "little-alchemy": "https://littlealchemy.com/",
    "tiny-fishing": "https://en.wikipedia.org/wiki/Fishing",
    "2048-cupcakes": "https://en.wikipedia.org/wiki/2048_(video_game)",
    "basketball-legends": "https://en.wikipedia.org/wiki/Basketball",
    "basketball-stars": "https://en.wikipedia.org/wiki/Basketball",
    "vex-3": "https://en.wikipedia.org/wiki/Vex_(video_game)",
    "vex-4": "https://en.wikipedia.org/wiki/Vex_(video_game)",
    "vex-5": "https://en.wikipedia.org/wiki/Vex_(video_game)",
    "vex-6": "https://en.wikipedia.org/wiki/Vex_(video_game)",
    "vex-7": "https://en.wikipedia.org/wiki/Vex_(video_game)",
    "moto-x3m-2": "https://en.wikipedia.org/wiki/Moto_X3M",
    "moto-x3m-3": "https://en.wikipedia.org/wiki/Moto_X3M",
    "moto-x3m-pool": "https://en.wikipedia.org/wiki/Moto_X3M",
    "moto-x3m-spooky": "https://en.wikipedia.org/wiki/Moto_X3M",
    "moto-x3m-winter": "https://en.wikipedia.org/wiki/Moto_X3M",
}

# ---------- 4. Internal links: keyword -> (target slug, anchor text) ----------
INTERNAL = {
    "geometry dash": ("geometry-dash-tips-for-beginners", "our Geometry Dash guide"),
    "slope": ("slope-game-high-score-tips", "our Slope high-score guide"),
    "2048": ("how-to-beat-2048-every-time", "our 2048 strategy guide"),
    "among us": ("among-us-tips-to-win", "our Among Us tips"),
    "1v1.lol": ("how-to-play-1v1-lol", "our 1v1.LOL guide"),
    "tetris": ("tetris-high-score-strategy", "our Tetris strategy guide"),
    "pac-man": ("how-to-play-pac-man", "our Pac-Man guide"),
    "minecraft": ("how-to-get-better-at-minecraft", "our Minecraft tips"),
    "fireboy": ("fireboy-and-watergirl-co-op-guide", "our Fireboy and Watergirl guide"),
    "flappy bird": ("how-to-play-flappy-bird", "our Flappy Bird guide"),
    "snake": ("how-to-play-snake", "our Snake guide"),
    "chess": ("how-to-play-chess-online", "our chess guide"),
    "temple run": ("how-to-play-temple-run-2", "our Temple Run 2 guide"),
    "crossy road": ("how-to-play-crossy-road", "our Crossy Road guide"),
    "helix jump": ("how-to-play-helix-jump", "our Helix Jump guide"),
    "cut the rope": ("how-to-play-cut-the-rope", "our Cut the Rope guide"),
    "agar.io": ("how-to-play-agar-io", "our Agar.io guide"),
    "slither.io": ("how-to-play-slither-io", "our Slither.io guide"),
    "vex": ("how-to-play-vex-3", "our Vex guide"),
    "moto x3m": ("moto-x3m-all-levels-guide", "our Moto X3M guide"),
    "subway surfers": ("how-to-play-subway-surfers-tips", "our Subway Surfers guide"),
    "fortnite": ("how-to-get-better-at-fortnite", "our Fortnite guide"),
    "roblox": ("best-free-games-on-roblox", "our Roblox game list"),
    "steam": ("best-free-games-on-steam", "our free Steam games list"),
    "solitaire": ("how-to-play-solitaire", "our Solitaire guide"),
    "basketball": ("how-to-play-basketball-legends", "our basketball game guide"),
    "browser games": ("best-browser-games-no-download", "our no-download browser games list"),
    "fps": ("best-free-browser-fps-games", "our free browser FPS list"),
    "typing": ("how-to-type-faster", "our typing guide"),
    "reaction time": ("how-to-improve-reaction-time-gaming", "our reaction time guide"),
    "gaming setup": ("gaming-setup-on-a-budget", "our budget gaming setup guide"),
    "gaming pc": ("how-to-build-a-gaming-pc-on-a-budget", "our budget gaming PC guide"),
    "gaming laptop": ("best-gaming-laptops-under-2000", "our gaming laptop guide"),
    "gaming keyboard": ("how-to-choose-a-gaming-keyboard", "our gaming keyboard guide"),
    "gaming mouse": ("how-to-set-up-gaming-mouse", "our gaming mouse guide"),
    "chromebook": ("gaming-on-a-chromebook", "our Chromebook gaming guide"),
    "stream": ("how-to-stream-your-gameplay", "our streaming guide"),
    "record": ("how-to-record-your-gameplay", "our recording guide"),
    "aim": ("how-to-improve-your-aim-in-fps", "our aim guide"),
    "2-player": ("best-2-player-games-online", "our 2-player games list"),
    "multiplayer": ("best-multiplayer-browser-games", "our multiplayer browser games list"),
    "kids": ("best-games-to-play-with-kids", "our games for kids list"),
    "low-end": ("best-games-for-low-end-pcs", "our low-end PC games list"),
    "phone": ("best-browser-games-for-phone", "our phone browser games list"),
    "laptop": ("best-games-for-a-laptop", "our laptop games list"),
    "retro": ("best-retro-games-online-free", "our retro games list"),
    "tower defense": ("best-tower-defense-games-browser", "our tower defense games list"),
    "racing": ("best-racing-games-browser", "our racing games list"),
    "sports": ("best-sports-games-online", "our sports games list"),
    "action": ("best-action-games-browser", "our action games list"),
    "zombie": ("best-zombie-games-browser", "our zombie games list"),
    "cooking": ("best-cooking-games-browser", "our cooking games list"),
    "driving": ("best-driving-games-online", "our driving games list"),
    "puzzle": ("best-puzzle-games-brain", "our puzzle games list"),
    "idle": ("best-idle-games-browser", "our idle games list"),
    "io games": ("best-io-games-online", "our .io games list"),
    "school": ("best-free-games-for-school-computers", "our school computer games list"),
    "friends": ("best-games-to-play-with-friends-online", "our games to play with friends list"),
    "bored": ("best-games-to-play-when-bored", "our games when bored list"),
    "quick break": ("best-games-for-a-quick-break", "our quick break games list"),
    "work": ("best-games-that-look-like-work", "our games that look like work list"),
    "beginners": ("best-games-for-beginners", "our beginner games list"),
    "class": ("best-games-to-play-in-class", "our games to play in class list"),
    "hands": ("best-games-to-play-with-your-hands", "our hand games list"),
    "without downloading": ("best-browser-games-no-download", "our no-download games list"),
    "like minecraft": ("best-games-like-minecraft", "our games like Minecraft list"),
    "like among us": ("games-like-among-us", "our games like Among Us list"),
    "like geometry dash": ("games-like-geometry-dash", "our games like Geometry Dash list"),
    "impossible quiz": ("how-to-beat-the-impossible-quiz", "our Impossible Quiz guide"),
    "stickman": ("how-to-play-stickman-hook", "our Stickman Hook guide"),
    "run 3": ("how-to-play-run-3", "our Run 3 guide"),
    "paper.io": ("how-to-play-paper-io", "our Paper.io guide"),
    "snake.io": ("how-to-play-snake-io", "our Snake.io guide"),
    "little alchemy": ("how-to-play-little-alchemy", "our Little Alchemy guide"),
    "tiny fishing": ("how-to-play-tiny-fishing", "our Tiny Fishing guide"),
    "2048 cupcakes": ("how-to-play-2048-cupcakes", "our 2048 Cupcakes guide"),
    "basketball legends": ("how-to-play-basketball-legends", "our Basketball Legends guide"),
    "basketball stars": ("how-to-play-basketball-stars", "our Basketball Stars guide"),
    "vex 3": ("how-to-play-vex-3", "our Vex 3 guide"),
    "vex 4": ("how-to-play-vex-4", "our Vex 4 guide"),
    "vex 5": ("how-to-play-vex-5", "our Vex 5 guide"),
    "vex 6": ("how-to-play-vex-6", "our Vex 6 guide"),
    "vex 7": ("how-to-play-vex-7", "our Vex 7 guide"),
    "moto x3m 2": ("how-to-play-moto-x3m-2", "our Moto X3M 2 guide"),
    "moto x3m 3": ("how-to-play-moto-x3m-3", "our Moto X3M 3 guide"),
    "moto x3m pool": ("how-to-play-moto-x3m-pool", "our Moto X3M Pool Party guide"),
    "moto x3m spooky": ("how-to-play-moto-x3m-spooky", "our Moto X3M Spooky Land guide"),
    "moto x3m winter": ("how-to-play-moto-x3m-winter", "our Moto X3M Winter guide"),
    "temple run 2": ("how-to-play-temple-run-2", "our Temple Run 2 guide"),
    "crossy road": ("how-to-play-crossy-road", "our Crossy Road guide"),
    "helix jump": ("how-to-play-helix-jump", "our Helix Jump guide"),
    "cut the rope": ("how-to-play-cut-the-rope", "our Cut the Rope guide"),
    "agar.io": ("how-to-play-agar-io", "our Agar.io guide"),
    "slither.io": ("how-to-play-slither-io", "our Slither.io guide"),
    "snake.io": ("how-to-play-snake-io", "our Snake.io guide"),
    "paper.io": ("how-to-play-paper-io", "our Paper.io guide"),
    "run 3": ("how-to-play-run-3", "our Run 3 guide"),
    "stickman hook": ("how-to-play-stickman-hook", "our Stickman Hook guide"),
    "little alchemy": ("how-to-play-little-alchemy", "our Little Alchemy guide"),
    "tiny fishing": ("how-to-play-tiny-fishing", "our Tiny Fishing guide"),
    "2048 cupcakes": ("how-to-play-2048-cupcakes", "our 2048 Cupcakes guide"),
    "basketball legends": ("how-to-play-basketball-legends", "our Basketball Legends guide"),
    "basketball stars": ("how-to-play-basketball-stars", "our Basketball Stars guide"),
    "vex 3": ("how-to-play-vex-3", "our Vex 3 guide"),
    "vex 4": ("how-to-play-vex-4", "our Vex 4 guide"),
    "vex 5": ("how-to-play-vex-5", "our Vex 5 guide"),
    "vex 6": ("how-to-play-vex-6", "our Vex 6 guide"),
    "vex 7": ("how-to-play-vex-7", "our Vex 7 guide"),
    "moto x3m 2": ("how-to-play-moto-x3m-2", "our Moto X3M 2 guide"),
    "moto x3m 3": ("how-to-play-moto-x3m-3", "our Moto X3M 3 guide"),
    "moto x3m pool": ("how-to-play-moto-x3m-pool", "our Moto X3M Pool Party guide"),
    "moto x3m spooky": ("how-to-play-moto-x3m-spooky", "our Moto X3M Spooky Land guide"),
    "moto x3m winter": ("how-to-play-moto-x3m-winter", "our Moto X3M Winter guide"),
}

def pick_external(slug, title):
    t = title.lower()
    for key, url in EXTERNAL.items():
        if key in slug or key in t:
            return url
    return None

def pick_internal(slug, title):
    t = title.lower()
    found = []
    for key, (target_slug, anchor) in INTERNAL.items():
        if target_slug == slug:
            continue
        if key in t or key in slug:
            found.append((target_slug, anchor))
        if len(found) >= 2:
            break
    return found

# Category-based fallback internal links so every article gets 2 internal links
CATEGORY_FALLBACK = {
    "Guides": [
        ("how-to-get-better-at-gaming", "our guide to getting better at gaming"),
        ("how-to-improve-reaction-time-gaming", "our reaction time guide"),
    ],
    "Game Lists": [
        ("best-browser-games-no-download", "our no-download browser games list"),
        ("best-games-for-a-quick-break", "our quick break games list"),
    ],
    "Gaming Culture": [
        ("the-history-of-browser-games", "the history of browser games"),
        ("best-free-browser-games-2026", "the best free browser games of 2026"),
    ],
}

def pick_internal_full(slug, title, category):
    found = pick_internal(slug, title)
    if len(found) >= 2:
        return found
    for target_slug, anchor in CATEGORY_FALLBACK.get(category, []):
        if target_slug == slug:
            continue
        if not any(t == target_slug for t, _ in found):
            found.append((target_slug, anchor))
        if len(found) >= 2:
            break
    return found

def enrich(a):
    """Return a copy of article `a` with cover_image, images, external_link, internal_links added."""
    a = dict(a)
    slug = a["slug"]
    cover = None
    images = []
    if slug in LOCAL:
        cover = f"/images/{LOCAL[slug]}"
        images.append({"url": f"/images/{LOCAL[slug]}", "alt": a["title"]})
    if slug in WM:
        if not cover:
            cover = WM[slug][0][0]
        for url, alt in WM[slug][1:3]:
            images.append({"url": url, "alt": alt})
    if not images and slug in WM:
        images.append({"url": WM[slug][0][0], "alt": WM[slug][0][1]})
    if len(images) < 2 and slug in WM:
        for url, alt in WM[slug]:
            if len(images) >= 2:
                break
            if not any(i["url"] == url for i in images):
                images.append({"url": url, "alt": alt})
    if cover:
        a["cover_image"] = cover
    if images:
        a["images"] = images[:2]
    ext = pick_external(slug, a["title"])
    if ext:
        a["external_link"] = ext
    ints = pick_internal_full(slug, a["title"], a.get("category", ""))
    if ints:
        a["internal_links"] = ints
    return a

def enrich_all(articles):
    return [enrich(a) for a in articles]