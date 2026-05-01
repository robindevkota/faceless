#!/usr/bin/env python3
"""
assemble_video.py — combines stock clips + voiceover into final 9:16 short
Reads:  ./temp/voice.mp3       (voiceover)
        ./stock/               (stock video clips)
Writes: ./temp/output.mp4      (final video, ready to upload)
Requires: ffmpeg in PATH
"""

import os
import sys
import json
import random
import subprocess
import tempfile

VOICE_FILE  = "./temp/voice.mp3"
SCRIPT_FILE = "./temp/script.json"
STOCK_DIR   = "./stock"
MUSIC_DIR   = "./music"
OUTPUT_FILE = "./temp/output.mp4"
TEMP_DIR    = "./temp"

import platform
if platform.system() == "Windows":
    _ff = r"C:\Users\user\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin"
    FFMPEG  = os.path.join(_ff, "ffmpeg.exe")
    FFPROBE = os.path.join(_ff, "ffprobe.exe")
else:
    FFMPEG  = "ffmpeg"
    FFPROBE = "ffprobe"

# 9:16 vertical (Shorts/Reels format)
WIDTH  = 1080
HEIGHT = 1920


def check_ffmpeg():
    try:
        subprocess.run([FFMPEG, "-version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: ffmpeg not found. Install from https://ffmpeg.org/download.html")
        sys.exit(1)


def get_duration(path: str) -> float:
    result = subprocess.run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())


def get_stock_clips() -> list:
    clips = [
        os.path.join(STOCK_DIR, f)
        for f in os.listdir(STOCK_DIR)
        if f.endswith(".mp4")
    ]
    if not clips:
        print(f"ERROR: No stock clips found in {STOCK_DIR}. Run download_assets.py first.")
        sys.exit(1)
    return clips


def get_music_file() -> str | None:
    if not os.path.exists(MUSIC_DIR):
        return None
    tracks = [
        os.path.join(MUSIC_DIR, f)
        for f in os.listdir(MUSIC_DIR)
        if f.endswith(".mp3")
    ]
    return random.choice(tracks) if tracks else None


def build_video(voice_path: str, clips: list, voice_duration: float, title: str):
    os.makedirs(TEMP_DIR, exist_ok=True)

    # shuffle clips for variety
    random.shuffle(clips)

    # build a concat list — repeat clips until we cover voice duration
    concat_list_path = os.path.join(TEMP_DIR, "concat.txt")
    total = 0.0
    used_clips = []
    clip_pool = clips * 10  # repeat pool so we never run out

    for clip in clip_pool:
        if total >= voice_duration + 1:
            break
        try:
            d = get_duration(clip)
            used_clips.append(clip)
            total += d
        except Exception:
            continue

    if not used_clips:
        print("ERROR: Could not read any stock clips.")
        sys.exit(1)

    # write concat file
    with open(concat_list_path, "w") as f:
        for clip in used_clips:
            abs_path = os.path.abspath(clip).replace("\\", "/")
            f.write(f"file '{abs_path}'\n")

    # step 1: concat + scale to 9:16, trim to voice duration
    raw_video = os.path.join(TEMP_DIR, "raw_video.mp4")
    subprocess.run([
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0", "-i", concat_list_path,
        "-t", str(voice_duration),
        "-vf", f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
               f"crop={WIDTH}:{HEIGHT},setsar=1",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-an", raw_video
    ], check=True)

    # step 2: add title text overlay + voiceover (+ optional background music)
    music_file = get_music_file()
    # clean title — remove non-ASCII chars, escape special chars for ffmpeg
    safe_title = title.encode("ascii", "ignore").decode()
    safe_title = safe_title.replace("'", "").replace(":", " ").replace("\\", "").replace("%", "")[:55]

    # write title to a file to avoid shell escaping issues
    title_file = os.path.join(TEMP_DIR, "title.txt")
    with open(title_file, "w", encoding="ascii", errors="ignore") as f:
        f.write(safe_title)

    # text overlay filter — bold white text at bottom (no fontconfig needed)
    text_filter = (
        f"drawtext=textfile='{title_file.replace(chr(92), '/')}'"
        f":fontsize=48:fontcolor=white:borderw=3:bordercolor=black"
        f":x=(w-text_w)/2:y=h*0.88:line_spacing=8"
    )

    if music_file:
        subprocess.run([
            FFMPEG, "-y",
            "-i", raw_video,
            "-i", os.path.abspath(voice_path),
            "-i", os.path.abspath(music_file),
            "-filter_complex",
                "[2:a]volume=0.08[music];"
                "[1:a][music]amix=inputs=2:duration=first[a]",
            "-map", "0:v", "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-t", str(voice_duration),
            "-movflags", "+faststart",
            OUTPUT_FILE
        ], check=True)
    else:
        subprocess.run([
            FFMPEG, "-y",
            "-i", raw_video,
            "-i", os.path.abspath(voice_path),
            "-map", "0:v", "-map", "1:a",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-t", str(voice_duration),
            "-movflags", "+faststart",
            OUTPUT_FILE
        ], check=True)

    size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print(f"Video assembled: {OUTPUT_FILE} ({size_mb:.1f} MB, {voice_duration:.1f}s)")


def main():
    check_ffmpeg()

    if not os.path.exists(VOICE_FILE):
        print(f"ERROR: {VOICE_FILE} not found. Run edge_tts_voice.py first.")
        sys.exit(1)

    if not os.path.exists(SCRIPT_FILE):
        print(f"ERROR: {SCRIPT_FILE} not found. Run gemini_script.py first.")
        sys.exit(1)

    with open(SCRIPT_FILE, encoding="utf-8") as f:
        script_data = json.load(f)

    title = script_data.get("title", "Mind Fact Daily")
    voice_duration = get_duration(VOICE_FILE)
    print(f"Voice duration: {voice_duration:.1f}s")
    print(f"Title: {title}")

    clips = get_stock_clips()
    print(f"Found {len(clips)} stock clips")

    build_video(VOICE_FILE, clips, voice_duration, title)


if __name__ == "__main__":
    main()
