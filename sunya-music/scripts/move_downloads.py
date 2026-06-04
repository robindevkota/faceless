#!/usr/bin/env python3
"""
move_downloads.py — watches Downloads folder for new Suno MP3s
and moves them to the correct folder based on user input.

Usage:
  python move_downloads.py

It will show you all new MP3s in Downloads and ask where each goes.
"""

import os
import shutil
import time

DOWNLOADS = os.path.expanduser("~/Downloads")
BASE_DIR  = os.path.join(os.path.dirname(__file__), "..")

DESTINATIONS = {
    # Bhajans
    "1":  ("monday/shiva",     os.path.join(BASE_DIR, "audio", "monday")),
    "2":  ("tuesday/hanuman",  os.path.join(BASE_DIR, "audio", "tuesday")),
    "3":  ("wednesday/ganesha",os.path.join(BASE_DIR, "audio", "wednesday")),
    "4":  ("thursday/vishnu",  os.path.join(BASE_DIR, "audio", "thursday")),
    "5":  ("friday/lakshmi",   os.path.join(BASE_DIR, "audio", "friday")),
    "6":  ("saturday/shani",   os.path.join(BASE_DIR, "audio", "saturday")),
    "7":  ("sunday/surya",     os.path.join(BASE_DIR, "audio", "sunday")),
    # Nepali songs
    "8":  ("nepali-songs",     os.path.join(BASE_DIR, "nepali-songs", "audio")),
    # Meditation
    "9":  ("meditation/peace", os.path.join(BASE_DIR, "meditation", "peace", "audio")),
    "10": ("meditation/sleep", os.path.join(BASE_DIR, "meditation", "sleep", "audio")),
    "11": ("meditation/focus", os.path.join(BASE_DIR, "meditation", "focus", "audio")),
    "12": ("meditation/healing",os.path.join(BASE_DIR, "meditation", "healing", "audio")),
}


def get_next_filename(dest_dir, prefix):
    """Auto-number the file: shiva_5.mp3, shiva_6.mp3 etc."""
    existing = [f for f in os.listdir(dest_dir) if f.endswith(".mp3")]
    nums = []
    for f in existing:
        parts = f.replace(".mp3", "").split("_")
        if len(parts) >= 2 and parts[-1].isdigit():
            nums.append(int(parts[-1]))
    next_num = max(nums) + 1 if nums else 1
    return f"{prefix}_{next_num}.mp3"


def main():
    print("=" * 50)
    print("Suno Download Mover")
    print("=" * 50)
    print("\nScanning Downloads folder for MP3 files...\n")

    mp3s = sorted([
        f for f in os.listdir(DOWNLOADS)
        if f.endswith(".mp3")
    ], key=lambda f: os.path.getmtime(os.path.join(DOWNLOADS, f)), reverse=True)

    if not mp3s:
        print("No MP3 files found in Downloads.")
        return

    print(f"Found {len(mp3s)} MP3 file(s):\n")
    for i, f in enumerate(mp3s):
        size = os.path.getsize(os.path.join(DOWNLOADS, f)) // (1024 * 1024)
        print(f"  [{i+1}] {f} ({size} MB)")

    print("\nDestination options:")
    for key, (name, _) in DESTINATIONS.items():
        print(f"  {key:>2}. {name}")
    print("   s. Skip this file")
    print("   q. Quit\n")

    for mp3 in mp3s:
        src = os.path.join(DOWNLOADS, mp3)
        print(f"\nFile: {mp3}")
        choice = input("Where to move? (1-12 / s=skip / q=quit): ").strip().lower()

        if choice == "q":
            break
        if choice == "s":
            print("  Skipped.")
            continue
        if choice not in DESTINATIONS:
            print("  Invalid choice, skipping.")
            continue

        name, dest_dir = DESTINATIONS[choice]
        os.makedirs(dest_dir, exist_ok=True)

        # Determine prefix from folder name
        prefix_map = {
            "1": "shiva", "2": "hanuman", "3": "ganesha",
            "4": "vishnu", "5": "lakshmi", "6": "shani", "7": "surya",
        }
        if choice in prefix_map:
            new_name = get_next_filename(dest_dir, prefix_map[choice])
        else:
            # For nepali/meditation, ask for custom name
            custom = input(f"  Enter filename (without .mp3, e.g. maya_ko_rang): ").strip()
            new_name = f"{custom}.mp3" if custom else mp3

        dest = os.path.join(dest_dir, new_name)
        shutil.move(src, dest)
        print(f"  Moved → {dest}")

    print("\nDone!")


if __name__ == "__main__":
    main()
