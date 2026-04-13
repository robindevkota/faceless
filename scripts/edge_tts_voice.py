#!/usr/bin/env python3
"""
edge_tts_voice.py — generates voiceover using Microsoft Edge TTS (100% free, no limits)
Reads:  ./temp/script.json
Writes: ./temp/voice.mp3
"""

import asyncio
import json
import os
import sys

try:
    import edge_tts
except ImportError:
    print("edge-tts not installed. Run: pip install edge-tts")
    sys.exit(1)

# ── Config ────────────────────────────────────────────────────────────────────
# Great free voices — pick one:
#   en-US-AriaNeural       female, warm, natural (best overall)
#   en-US-GuyNeural        male, professional
#   en-US-JennyNeural      female, friendly
#   en-GB-SoniaNeural      female, British accent
#   en-AU-NatashaNeural    female, Australian accent
VOICE = "en-US-AriaNeural"

INPUT_FILE  = "./temp/script.json"
OUTPUT_FILE = "./temp/voice.mp3"

# ── Main ──────────────────────────────────────────────────────────────────────

async def generate_voice(text: str, voice: str, output: str):
    communicate = edge_tts.Communicate(text, voice=voice, rate="+5%", volume="+0%")
    await communicate.save(output)
    size_kb = os.path.getsize(output) // 1024
    print(f"Voice saved to {output} ({size_kb} KB)")


def main():
    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: {INPUT_FILE} not found. Run gemini_script.py first.")
        sys.exit(1)

    with open(INPUT_FILE, encoding="utf-8") as f:
        data = json.load(f)

    script = data.get("script", "").strip()
    if not script:
        print("ERROR: 'script' field is empty in script.json")
        sys.exit(1)

    print(f"Generating voice with {VOICE}...")
    print(f"Script length: {len(script)} chars")

    os.makedirs("./temp", exist_ok=True)
    asyncio.run(generate_voice(script, VOICE, OUTPUT_FILE))


if __name__ == "__main__":
    main()
