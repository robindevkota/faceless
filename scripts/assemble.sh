#!/bin/bash
# assemble.sh — builds final MP4 from stock clips + voice + subtitles

set -e

STOCK_DIR="./stock"
TEMP_DIR="./temp"

mkdir -p "$TEMP_DIR/clips_normalized"

# ── 1. Pick 4 random stock clips ──────────────────────────────────────────────
mapfile -t ALL_CLIPS < <(ls "$STOCK_DIR"/*.mp4 2>/dev/null)
if [ ${#ALL_CLIPS[@]} -lt 1 ]; then
  echo "ERROR: No stock clips found in $STOCK_DIR"
  exit 1
fi
mapfile -t CLIPS < <(printf '%s\n' "${ALL_CLIPS[@]}" | shuf | head -n 4)
echo "Selected clips:"
printf '%s\n' "${CLIPS[@]}"

# ── 2. Normalize each clip to same resolution/fps/format ─────────────────────
echo "Normalizing clips to 1080x1920 portrait..."
rm -f "$TEMP_DIR/clips.txt"
i=0
for clip in "${CLIPS[@]}"; do
  out="$TEMP_DIR/clips_normalized/clip_${i}.mp4"
  # Loop each clip to ensure minimum 15 seconds, then trim to 15s
  ffmpeg -y -stream_loop -1 -i "$clip" \
    -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" \
    -r 30 -t 15 -c:v libx264 -preset fast -crf 23 \
    -an \
    "$out" 2>/dev/null
  echo "file '$(realpath "$out")'" >> "$TEMP_DIR/clips.txt"
  i=$((i+1))
done

echo "Clip list:"
cat "$TEMP_DIR/clips.txt"

# ── 3. Generate subtitles via Whisper ─────────────────────────────────────────
SUBTITLE_FILTER=""
if command -v whisper &> /dev/null; then
  echo "Generating subtitles..."
  whisper "$TEMP_DIR/voice.mp3" \
    --model tiny \
    --output_format srt \
    --output_dir "$TEMP_DIR/" 2>/dev/null
  mv -f "$TEMP_DIR/voice.srt" "$TEMP_DIR/subs.srt" 2>/dev/null || true
  if [ -f "$TEMP_DIR/subs.srt" ]; then
    SUBTITLE_FILTER=",subtitles=$TEMP_DIR/subs.srt:force_style='FontSize=20,Alignment=2,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2,Bold=1'"
    echo "Subtitles ready."
  fi
else
  echo "Whisper not found — skipping subtitles"
fi

# ── 4. Concat clips + add voiceover ──────────────────────────────────────────
echo "Assembling final video..."
ffmpeg -y \
  -f concat -safe 0 -i "$TEMP_DIR/clips.txt" \
  -i "$TEMP_DIR/voice.mp3" \
  -vf "scale=1080:1920${SUBTITLE_FILTER}" \
  -map 0:v -map 1:a \
  -t 60 \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  "$TEMP_DIR/output.mp4"

echo "Video ready: $TEMP_DIR/output.mp4"
