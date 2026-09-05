#!/usr/bin/env python3
# Loads real, verified Wikimedia Commons image URLs from image_map.json (fetched via the
# Commons API), with curated overrides for the handful of topics where the API returned
# irrelevant results. Each entry: slug -> list of (url, alt); first is the cover.
import json, os

_OVERRIDES = {
    "how-to-play-subway-surfers-tips": [
        ("https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e0/Man_at_Dundas_subway_station%2C_Toronto%2C_2008-05-06.jpg/960px-Man_at_Dundas_subway_station%2C_Toronto%2C_2008-05-06.jpg", "A subway station, like the tracks in Subway Surfers"),
    ],
    "how-to-play-slither-io": [
        ("https://thumb.wikimedia.org/wikipedia/commons/thumb/3/36/Green_snake_looking_at_me.jpg/960px-Green_snake_looking_at_me.jpg", "A green snake, like the ones in Slither.io"),
    ],
    "how-to-improve-your-aim-in-fps": [
        ("https://upload.wikimedia.org/wikipedia/commons/b/b3/BgeFpsShooter.jpg", "A first-person shooter game"),
        ("https://thumb.wikimedia.org/wikipedia/commons/thumb/1/1d/Computer_mouse_1_2015-02-28.JPG/960px-Computer_mouse_1_2015-02-28.JPG", "A computer mouse for aiming"),
    ],
    "how-to-record-your-gameplay": [
        ("https://thumb.wikimedia.org/wikipedia/commons/thumb/7/7f/Google_Stadia_Cloud-gaming_%2848605895992%29.jpg/960px-Google_Stadia_Cloud-gaming_%2848605895992%29.jpg", "Recording gameplay on screen"),
    ],
    "how-to-build-a-gaming-pc-on-a-budget": [
        ("https://thumb.wikimedia.org/wikipedia/commons/thumb/3/31/Gaming_PC-Setup_-_Astaroth-_The_Completed_System.jpg/960px-Gaming_PC-Setup_-_Astaroth-_The_Completed_System.jpg", "A complete gaming PC setup"),
    ],
    "best-games-for-beginners": [
        ("https://thumb.wikimedia.org/wikipedia/commons/thumb/1/11/Drawing_for_beginners_%281920%29_%2814750197431%29.jpg/960px-Drawing_for_beginners_%281920%29_%2814750197431%29.jpg", "Learning something new"),
    ],
}

# alt text for the real API results (slug -> list of alt strings, aligned to image order)
_ALTS = {
    "best-free-browser-games-2026": ["A classic browser game", "Freeciv, a free browser strategy game"],
    "best-2-player-games-online": ["Two players at a LAN party", "Multiplayer game development"],
    "best-idle-games-browser": ["Idle game character sprite sheet"],
    "best-puzzle-games-brain": ["A jigsaw puzzle in progress", "Puzzle pieces being assembled"],
    "best-racing-games-browser": ["Racing cars on a track"],
    "best-sports-games-online": ["An esports tournament"],
    "best-action-games-browser": ["An action game logo"],
    "best-io-games-online": ["Surviv.io, a popular .io game"],
    "how-to-get-better-at-gaming": ["Hands holding a game controller", "A modern game controller"],
    "best-typing-games": ["A backlit keyboard for typing", "Fingers on a keyboard"],
    "best-multiplayer-browser-games": ["A multiplayer gaming event"],
    "best-tower-defense-games-browser": ["A tower defense game grid"],
    "best-zombie-games-browser": ["A zombie from a video game"],
    "best-cooking-games-browser": ["Cooking rice in a kitchen"],
    "best-driving-games-online": ["Driving a racing car"],
    "best-free-games-for-school-computers": ["A school computer classroom"],
    "best-games-to-play-with-friends-online": ["Friends playing video games together"],
    "gaming-setup-on-a-budget": ["A complete gaming PC setup", "A console gaming setup"],
    "best-games-to-play-when-bored": ["A bored person"],
    "how-to-type-faster": ["Typing on a keyboard"],
    "best-games-for-low-end-pcs": ["A laptop keyboard"],
    "best-browser-games-for-phone": ["Playing a game on a smartphone"],
    "best-free-browser-fps-games": ["A first-person shooter game"],
    "how-to-get-better-at-fps-games": ["A first-person shooter game"],
    "best-games-that-look-like-work": ["A home office with a computer"],
    "best-retro-games-online-free": ["A retro arcade console"],
    "how-to-improve-reaction-time-gaming": ["Reaction time stages diagram"],
    "best-games-to-play-with-kids": ["Children playing video games"],
    "how-to-play-solitaire": ["A solitaire card game"],
    "how-to-set-up-gaming-mouse": ["A Logitech gaming mouse"],
    "best-browser-games-no-download": ["A browser game screenshot"],
    "how-to-play-agar-io": ["Agar.io gameplay"],
    "best-gaming-laptops-under-2000": ["A gaming laptop"],
    "the-history-of-browser-games": ["The Computer History Museum"],
    "how-to-stream-your-gameplay": ["Cloud gaming"],
    "best-free-games-on-steam": ["A game on Steam"],
    "how-to-choose-a-gaming-keyboard": ["A backlit gaming keyboard"],
    "gaming-on-a-chromebook": ["A Chromebook laptop"],
    "best-free-games-on-roblox": ["The Roblox logo"],
    "how-to-get-better-at-fortnite": ["Fortnite Battle Royale"],
    "best-games-for-a-quick-break": ["A coffee break"],
    "best-games-like-minecraft": ["Minecraft lush caves"],
    "best-games-to-play-without-downloading": ["A browser game"],
    "best-games-to-play-in-class": ["Students in a classroom"],
    "how-to-get-better-at-typing": ["A keyboard for typing practice"],
    "best-games-for-a-laptop": ["A laptop computer"],
    "best-games-to-play-with-your-hands": ["A hand game"],
    "best-games-for-a-phone": ["A smartphone"],
}

def load_wm():
    """Return slug -> list of (url, alt) built from image_map.json + overrides."""
    wm = {}
    path = os.path.join(os.path.dirname(__file__), "image_map.json")
    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
        for slug, results in data.items():
            if slug in _OVERRIDES:
                continue
            alts = _ALTS.get(slug, [])
            picks = []
            for i, (title, url) in enumerate(results[:2]):
                if url.startswith("ERR"):
                    continue
                alt = alts[i] if i < len(alts) else title.split(":")[-1].strip()
                picks.append((url, alt))
            if picks:
                wm[slug] = picks
    wm.update(_OVERRIDES)
    return wm

WM = load_wm()