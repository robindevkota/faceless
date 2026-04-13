#!/usr/bin/env python3
"""
gemini_script.py — fetches trending topic and generates video script via Gemini API
Usage: python3 gemini_script.py [optional: "manual topic override"]
Output: ./temp/script.json
"""

import sys
import os
import json
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

# ── Config ────────────────────────────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL   = "gemini-1.5-flash"
GEMINI_URL     = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

TRENDS_URL     = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"

# Change this to your niche
NICHE = "personal finance"

# ── Helpers ───────────────────────────────────────────────────────────────────

def fetch_trending_topic():
    """Pull the #1 trending topic from Google Trends RSS."""
    try:
        req = urllib.request.Request(
            TRENDS_URL,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read()
        root = ET.fromstring(data)
        topic = root.find("./channel/item/title").text
        print(f"Trending topic: {topic}")
        return topic
    except Exception as e:
        print(f"WARNING: Could not fetch trending topic ({e}). Using fallback.")
        return "how to save money fast"


def build_prompt(topic: str) -> str:
    return f"""You are a faceless YouTube scriptwriter for a {NICHE} channel.
Today's topic: {topic}

Write a 60-second video script optimised for high retention. Include:
- A strong hook in the first 5 seconds (question, shocking fact, or bold statement)
- 3 key points, each under 15 seconds
- A clear call-to-action at the end (like, subscribe, comment)

Return ONLY valid JSON with these exact fields:
{{
  "script": "full spoken script here — natural, conversational tone",
  "title": "SEO YouTube title under 60 chars",
  "description": "150-word YouTube description with keywords and affiliate placeholder",
  "hashtags": ["tag1","tag2","tag3","tag4","tag5","tag6","tag7","tag8","tag9","tag10"],
  "tiktok_caption": "punchy caption under 150 chars with 3 hashtags",
  "hook": "first sentence only — used as on-screen text overlay"
}}

No extra text. No markdown. JSON only."""


def call_gemini(prompt: str) -> dict:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is not set")

    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 1024
        }
    }).encode()

    req = urllib.request.Request(
        GEMINI_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            response = json.loads(r.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        raise RuntimeError(f"Gemini API error {e.code}: {error_body}")

    raw_text = response["candidates"][0]["content"]["parts"][0]["text"].strip()

    # Strip markdown code fences if Gemini wraps in ```json ... ```
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()

    return json.loads(raw_text)


def save_script(data: dict):
    os.makedirs("./temp", exist_ok=True)
    with open("./temp/script.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Script saved to ./temp/script.json")
    print(f"Title: {data.get('title', '')}")
    print(f"Hook:  {data.get('hook', '')}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # Allow manual topic override via CLI arg
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
        print(f"Using manual topic: {topic}")
    else:
        topic = fetch_trending_topic()

    prompt = build_prompt(topic)
    print("Calling Gemini API...")
    data = call_gemini(prompt)
    save_script(data)


if __name__ == "__main__":
    main()
