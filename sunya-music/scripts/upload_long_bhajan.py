#!/usr/bin/env python3
"""
upload_long_bhajan.py — stitches all 4 bhajans for today's day into one long video
and uploads to SUNYAMusic YouTube channel.
"""

import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
import json
import subprocess
import urllib.request
import urllib.parse
import platform
from datetime import datetime, timezone, timedelta

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

BASE_DIR     = os.path.join(os.path.dirname(__file__), "..")
AUDIO_DIR    = os.path.join(BASE_DIR, "audio")
LYRICS_DIR   = os.path.join(BASE_DIR, "lyrics")
BG_DIR       = os.path.join(BASE_DIR, "backgrounds")
TEMP_DIR     = os.path.join(BASE_DIR, "temp")
CONCAT_LIST  = os.path.join(TEMP_DIR, "long_concat.txt")
OUTPUT_VIDEO = os.path.join(TEMP_DIR, "long_bhajan_output.mp4")

DAY_MAP = {
    0: ("monday",    "shiva",   "शिव"),
    1: ("tuesday",   "hanuman", "हनुमान"),
    2: ("wednesday", "ganesha", "गणेश"),
    3: ("thursday",  "vishnu",  "विष्णु"),
    4: ("friday",    "lakshmi", "लक्ष्मी"),
    5: ("saturday",  "shani",   "शनि"),
    6: ("sunday",    "surya",   "सूर्य"),
}

LONG_TITLES = {
    "monday":    "शिव भजन संग्रह | Complete Shiva Bhajan Collection | Monday Special | सोमवार भजन",
    "tuesday":   "हनुमान भजन संग्रह | Complete Hanuman Bhajan Collection | Tuesday Special | मंगलवार भजन",
    "wednesday": "गणेश भजन संग्रह | Complete Ganesha Bhajan Collection | Wednesday Special | बुधवार भजन",
    "thursday":  "विष्णु भजन संग्रह | Complete Vishnu Bhajan Collection | Thursday Special | गुरुवार भजन",
    "friday":    "लक्ष्मी भजन संग्रह | Complete Lakshmi Bhajan Collection | Friday Special | शुक्रवार भजन",
    "saturday":  "शनि भजन संग्रह | Complete Shani Bhajan Collection | Saturday Special | शनिवार भजन",
    "sunday":    "सूर्य भजन संग्रह | Complete Surya Bhajan Collection | Sunday Special | रविवार भजन",
}

LONG_DESCRIPTIONS = {
    "monday":    "सोमवार विशेष - भगवान शिव के चार सुंदर भजनों का संग्रह\nॐ नमः शिवाय - महादेव की भक्ति में डूब जाएं।\n\n🎵 SUNYAMusic — Sounds for the Soul\n\n#shivabhajan #mondaybhajan #hindibhajan #mahashiv #sunyamusic",
    "tuesday":   "मंगलवार विशेष - श्री हनुमान जी के चार सुंदर भजनों का संग्रह\nजय हनुमान - बजरंगबली की भक्ति में डूब जाएं।\n\n🎵 SUNYAMusic — Sounds for the Soul\n\n#hanumaanbhajan #tuesdaybhajan #hindibhajan #bajrangbali #sunyamusic",
    "wednesday": "बुधवार विशेष - भगवान गणेश के चार सुंदर भजनों का संग्रह\nॐ गं गणपतये नमः - गणपति की भक्ति में डूब जाएं।\n\n🎵 SUNYAMusic — Sounds for the Soul\n\n#ganeshabhajan #wednesdaybhajan #hindibhajan #ganpati #sunyamusic",
    "thursday":  "गुरुवार विशेष - भगवान विष्णु के चार सुंदर भजनों का संग्रह\nॐ नमो नारायण - विष्णु भगवान की भक्ति में डूब जाएं।\n\n🎵 SUNYAMusic — Sounds for the Soul\n\n#vishnubhajan #thursdaybhajan #hindibhajan #narayana #sunyamusic",
    "friday":    "शुक्रवार विशेष - माँ लक्ष्मी के चार सुंदर भजनों का संग्रह\nॐ श्री महालक्ष्म्यै नमः - लक्ष्मी माँ की भक्ति में डूब जाएं।\n\n🎵 SUNYAMusic — Sounds for the Soul\n\n#lakshmibhajan #fridaybhajan #hindibhajan #mahalakshmi #sunyamusic",
    "saturday":  "शनिवार विशेष - शनि देव के चार सुंदर भजनों का संग्रह\nॐ शं शनिश्चराय नमः - शनि देव की भक्ति में डूब जाएं।\n\n🎵 SUNYAMusic — Sounds for the Soul\n\n#shanibhajan #saturdaybhajan #hindibhajan #shanidev #sunyamusic",
    "sunday":    "रविवार विशेष - सूर्य देव के चार सुंदर भजनों का संग्रह\nॐ सूर्याय नमः - सूर्यदेव की भक्ति में डूब जाएं।\n\n🎵 SUNYAMusic — Sounds for the Soul\n\n#suryabhajan #sundaybhajan #hindibhajan #suryadev #sunyamusic",
}

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


def stitch_audio(audio_day_dir, god_name):
    os.makedirs(TEMP_DIR, exist_ok=True)
    mp3s = sorted([f for f in os.listdir(audio_day_dir) if f.endswith(".mp3")])
    if not mp3s:
        print(f"ERROR: No MP3 files in {audio_day_dir}")
        sys.exit(1)
    print(f"Stitching {len(mp3s)} tracks: {mp3s}")
    with open(CONCAT_LIST, "w") as f:
        for mp3 in mp3s:
            path = os.path.join(audio_day_dir, mp3).replace("\\", "/")
            f.write(f"file '{path}'\n")
    concat_audio = os.path.join(TEMP_DIR, "long_stitched.mp3")
    cmd = [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", CONCAT_LIST, "-c", "copy", concat_audio]
    subprocess.run(cmd, check=True)
    return concat_audio


def make_video(audio_path, day_folder):
    bg_image = next((os.path.join(BG_DIR, f"{day_folder}.{ext}") for ext in ["jpg", "png"]
                     if os.path.exists(os.path.join(BG_DIR, f"{day_folder}.{ext}"))), None)
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
        print("No background — using black.")
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


def upload_to_youtube(access_token, video_path, title, description):
    metadata = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": ["bhajan", "hindi bhajan", "devotional", "SUNYAMusic", "bhajan collection"],
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

    nepal_tz = timezone(timedelta(hours=5, minutes=45))
    weekday  = datetime.now(nepal_tz).weekday()
    day_folder, god_name, god_hindi = DAY_MAP[weekday]

    print(f"Nepal time: {datetime.now(nepal_tz).strftime('%A %H:%M')} → {day_folder} ({god_hindi})")

    audio_day_dir = os.path.join(AUDIO_DIR, day_folder)
    if not os.path.isdir(audio_day_dir):
        print(f"ERROR: {audio_day_dir} not found")
        sys.exit(1)

    title       = LONG_TITLES[day_folder]
    description = LONG_DESCRIPTIONS[day_folder]

    print(f"Title: {title}")

    stitched    = stitch_audio(audio_day_dir, god_name)
    video_path  = make_video(stitched, day_folder)
    access_token = get_access_token()
    upload_to_youtube(access_token, video_path, title, description)


if __name__ == "__main__":
    main()
