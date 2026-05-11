#!/usr/bin/env python3
"""
upload_facebook.py — uploads bhajan video to Music Daily Facebook page
Uses the Resumable Upload API to get a file handle, then publishes via /<PAGE_ID>/videos.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error

# load .env from parent folder
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

GRAPH_BASE       = "https://graph.facebook.com/v19.0"
GRAPH_VIDEO_BASE = "https://graph-video.facebook.com/v19.0"

TEMP_DIR   = os.path.join(os.path.dirname(__file__), "..", "temp")
VIDEO_FILE = os.path.join(TEMP_DIR, "music_output.mp4")
META_FILE  = os.path.join(TEMP_DIR, "music_meta.json")


def start_upload_session(file_size):
    """Step 1: Start upload session, get upload session ID."""
    url = f"{GRAPH_BASE}/{APP_ID}/uploads?" + urllib.parse.urlencode({
        "file_name":   "music_output.mp4",
        "file_length": file_size,
        "file_type":   "video/mp4",
        "access_token": PAGE_TOKEN,
    })
    req = urllib.request.Request(url, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Upload session start error {e.code}: {e.read().decode()}")

    session_id = result.get("id")
    if not session_id:
        raise RuntimeError(f"No upload session ID returned: {result}")
    print(f"Upload session: {session_id}")
    return session_id


def upload_file(session_id, file_path):
    """Step 2: Upload file bytes, get file handle."""
    url = f"{GRAPH_BASE}/{session_id}"
    with open(file_path, "rb") as f:
        video_data = f.read()

    req = urllib.request.Request(url, data=video_data, method="POST")
    req.add_header("Authorization", f"OAuth {PAGE_TOKEN}")
    req.add_header("file_offset", "0")
    req.add_header("Content-Type", "video/mp4")
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            result = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Upload error {e.code}: {e.read().decode()}")

    handle = result.get("h")
    if not handle:
        raise RuntimeError(f"No file handle returned: {result}")
    print(f"File handle obtained: {handle[:30]}...")
    return handle


def publish_video(file_handle, title, description):
    """Step 3: Publish the video using the file handle."""
    url = f"{GRAPH_VIDEO_BASE}/{PAGE_ID}/videos"

    boundary = "----FacebookPublishBoundary"
    body = ""
    for name, value in [
        ("access_token", PAGE_TOKEN),
        ("title", title[:255]),
        ("description", description[:2200]),
        ("fbuploader_video_file_chunk", file_handle),
        ("published", "true"),
    ]:
        body += f"--{boundary}\r\n"
        body += f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
        body += f"{value}\r\n"
    body += f"--{boundary}--\r\n"

    req = urllib.request.Request(url, data=body.encode(), method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
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

    title, description = "Bhajan", "Daily bhajan — SUNYAMusic"
    if os.path.exists(META_FILE):
        with open(META_FILE, encoding="utf-8") as f:
            meta = json.load(f)
        title       = meta.get("title", title)
        description = meta.get("description", description)

    print(f"Title: {title}")
    file_size = os.path.getsize(VIDEO_FILE)
    print(f"Video size: {file_size // (1024*1024)} MB")

    session_id  = start_upload_session(file_size)
    file_handle = upload_file(session_id, VIDEO_FILE)
    publish_video(file_handle, title, description)


if __name__ == "__main__":
    main()
