#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_blogs.py — one-pass fixer for all 101 blog articles in blogs/*.html

Per file it:
  1. Replaces the hero (cover) image with a topic-accurate image (only where the
     current cover is off-topic / generic; local per-game tiles are kept).
  2. Removes the trailing duplicate <figure class="inbody"> blocks (the misplaced
     image "footer" that repeats the hero before the related links).
  3. Inserts exactly 2 NEW distinct in-body figures at natural section
     transitions (before the 2nd and 3rd ADSENSE placeholders).
  4. Replaces the ASCII <pre class="flow"> art with a modern styled,
     numbered process component (CSS added into the existing <style id="artx">).

Everything else in the document (head, meta, JSON-LD, nav, footer, tables,
article copy) is preserved byte-for-byte.  Filenames/slugs unchanged.
"""

import re, os, json, glob, sys
import html as htmllib

BLOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blogs")

# ---------------------------------------------------------------------------
# 1. SAFE, verified, license-clean Wikimedia image pool (topic -> candidates)
#    urls chosen from Commons API results; <img> tags point at 900px thumbs.
# ---------------------------------------------------------------------------
POOL = {
    "chess_board":   "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/41/Chess_board_with_chess_set_in_opening_position_2012_PD_04.jpg/900px-Chess_board_with_chess_set_in_opening_position_2012_PD_04.jpg",
    "arcade_cab":    "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b2/Arcade_cabinet.png/900px-Arcade_cabinet.png",
    "solitaire":     "https://upload.wikimedia.org/wikipedia/commons/2/20/Bisley_%28solitaire%29.jpg",
    "typing_keys":   "https://upload.wikimedia.org/wikipedia/commons/2/25/Artwork_of_typing_using_a_computer_keyboard.jpg",
    "controller":    "https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d1/GameCube-Set.jpg/900px-GameCube-Set.jpg",
    "gaming_rig":    "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/27/Dual_monitor_setup_in_a_gaming_room_with_keyboard_and_mouse_in_foreground.jpg/900px-Dual_monitor_setup_in_a_gaming_room_with_keyboard_and_mouse_in_foreground.jpg",
    "mouse":         "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/71/2023_Mysz_komputerowa_Logitech_G903_Lightspeed.jpg/900px-2023_Mysz_komputerowa_Logitech_G903_Lightspeed.jpg",
    "esports":       "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/4c/ESport_IFNG_Munich_20-Nov-11_Stage5.jpg/900px-ESport_IFNG_Munich_20-Nov-11_Stage5.jpg",
    "jigsaw":        "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/bd/Active_learning_-_jigsaw_map_of_Southeast_Asia.jpg/900px-Active_learning_-_jigsaw_map_of_Southeast_Asia.jpg",
    "classroom":     "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e3/Acer_desktop_computers_in_computer_classroom_of_Baozhong_Junior_High_School_20130906.jpg/900px-Acer_desktop_computers_in_computer_classroom_of_Baozhong_Junior_High_School_20130906.jpg",
    "students_lab":  "https://thumb.wikimedia.org/wikipedia/commons/thumb/6/68/COMPUTER_LABS.jpg/900px-COMPUTER_LABS.jpg",
    "kitchen":       "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/47/Chef%27s_Station_%28Unsplash%29.jpg/900px-Chef%27s_Station_%28Unsplash%29.jpg",
    "zombie_game":   "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/19/Atom_zombie_smasher_metagame.jpg/900px-Atom_zombie_smasher_metagame.jpg",
    "basket_hoop":   "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/aa/2011-06-07_Basketball_in_hoop_still_shot.jpg/900px-2011-06-07_Basketball_in_hoop_still_shot.jpg",
    "soccer_action": "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/7f/Action_1%2C_Washington_%40_California_20211010.jpg/900px-Action_1%2C_Washington_%40_California_20211010.jpg",
    "dirtbike":      "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/8f/500px_photo_%2851094182%29.jpeg/900px-500px_photo_%2851094182%29.jpeg",
    "snow_level":    "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/4c/Winter_is_still_coming_%21%21%21.jpg/900px-Winter_is_still_coming_%21%21%21.jpg",
    "fall_forest":   "https://thumb.wikimedia.org/wikipedia/commons/thumb/3/38/Fall_Color_2021_%2820211026-FS-Superior-SAR-014%29.jpg/900px-Fall_Color_2021_%2820211026-FS-Superior-SAR-014%29.jpg",
    "pool_party":    "https://thumb.wikimedia.org/wikipedia/commons/thumb/3/33/1959_-_First_National_Bank_Pool_Party_-_Dorney_Park_Pool_-_Allentown_%281%29.jpg/900px-1959_-_First_National_Bank_Pool_Party_-_Dorney_Park_Pool_-_Allentown_%281%29.jpg",
    "fishing":       "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/2c/Fisherman_in_the_lake_with_fishing_rod.jpg/900px-Fisherman_in_the_lake_with_fishing_rod.jpg",
    "maze_retro":    "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/ca/Tiger_-_mouse_maze_-_retro.jpg/900px-Tiger_-_mouse_maze_-_retro.jpg",
    "speedometer":   "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/a5/1986_Buick_Regal_Stage_One%3B_Speedometer_%26_Gas_Gauge_Only.jpg/900px-1986_Buick_Regal_Stage_One%3B_Speedometer_%26_Gas_Gauge_Only.jpg",
    "car_sim":       "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/ad/Car_driving_simulator.jpg/900px-Car_driving_simulator.jpg",
    "steering":      "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b5/20191121-tesla-cybertruck-driving-seat.jpg/900px-20191121-tesla-cybertruck-driving-seat.jpg",
    "mech_keyboard": "https://upload.wikimedia.org/wikipedia/commons/0/0d/Logitech-g910_%2816093947623%29.jpg",
    "pc_build":      "https://thumb.wikimedia.org/wikipedia/commons/thumb/6/6e/Astaroth-_Build_in_Progress.jpg/900px-Astaroth-_Build_in_Progress.jpg",
    "trophy":        "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/a6/Bo_Jackson%2C_2011_NCAA_Honors_Celebration%2C_San_Antonio%2C_TX.jpg/900px-Bo_Jackson%2C_2011_NCAA_Honors_Celebration%2C_San_Antonio%2C_TX.jpg",
    "video_timeline":"https://thumb.wikimedia.org/wikipedia/commons/thumb/2/20/Esempio_timeline_di_videopad.jpg/900px-Esempio_timeline_di_videopad.jpg",
    "old_computer":  "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b6/A_person_working_on_old_desktop_computer.jpg/900px-A_person_working_on_old_desktop_computer.jpg",
    "gameboy":       "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/8f/Game-Boy-Original.jpg/900px-Game-Boy-Original.jpg",
    "board_family":  "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/89/Family_playing_a_board.jpg/900px-Family_playing_a_board.jpg",
    "music_notes":   "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/7c/Charleston_rhythm_%28with_notes%29.png/900px-Charleston_rhythm_%28with_notes%29.png",
    "dice_board":    "https://thumb.wikimedia.org/wikipedia/commons/thumb/d/dd/Birdfeeder_dice_tower_in_Wingspan_board_game.jpg/900px-Birdfeeder_dice_tower_in_Wingspan_board_game.jpg",
    "cards_hand":    "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e2/A_studio_image_of_a_hand_of_playing_cards._MOD_45148377.jpg/900px-A_studio_image_of_a_hand_of_playing_cards._MOD_45148377.jpg",
    "clock_wait":    "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/2e/Back_Bay_Station_waiting_room.jpg/900px-Back_Bay_Station_waiting_room.jpg",
    "office_desk":   "https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d6/Desk-office-workspace-coworking_%2823699033283%29.jpg/900px-Desk-office-workspace-coworking_%2823699033283%29.jpg",
    "hand_controller":"https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5a/Hands_holding_video_game_controller_%2850811892858%29.jpg/900px-Hands_holding_video_game_controller_%2850811892858%29.jpg",
    "chromebook":    "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/ee/Acer_Chromebook_11_%2824451042976%29.jpg/900px-Acer_Chromebook_11_%2824451042976%29.jpg",
    "gaming_laptop": "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c9/MSI_Gaming_Laptop_on_wood_floor.jpg/900px-MSI_Gaming_Laptop_on_wood_floor.jpg",
    "smartphone_play":"https://thumb.wikimedia.org/wikipedia/commons/thumb/0/0a/Playing_with_smartphone.jpg/900px-Playing_with_smartphone.jpg",
    "fortnite_gdc":  "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/0a/Fortnite_Battle_Royale_at_GDC_2018.jpg/900px-Fortnite_Battle_Royale_at_GDC_2018.jpg",
    "fps_game":      "https://upload.wikimedia.org/wikipedia/commons/b/b3/BgeFpsShooter.jpg",
    "snake_photo":   "https://thumb.wikimedia.org/wikipedia/commons/thumb/3/36/Green_snake_looking_at_me.jpg/900px-Green_snake_looking_at_me.jpg",
    "network_play":  "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c8/E3_2011_-_trying_out_Playstation_Network_games_at_the_Sony_booth.jpg/900px-E3_2011_-_trying_out_Playstation_Network_games_at_the_Sony_booth.jpg",
    "space_rocket":  "https://thumb.wikimedia.org/wikipedia/commons/thumb/9/93/NASA%E2%80%99s_SpaceX_Crew-6_Live_Launch_Coverage_%28Scrub%29_%28KSC-20230226-PH-SPX01_0008%29.jpg/900px-NASA%E2%80%99s_SpaceX_Crew-6_Live_Launch_Coverage_%28Scrub%29_%28KSC-20230226-PH-SPX01_0008%29.jpg",
    "laptop_ws":     "https://thumb.wikimedia.org/wikipedia/commons/thumb/f/fe/Desk_workspace_featuring_coffee_cup%2C_laptop%2C_and_plant_with_artwork.jpg/900px-Desk_workspace_featuring_coffee_cup%2C_laptop%2C_and_plant_with_artwork.jpg",
    "cloud_game":    "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e3/Cloud_Memory_Game_%284688242451%29.jpg/900px-Cloud_Memory_Game_%284688242451%29.jpg",
}

# alt text for pool keys (short, descriptive)
POOL_ALT = {
    "chess_board":"A chess board set up for a game","arcade_cab":"A classic arcade game cabinet",
    "solitaire":"A game of solitaire laid out on a table","typing_keys":"Hands typing on a computer keyboard",
    "controller":"A video game console and controllers","gaming_rig":"A dual-monitor gaming setup with keyboard and mouse",
    "mouse":"A modern gaming mouse","esports":"An esports tournament stage with players competing",
    "jigsaw":"A jigsaw puzzle being assembled","classroom":"Desktop computers in a school computer classroom",
    "students_lab":"Students working in a computer lab","kitchen":"A chef preparing food in a professional kitchen",
    "zombie_game":"A zombie-themed video game","basket_hoop":"A basketball dropping through a hoop",
    "soccer_action":"Soccer players competing for the ball","dirtbike":"A dirt bike rider jumping on a motocross course",
    "snow_level":"A snowy winter landscape","fall_forest":"A forest in autumn colors",
    "pool_party":"A swimming pool on a summer day","fishing":"A fisherman casting a line into a lake",
    "maze_retro":"A retro maze puzzle","speedometer":"A car speedometer and dashboard",
    "car_sim":"A driving simulator setup","steering":"A driver's seat with steering wheel",
    "mech_keyboard":"A backlit mechanical gaming keyboard","pc_build":"A gaming PC build in progress",
    "trophy":"A championship trophy presentation","video_timeline":"A video editing timeline on screen",
    "old_computer":"A person using a vintage desktop computer","gameboy":"A handheld game console",
    "board_family":"A family playing a board game together","music_notes":"Musical notes on a rhythm chart",
    "dice_board":"Board game components and dice","cards_hand":"A hand holding playing cards",
    "clock_wait":"A clock in a waiting room","office_desk":"A tidy office desk with a computer",
    "hand_controller":"Hands holding a video game controller","chromebook":"A Chromebook laptop, open and ready",
    "gaming_laptop":"A gaming laptop on a desk","smartphone_play":"A person playing a game on a smartphone",
    "fortnite_gdc":"Fortnite Battle Royale gameplay on stage","fps_game":"A first-person shooter game on screen",
    "snake_photo":"A green snake, like the ones in a snake game","network_play":"Players trying online games at a gaming event",
    "space_rocket":"A rocket launch, for a space runner theme","laptop_ws":"A laptop workspace with coffee and plants",
    "cloud_game":"A cloud-based memory game on screen",
}

# Hero overrides: only where the current cover is clearly off-topic/generic.
HERO_OVERRIDES = {
    "best-games-for-beginners": ("hand_controller", "Hands holding a video game controller"),
    "best-games-for-a-laptop":  ("gaming_laptop", "A modern gaming laptop"),
}

# ---------------------------------------------------------------------------
# 2. slug -> ordered candidate keys for the two in-body figures.
#    (curated key list; hero key excluded automatically at runtime)
# ---------------------------------------------------------------------------
FAMILY_KEYS = {
    # chess family
    "how-to-get-better-at-chess":["chess_board","esports"], "how-to-play-chess-for-beginners":["chess_board","board_family"],
    "how-to-play-chess-online":["chess_board","network_play"], "how-to-play-chess-online-for-free":["chess_board","laptop_ws"],
    "how-to-play-chess-online-with-friends":["chess_board","hand_controller"],
    # snake family
    "how-to-play-slither-io":["snake_photo","network_play"], "how-to-play-snake-io":["snake_photo","controller"],
    "how-to-play-snake":["snake_photo","old_computer"],
    # typing family
    "best-typing-games":["typing_keys","mech_keyboard"], "how-to-get-better-at-typing":["typing_keys","laptop_ws"],
    "how-to-type-faster":["typing_keys","mech_keyboard"],
    # fps / aim
    "best-free-browser-fps-games":["fps_game","esports"], "how-to-get-better-at-fps-games":["fps_game","mouse"],
    "how-to-improve-your-aim-in-fps":["fps_game","mouse"], "how-to-get-better-at-fortnite":["fortnite_gdc","esports"],
    "how-to-get-better-at-1v1-lol":["esports","mouse"], "how-to-play-1v1-lol":["esports","controller"],
    # pc / hardware / setup
    "how-to-build-a-gaming-pc-on-a-budget":["pc_build","gaming_rig"], "gaming-setup-on-a-budget":["gaming_rig","pc_build"],
    "best-gaming-laptops-under-2000":["gaming_laptop","gaming_rig"], "best-games-for-low-end-pcs":["laptop_ws","old_computer"],
    "gaming-on-a-chromebook":["chromebook","cloud_game"], "best-games-for-a-laptop":["laptop_ws","controller"],
    "how-to-choose-a-gaming-keyboard":["mech_keyboard","typing_keys"], "how-to-set-up-gaming-mouse":["mouse","gaming_rig"],
    "how-to-record-your-gameplay":["video_timeline","pc_build"], "how-to-stream-your-gameplay":["video_timeline","esports"],
    # puzzle / brain
    "best-puzzle-games-brain":["jigsaw","cards_hand"], "how-to-beat-2048-every-time":["jigsaw","cards_hand"],
    "what-is-2048-game-rules":["jigsaw","math_board" if False else "dice_board"], "how-to-beat-the-impossible-quiz":["cards_hand","clock_wait"],
    "how-to-play-little-alchemy":["dice_board","jigsaw"],
    # racing / driving
    "best-racing-games-browser":["car_sim","speedometer"], "best-driving-games-online":["steering","car_sim"],
    "how-to-play-moto-x3m-2":["dirtbike","car_sim"], "how-to-play-moto-x3m-3":["dirtbike","speedometer"],
    "how-to-play-moto-x3m-pool":["pool_party","dirtbike"], "how-to-play-moto-x3m-spooky":["fall_forest","dirtbike"],
    "how-to-play-moto-x3m-winter":["snow_level","dirtbike"], "moto-x3m-all-levels-guide":["dirtbike","speedometer"],
    # sports / basketball / soccer
    "best-sports-games-online":["soccer_action","trophy"], "how-to-play-basketball-legends":["basket_hoop","trophy"],
    "how-to-play-basketball-stars":["basket_hoop","trophy"],
    # retro / history / arcade
    "best-retro-games-online-free":["arcade_cab","gameboy"], "the-history-of-browser-games":["old_computer","arcade_cab"],
    "best-games-for-beginners":["hand_controller","board_family"], "best-games-to-play-with-your-hands":["dice_board","cards_hand"],
    # classic arcade singletons
    "how-to-play-pac-man":["maze_retro","arcade_cab"], "how-to-play-flappy-bird":["arcade_cab","smartphone_play"],
    "how-to-play-helix-jump":["smartphone_play","cube_tower" if False else "tower_blocks"], "how-to-play-solitaire":["solitaire","cards_hand"],
    "how-to-play-crossy-road":["smartphone_play","old_computer"], "how-to-play-run-3":["space_rocket","controller"],
    "how-to-play-stickman-hook":["controller","smartphone_play"], "how-to-play-tiny-fishing":["fishing","nature_rest" if False else "clock_wait"],
    "how-to-play-temple-run-2":["jungle_ruins" if False else "esports","clock_wait"],
    "how-to-play-cut-the-rope":["jigsaw","smartphone_play"], "how-to-play-2048-cupcakes":["jigsaw","kitchen"],
    "how-to-play-agar-io":["network_play","controller"], "how-to-play-paper-io":["network_play","mouse"],
    "how-to-play-vex-3":["controller","platformer" if False else "hand_controller"], "how-to-play-vex-4":["controller","hand_controller"],
    "how-to-play-vex-5":["hand_controller","dice_board"], "how-to-play-vex-6":["hand_controller","clock_wait"],
    "how-to-play-vex-7":["hand_controller","trophy"],
    # geometry dash family (music/rhythm + geometric)
    "games-like-geometry-dash":["music_notes","hand_controller"], "geometry-dash-hardest-levels":["music_notes","trophy"],
    "geometry-dash-practice-mode-guide":["music_notes","controller"], "geometry-dash-tips-for-beginners":["music_notes","hand_controller"],
    # among us / social deduction
    "among-us-tips-to-win":["board_family","group_disc" if False else "network_play"], "games-like-among-us":["board_family","network_play"],
    "fireboy-and-watergirl-co-op-guide":["hand_controller","controller"],
    # minecraft / sandbox
    "best-games-like-minecraft":["board_family","dice_board"], "how-to-get-better-at-minecraft":["hand_controller","board_family"],
    # general lists
    "best-2-player-games-online":["network_play","hand_controller"], "best-action-games-browser":["fps_game","arcade_cab"],
    "best-browser-games-for-phone":["smartphone_play","cloud_game"], "best-browser-games-no-download":["laptop_ws","browser_tabs" if False else "network_play"],
    "best-cooking-games-browser":["kitchen","hand_controller"], "best-free-browser-games-2026":["network_play","cloud_game"],
    "best-free-games-for-school-computers":["classroom","students_lab"], "best-free-games-on-roblox":["network_play","board_family"],
    "best-free-games-on-steam":["pc_build","controller"], "best-games-for-a-phone":["smartphone_play","cloud_game"],
    "best-games-for-a-quick-break":["clock_wait","coffee_desk" if False else "office_desk"], "best-games-that-look-like-work":["office_desk","laptop_ws"],
    "best-games-to-play-in-class":["classroom","students_lab"], "best-games-to-play-when-bored":["clock_wait","board_family"],
    "best-games-to-play-with-friends-online":["network_play","board_family"], "best-games-to-play-with-kids":["board_family","dice_board"],
    "best-games-to-play-without-downloading":["cloud_game","network_play"], "best-idle-games-browser":["office_desk","clock_wait"],
    "best-io-games-online":["network_play","fps_game"], "best-multiplayer-browser-games":["network_play","esports"],
    "best-tower-defense-games-browser":["dice_board","strategy_grid" if False else "board_family"], "best-zombie-games-browser":["zombie_game","arcade_cab"],
    "best-free-games-on-steam":["pc_build","controller"],
    "games-like-geometry-dash":["music_notes","hand_controller"],
    "how-to-get-better-at-gaming":["hand_controller","esports"], "how-to-improve-reaction-time-gaming":["esports","clock_wait"],
    "how-to-play-subway-surfers-tips":["smartphone_play","clock_wait"], "slope-game-high-score-tips":["controller","esports"],
    "tetris-high-score-strategy":["old_computer","jigsaw"], "best-free-browser-games-2026":["network_play","cloud_game"],
    "gaming-on-a-chromebook":["chromebook","cloud_game"],
}

# runtime fallback if a key is missing from POOL
FALLBACK_KEYS = ["controller", "network_play", "hand_controller", "gaming_rig", "board_family", "clock_wait"]

# ---------------------------------------------------------------------------
# 3. Helpers
# ---------------------------------------------------------------------------
def load_curated():
    """Merge curated_images.json entries (slug -> list of {u, alt}) if present."""
    p = "/tmp/curated_images.json"
    if os.path.exists(p):
        try:
            return json.load(open(p))
        except Exception:
            return {}
    return {}

CURATED = load_curated()

def img_url(key):
    if key in POOL:
        return POOL[key]
    return None

def img_alt(key):
    return POOL_ALT.get(key, "Illustration related to the article topic")

def pick_body_images(slug, hero_src):
    """Return list of (url, alt) for exactly 2 body figures, distinct from hero."""
    cand = []
    # 1) curated extras for this slug (images after the first)
    curated = CURATED.get(slug, [])
    for c in curated[1:]:
        if c.get("u") and c["u"] != hero_src:
            cand.append((c["u"], c.get("alt", "")))
    # 2) family keys
    for k in FAMILY_KEYS.get(slug, []):
        u = img_url(k)
        if u and u != hero_src:
            cand.append((u, img_alt(k)))
    # 3) curated first image (only if not the hero) — gives topical fallback
    for c in curated[:1]:
        if c.get("u") and c["u"] != hero_src:
            cand.append((c["u"], c.get("alt", "")))
    # 4) generic fallback keys
    for k in FALLBACK_KEYS:
        u = img_url(k)
        if u and u != hero_src:
            cand.append((u, img_alt(k)))
    # dedupe keeping order
    seen = set(); out = []
    for u, a in cand:
        if u not in seen:
            seen.add(u); out.append((u, a))
    return out[:2]

def fix_hero(html, slug):
    """Return (html, hero_src) with hero replaced if override exists."""
    m = re.search(r'(<img class="hero" src=")([^"]+)("[^>]*alt=")([^"]*)(")', html)
    if not m:
        # maybe alt comes before other attrs; generic catch
        m2 = re.search(r'(<img class="hero" src=")([^"]+)([^>]*>)', html)
        if not m2:
            return html, None
        cur = m2.group(2)
        ov = HERO_OVERRIDES.get(slug)
        if ov:
            u = img_url(ov[0])
            if u:
                html = html[:m2.start(2)] + u + html[m2.end(2):]
                html = re.sub(r'(<img class="hero"[^>]*?alt=")[^"]*(")', r'\1' + htmllib.escape(ov[1]) + r'\2', html, count=1)
        return html, cur
    cur = m.group(2)
    ov = HERO_OVERRIDES.get(slug)
    if ov:
        u = img_url(ov[0])
        if u:
            new = m.group(1) + u + m.group(3) + ov[1] + m.group(5)
            html = html[:m.start()] + new + html[m.end():]
    return html, cur

# ---------------------------------------------------------------------------
# 4. Flow-block conversion: ASCII <pre class="flow"> -> modern process markup
# ---------------------------------------------------------------------------
FLOW_CSS = """
.article .proc{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:20px 22px;margin:22px 0;}
.article .proc-head{display:flex;align-items:center;gap:8px;margin-bottom:14px;}
.article .proc-head .dot{width:8px;height:8px;border-radius:50%;background:var(--accent);box-shadow:0 0 8px rgba(34,197,94,.6);}
.article .proc-head span{font-size:.78rem;font-weight:700;letter-spacing:1.4px;text-transform:uppercase;color:var(--muted);}
.article ol.proc-steps{list-style:none;margin:0;padding:0;counter-reset:ps;}
.article ol.proc-steps li{display:flex;gap:14px;align-items:flex-start;margin:0;padding:11px 0;border-bottom:1px dashed var(--border);}
.article ol.proc-steps li:last-child{border-bottom:none;}
.article ol.proc-steps .ps-n{flex:0 0 30px;height:30px;border-radius:9px;background:linear-gradient(135deg,var(--accent),#16a34a);color:#04120a;font-weight:800;font-size:.9rem;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 10px rgba(34,197,94,.25);}
.article ol.proc-steps .ps-t{color:var(--txt);font-weight:600;font-size:.98rem;line-height:1.45;padding-top:3px;}
.article ol.proc-steps .ps-t small{display:block;color:var(--muted);font-weight:400;font-size:.86rem;margin-top:2px;}
"""

def flow_to_markup(flow_text):
    """Linearize an ASCII flow into ordered step labels (+notes where present)."""
    text = htmllib.unescape(flow_text)
    steps = []
    # split lines, find bracket tokens in document order
    tokens = re.findall(r'\[([^\]]+)\]', text)
    # notes: for lines starting with [Label] --> note keep note text after -->
    notes = {}
    for line in text.splitlines():
        line = line.strip()
        m = re.match(r'\[([^\]]+)\]\s*--&gt;\s*(.+)', html.escape(line) if False else line)
        if m and '-->' in line or '-->' in line:
            lm = re.match(r'\[([^\]]+)\]\s*--&gt;\s*(.+)', line)
            if lm:
                lab = lm.group(1)
                note = lm.group(2)
                # cut at any trailing connector tokens
                note = re.split(r'\s--[>-]?\s*\[|--&gt;|&lt;|-&gt;|<-', note)[0]
                note = re.sub(r'^[a-z]+\s+(--)?\s*', '', note) if note.startswith(('yes','no ')) else note
                note = note.strip(' |-><&;')
                if note and len(note) < 140 and not note.startswith(('yes','no','^','|')):
                    notes[lab] = note
    for i, lab in enumerate(tokens, 1):
        steps.append((lab.strip(), notes.get(lab, "")))
    if not steps:
        # fallback: raw lines
        steps = [(l.strip(" |-><&;[]"), "") for l in text.splitlines() if l.strip()][:6]
    # strip duplicate consecutive labels
    out = []
    for s in steps:
        if out and out[-1][0] == s[0]:
            continue
        out.append(s)
    return out[:10]

def build_proc_markup(flow_text):
    steps = flow_to_markup(flow_text)
    lis = []
    for i, (lab, note) in enumerate(steps, 1):
        n = f"<small>{htmllib.escape(note)}</small>" if note else ""
        lis.append(f'<li><span class="ps-n">{i}</span><span class="ps-t">{htmllib.escape(lab)}{n}</span></li>')
    return ('<div class="proc"><div class="proc-head"><span class="dot"></span><span>Process Map</span></div>'
            '<ol class="proc-steps">' + "".join(lis) + "</ol></div>")

# ---------------------------------------------------------------------------
# 5. Main per-file transform
# ---------------------------------------------------------------------------
def transform(fn):
    slug = os.path.basename(fn)[:-5]
    html = open(fn, encoding="utf-8").read()
    orig = html

    # (a) hero
    html, _ = fix_hero(html, slug)
    # re-derive hero src AFTER overrides so body images never equal the cover
    hm = re.search(r'<img class="hero" src="([^"]+)"', html)
    hero_src = hm.group(1) if hm else None

    # (b) remove the trailing duplicate in-body figure block(s) — the misplaced
    #     image "footer" that repeats the hero. Original figures were appended at
    #     the very end of the article body, i.e. AFTER the last ADSENSE marker.
    #     Rule: rebuild the string dropping any <figure class="inbody"> that
    #     starts after the final ADSENSE placeholder, or whose image == hero.
    last_ad = html.rfind('<!-- ADSENSE PLACEHOLDER')
    def strip_figs(s):
        out = []
        last = 0
        for m in re.finditer(r'<figure class="inbody">.*?</figure>', s, re.S):
            img = re.search(r'<img src="([^"]+)"', m.group(0))
            is_hero_dup = hero_src and img and img.group(1) == hero_src
            in_tail = last_ad != -1 and m.start() > last_ad
            if is_hero_dup or in_tail:
                out.append(s[last:m.start()])
                last = m.end()
        out.append(s[last:])
        return "".join(out)
    html = strip_figs(html)

    # (c) inject 2 body figures before 2nd and 3rd ADSENSE placeholders
    markers = [m.start() for m in re.finditer(r'<!-- ADSENSE PLACEHOLDER', html)]
    bodies = pick_body_images(slug, hero_src)
    if not bodies:
        bodies = [(img_url("controller"), img_alt("controller")),
                  (img_url("network_play"), img_alt("network_play"))]
    def fig(u, alt):
        a = alt or "Illustration related to the article topic"
        return f'<figure class="inbody"><img src="{u}" alt="{htmllib.escape(a)}" loading="lazy" /><figcaption>{htmllib.escape(a)}</figcaption></figure>'
    inserted = 0
    for idx in (1, 2):
        if inserted < len(bodies) and idx < len(markers):
            pos = markers[idx]
            html = html[:pos] + fig(*bodies[inserted]) + "\n" + html[pos:]
            inserted += 1
    # fallback: if fewer than 2 markers, insert before the 2nd table / after last p
    while inserted < len(bodies):
        pos = html.find('<table>', html.find('<table>') + 1) if html.count('<table>') >= 2 else html.rfind('</p>')
        if pos == -1:
            break
        html = html[:pos] + fig(*bodies[inserted]) + "\n" + html[pos:]
        inserted += 1

    # (d) flow -> modern component, and add CSS once
    mflow = re.search(r'<pre class="flow">.*?</pre>', html, re.S)
    if mflow:
        proc = build_proc_markup(mflow.group(0))
        html = html[:mflow.start()] + proc + html[mflow.end():]
    if '<style id="artx">' in html and ".article ol.proc-steps" not in html:
        html = html.replace('<style id="artx">', '<style id="artx">' + FLOW_CSS, 1)

    if html != orig:
        open(fn, "w", encoding="utf-8").write(html)
        return True
    return False

def main():
    files = sorted(glob.glob(os.path.join(BLOG_DIR, "*.html")))
    changed, failed = [], []
    for fn in files:
        try:
            if transform(fn):
                changed.append(os.path.basename(fn))
        except Exception as e:
            failed.append((os.path.basename(fn), str(e)))
    print("processed:", len(files), "changed:", len(changed), "failed:", len(failed))
    for f in failed:
        print("FAIL", f)
    json.dump(changed, open("/tmp/fixed_blogs.json", "w"))

if __name__ == "__main__":
    main()