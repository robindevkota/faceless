#!/usr/bin/env python3
"""
upload_facebook.py — uploads bhajan as a Reel to Music Daily Facebook page.
No publish_video permission needed — only pages_manage_posts.

Flow:
  1. POST /<PAGE_ID>/video_reels (upload_phase=start) → video_id + upload_url
  2. POST rupload.facebook.com/video-upload/v25.0/<video_id> with raw binary
  3. POST /<PAGE_ID>/video_reels (upload_phase=finish) → published
"""

import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
import json
import subprocess
import platform
import urllib.request
import urllib.parse
import urllib.error

# load .env
_env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

PAGE_TOKEN = os.environ.get("FACEBOOK_MUSIC_PAGE_TOKEN", "")
PAGE_ID    = os.environ.get("FACEBOOK_MUSIC_PAGE_ID", "")

GRAPH_BASE   = "https://graph.facebook.com/v25.0"
RUPLOAD_BASE = "https://rupload.facebook.com/video-upload/v25.0"

TEMP_DIR      = os.path.join(os.path.dirname(__file__), "..", "temp")
VIDEO_FILE    = os.path.join(TEMP_DIR, "music_output.mp4")
REEL_FILE     = os.path.join(TEMP_DIR, "reel_output.mp4")
META_FILE     = os.path.join(TEMP_DIR, "music_meta.json")

if platform.system() == "Windows":
    _ff = r"C:\Users\user\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin"
    FFMPEG = os.path.join(_ff, "ffmpeg.exe")
else:
    FFMPEG = "ffmpeg"


def make_reel_video():
    """Convert landscape 1920x1080 to vertical 1080x1920 for Reels (max 90s)."""
    print("Converting to vertical Reel format (1080x1920, max 90s)...")
    cmd = [
        FFMPEG, "-y",
        "-i", VIDEO_FILE,
        "-t", "90",
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v", "libx264", "-preset", "fast", "-crf", "28",
        "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2",
        "-r", "30",
        "-movflags", "+faststart",
        REEL_FILE
    ]
    subprocess.run(cmd, check=True)
    size_mb = os.path.getsize(REEL_FILE) / (1024 * 1024)
    print(f"Reel video created: {size_mb:.1f} MB")
    return REEL_FILE


def start_upload_session():
    """Step 1: Initialize upload session, get video_id and upload_url."""
    print("Step 1: Starting Reel upload session...")
    payload = json.dumps({
        "upload_phase":  "start",
        "access_token":  PAGE_TOKEN,
    }).encode()
    url = f"{GRAPH_BASE}/{PAGE_ID}/video_reels"
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Session start error {e.code}: {e.read().decode()}")
    print(f"  video_id: {result.get('video_id')}")
    return result["video_id"], result["upload_url"]


def upload_reel(video_id, reel_path):
    """Step 2: Upload reel binary to rupload.facebook.com."""
    file_size = os.path.getsize(reel_path)
    print(f"Step 2: Uploading {file_size // (1024*1024)} MB to Facebook...")
    with open(reel_path, "rb") as f:
        video_data = f.read()
    url = f"{RUPLOAD_BASE}/{video_id}"
    req = urllib.request.Request(url, data=video_data, method="POST")
    req.add_header("Authorization", f"OAuth {PAGE_TOKEN}")
    req.add_header("offset", "0")
    req.add_header("file_size", str(file_size))
    req.add_header("Content-Type", "application/octet-stream")
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            result = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Upload error {e.code}: {e.read().decode()}")
    if not result.get("success"):
        raise RuntimeError(f"Upload not successful: {result}")
    print("  Upload complete.")


def publish_reel(video_id, description):
    """Step 3: Publish the reel."""
    print("Step 3: Publishing Reel...")
    params = urllib.parse.urlencode({
        "access_token": PAGE_TOKEN,
        "video_id":     video_id,
        "upload_phase": "finish",
        "video_state":  "PUBLISHED",
        "description":  description[:2200],
    })
    url = f"{GRAPH_BASE}/{PAGE_ID}/video_reels?{params}"
    req = urllib.request.Request(url, data=b"", method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            result = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Publish error {e.code}: {e.read().decode()}")
    if result.get("success"):
        print("Facebook Reel published successfully!")
    else:
        raise RuntimeError(f"Publish failed: {result}")


def main():
    if not PAGE_TOKEN:
        print("ERROR: FACEBOOK_MUSIC_PAGE_TOKEN is not set")
        sys.exit(1)
    if not PAGE_ID:
        print("ERROR: FACEBOOK_MUSIC_PAGE_ID is not set")
        sys.exit(1)
    if not os.path.exists(VIDEO_FILE):
        print(f"ERROR: {VIDEO_FILE} not found — YouTube step must run first")
        sys.exit(1)

    title       = "Daily Bhajan"
    description = "🎵 SUNYAMusic — Sounds for the Soul\n#bhajan #devotional #hindibhajan #sunyamusic"
    if os.path.exists(META_FILE):
        with open(META_FILE, encoding="utf-8") as f:
            meta = json.load(f)
        title       = meta.get("title", title)
        description = meta.get("description", description)

    print(f"Title: {title}")

    reel_path = make_reel_video()
    video_id, upload_url = start_upload_session()
    upload_reel(video_id, reel_path)
    publish_reel(video_id, f"{title}\n\n{description}")


if __name__ == "__main__":
    main()
