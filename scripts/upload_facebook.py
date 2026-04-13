#!/usr/bin/env python3
"""
upload_facebook.py — uploads video as Facebook Reel via Graph API
Reads: ./temp/script.json  (for description)
       ./temp/output.mp4   (the video)
Env vars required:
  FACEBOOK_PAGE_TOKEN   (Page Access Token from developers.facebook.com)
  FACEBOOK_PAGE_ID      (your Facebook Page ID)
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error

# ── Config ────────────────────────────────────────────────────────────────────
PAGE_TOKEN = os.environ.get("FACEBOOK_PAGE_TOKEN", "")
PAGE_ID    = os.environ.get("FACEBOOK_PAGE_ID", "")

GRAPH_BASE = "https://graph.facebook.com/v19.0"

VIDEO_FILE  = "./temp/output.mp4"
SCRIPT_FILE = "./temp/script.json"

# ── Helpers ───────────────────────────────────────────────────────────────────

def start_upload_session(video_size: int) -> str:
    """Initialize a resumable upload session, return upload_session_id."""
    params = urllib.parse.urlencode({
        "access_token":  PAGE_TOKEN,
        "upload_phase":  "start",
        "file_size":     video_size
    })
    url = f"{GRAPH_BASE}/{PAGE_ID}/videos?{params}"

    req = urllib.request.Request(url, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Facebook start error {e.code}: {e.read().decode()}")

    session_id = result.get("upload_session_id")
    if not session_id:
        raise RuntimeError(f"No upload_session_id in response: {result}")

    print(f"Facebook upload session: {session_id}")
    return session_id


def upload_video_chunk(session_id: str, video_path: str, video_size: int):
    """Upload the video file in one chunk."""
    with open(video_path, "rb") as f:
        video_data = f.read()

    params = urllib.parse.urlencode({
        "access_token":      PAGE_TOKEN,
        "upload_phase":      "transfer",
        "upload_session_id": session_id,
        "start_offset":      0
    })
    url = f"{GRAPH_BASE}/{PAGE_ID}/videos?{params}"

    req = urllib.request.Request(
        url,
        data=video_data,
        headers={
            "Content-Type":   "application/octet-stream",
            "Content-Length": str(video_size)
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            result = json.loads(r.read())
            print(f"Chunk upload response: {result}")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Facebook chunk error {e.code}: {e.read().decode()}")


def finish_upload(session_id: str, description: str) -> str:
    """Finalize the upload and publish the video."""
    params = urllib.parse.urlencode({
        "access_token":      PAGE_TOKEN,
        "upload_phase":      "finish",
        "upload_session_id": session_id,
        "description":       description[:2200],
        "published":         "true"
    })
    url = f"{GRAPH_BASE}/{PAGE_ID}/videos?{params}"

    req = urllib.request.Request(url, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            result = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Facebook finish error {e.code}: {e.read().decode()}")

    video_id = result.get("video_id") or result.get("id", "unknown")
    print(f"Facebook upload complete! Video ID: {video_id}")
    return video_id


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if not PAGE_TOKEN:
        print("ERROR: FACEBOOK_PAGE_TOKEN is not set")
        sys.exit(1)
    if not PAGE_ID:
        print("ERROR: FACEBOOK_PAGE_ID is not set")
        sys.exit(1)

    if not os.path.exists(VIDEO_FILE):
        print(f"ERROR: {VIDEO_FILE} not found")
        sys.exit(1)

    with open(SCRIPT_FILE, encoding="utf-8") as f:
        script_data = json.load(f)

    description = script_data.get("description", script_data.get("title", ""))
    hashtags    = script_data.get("hashtags", [])
    tags_str    = " ".join(f"#{t.lstrip('#')}" for t in hashtags)
    full_desc   = f"{description}\n\n{tags_str}"

    video_size  = os.path.getsize(VIDEO_FILE)
    print(f"Uploading to Facebook ({video_size // (1024*1024)} MB)...")

    session_id = start_upload_session(video_size)
    upload_video_chunk(session_id, VIDEO_FILE, video_size)
    finish_upload(session_id, full_desc)


if __name__ == "__main__":
    main()
