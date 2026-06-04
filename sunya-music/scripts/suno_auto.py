#!/usr/bin/env python3
"""
suno_auto.py — automates Suno song generation using pyautogui.

HOW TO USE:
1. Open Chrome → go to https://suno.com/create
2. Click "Advanced" button to switch to custom mode
3. Make sure the Style field and Lyrics field are visible
4. Minimize VSCode / Claude
5. Run: python sunya-music/scripts/suno_auto.py
6. DON'T touch mouse/keyboard while running
7. After each generation, it waits ~3 min then downloads both variants

SETUP (first time only):
- Run with --calibrate to click on each field and save positions
  python sunya-music/scripts/suno_auto.py --calibrate
"""

import pyautogui
import pyperclip
import time
import sys
import os
import json
import re

pyautogui.FAILSAFE = True  # Move mouse to top-left corner to abort
pyautogui.PAUSE = 0.3

SCRIPT_DIR  = os.path.dirname(__file__)
BASE_DIR    = os.path.join(SCRIPT_DIR, "..")
MD_FILE     = os.path.join(BASE_DIR, "SUNO_ALL_BHAJANS.md")
CONFIG_FILE = os.path.join(SCRIPT_DIR, "suno_positions.json")
PROGRESS_FILE = os.path.join(SCRIPT_DIR, "suno_progress.json")

WAIT_GENERATE  = 180  # seconds to wait for generation (3 min)
WAIT_DOWNLOAD  = 5    # seconds between actions


def load_config():
    if not os.path.exists(CONFIG_FILE):
        print("ERROR: No calibration file found. Run with --calibrate first.")
        sys.exit(1)
    with open(CONFIG_FILE) as f:
        return json.load(f)


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    print(f"Saved positions to {CONFIG_FILE}")


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"last_completed": -1}


def save_progress(idx):
    with open(PROGRESS_FILE, "w") as f:
        json.dump({"last_completed": idx}, f)


def parse_songs(md_file):
    """Parse SUNO_ALL_BHAJANS.md into list of (name, style, lyrics) tuples."""
    with open(md_file, encoding="utf-8") as f:
        content = f.read()

    songs = []
    # Split by song headers
    blocks = re.split(r'---\n## .+? SONG \d+ — (\w+_\d+)', content)

    # Re-parse properly
    pattern = re.compile(
        r'##\s+\w+ SONG \d+ — (\w+)\s*\n\s*STYLE:\s*\n(.+?)\n\s*LYRICS:\s*\n(.+?)(?=\n---|\Z)',
        re.DOTALL
    )

    for m in pattern.finditer(content):
        name   = m.group(1).strip()
        style  = m.group(2).strip()
        lyrics = m.group(3).strip()
        songs.append((name, style, lyrics))

    return songs


def calibrate():
    """Interactive calibration — click on each UI element to record positions."""
    config = {}
    print("\n=== SUNO CALIBRATION ===")
    print("Make sure Suno is open in Advanced/Custom mode.")
    print("You have 5 seconds after each prompt to click the target.\n")

    targets = [
        ("style_field",   "Click INSIDE the STYLE field"),
        ("lyrics_field",  "Click INSIDE the LYRICS field"),
        ("create_button", "Click the CREATE button"),
        ("download_btn1", "Click the DOWNLOAD button on the FIRST generated song"),
        ("download_btn2", "Click the DOWNLOAD button on the SECOND generated song"),
    ]

    for key, instruction in targets:
        print(f"\n{instruction}")
        print("Moving mouse in 3 seconds...")
        for i in range(3, 0, -1):
            print(f"  {i}...")
            time.sleep(1)
        print("  MOVE YOUR MOUSE NOW — recording in 5 seconds")
        time.sleep(5)
        x, y = pyautogui.position()
        config[key] = [x, y]
        print(f"  Recorded: ({x}, {y})")

    save_config(config)
    print("\nCalibration complete! Now run without --calibrate to start generating.")


def clear_field(x, y):
    """Click field and select all + delete."""
    pyautogui.click(x, y)
    time.sleep(0.3)
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.2)
    pyautogui.press("delete")
    time.sleep(0.2)


def paste_text(text):
    """Copy text to clipboard and paste."""
    pyperclip.copy(text)
    time.sleep(0.3)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.5)


def generate_song(config, name, style, lyrics, idx):
    print(f"\n[{idx+1}] Generating: {name}")
    print(f"  Style: {style[:60]}...")

    sx, sy = config["style_field"]
    lx, ly = config["lyrics_field"]
    cx, cy = config["create_button"]

    # Paste style
    print("  Pasting style...")
    clear_field(sx, sy)
    paste_text(style)
    time.sleep(0.5)

    # Paste lyrics
    print("  Pasting lyrics...")
    clear_field(lx, ly)
    paste_text(lyrics)
    time.sleep(0.5)

    # Click Create
    print("  Clicking Create...")
    pyautogui.click(cx, cy)
    time.sleep(1)

    # Wait for generation
    print(f"  Waiting {WAIT_GENERATE}s for generation...")
    for remaining in range(WAIT_GENERATE, 0, -10):
        print(f"    {remaining}s remaining...", end="\r")
        time.sleep(10)
    print()

    # Download both variants
    d1x, d1y = config["download_btn1"]
    d2x, d2y = config["download_btn2"]

    print("  Downloading song 1...")
    pyautogui.click(d1x, d1y)
    time.sleep(WAIT_DOWNLOAD)

    print("  Downloading song 2...")
    pyautogui.click(d2x, d2y)
    time.sleep(WAIT_DOWNLOAD)

    print(f"  Done! Song {name} generated and downloaded.")


def main():
    if "--calibrate" in sys.argv:
        calibrate()
        return

    songs = parse_songs(MD_FILE)
    if not songs:
        print("ERROR: No songs found in SUNO_ALL_BHAJANS.md")
        sys.exit(1)

    print(f"Found {len(songs)} songs to generate.")

    progress = load_progress()
    start_idx = progress["last_completed"] + 1

    if start_idx > 0:
        print(f"Resuming from song {start_idx + 1} ({songs[start_idx][0]})")

    config = load_config()

    print("\nStarting in 5 seconds — switch to Suno Chrome window NOW!")
    for i in range(5, 0, -1):
        print(f"  {i}...")
        time.sleep(1)

    # Process songs in batches of 2 (Suno queue limit)
    for idx in range(start_idx, len(songs)):
        name, style, lyrics = songs[idx]

        try:
            generate_song(config, name, style, lyrics, idx)
            save_progress(idx)
        except pyautogui.FailSafeException:
            print("\nABORTED — mouse moved to corner.")
            print(f"Progress saved. Last completed: song {idx} ({name})")
            sys.exit(0)
        except Exception as e:
            print(f"ERROR on {name}: {e}")
            print("Skipping and continuing...")
            save_progress(idx)

        # Small break between songs
        if idx < len(songs) - 1:
            print(f"  Waiting 10s before next song...")
            time.sleep(10)

    print("\n✓ All songs generated!")
    print("Run: python sunya-music/scripts/move_downloads.py to sort files.")


if __name__ == "__main__":
    main()
