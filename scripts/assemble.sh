#!/bin/bash
# assemble.sh — builds final MP4 from stock clips + voice + music + subtitles

set -e

STOCK_DIR="./stock"
MUSIC_DIR="./music"
TEMP_DIR="./temp"

mkdir -p "$TEMP_DIR"

# ── 1. Pick 4 random stock clips ──────────────────────────────────────────────
mapfile -t ALL_CLIPS < <(ls "$STOCK_DIR"/*.mp4 2>/dev/null)
if [ ${#ALL_CLIPS[@]} -lt 1 ]; then
  echo "ERROR: No stock clips found in $STOCK_DIR"
  exit 1
fi

# Shuffle and pick up to 4
mapfile -t CLIPS < <(printf '%s\n' "${ALL_CLIPS[@]}" | shuf | head -n 4)

# ── 2. Pick 1 valid music track (verify it's real audio) ─────────────────────
MUSIC=""
mapfile -t ALL_MUSIC < <(ls "$MUSIC_DIR"/*.mp3 2>/dev/null)
for candidate in "${ALL_MUSIC[@]}"; do
  # Check if ffprobe sees an audio stream
  if ffprobe -v error -select_streams a -show_entries stream=codec_type \
     -of default=noprint_wrappers=1:nokey=1 "$candidate" 2>/dev/null | grep -q audio; then
    MUSIC="$candidate"
    echo "Using music: $MUSIC"
    break
  else
    echo "Skipping invalid music file: $candidate"
  fi
done
if [ -z "$MUSIC" ]; then
  echo "WARNING: No valid music found — continuing without background music"
fi

# ── 3. Build FFmpeg clip list ─────────────────────────────────────────────────
rm -f "$TEMP_DIR/clips.txt"
for clip in "${CLIPS[@]}"; do
  echo "file '$(realpath "$clip")'" >> "$TEMP_DIR/clips.txt"
done

echo "Using clips:"
cat "$TEMP_DIR/clips.txt"

# ── 4. Generate subtitles from voiceover via Whisper ─────────────────────────
if command -v whisper &> /dev/null; then
  echo "Generating subtitles with Whisper..."
  whisper "$TEMP_DIR/voice.mp3" \
    --model tiny \
    --output_format srt \
    --output_dir "$TEMP_DIR/"
  # whisper names the output file after the input file
  mv -f "$TEMP_DIR/voice.srt" "$TEMP_DIR/subs.srt" 2>/dev/null || true
  SUBTITLE_FILTER=",subtitles=$TEMP_DIR/subs.srt:force_style='FontSize=22,Alignment=2,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2,Bold=1'"
else
  echo "WARNING: whisper not found — skipping subtitles"
  SUBTITLE_FILTER=""
fi

# ── 5. Assemble video ─────────────────────────────────────────────────────────
echo "Assembling video..."

if [ -n "$MUSIC" ]; then
  ffmpeg -y \
    -f concat -safe 0 -i "$TEMP_DIR/clips.txt" \
    -i "$TEMP_DIR/voice.mp3" \
    -i "$MUSIC" \
    -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920${SUBTITLE_FILTER}" \
    -filter_complex "[1:a]volume=1.0[v];[2:a]volume=0.2[m];[v][m]amix=inputs=2:duration=first[audio]" \
    -map 0:v -map "[audio]" \
    -t 60 \
    -c:v libx264 -preset fast -crf 23 \
    -c:a aac -b:a 128k \
    -movflags +faststart \
    "$TEMP_DIR/output.mp4"
else
  ffmpeg -y \
    -f concat -safe 0 -i "$TEMP_DIR/clips.txt" \
    -i "$TEMP_DIR/voice.mp3" \
    -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920${SUBTITLE_FILTER}" \
    -map 0:v -map 1:a \
    -t 60 \
    -c:v libx264 -preset fast -crf 23 \
    -c:a aac -b:a 128k \
    -movflags +faststart \
    "$TEMP_DIR/output.mp4"
fi

echo "Video ready: $TEMP_DIR/output.mp4"
