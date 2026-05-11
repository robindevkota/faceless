#!/usr/bin/env python3
"""
upload_meditation.py — stitches all MP3s in a random meditation type folder
into one long video and uploads to SUNYAMusic YouTube channel.

Folder structure:
  sunya-music/meditation/peace/audio/    ← MP3s
  sunya-music/meditation/peace/bg.jpg    ← background image
  sunya-music/meditation/peace/title.txt ← YouTube title
  (same for sleep, focus, healing)
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

BASE_DIR       = os.path.join(os.path.dirname(__file__), "..")
MEDITATION_DIR = os.path.join(BASE_DIR, "meditation")
TEMP_DIR       = os.path.join(MEDITATION_DIR, "temp")
USED_FILE      = os.path.join(TEMP_DIR, "used_types.json")
OUTPUT_VIDEO   = os.path.join(TEMP_DIR, "meditation_output.mp4")
CONCAT_LIST    = os.path.join(TEMP_DIR, "concat.txt")

TYPES = ["peace", "sleep", "focus", "healing", "rain"]

TOKEN_URL  = "https://oauth2.googleapis.com/token"
UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"

if platform.system() == "Windows":
    _ff = r"C:\Users\user\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin"
    FFMPEG = os.path.join(_ff, "ffmpeg.exe")
else:
    FFMPEG = "ffmpeg"

DESCRIPTIONS = {
    "peace": """Peaceful Meditation Music for Inner Peace & Calm 🌿

Let this soothing music wash away your stress and bring deep tranquility to your mind and body.
Perfect for meditation, yoga, relaxation, and unwinding after a long day.

✨ Benefits:
• Reduces stress and anxiety
• Promotes inner peace and calm
• Perfect for meditation and yoga
• Helps with relaxation and mindfulness

🎵 SUNYAMusic — Sounds for the Soul

#meditationmusic #peacefulmusic #relaxingmusic #innerpeace #calmmusic #stressrelief #yoga #mindfulness #sunyamusic""",

    "sleep": """Deep Sleep Music for Peaceful Rest 🌙

Drift into a deep, restful sleep with this calming music. Designed to quiet your mind and help you fall asleep naturally.

✨ Benefits:
• Helps you fall asleep faster
• Promotes deep, restful sleep
• Reduces nighttime anxiety
• Peaceful dreams

🎵 SUNYAMusic — Sounds for the Soul

#sleepmusic #deepsleeep #relaxingmusic #calmmusic #sleepmeditation #peacefulnight #sunyamusic""",

    "focus": """Focus Music for Deep Work & Study 🎯

Boost your concentration and productivity with this calming background music. Designed to help you enter a flow state.

✨ Benefits:
• Improves focus and concentration
• Boosts productivity
• Reduces distractions
• Perfect for studying and deep work

🎵 SUNYAMusic — Sounds for the Soul

#focusmusic #studymusic #concentration #productivity #workmusic #deepwork #flowstate #sunyamusic""",

    "rain": """Rain & Thunder Sounds for Deep Sleep 🌧️

Let the soothing sound of rainfall and distant thunder lull you into a deep, peaceful sleep.
Perfect for sleep, relaxation, studying, or simply unwinding.

✨ Benefits:
• Blocks out background noise
• Helps you fall asleep faster
• Deep relaxation and stress relief
• Perfect white noise for sleep and focus

🎵 SUNYAMusic — Sounds for the Soul

#rainsounds #thundersounds #sleepmusic #rainfordeepsleep #whitenoise #relaxingsounds #stormsounds #sunyamusic""",

    "healing": """Healing Meditation Music | Positive Energy & Stress Relief 💚

Allow this healing music to restore balance and harmony to your mind, body and spirit.

✨ Benefits:
• Deep emotional healing
• Releases stress and tension
• Restores positive energy
• Balances mind, body and spirit

🎵 SUNYAMusic — Sounds for the Soul

#healingmusic #432hz #meditationmusic #positiveenergy #stressrelief #healing #sunyamusic""",
}

