#!/usr/bin/env python3
"""
upload_facebook.py — uploads bhajan video to Music Daily Facebook page
using the Resumable Upload API (no publish_video permission needed).
Step 1: Start upload session → get video_id
Step 2: Upload file chunks
Step 3: Publish video to page
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

GRAPH_BASE       = "https://graph.facebook.com/v19.0"
GRAPH_VIDEO_BASE = "https://graph-video.facebook.com/v19.0"

TEMP_DIR   = os.path.join(os.path.dirname(__file__), "..", "temp")
VIDEO_FILE = os.path.join(TEMP_DIR, "music_output.mp4")
META_FILE  = os.path.join(TEMP_DIR, "music_meta.json")

CHUNK_SIZE = 10 * 1024 * 1024  # 10 MB chunks


def api_post(url, data, headers=None, timeout=120):
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"API error {e.code}: {e.read().decode()}")


def start_upload_session(file_size):
    """Step 1: Start a resumable upload session, get upload_session_id and video_id."""
    print("Starting upload session...")
    payload = json.dumps({
        "access_token": PAGE_TOKEN,
        "file_size": file_size,
    }).encode()
    url = f"{GRAPH_VIDEO_BASE}/{PAGE_ID}/videos"
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Session start error {e.code}: {e.read().decode()}")
    print(f"Session response: {result}")
    return result.get("upload_session_id"), result.get("video_id")


def upload_chunks(upload_session_id, video_id, file_size):
    """Step 2: Upload file in chunks."""
    print(f"Uploading {file_size // (1024*1024)} MB in chunks...")
    offset = 0
    with open(VIDEO_FILE, "rb") as f:
        while offset < file_size:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break

            boundary = b"chunk_boundary_sunyamusic"
            body = io.BytesIO()

            def field(name, value):
                body.write(b"--" + boundary + b"\r\n")
                body.write(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
                body.write(value if isinstance(value, bytes) else value.encode())
                body.write(b"\r\n")

            field("access_token", PAGE_TOKEN)
            field("upload_session_id", str(upload_session_id))
            field("start_offset", str(offset))

            body.write(b"--" + boundary + b"\r\n")
            body.write(b'Content-Disposition: form-data; name="video_file_chunk"; filename="chunk.mp4"\r\n')
            body.write(b"Content-Type: application/octet-stream\r\n\r\n")
            body.write(chunk)
            body.write(b"\r\n")
            body.write(b"--" + boundary + b"--\r\n")

            body_bytes = body.getvalue()
            content_type = f"multipart/form-data; boundary={boundary.decode()}"

            url = f"{GRAPH_VIDEO_BASE}/{PAGE_ID}/videos"
            req = urllib.request.Request(url, data=body_bytes, method="POST")
            req.add_header("Content-Type", content_type)

            try:
                with urllib.request.urlopen(req, timeout=300) as r:
                    result = json.loads(r.read())
            except urllib.error.HTTPError as e:
                raise RuntimeError(f"Chunk upload error {e.code}: {e.read().decode()}")

            next_offset = int(result.get("start_offset", offset + len(chunk)))
            print(f"  Uploaded {next_offset // (1024*1024)} / {file_size // (1024*1024)} MB")
            offset = next_offset

    print("All chunks uploaded.")


def publish_video(video_id, title, description):
    """Step 3: Publish the uploaded video."""
    print("Publishing video...")
    payload = json.dumps({
        "access_token":  PAGE_TOKEN,
        "video_id":      video_id,
        "title":         title[:255],
        "description":   description[:2200],
        "published":     True,
    }).encode()
    url = f"{GRAPH_BASE}/{PAGE_ID}/videos"
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            result = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Publish error {e.code}: {e.read().decode()}")
    print(f"Facebook upload complete! Video ID: {result.get('id', video_id)}")
    return result


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
    description = "🎵 SUNYAMusic — Sounds for the Soul"
    if os.path.exists(META_FILE):
        with open(META_FILE, encoding="utf-8") as f:
            meta = json.load(f)
        title       = meta.get("title", title)
        description = meta.get("description", description)

    print(f"Title: {title}")

    file_size = os.path.getsize(VIDEO_FILE)
    upload_session_id, video_id = start_upload_session(file_size)

    if not upload_session_id or not video_id:
        print("ERROR: Failed to start upload session")
        sys.exit(1)

    upload_chunks(upload_session_id, video_id, file_size)
    publish_video(video_id, title, description)


if __name__ == "__main__":
    main()
