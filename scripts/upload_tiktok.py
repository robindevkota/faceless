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
import time
import urllib.request
import urllib.error

ACCESS_TOKEN = os.environ.get("TIKTOK_ACCESS_TOKEN", "")

CREATOR_URL = "https://open.tiktokapis.com/v2/post/publish/creator_info/query/"
INIT_URL    = "https://open.tiktokapis.com/v2/post/publish/video/init/"
STATUS_URL  = "https://open.tiktokapis.com/v2/post/publish/status/fetch/"

VIDEO_FILE  = "./temp/output.mp4"
SCRIPT_FILE = "./temp/script.json"


def auth_headers() -> dict:
    return {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type":  "application/json; charset=UTF-8"
    }


def query_creator_info() -> dict:
    req = urllib.request.Request(
        CREATOR_URL,
        data=b"{}",
        headers=auth_headers(),
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"TikTok creator_info error {e.code}: {e.read().decode()}")

    if result.get("error", {}).get("code") != "ok":
        raise RuntimeError(f"TikTok creator_info failed: {result}")

    data = result["data"]
    print(f"Creator: @{data['creator_username']} ({data['creator_nickname']})")
    print(f"Max video duration: {data['max_video_post_duration_sec']}s")
    return data


def init_upload(caption: str, video_size: int, privacy_options: list) -> dict:
    # Use PUBLIC_TO_EVERYONE if available, otherwise first option
    privacy = "PUBLIC_TO_EVERYONE" if "PUBLIC_TO_EVERYONE" in privacy_options else privacy_options[0]

    body = json.dumps({
        "post_info": {
            "title":           caption[:150],
            "privacy_level":   privacy,
            "disable_duet":    False,
            "disable_comment": False,
            "disable_stitch":  False
        },
        "source_info": {
            "source":            "FILE_UPLOAD",
            "video_size":        video_size,
            "chunk_size":        video_size,
            "total_chunk_count": 1
        }
    }).encode()

    req = urllib.request.Request(
        INIT_URL,
        data=body,
        headers=auth_headers(),
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
    print(f"Upload initialized. publish_id: {data['publish_id']}")
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
            print(f"Upload status: {r.status}")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"TikTok upload error {e.code}: {e.read().decode()}")


def check_status(publish_id: str) -> str:
    body = json.dumps({"publish_id": publish_id}).encode()
    req = urllib.request.Request(
        STATUS_URL,
        data=body,
        headers=auth_headers(),
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"TikTok status error {e.code}: {e.read().decode()}")

    status = result.get("data", {}).get("status", "UNKNOWN")
    return status


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

    # Step 1: query creator info (required by TikTok API)
    creator = query_creator_info()
    privacy_options = creator.get("privacy_level_options", ["PUBLIC_TO_EVERYONE"])

    # Step 2: initialize upload
    init_data  = init_upload(caption, video_size, privacy_options)
    upload_url = init_data["upload_url"]
    publish_id = init_data["publish_id"]

    # Step 3: upload video
    upload_chunk(upload_url, VIDEO_FILE, video_size)

    # Step 4: poll status (up to 2 minutes)
    print("Checking publish status...")
    for _ in range(24):
        time.sleep(5)
        status = check_status(publish_id)
        print(f"  Status: {status}")
        if status in ("PUBLISH_COMPLETE", "SUCCESS"):
            print("TikTok upload complete!")
            return
        if status in ("FAILED", "PUBLISH_FAILED"):
            raise RuntimeError(f"TikTok publish failed. publish_id: {publish_id}")

    print(f"Upload submitted. publish_id: {publish_id} (still processing)")


if __name__ == "__main__":
    main()