TAGS = {
    "peace":   ["meditation music", "peaceful music", "relaxing music", "inner peace", "calm music", "stress relief", "yoga music", "mindfulness", "SUNYAMusic"],
    "sleep":   ["sleep music", "deep sleep", "relaxing music", "calm music", "sleep meditation", "peaceful night", "insomnia relief", "SUNYAMusic"],
    "focus":   ["focus music", "study music", "concentration music", "productivity music", "work music", "deep work", "flow state", "SUNYAMusic"],
    "healing": ["healing music", "432hz", "meditation music", "positive energy", "stress relief", "healing frequency", "SUNYAMusic"],
    "rain":    ["rain sounds", "thunder sounds", "sleep music", "rain for sleep", "white noise", "relaxing rain", "storm sounds", "SUNYAMusic"],
}


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


def pick_type(used):
    """Pick the least-recently-used meditation type."""
    used_list = used.get("order", [])
    unused = [t for t in TYPES if t not in used_list]
    if not unused:
        # all used — reset cycle
        print("All meditation types used — resetting cycle.")
        used_list = []
        unused = TYPES
    chosen = random.choice(unused)
    used_list.append(chosen)
    used["order"] = used_list
    return chosen


def stitch_audio(audio_dir):
    """Concatenate all MP3s in the folder into one file."""
    mp3s = sorted([f for f in os.listdir(audio_dir) if f.endswith(".mp3")])
    if not mp3s:
        print(f"ERROR: No MP3 files in {audio_dir}")
        sys.exit(1)

    print(f"Stitching {len(mp3s)} tracks: {mp3s}")

    os.makedirs(TEMP_DIR, exist_ok=True)

    # write concat list
    with open(CONCAT_LIST, "w") as f:
        for mp3 in mp3s:
            path = os.path.join(audio_dir, mp3).replace("\\", "/")
            f.write(f"file '{path}'\n")

    concat_audio = os.path.join(TEMP_DIR, "stitched.mp3")
    cmd = [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", CONCAT_LIST,
           "-c", "copy", concat_audio]
    subprocess.run(cmd, check=True)

    duration = get_duration(concat_audio)
    print(f"Total audio duration: {duration:.0f}s ({duration/60:.1f} min)")
    return concat_audio


def get_duration(audio_path):
    cmd = [FFMPEG, "-i", audio_path, "-f", "null", "-"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    for line in result.stderr.split("\n"):
        if "Duration" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = parts.split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    return 0


def make_video(audio_path, type_dir):
    bg = next((os.path.join(type_dir, f"bg.{ext}") for ext in ["jpg", "png"]
               if os.path.exists(os.path.join(type_dir, f"bg.{ext}"))), None)

    if bg:
        print(f"Using background: {bg}")
        cmd = [
            FFMPEG, "-y",
            "-loop", "1", "-i", bg,
            "-i", audio_path,
            "-c:v", "libx264", "-preset", "fast", "-crf", "28",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            "-movflags", "+faststart",
            "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080",
            OUTPUT_VIDEO
        ]
    else:
        print("No background image found — using black background.")
        cmd = [
            FFMPEG, "-y",
            "-f", "lavfi", "-i", "color=c=black:size=1920x1080:rate=1",
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

    size_mb = os.path.getsize(video_path) // (1024 * 1024)
    print(f"Uploading {size_mb} MB to YouTube...")

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

    used = load_used()
    meditation_type = pick_type(used)
    save_used(used)

    type_dir  = os.path.join(MEDITATION_DIR, meditation_type)
    audio_dir = os.path.join(type_dir, "audio")

    print(f"Meditation type: {meditation_type}")

    if not os.path.isdir(audio_dir):
        print(f"ERROR: {audio_dir} not found")
        sys.exit(1)

    # read title
    title_file = os.path.join(type_dir, "title.txt")
    title = open(title_file, encoding="utf-8").read().strip() if os.path.exists(title_file) else f"{meditation_type.title()} Meditation Music | SUNYAMusic"

    description = DESCRIPTIONS.get(meditation_type, f"{meditation_type.title()} meditation music — SUNYAMusic")
    tags        = TAGS.get(meditation_type, ["meditation", "SUNYAMusic"])

    stitched_audio = stitch_audio(audio_dir)
    video_path     = make_video(stitched_audio, type_dir)

    access_token = get_access_token()
    upload_to_youtube(access_token, video_path, title, description, tags)


if __name__ == "__main__":
    main()
