#!/usr/bin/env python3
"""
upload_music.py — picks a random unused song from ./audio/ and uploads to SUNYAMusic YouTube channel
Reads:  ./audio/*.mp3        (your Suno songs)
        ./audio/songs.json   (optional metadata: title, description per song)
Writes: ./temp/used_songs.json  (tracks which songs have been posted)
"""

import os
import sys
import json
import random
import subprocess
import urllib.request
import urllib.parse
import urllib.error
import platform

# load .env from parent folder
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

AUDIO_DIR      = os.path.join(os.path.dirname(__file__), "..", "audio")
TEMP_DIR       = os.path.join(os.path.dirname(__file__), "..", "temp")
USED_FILE      = os.path.join(TEMP_DIR, "used_songs.json")
SONGS_META     = os.path.join(AUDIO_DIR, "songs.json")
OUTPUT_VIDEO   = os.path.join(TEMP_DIR, "music_output.mp4")

# background image for video (place a bg.jpg in sunya-music/ or we use black)
BG_IMAGE = os.path.join(os.path.dirname(__file__), "..", "bg.jpg")

if platform.system() == "Windows":
    _ff = r"C:\Users\user\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin"
    FFMPEG  = os.path.join(_ff, "ffmpeg.exe")
else:
    FFMPEG = "ffmpeg"

TOKEN_URL  = "https://oauth2.googleapis.com/token"
UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"


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
    if os.path.exists(USED_FILE):
        with open(USED_FILE) as f:
            return json.load(f)
    return []


def save_used(used):
    with open(USED_FILE, "w") as f:
        json.dump(used, f)


def get_songs():
    songs = [
        f for f in os.listdir(AUDIO_DIR)
        if f.endswith(".mp3")
    ]
    return songs


def load_metadata():
    if os.path.exists(SONGS_META):
        with open(SONGS_META, encoding="utf-8") as f:
            return json.load(f)
    return {}


def make_video(audio_path: str, title: str) -> str:
    os.makedirs(TEMP_DIR, exist_ok=True)

    if os.path.exists(BG_IMAGE):
        # use background image
        cmd = [
            FFMPEG, "-y",
            "-loop", "1", "-i", BG_IMAGE,
            "-i", audio_path,
            "-c:v", "libx264", "-preset", "fast", "-crf", "28",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            "-movflags", "+faststart",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
            OUTPUT_VIDEO
        ]
    else:
        # black background
        cmd = [
            FFMPEG, "-y",
            "-f", "lavfi", "-i", "color=c=black:size=1080x1920:rate=1",
            "-i", audio_path,
            "-c:v", "libx264", "-preset", "fast", "-crf", "28",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            "-movflags", "+faststart",
            OUTPUT_VIDEO
        ]
    subprocess.run(cmd, check=True)
    size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
    print(f"Video created: {OUTPUT_VIDEO} ({size_mb:.1f} MB)")
    return OUTPUT_VIDEO


def upload_to_youtube(access_token: str, video_path: str, title: str, description: str, tags: list):
    metadata = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags,
            "categoryId": "10",  # Music category
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

    print(f"Upload URI obtained. Uploading {os.path.getsize(video_path) // (1024*1024)} MB...")

    with open(video_path, "rb") as f:
        video_data = f.read()

    upload_req = urllib.request.Request(upload_uri, data=video_data, method="PUT")
    upload_req.add_header("Content-Type", "video/mp4")

    with urllib.request.urlopen(upload_req) as r:
        result = json.loads(r.read())

    video_id = result.get("id", "")
    print(f"YouTube upload complete! Video ID: {video_id}")
    print(f"URL: https://www.youtube.com/watch?v={video_id}")
    return video_id


def main():
    if not all([CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN]):
        print("ERROR: YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_MUSIC_REFRESH_TOKEN must be set in .env")
        sys.exit(1)

    songs = get_songs()
    if not songs:
        print(f"ERROR: No .mp3 files found in {AUDIO_DIR}")
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

    audio_path = os.path.join(AUDIO_DIR, song_file)
    print(f"Selected: {song_file} ({len(used)}/{len(songs)})")

    # get metadata from songs.json or use filename
    metadata = load_metadata()
    song_name = os.path.splitext(song_file)[0]
    song_info = metadata.get(song_file, metadata.get(song_name, {}))

    title       = song_info.get("title", song_name)
    description = song_info.get("description", f"{title} — AI generated music by SUNYAMusic")
    tags        = song_info.get("tags", ["music", "aimusic", "suno", "relaxing", "SUNYAMusic"])

    print(f"Title: {title}")

    video_path = make_video(audio_path, title)
    access_token = get_access_token()
    upload_to_youtube(access_token, video_path, title, description, tags)


if __name__ == "__main__":
    main()
