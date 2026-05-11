#!/usr/bin/env python3
"""
upload_facebook.py — uploads bhajan video to Music Daily Facebook page
Uses direct multipart POST to graph-video.facebook.com/<PAGE_ID>/videos
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

GRAPH_VIDEO_BASE = "https://graph-video.facebook.com/v19.0"

TEMP_DIR   = os.path.join(os.path.dirname(__file__), "..", "temp")
VIDEO_FILE = os.path.join(TEMP_DIR, "music_output.mp4")
META_FILE  = os.path.join(TEMP_DIR, "music_meta.json")


def encode_multipart(fields, file_path):
    boundary = b"fbvideoboundary1234567890"
    body = io.BytesIO()

    for name, value in fields.items():
        body.write(b"--" + boundary + b"\r\n")
        body.write(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        body.write(value.encode("utf-8") + b"\r\n")

    # video file part
    filename = os.path.basename(file_path)
    body.write(b"--" + boundary + b"\r\n")
    body.write(f'Content-Disposition: form-data; name="source"; filename="{filename}"\r\n'.encode())
    body.write(b"Content-Type: video/mp4\r\n\r\n")
    with open(file_path, "rb") as f:
        body.write(f.read())
    body.write(b"\r\n")

    body.write(b"--" + boundary + b"--\r\n")
    content_type = f"multipart/form-data; boundary={boundary.decode()}"
    return body.getvalue(), content_type


def upload_video(title, description):
    file_size = os.path.getsize(VIDEO_FILE)
    print(f"Uploading to Facebook ({file_size // (1024*1024)} MB)...")

    fields = {
        "access_token": PAGE_TOKEN,
        "title":        title[:255],
        "description":  description[:2200],
        "published":    "true",
    }

    body_bytes, content_type = encode_multipart(fields, VIDEO_FILE)

    url = f"{GRAPH_VIDEO_BASE}/{PAGE_ID}/videos"
    req = urllib.request.Request(url, data=body_bytes, method="POST")
    req.add_header("Content-Type", content_type)

    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            result = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Upload error {e.code}: {e.read().decode()}")

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
    upload_video(title, description)


if __name__ == "__main__":
    main()
