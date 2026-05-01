#!/usr/bin/env python3
"""
download_assets.py — downloads free stock clips from Pexels API
Run once to populate your stock/ folder with HD psychology-themed clips.
"""

import urllib.request
import urllib.parse
import json
import os
import sys

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")
STOCK_DIR = "./stock"
MUSIC_DIR = "./music"

VIDEO_QUERIES = [
    "brain neurons", "meditation", "human mind", "thinking person",
    "nature walk", "ocean waves", "city timelapse", "sunrise",
    "people talking", "psychology", "stress", "happiness",
    "focus study", "breathe relax"
]

VIDEO_COUNT = 60
MAX_FILE_SIZE_MB = 80


def download_file(url: str, dest: str) -> bool:
    print(f"  Downloading {os.path.basename(dest)}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
    except Exception as e:
        print(f"  Failed: {e}")
        return False
    size_mb = len(data) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        print(f"  Skipping — too large ({size_mb:.1f} MB)")
        return False
    with open(dest, "wb") as f:
        f.write(data)
    print(f"  Saved ({size_mb:.1f} MB)")
    return True


def fetch_pexels_videos(query: str, per_page: int = 5) -> list:
    params = urllib.parse.urlencode({
        "query": query,
        "per_page": per_page,
        "orientation": "portrait",  # vertical = 9:16 ready
        "size": "medium",
    })
    req = urllib.request.Request(
        f"https://api.pexels.com/videos/search?{params}",
        headers={"Authorization": PEXELS_API_KEY}
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read()).get("videos", [])


def best_video_url(video: dict) -> str:
    files = video.get("video_files", [])
    # prefer HD (720 or 1080), portrait orientation
    for quality in ["hd", "sd"]:
        for f in files:
            if f.get("quality") == quality:
                return f.get("link", "")
    # fallback: just take first
    return files[0].get("link", "") if files else ""


def main():
    if not PEXELS_API_KEY:
        print("ERROR: PEXELS_API_KEY not set in environment or .env file.")
        print("Get a free key at https://www.pexels.com/api/")
        sys.exit(1)

    os.makedirs(STOCK_DIR, exist_ok=True)
    os.makedirs(MUSIC_DIR, exist_ok=True)

    existing = {f for f in os.listdir(STOCK_DIR) if f.endswith(".mp4")}
    print(f"Already have {len(existing)} clips in {STOCK_DIR}/")
    print(f"Target: {VIDEO_COUNT} clips total\n")

    downloaded = len(existing)

    for query in VIDEO_QUERIES:
        if downloaded >= VIDEO_COUNT:
            break
        print(f"Searching Pexels: '{query}'")
        try:
            videos = fetch_pexels_videos(query, per_page=5)
            for video in videos:
                if downloaded >= VIDEO_COUNT:
                    break
                vid_id = video.get("id")
                dest = os.path.join(STOCK_DIR, f"pexels_{vid_id}.mp4")
                if os.path.exists(dest):
                    print(f"  Skipping {vid_id} (exists)")
                    downloaded += 1
                    continue
                url = best_video_url(video)
                if not url:
                    print(f"  No URL for video {vid_id}")
                    continue
                if download_file(url, dest):
                    downloaded += 1
        except Exception as e:
            print(f"  WARNING: {e}")

    total = len([f for f in os.listdir(STOCK_DIR) if f.endswith(".mp4")])
    print(f"\nDone! {total} clips in {STOCK_DIR}/")


if __name__ == "__main__":
    main()
