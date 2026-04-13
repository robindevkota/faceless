#!/usr/bin/env python3
"""
upload_youtube.py — uploads final video to YouTube using Data API v3
Reads: ./temp/script.json  (for title, description, hashtags)
       ./temp/output.mp4   (the video)
Env vars required:
  YOUTUBE_CLIENT_ID
  YOUTUBE_CLIENT_SECRET
  YOUTUBE_REFRESH_TOKEN
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error

# ── Config ────────────────────────────────────────────────────────────────────
CLIENT_ID      = os.environ.get("YOUTUBE_CLIENT_ID", "")
CLIENT_SECRET  = os.environ.get("YOUTUBE_CLIENT_SECRET", "")
REFRESH_TOKEN  = os.environ.get("YOUTUBE_REFRESH_TOKEN", "")

TOKEN_URL      = "https://oauth2.googleapis.com/token"
UPLOAD_URL     = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"

VIDEO_FILE     = "./temp/output.mp4"
SCRIPT_FILE    = "./temp/script.json"

# ── Helpers ───────────────────────────────────────────────────────────────────

def get_access_token() -> str:
    body = urllib.parse.urlencode({
        "client_id":     CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type":    "refresh_token"
    }).encode()

    req = urllib.request.Request(TOKEN_URL, data=body, method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())

    if "access_token" not in data:
        raise RuntimeError(f"Token error: {data}")

    print("Access token obtained.")
    return data["access_token"]


def build_metadata(script_data: dict) -> dict:
    title       = script_data.get("title", "Daily Video")[:100]
    description = script_data.get("description", "")
    hashtags    = script_data.get("hashtags", [])

    # Append hashtags to description
    tags_str = " ".join(f"#{t.lstrip('#')}" for t in hashtags)
    full_description = f"{description}\n\n{tags_str}"

    return {
        "snippet": {
            "title":       title,
            "description": full_description,
            "tags":        hashtags,
            "categoryId":  "22"   # People & Blogs — change to 27 (Education) if preferred
        },
        "status": {
            "privacyStatus":           "public",
            "selfDeclaredMadeForKids": False
        }
    }


def upload_video(access_token: str, metadata: dict, video_path: str):
    video_size = os.path.getsize(video_path)

    # Step 1: initiate resumable upload, get upload URI
    meta_body = json.dumps(metadata).encode()
    init_req = urllib.request.Request(
        UPLOAD_URL,
        data=meta_body,
        headers={
            "Authorization":    f"Bearer {access_token}",
            "Content-Type":     "application/json; charset=UTF-8",
            "X-Upload-Content-Type": "video/mp4",
            "X-Upload-Content-Length": str(video_size)
        },
        method="POST"
    )

    with urllib.request.urlopen(init_req, timeout=30) as r:
        upload_uri = r.headers["Location"]

    print(f"Upload URI obtained. Uploading {video_size // (1024*1024)} MB...")

    # Step 2: upload the video bytes
    with open(video_path, "rb") as f:
        video_data = f.read()

    upload_req = urllib.request.Request(
        upload_uri,
        data=video_data,
        headers={
            "Content-Type":   "video/mp4",
            "Content-Length": str(video_size)
        },
        method="PUT"
    )

    with urllib.request.urlopen(upload_req, timeout=300) as r:
        result = json.loads(r.read())

    video_id = result.get("id", "unknown")
    print(f"YouTube upload complete! Video ID: {video_id}")
    print(f"URL: https://www.youtube.com/watch?v={video_id}")
    return video_id


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    for var in ["YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN"]:
        if not os.environ.get(var):
            print(f"ERROR: {var} is not set")
            sys.exit(1)

    if not os.path.exists(VIDEO_FILE):
        print(f"ERROR: {VIDEO_FILE} not found")
        sys.exit(1)

    with open(SCRIPT_FILE, encoding="utf-8") as f:
        script_data = json.load(f)

    access_token = get_access_token()
    metadata     = build_metadata(script_data)
    upload_video(access_token, metadata, VIDEO_FILE)


if __name__ == "__main__":
    main()
