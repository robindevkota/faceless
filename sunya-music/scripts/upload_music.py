#!/usr/bin/env python3
"""
upload_music.py — picks today's day folder, uploads one unused song to SUNYAMusic.
Structure:
  sunya-music/audio/monday/   ← mp3s for Monday (Shiva)
  sunya-music/audio/tuesday/  ← mp3s for Tuesday (Hanuman)
  ... etc.
Metadata (title, description, tags) is read from sunya-music/lyrics/dayN_<day>_<god>.md
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
import urllib.error
import platform
from datetime import datetime

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

BASE_DIR    = os.path.join(os.path.dirname(__file__), "..")
AUDIO_DIR   = os.path.join(BASE_DIR, "audio")
LYRICS_DIR  = os.path.join(BASE_DIR, "lyrics")
TEMP_DIR    = os.path.join(BASE_DIR, "temp")
USED_FILE   = os.path.join(TEMP_DIR, "used_songs.json")
OUTPUT_VIDEO = os.path.join(TEMP_DIR, "music_output.mp4")
BG_DIR      = os.path.join(BASE_DIR, "backgrounds")

# day index → (folder name, lyrics file prefix)
DAY_MAP = {
    0: "monday",
    1: "tuesday",
    2: "wednesday",
    3: "thursday",
    4: "friday",
    5: "saturday",
    6: "sunday",
}

if platform.system() == "Windows":
    _ff = r"C:\Users\user\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin"
    FFMPEG = os.path.join(_ff, "ffmpeg.exe")
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
        with open(USED_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_used(used):
    with open(USED_FILE, "w", encoding="utf-8") as f:
        json.dump(used, f, ensure_ascii=False, indent=2)


def parse_lyrics_md(lyrics_file):
    """Extract YOUTUBE TITLE, DESCRIPTION, and TAGS from a lyrics .md file."""
    title, description, tags = "", "", []

    if not os.path.exists(lyrics_file):
        return title, description, tags

    with open(lyrics_file, encoding="utf-8") as f:
        content = f.read()

    # extract title
    if "## YOUTUBE TITLE:" in content:
        after = content.split("## YOUTUBE TITLE:")[1]
        title = after.split("##")[0].strip()

    # extract description (everything between YOUTUBE DESCRIPTION: and YOUTUBE TAGS:)
    if "## YOUTUBE DESCRIPTION:" in content and "## YOUTUBE TAGS:" in content:
        after = content.split("## YOUTUBE DESCRIPTION:")[1]
        description = after.split("## YOUTUBE TAGS:")[0].strip()

    # extract tags (comma-separated last section)
    if "## YOUTUBE TAGS:" in content:
        after = content.split("## YOUTUBE TAGS:")[1].strip()
        tags = [t.strip() for t in after.split(",") if t.strip()]

    return title, description, tags


def make_video(audio_path, day_folder):
    os.makedirs(TEMP_DIR, exist_ok=True)

    bg_image = next((os.path.join(BG_DIR, f"{day_folder}.{ext}") for ext in ["jpg", "png"] if os.path.exists(os.path.join(BG_DIR, f"{day_folder}.{ext}"))), None)

    if bg_image:
        print(f"Using background: {bg_image}")
        cmd = [
            FFMPEG, "-y",
            "-loop", "1", "-i", bg_image,
            "-i", audio_path,
            "-c:v", "libx264", "-preset", "fast", "-crf", "28",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            "-movflags", "+faststart",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
            OUTPUT_VIDEO
        ]
    else:
        print("No background image found — using black background.")
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


def upload_to_youtube(access_token, video_path, title, description, tags):
    metadata = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags,
            "categoryId": "10",  # Music
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
        print("ERROR: YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_MUSIC_REFRESH_TOKEN must be set")
        sys.exit(1)

    # get today's day (0=Monday, 6=Sunday)
    weekday = datetime.utcnow().weekday()
    day_folder = DAY_MAP[weekday]

    audio_day_dir = os.path.join(AUDIO_DIR, day_folder)
    if not os.path.isdir(audio_day_dir):
        print(f"ERROR: No folder found at {audio_day_dir} — create it and add mp3 files.")
        sys.exit(1)

    songs = [f for f in os.listdir(audio_day_dir) if f.endswith(".mp3")]
    if not songs:
        print(f"ERROR: No .mp3 files in {audio_day_dir}")
        sys.exit(1)

    # track used songs per day folder
    used = load_used()
    used_for_day = used.get(day_folder, [])
    unused = [s for s in songs if s not in used_for_day]

    if not unused:
        print(f"All {day_folder} songs used — resetting cycle.")
        used_for_day = []
        unused = songs

    song_file = random.choice(unused)
    used_for_day.append(song_file)
    used[day_folder] = used_for_day
    save_used(used)

    audio_path = os.path.join(audio_day_dir, song_file)
    print(f"Day: {day_folder} | Song: {song_file} ({len(used_for_day)}/{len(songs)})")

    # pick a random lyrics file from the day's lyrics subfolder
    lyrics_day_dir = os.path.join(LYRICS_DIR, day_folder)
    lyrics_files = [f for f in os.listdir(lyrics_day_dir) if f.endswith(".md")] if os.path.isdir(lyrics_day_dir) else []
    lyrics_file = os.path.join(lyrics_day_dir, random.choice(lyrics_files)) if lyrics_files else None
    title, description, tags = parse_lyrics_md(lyrics_file) if lyrics_file else ("", "", [])

    if not title:
        title = os.path.splitext(song_file)[0]
    if not description:
        description = f"{title} — SUNYAMusic"
    if not tags:
        tags = ["bhajan", "hindi bhajan", "devotional", "SUNYAMusic"]

    print(f"Title: {title}")

    video_path = make_video(audio_path, day_folder)
    access_token = get_access_token()
    upload_to_youtube(access_token, video_path, title, description, tags)


if __name__ == "__main__":
    main()
