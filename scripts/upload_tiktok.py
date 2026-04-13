#!/usr/bin/env python3
"""
upload_tiktok.py — uploads video to TikTok via Content Posting API
Reads: ./temp/script.json  (for caption)
       ./temp/output.mp4   (the video)
Env vars required:
  TIKTOK_ACCESS_TOKEN
"""

import os
import sys
import json
import urllib.request
import urllib.error

# ── Config ────────────────────────────────────────────────────────────────────
ACCESS_TOKEN = os.environ.get("TIKTOK_ACCESS_TOKEN", "")

INIT_URL   = "https://open.tiktokapis.com/v2/post/publish/video/init/"
STATUS_URL = "https://open.tiktokapis.com/v2/post/publish/status/fetch/"

VIDEO_FILE  = "./temp/output.mp4"
SCRIPT_FILE = "./temp/script.json"

# ── Helpers ───────────────────────────────────────────────────────────────────

def init_upload(caption: str, video_size: int) -> dict:
    body = json.dumps({
        "post_info": {
            "title":           caption[:150],
            "privacy_level":   "PUBLIC_TO_EVERYONE",
            "disable_duet":    False,
            "disable_comment": False,
            "disable_stitch":  False
        },
        "source_info": {
            "source":          "FILE_UPLOAD",
            "video_size":      video_size,
            "chunk_size":      video_size,
            "total_chunk_count": 1
        }
    }).encode()

    req = urllib.request.Request(
        INIT_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type":  "application/json; charset=UTF-8"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"TikTok init error {e.code}: {e.read().decode()}")

    if result.get("error", {}).get("code") != "ok":
        raise RuntimeError(f"TikTok init failed: {result}")

    data = result["data"]
    print(f"TikTok upload initialized. publish_id: {data['publish_id']}")
    return data


def upload_chunk(upload_url: str, video_path: str, video_size: int):
    with open(video_path, "rb") as f:
        video_data = f.read()

    req = urllib.request.Request(
        upload_url,
        data=video_data,
        headers={
            "Content-Type":   "video/mp4",
            "Content-Length": str(video_size),
            "Content-Range":  f"bytes 0-{video_size - 1}/{video_size}"
        },
        method="PUT"
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            print(f"TikTok chunk upload status: {r.status}")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"TikTok upload error {e.code}: {e.read().decode()}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if not ACCESS_TOKEN:
        print("ERROR: TIKTOK_ACCESS_TOKEN is not set")
        sys.exit(1)

    if not os.path.exists(VIDEO_FILE):
        print(f"ERROR: {VIDEO_FILE} not found")
        sys.exit(1)

    with open(SCRIPT_FILE, encoding="utf-8") as f:
        script_data = json.load(f)

    caption    = script_data.get("tiktok_caption", script_data.get("title", "Check this out!"))
    video_size = os.path.getsize(VIDEO_FILE)

    print(f"Uploading to TikTok ({video_size // (1024*1024)} MB)...")
    print(f"Caption: {caption}")

    init_data  = init_upload(caption, video_size)
    upload_url = init_data["upload_url"]

    upload_chunk(upload_url, VIDEO_FILE, video_size)

    print(f"TikTok upload complete! publish_id: {init_data['publish_id']}")
    print("Note: Video will be processed by TikTok (usually 1-5 minutes)")


if __name__ == "__main__":
    main()
