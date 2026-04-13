#!/usr/bin/env python3
"""
download_assets.py — downloads free stock clips and music from Pixabay API
Run once to populate your stock/ and music/ folders.
"""

import urllib.request
import urllib.parse
import json
import os
import sys

PIXABAY_API_KEY = os.environ.get("PIXABAY_API_KEY", "")
STOCK_DIR = "./stock"
MUSIC_DIR = "./music"
VIDEO_QUERIES = ["money", "finance", "city timelapse", "business", "success", "technology"]
MUSIC_QUERIES = ["lofi background", "calm background music"]
VIDEO_COUNT = 10
MUSIC_COUNT = 5
MAX_FILE_SIZE_MB = 80  # skip files larger than this


def download_file(url: str, dest: str) -> bool:
    print(f"  Downloading {os.path.basename(dest)}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    size_mb = len(data) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        print(f"  Skipping — too large ({size_mb:.1f} MB > {MAX_FILE_SIZE_MB} MB limit)")
        return False
    with open(dest, "wb") as f:
        f.write(data)
    print(f"  Saved ({size_mb:.1f} MB)")
    return True


def fetch_pixabay_videos(query: str, count: int) -> list:
    params = urllib.parse.urlencode({
        "key": PIXABAY_API_KEY, "q": query,
        "video_type": "film", "per_page": count, "safesearch": "true"
    })
    with urllib.request.urlopen(f"https://pixabay.com/api/videos/?{params}", timeout=15) as r:
        return json.loads(r.read()).get("hits", [])


def fetch_pixabay_music(query: str, count: int) -> list:
    params = urllib.parse.urlencode({
        "key": PIXABAY_API_KEY, "q": query,
        "media_type": "music", "per_page": count, "safesearch": "true"
    })
    with urllib.request.urlopen(f"https://pixabay.com/api/?{params}", timeout=15) as r:
        return json.loads(r.read()).get("hits", [])


def main():
    if not PIXABAY_API_KEY:
        print("ERROR: PIXABAY_API_KEY not set.")
        sys.exit(1)

    os.makedirs(STOCK_DIR, exist_ok=True)
    os.makedirs(MUSIC_DIR, exist_ok=True)

    print(f"\nDownloading {VIDEO_COUNT} stock video clips (max {MAX_FILE_SIZE_MB}MB each)...")
    downloaded = 0
    for query in VIDEO_QUERIES:
        if downloaded >= VIDEO_COUNT:
            break
        print(f"\nSearching: '{query}'")
        try:
            for hit in fetch_pixabay_videos(query, 5):
                if downloaded >= VIDEO_COUNT:
                    break
                videos = hit.get("videos", {})
                url = (videos.get("medium", {}).get("url") or
                       videos.get("small", {}).get("url") or
                       videos.get("tiny", {}).get("url"))
                if not url:
                    continue
                dest = os.path.join(STOCK_DIR, f"clip_{hit['id']}.mp4")
                if os.path.exists(dest):
                    print(f"  Skipping (exists)")
                    downloaded += 1
                    continue
                if download_file(url, dest):
                    downloaded += 1
        except Exception as e:
            print(f"  WARNING: {e}")

    print(f"\nDownloaded {downloaded} video clips.")

    print(f"\nDownloading {MUSIC_COUNT} music tracks...")
    downloaded_music = 0
    for query in MUSIC_QUERIES:
        if downloaded_music >= MUSIC_COUNT:
            break
        print(f"\nSearching music: '{query}'")
        try:
            for hit in fetch_pixabay_music(query, 5):
                if downloaded_music >= MUSIC_COUNT:
                    break
                url = hit.get("audio", {}).get("url") or hit.get("previewURL", "")
                if not url:
                    continue
                dest = os.path.join(MUSIC_DIR, f"music_{hit['id']}.mp3")
                if os.path.exists(dest):
                    downloaded_music += 1
                    continue
                if download_file(url, dest):
                    downloaded_music += 1
        except Exception as e:
            print(f"  WARNING: {e}")

    print(f"\nDone! {downloaded} clips, {downloaded_music} music tracks.")


if __name__ == "__main__":
    main()
