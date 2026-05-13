#!/usr/bin/env python3
"""
upload_nepali.py — picks a random unused Nepali song, makes a video and uploads to SUNYAMusic.

Structure:
  sunya-music/nepali-songs/audio/        ← MP3 files (named same as lyrics file e.g. kisaan_1.mp3)
  sunya-music/nepali-songs/lyrics/       ← metadata .md files (kisaan_1.md)
  sunya-music/nepali-songs/backgrounds/  ← images named same as song (kisaan_1.jpg or kisaan_1.png)
  sunya-music/nepali-songs/temp/         ← output video
"""

import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
import json
import random
import subprocess
import urllib.request
import urllib.parse
import platform
from datetime import datetime

# load .env
_env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

CLIENT_ID     = os.environ.get("YOUTUBE_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("YOUTUBE_CLIENT_SECRET", "")
REFRESH_TOKEN = os.environ.get("YOUTUBE_MUSIC_REFRESH_TOKEN", "")

BASE_DIR    = os.path.join(os.path.dirname(__file__), "..")
SONGS_DIR   = os.path.join(BASE_DIR, "nepali-songs")
AUDIO_DIR   = os.path.join(SONGS_DIR, "audio")
LYRICS_DIR  = os.path.join(SONGS_DIR, "lyrics")
BG_DIR      = os.path.join(SONGS_DIR, "backgrounds")
TEMP_DIR    = os.path.join(SONGS_DIR, "temp")
USED_FILE   = os.path.join(SONGS_DIR, "used_songs.json")
OUTPUT_VIDEO = os.path.join(TEMP_DIR, "nepali_output.mp4")

TOKEN_URL  = "https://oauth2.googleapis.com/token"
UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"

if platform.system() == "Windows":
    _ff = r"C:\Users\user\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin"
    FFMPEG = os.path.join(_ff, "ffmpeg.exe")
else:
    FFMPEG = "ffmpeg"


def get_access_token():
    body = urllib.parse.urlencode({
        "client_id":     CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type":    "refresh_token"
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=body, method="POST")
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
    if "access_token" not in data:
        print(f"Token error: {data}")
        sys.exit(1)
    print("Access token obtained.")
    return data["access_token"]


def load_used():
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(SONGS_DIR, exist_ok=True)
    if os.path.exists(USED_FILE):
        with open(USED_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []


def save_used(used):
    with open(USED_FILE, "w", encoding="utf-8") as f:
        json.dump(used, f, ensure_ascii=False, indent=2)


def parse_lyrics_md(lyrics_file):
    title, description, tags = "", "", []
    if not os.path.exists(lyrics_file):
        return title, description, tags
    with open(lyrics_file, encoding="utf-8") as f:
        content = f.read()
    if "## YOUTUBE TITLE:" in content:
        after = content.split("## YOUTUBE TITLE:")[1]
        title = after.split("##")[0].strip()
    if "## YOUTUBE DESCRIPTION:" in content and "## YOUTUBE TAGS:" in content:
        after = content.split("## YOUTUBE DESCRIPTION:")[1]
        description = after.split("## YOUTUBE TAGS:")[0].strip()
    if "## YOUTUBE TAGS:" in content:
        after = content.split("## YOUTUBE TAGS:")[1].strip()
        tags = [t.strip() for t in after.split(",") if t.strip()]
    return title, description, tags


def make_video(audio_path, song_name):
    os.makedirs(TEMP_DIR, exist_ok=True)
    bg_image = next((os.path.join(BG_DIR, f"{song_name}.{ext}") for ext in ["jpg", "png"]
                     if os.path.exists(os.path.join(BG_DIR, f"{song_name}.{ext}"))), None)

    if bg_image:
        print(f"Using background: {bg_image}")
        cmd = [
            FFMPEG, "-y",
            "-loop", "1", "-i", bg_image,
            "-i", audio_path,
            "-c:v", "libx264", "-preset", "fast", "-crf", "28",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest", "-movflags", "+faststart",
            "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080",
            OUTPUT_VIDEO
        ]
    else:
        print("No background found — using black background.")
        cmd = [
            FFMPEG, "-y",
            "-f", "lavfi", "-i", "color=c=black:size=1920x1080:rate=1",
            "-i", audio_path,
            "-c:v", "libx264", "-preset", "fast", "-crf", "28",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest", "-movflags", "+faststart",
            OUTPUT_VIDEO
        ]
    subprocess.run(cmd, check=True)
    size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
    print(f"Video created: {OUTPUT_VIDEO} ({size_mb:.1f} MB)")
    return OUTPUT_VIDEO


def upload_to_youtube(access_token, video_path, title, description, tags):
    metadata = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags,
            "categoryId": "10",
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        }
    }
    meta_bytes = json.dumps(metadata).encode()
    init_req = urllib.request.Request(UPLOAD_URL, data=meta_bytes, method="POST")
    init_req.add_header("Authorization", f"Bearer {access_token}")
    init_req.add_header("Content-Type", "application/json")
    init_req.add_header("X-Upload-Content-Type", "video/mp4")
    init_req.add_header("X-Upload-Content-Length", str(os.path.getsize(video_path)))
    with urllib.request.urlopen(init_req) as r:
        upload_uri = r.getheader("Location")
    print(f"Uploading {os.path.getsize(video_path) // (1024*1024)} MB...")
    with open(video_path, "rb") as f:
        video_data = f.read()
    upload_req = urllib.request.Request(upload_uri, data=video_data, method="PUT")
    upload_req.add_header("Content-Type", "video/mp4")
    with urllib.request.urlopen(upload_req) as r:
        result = json.loads(r.read())
    video_id = result.get("id", "")
    print(f"Upload complete! https://www.youtube.com/watch?v={video_id}")
    return video_id


def main():
    if not all([CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN]):
        print("ERROR: YouTube credentials not set")
        sys.exit(1)

    songs = [f for f in os.listdir(AUDIO_DIR) if f.endswith(".mp3")]
    if not songs:
        print(f"ERROR: No MP3 files in {AUDIO_DIR}")
        sys.exit(1)

    used = load_used()
    unused = [s for s in songs if s not in used]
    if not unused:
        print("All songs used — resetting cycle.")
        used = []
        unused = songs

    song_file = random.choice(unused)
    used.append(song_file)
    save_used(used)

    song_name  = os.path.splitext(song_file)[0]
    audio_path = os.path.join(AUDIO_DIR, song_file)
    lyrics_file = os.path.join(LYRICS_DIR, f"{song_name}.md")

    print(f"Song: {song_file}")

    title, description, tags = parse_lyrics_md(lyrics_file)
    if not title:
        title = song_name.replace("_", " ").title()
    if not description:
        description = f"{title} — SUNYAMusic"
    if not tags:
        tags = ["nepali song", "nepali folk", "SUNYAMusic"]

    print(f"Title: {title}")

    video_path   = make_video(audio_path, song_name)
    access_token = get_access_token()
    upload_to_youtube(access_token, video_path, title, description, tags)


if __name__ == "__main__":
    main()
