#!/usr/bin/env python3
"""
upload_facebook.py — uploads bhajan video to Music Daily Facebook page
using the Resumable Upload API (pages_manage_posts only, no publish_video needed).

Flow:
  1. POST /<APP_ID>/uploads          → upload_session_id
  2. POST /upload:<SESSION_ID>       → file handle "h"
  3. POST /<PAGE_ID>/videos          → published video
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
import io

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
APP_ID     = os.environ.get("FACEBOOK_APP_ID", "")

GRAPH_BASE       = "https://graph.facebook.com/v25.0"
GRAPH_VIDEO_BASE = "https://graph-video.facebook.com/v25.0"

TEMP_DIR   = os.path.join(os.path.dirname(__file__), "..", "temp")
VIDEO_FILE = os.path.join(TEMP_DIR, "music_output.mp4")
META_FILE  = os.path.join(TEMP_DIR, "music_meta.json")


def start_upload_session(file_size, file_name):
    """Step 1: Start upload session, returns upload_session_id."""
    print("Step 1: Starting upload session...")
    params = urllib.parse.urlencode({
        "file_name":   file_name,
        "file_length": file_size,
        "file_type":   "video/mp4",
        "access_token": PAGE_TOKEN,
    })
    url = f"{GRAPH_BASE}/{APP_ID}/uploads?{params}"
    req = urllib.request.Request(url, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Session start error {e.code}: {e.read().decode()}")
    print(f"  Upload session: {result}")
    session_id = result.get("id", "")
    if not session_id:
        raise RuntimeError(f"No upload session ID in response: {result}")
    return session_id


def upload_file(session_id, file_size):
    """Step 2: Upload raw binary, returns file handle."""
    print(f"Step 2: Uploading {file_size // (1024*1024)} MB...")
    url = f"{GRAPH_BASE}/{session_id}"
    with open(VIDEO_FILE, "rb") as f:
        video_data = f.read()
    req = urllib.request.Request(url, data=video_data, method="POST")
    req.add_header("Authorization", f"OAuth {PAGE_TOKEN}")
    req.add_header("file_offset", "0")
    req.add_header("Content-Type", "video/mp4")
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            result = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Upload error {e.code}: {e.read().decode()}")
    handle = result.get("h", "")
    if not handle:
        raise RuntimeError(f"No file handle in response: {result}")
    print(f"  File handle obtained: {handle[:30]}...")
    return handle


def publish_video(file_handle, title, description):
    """Step 3: Publish video to page using file handle."""
    print("Step 3: Publishing video to Facebook page...")

    boundary = b"fbvideoboundary_sunyamusic"
    body = io.BytesIO()

    def field(name, value):
        body.write(b"--" + boundary + b"\r\n")
        body.write(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        body.write(value.encode("utf-8"))
        body.write(b"\r\n")

    field("access_token", PAGE_TOKEN)
    field("title", title[:255])
    field("description", description[:2200])
    field("fbuploader_video_file_chunk", file_handle)
    body.write(b"--" + boundary + b"--\r\n")

    body_bytes = body.getvalue()
    content_type = f"multipart/form-data; boundary={boundary.decode()}"

    url = f"{GRAPH_VIDEO_BASE}/{PAGE_ID}/videos"
    req = urllib.request.Request(url, data=body_bytes, method="POST")
    req.add_header("Content-Type", content_type)

    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            result = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Publish error {e.code}: {e.read().decode()}")

    video_id = result.get("id", "unknown")
    print(f"Facebook upload complete! Video ID: {video_id}")
    return video_id


def main():
    if not PAGE_TOKEN:
        print("ERROR: FACEBOOK_MUSIC_PAGE_TOKEN is not set")
        sys.exit(1)
    if not PAGE_ID:
        print("ERROR: FACEBOOK_MUSIC_PAGE_ID is not set")
        sys.exit(1)
    if not APP_ID:
        print("ERROR: FACEBOOK_APP_ID is not set")
        sys.exit(1)
    if not os.path.exists(VIDEO_FILE):
        print(f"ERROR: {VIDEO_FILE} not found — YouTube step must run first")
        sys.exit(1)

    title       = "Daily Bhajan"
    description = "🎵 SUNYAMusic — Sounds for the Soul"
    if os.path.exists(META_FILE):
        with open(META_FILE, encoding="utf-8") as f:
            meta = json.load(f)
        title       = meta.get("title", title)
        description = meta.get("description", description)

    print(f"Title: {title}")

    file_size = os.path.getsize(VIDEO_FILE)
    file_name = os.path.basename(VIDEO_FILE)

    session_id  = start_upload_session(file_size, file_name)
    file_handle = upload_file(session_id, file_size)
    publish_video(file_handle, title, description)


if __name__ == "__main__":
    main()
