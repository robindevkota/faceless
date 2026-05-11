#!/usr/bin/env python3
"""
upload_facebook.py — uploads bhajan video to Music Daily Facebook page
Uses simple (non-resumable) upload for files under 1GB.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
import io

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
GRAPH_BASE = "https://graph.facebook.com/v19.0"

TEMP_DIR   = os.path.join(os.path.dirname(__file__), "..", "temp")
VIDEO_FILE = os.path.join(TEMP_DIR, "music_output.mp4")
META_FILE  = os.path.join(TEMP_DIR, "music_meta.json")


def encode_multipart(fields, files):
    """Build multipart/form-data body."""
    boundary = b"----FacebookUploadBoundary7a8b9c"
    body = io.BytesIO()
    for name, value in fields.items():
        body.write(b"--" + boundary + b"\r\n")
        body.write(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        body.write(value.encode() + b"\r\n")
    for name, (filename, data) in files.items():
        body.write(b"--" + boundary + b"\r\n")
        body.write(f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode())
        body.write(b"Content-Type: video/mp4\r\n\r\n")
        body.write(data + b"\r\n")
    body.write(b"--" + boundary + b"--\r\n")
    content_type = f"multipart/form-data; boundary={boundary.decode()}"
    return body.getvalue(), content_type


def upload_video_resumable(title, description):
    video_size = os.path.getsize(VIDEO_FILE)
    print(f"Uploading to Facebook ({video_size // (1024*1024)} MB) via resumable upload...")

    # Phase 1: start
    params = urllib.parse.urlencode({
        "access_token": PAGE_TOKEN,
        "upload_phase":  "start",
        "file_size":     video_size
    })
    url = f"{GRAPH_BASE}/{PAGE_ID}/videos?{params}"
    req = urllib.request.Request(url, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Facebook start error {e.code}: {body}")
        raise

    session_id = result.get("upload_session_id")
    if not session_id:
        raise RuntimeError(f"No upload_session_id: {result}")
    print(f"Upload session: {session_id}")

    # Phase 2: transfer (multipart)
    with open(VIDEO_FILE, "rb") as f:
        video_data = f.read()

    body_bytes, content_type = encode_multipart(
        {
            "access_token":      PAGE_TOKEN,
            "upload_phase":      "transfer",
            "upload_session_id": session_id,
            "start_offset":      "0",
        },
        {"video_file_chunk": ("chunk.mp4", video_data)}
    )
    url = f"{GRAPH_BASE}/{PAGE_ID}/videos"
    req = urllib.request.Request(url, data=body_bytes, method="POST")
    req.add_header("Content-Type", content_type)
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            chunk_result = json.loads(r.read())
            print(f"Chunk uploaded: {chunk_result}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Facebook chunk error {e.code}: {body}")
        raise

    # Phase 3: finish
    params = urllib.parse.urlencode({
        "access_token":      PAGE_TOKEN,
        "upload_phase":      "finish",
        "upload_session_id": session_id,
        "title":             title[:255],
        "description":       description[:2200],
        "published":         "true"
    })
    url = f"{GRAPH_BASE}/{PAGE_ID}/videos?{params}"
    req = urllib.request.Request(url, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            result = json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Facebook finish error {e.code}: {body}")
        raise

    video_id = result.get("video_id") or result.get("id", "unknown")
    print(f"Facebook upload complete! Video ID: {video_id}")
    return video_id


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

    title, description = "Bhajan", "Daily bhajan — SUNYAMusic"
    if os.path.exists(META_FILE):
        with open(META_FILE, encoding="utf-8") as f:
            meta = json.load(f)
        title       = meta.get("title", title)
        description = meta.get("description", description)

    print(f"Title: {title}")
    upload_video_resumable(title, description)


if __name__ == "__main__":
    main()
