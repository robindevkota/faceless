"""
Suno Auto-Create Script
Automates pasting Style + Lyrics into Suno Advanced Mode and clicking Create.

Requirements: pip install pyautogui pyperclip
Before running: Open Suno in Chrome (Cursed profile) at suno.com/create, Advanced tab selected.
Move mouse to top-left corner to abort (failsafe).
"""

import pyautogui
import pyperclip
import time
import re
import subprocess
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────────
BHAJANS_FILE       = Path(__file__).parent.parent / "SUNO_ALL_BHAJANS.md"
STARTUP_DELAY      = 8    # seconds to switch to Chrome
DELAY_AFTER_CREATE = 5    # seconds between songs (within a batch)
QUEUE_SIZE         = 4    # Suno max queue
QUEUE_WAIT         = 120  # seconds to wait for queue to clear before next batch
START_FROM_SONG    = 3    # 1-indexed, change to resume mid-way
END_AT_SONG        = 3    # inclusive (test: 1 song only)

# ── Coordinates (get exact coords by hovering mouse and using get_mouse_position) ──
LYRICS_FIELD   = (360, 270)  # inside Lyrics textarea
STYLES_RESET   = (422, 442) # the reset/undo button next to Styles header
STYLES_FIELD   = (360, 490)  # inside Styles textarea
CREATE_BTN     = (411, 665)  # Create button (fixed position at bottom)

# ── Parse bhajans file ──────────────────────────────────────────────────────
def parse_bhajans(filepath):
    text = filepath.read_text(encoding="utf-8")
    songs = []
    blocks = re.split(r"---\n## [A-Z]+ SONG \d+ -- (\w+)", text)
    if len(blocks) < 3:
        # Try alternate dash style
        blocks = re.split(r"---\r?\n## [A-Z]+ SONG \d+ \xe2\x80\x94 (\w+)", text)
    if len(blocks) < 3:
        blocks = re.split(r"## [A-Z]+ SONG \d+ — (\w+)", text)

    i = 1
    while i < len(blocks) - 1:
        name = blocks[i].strip()
        body = blocks[i + 1]
        style_match  = re.search(r"STYLE:\n(.+?)(?=\nLYRICS:)", body, re.DOTALL)
        lyrics_match = re.search(r"LYRICS:\n(.+?)(?=\n---|\Z)", body, re.DOTALL)
        if style_match and lyrics_match:
            songs.append({
                "name":   name,
                "style":  style_match.group(1).strip(),
                "lyrics": lyrics_match.group(1).strip(),
            })
        i += 2
    return songs

# ── Paste helper ─────────────────────────────────────────────────────────────
def click_and_paste(x, y, text):
    pyautogui.click(x, y)   # single click to focus
    time.sleep(0.5)
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.2)
    pyautogui.press("backspace")
    time.sleep(0.2)
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.5)

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    songs = parse_bhajans(BHAJANS_FILE)
    print(f"Loaded {len(songs)} songs.")

    if not songs:
        print("ERROR: No songs parsed! Check the bhajans file path.")
        return

    subset = songs[START_FROM_SONG - 1 : END_AT_SONG]
    print(f"Creating songs {START_FROM_SONG} to {min(END_AT_SONG, len(songs))}")
    print(f"First song: {subset[0]['name']}")
    print(f"\nSwitch to Suno Chrome NOW - starting in {STARTUP_DELAY}s...")
    for i in range(STARTUP_DELAY, 0, -1):
        print(f"  {i}...", end="\r", flush=True)
        time.sleep(1)
    print("Starting!          ")

    pyautogui.FAILSAFE = True

    # Focus Chrome window via PowerShell
    subprocess.run([
        "powershell", "-Command",
        """
        $wshell = New-Object -ComObject wscript.shell
        $wshell.AppActivate('Suno | AI Music')
        """
    ], capture_output=True)
    time.sleep(1.0)

    for idx, song in enumerate(subset, start=START_FROM_SONG):
        print(f"\n[{idx}/{len(songs)}] {song['name']}")

        # 1. Paste LYRICS
        print("  -> Pasting lyrics...")
        click_and_paste(*LYRICS_FIELD, song["lyrics"])

        # 2. Clear styles then paste
        print("  -> Clearing styles...")
        pyautogui.click(STYLES_RESET[0], STYLES_RESET[1])  # click reset button
        time.sleep(0.5)
        print("  -> Pasting style...")
        click_and_paste(STYLES_FIELD[0], STYLES_FIELD[1], song["style"])

        # 3. Tab 30 times from Styles field to reach Create, then Enter
        time.sleep(1.0)  # wait for style field to settle
        print("  -> Tabbing to Create (30 tabs)...")
        for _ in range(30):
            pyautogui.press("tab")
            time.sleep(0.05)
        pyautogui.press("enter")
        time.sleep(1.0)

        print(f"  OK: {song['name']} submitted")

        # Pause every QUEUE_SIZE songs to let Suno generate
        songs_done = idx - START_FROM_SONG + 1
        if songs_done % QUEUE_SIZE == 0 and idx < min(END_AT_SONG, len(songs)):
            print(f"\nQueue full ({QUEUE_SIZE} songs). Waiting {QUEUE_WAIT}s...")
            for remaining in range(QUEUE_WAIT, 0, -10):
                print(f"   {remaining}s remaining...", end="\r", flush=True)
                time.sleep(10)
            print("  Resuming...                    ")
        else:
            time.sleep(DELAY_AFTER_CREATE)

    print(f"\nDone! {len(subset)} songs submitted.")

if __name__ == "__main__":
    main()
