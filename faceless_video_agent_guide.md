# Faceless Video Agent — Complete Blueprint

> **Budget:** $11/month | **Goal:** $300–$500/month | **Human input:** ~0 min/day

---

## Table of Contents

1. [Overview](#overview)
2. [Full Tech Stack](#full-tech-stack)
3. [Budget Breakdown](#budget-breakdown)
4. [How the Pipeline Works](#how-the-pipeline-works)
5. [Server Options — No Credit Card Needed](#server-options--no-credit-card-needed)
6. [Setup Guide](#setup-guide)
7. [Gemini API Script Prompt](#gemini-api-script-prompt)
8. [FFmpeg Video Assembly](#ffmpeg-video-assembly)
9. [GitHub Actions Workflow](#github-actions-workflow)
10. [n8n Workflow Structure](#n8n-workflow-structure)
11. [Niche Selection](#niche-selection)
12. [Quality Tips](#quality-tips)
13. [Revenue Timeline](#revenue-timeline)
14. [Video Tool Decision Guide](#video-tool-decision-guide)
15. [Honest Warnings](#honest-warnings)

---

## Overview

This system automatically produces and publishes one faceless video per day to YouTube, TikTok, and Facebook — with zero daily input from you after setup.

**The full loop runs in ~2 minutes:**

```
Daily cron (6am)
  → Google Trends (free topic)
  → Gemini 2.5 Flash-Lite API (free script + title + tags)
  → ElevenLabs API ($11/mo voiceover)
  → FFmpeg (free video assembly)
  → YouTube + TikTok + Facebook APIs (free publish)
```

---

## Full Tech Stack

| Tool | Purpose | Cost |
|------|---------|------|
| **Gemini 2.5 Flash-Lite API** | Script writing, SEO titles, hashtags | Free |
| **ElevenLabs Starter** | AI voiceover (30k chars/mo) | $11/mo |
| **GitHub Actions** | Automation backbone — no card needed | Free |
| **Your laptop (backup)** | Manual run if GitHub fails | Free |
| **FFmpeg** | Video assembly (clips + voice + subs + music) | Free |
| **Whisper.cpp** | Auto-subtitle generation | Free |
| **Pexels / Pixabay** | Stock footage library | Free |
| **Pixabay Music** | Royalty-free background music | Free |
| **YouTube Data API v3** | Auto-publish to YouTube | Free |
| **TikTok Content Posting API** | Auto-publish to TikTok | Free |
| **Facebook Graph API** | Auto-publish to Facebook/Reels | Free |
| **Google Trends RSS** | Daily trending topic discovery | Free |
| **Canva Free** | Manual thumbnails (10 min/video) | Free |
| **Claude Pro** | Weekly strategy + prompt refinement | $20/mo (you have it) |

**Total: $11/month — no credit card needed for any free tool**

---

## Budget Breakdown

```
ElevenLabs Starter ......... $11/mo   ← only paid tool
Gemini 2.5 Flash-Lite API ..  $0/mo   ← 1,000 free requests/day
GitHub Actions .............  $0/mo   ← 2,000 free minutes/month
Stock footage + music ......  $0/mo   ← Pexels, Pixabay
Platform APIs ..............  $0/mo   ← YouTube, TikTok, Facebook
─────────────────────────────────────
TOTAL ......................  $11/mo
Remaining from $50 budget .. $39/mo buffer
No credit card needed for any free tool
```

---

## How the Pipeline Works

### Step-by-step daily automation

**Step 1 — Trend discovery (10 sec)**
n8n fetches the top trending topic in your niche from Google Trends RSS feed. No human needed.

**Step 2 — Script generation (8 sec)**
n8n sends the topic to Gemini 2.5 Flash-Lite API. Returns JSON with:
- 60-second script
- YouTube title + description
- 10 hashtags
- TikTok caption

**Step 3 — Voiceover (15 sec)**
Script text is sent to ElevenLabs API. Returns an MP3 file.

**Step 4 — Video assembly (40 sec)**
FFmpeg runs inside GitHub Actions (or your laptop):
- Randomly selects 4 stock clips from the repo's stock folder
- Overlays the ElevenLabs MP3 voiceover
- Generates subtitles via Whisper.cpp
- Adds background music at 20% volume
- Exports final MP4 (60 seconds)

**Step 5 — Auto-publish (30 sec)**
n8n uploads the MP4 + metadata to YouTube, TikTok, and Facebook simultaneously using their official APIs.

**Total time: ~2 minutes. Human input: 0.**

---

## Server Options — No Credit Card Needed

You don't need Oracle Cloud. Here are 4 alternatives that are completely free and require no card:

### Option A — GitHub Actions (recommended)

GitHub gives you **2,000 free automation minutes/month** — more than enough for 1 video/day (~2 min each = 60 min/month used).

- No server to manage
- Runs in the cloud daily on schedule
- Free forever with a GitHub account
- See the [GitHub Actions Workflow](#github-actions-workflow) section below

### Option B — Your own laptop (simplest backup)

Run everything locally. Leave your laptop on at the scheduled time.

```bash
# Install on Windows (use Git Bash or WSL)
# Install on Mac
brew install ffmpeg node
npm install -g n8n

# Install on Linux
sudo apt install -y ffmpeg nodejs npm python3-pip
pip3 install openai-whisper

# Start n8n
n8n start
# Access at http://localhost:5678
```

Set a Windows Task Scheduler or Mac cron job to trigger at 6am daily.

### Option C — Render.com (free cloud hosting, no card)

1. Sign up at render.com — no credit card
2. Create a new Web Service → Deploy from GitHub
3. Use the n8n Docker image
4. Add UptimeRobot (free) to ping your URL every 5 min — keeps it awake

### Option D — Railway.app (free $5 credit/month)

1. Sign up at railway.app with your GitHub account — no card
2. Deploy n8n with one click from their template library
3. Free $5/month credit is enough for light daily automation

---

**Recommendation: use GitHub Actions as your primary runner + your laptop as manual backup.**

---

## Setup Guide

### 1. Create your GitHub repository

```bash
# Create a new private repo called "video-agent"
# Add these folders:
video-agent/
├── stock/          ← upload your stock clips here (git lfs for large files)
├── music/          ← upload music tracks here
├── scripts/
│   ├── assemble.sh
│   ├── upload_youtube.py
│   └── upload_tiktok.py
└── .github/
    └── workflows/
        └── daily_video.yml   ← your automation
```

### 2. Store secrets in GitHub (no hardcoded keys)

Go to your repo → Settings → Secrets and variables → Actions → New secret

Add these secrets:
- `GEMINI_API_KEY`
- `ELEVENLABS_API_KEY`
- `ELEVENLABS_VOICE_ID`
- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`
- `YOUTUBE_REFRESH_TOKEN`
- `TIKTOK_ACCESS_TOKEN`
- `FACEBOOK_PAGE_TOKEN`

### 3. Get your free Gemini API key

1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Click "Get API key" — no credit card needed
3. Use model: `gemini-2.5-flash-lite`
4. Free limits: **1,000 requests/day**, 15 RPM

### 4. Download stock footage (do this once, upload to GitHub)

Download 50–100 clips:

- [pexels.com/videos](https://pexels.com/videos) — search your niche keywords
- [pixabay.com/videos](https://pixabay.com/videos) — CC0 license, safe for monetisation
- [coverr.co](https://coverr.co) — high quality, free

Download 5–10 music tracks:

- [pixabay.com/music](https://pixabay.com/music)
- Search: "background lofi", "calm background music"

> **Note:** GitHub has a 100MB file size limit. Use [Git LFS](https://git-lfs.github.com) for video files, or store clips on Google Drive and download them in the workflow.

### 5. Connect platform APIs

**YouTube Data API v3**
- Go to console.cloud.google.com → Enable YouTube Data API v3
- Create OAuth2 credentials → authorise your channel
- Get refresh token using the OAuth2 Playground

**TikTok Content Posting API**
- Go to developers.tiktok.com → Create app → Request `video.publish` scope

**Facebook Graph API**
- Go to developers.facebook.com → Create app → Add Pages API
- Get page access token for your Facebook page

---

## Gemini API Script Prompt

Use this exact prompt in n8n's HTTP Request node:

```json
{
  "model": "gemini-2.5-flash-lite",
  "contents": [{
    "parts": [{
      "text": "You are a faceless YouTube scriptwriter for a [YOUR NICHE] channel.\n\nToday's topic: {{$json.topic}}\n\nWrite a 60-second video script optimised for high retention. Include:\n- A strong hook in the first 5 seconds (question, shocking fact, or bold statement)\n- 3 key points, each under 15 seconds\n- A clear call-to-action at the end\n\nReturn ONLY valid JSON with these exact fields:\n{\n  \"script\": \"full spoken script here\",\n  \"title\": \"SEO YouTube title under 60 chars\",\n  \"description\": \"150-word YouTube description with keywords\",\n  \"hashtags\": [\"tag1\", \"tag2\", \"tag3\", \"tag4\", \"tag5\", \"tag6\", \"tag7\", \"tag8\", \"tag9\", \"tag10\"],\n  \"tiktok_caption\": \"punchy caption under 150 chars with 3 hashtags\",\n  \"hook\": \"first sentence only — used as on-screen text overlay\"\n}\n\nNo extra text. No markdown. JSON only."
    }]
  }]
}
```

**Gemini API endpoint:**
```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key=YOUR_API_KEY
```

---

## FFmpeg Video Assembly

### Folder structure (GitHub repo or laptop)

```
video-agent/
├── stock/          ← your downloaded clips
├── music/          ← background music tracks
├── temp/           ← created during workflow run
│   ├── voice.mp3   ← from ElevenLabs
│   ├── subs.srt    ← from Whisper
│   └── output.mp4  ← final video
└── scripts/
    └── assemble.sh ← the script below
```

### assemble.sh

```bash
#!/bin/bash
# Randomly pick 4 stock clips
CLIPS=$(ls ./stock/*.mp4 | shuf -n 4)
MUSIC=$(ls ./music/*.mp3 | shuf -n 1)

# Create clip list for FFmpeg
mkdir -p ./temp
rm -f ./temp/clips.txt
for clip in $CLIPS; do
  echo "file '$clip'" >> ./temp/clips.txt
done

# Generate subtitles from voiceover
whisper ./temp/voice.mp3 \
  --model tiny \
  --output_format srt \
  --output_dir ./temp/

# Assemble final video
ffmpeg -y \
  -f concat -safe 0 -i ./temp/clips.txt \
  -i ./temp/voice.mp3 \
  -i "$MUSIC" \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,subtitles=./temp/voice.srt:force_style='FontSize=22,Alignment=2,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2'" \
  -filter_complex "[1:a]volume=1.0[v];[2:a]volume=0.2[m];[v][m]amix=inputs=2:duration=first[audio]" \
  -map 0:v -map "[audio]" \
  -t 60 \
  -c:v libx264 -c:a aac \
  ./temp/output.mp4

echo "Video ready: ./temp/output.mp4"
```

Make it executable:
```bash
chmod +x ./scripts/assemble.sh
```

---

## GitHub Actions Workflow

This is your main automation. Create this file at `.github/workflows/daily_video.yml` in your repo:

```yaml
name: Daily Video Pipeline
on:
  schedule:
    - cron: '0 6 * * *'   # runs every day at 6am UTC
  workflow_dispatch:        # lets you trigger manually too

jobs:
  make-and-publish:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Install dependencies
        run: |
          sudo apt-get update -qq
          sudo apt-get install -y ffmpeg python3-pip
          pip3 install openai-whisper requests google-auth google-auth-oauthlib

      - name: Fetch trending topic
        id: trend
        run: |
          TOPIC=$(python3 -c "
          import urllib.request, xml.etree.ElementTree as ET
          url = 'https://trends.google.com/trends/trendingsearches/daily/rss?geo=US'
          data = urllib.request.urlopen(url).read()
          root = ET.fromstring(data)
          title = root.find('./channel/item/title').text
          print(title)
          ")
          echo "topic=$TOPIC" >> $GITHUB_OUTPUT

      - name: Generate script with Gemini
        id: script
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: |
          python3 scripts/gemini_script.py "${{ steps.trend.outputs.topic }}"
          # saves output to ./temp/script.json

      - name: Generate voiceover with ElevenLabs
        env:
          ELEVENLABS_API_KEY: ${{ secrets.ELEVENLABS_API_KEY }}
          ELEVENLABS_VOICE_ID: ${{ secrets.ELEVENLABS_VOICE_ID }}
        run: |
          python3 scripts/elevenlabs_voice.py
          # reads script from ./temp/script.json
          # saves voice to ./temp/voice.mp3

      - name: Assemble video with FFmpeg
        run: bash scripts/assemble.sh

      - name: Upload to YouTube
        env:
          YOUTUBE_CLIENT_ID: ${{ secrets.YOUTUBE_CLIENT_ID }}
          YOUTUBE_CLIENT_SECRET: ${{ secrets.YOUTUBE_CLIENT_SECRET }}
          YOUTUBE_REFRESH_TOKEN: ${{ secrets.YOUTUBE_REFRESH_TOKEN }}
        run: python3 scripts/upload_youtube.py

      - name: Upload to TikTok
        env:
          TIKTOK_ACCESS_TOKEN: ${{ secrets.TIKTOK_ACCESS_TOKEN }}
        run: python3 scripts/upload_tiktok.py

      - name: Upload to Facebook
        env:
          FACEBOOK_PAGE_TOKEN: ${{ secrets.FACEBOOK_PAGE_TOKEN }}
        run: python3 scripts/upload_facebook.py
```

### gemini_script.py

```python
import sys, os, json, urllib.request

topic = sys.argv[1]
api_key = os.environ["GEMINI_API_KEY"]

prompt = f"""You are a faceless YouTube scriptwriter for a personal finance channel.
Today's topic: {topic}

Return ONLY valid JSON:
{{
  "script": "60-second spoken script with strong hook",
  "title": "SEO title under 60 chars",
  "description": "150-word YouTube description",
  "hashtags": ["tag1","tag2","tag3","tag4","tag5","tag6","tag7","tag8","tag9","tag10"],
  "tiktok_caption": "punchy caption under 150 chars",
  "hook": "first sentence for on-screen text"
}}
No extra text. JSON only."""

body = json.dumps({
    "contents": [{"parts": [{"text": prompt}]}]
}).encode()

req = urllib.request.Request(
    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}",
    data=body,
    headers={"Content-Type": "application/json"},
    method="POST"
)

with urllib.request.urlopen(req) as r:
    data = json.loads(r.read())

text = data["candidates"][0]["content"]["parts"][0]["text"]
os.makedirs("./temp", exist_ok=True)
with open("./temp/script.json", "w") as f:
    f.write(text)

print("Script saved.")
```

### elevenlabs_voice.py

```python
import os, json, urllib.request

with open("./temp/script.json") as f:
    data = json.load(f)

script = data["script"]
api_key = os.environ["ELEVENLABS_API_KEY"]
voice_id = os.environ["ELEVENLABS_VOICE_ID"]

body = json.dumps({
    "text": script,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
}).encode()

req = urllib.request.Request(
    f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
    data=body,
    headers={"Content-Type": "application/json", "xi-api-key": api_key},
    method="POST"
)

with urllib.request.urlopen(req) as r:
    audio = r.read()

with open("./temp/voice.mp3", "wb") as f:
    f.write(audio)

print("Voice saved.")
```

---

## n8n Workflow Structure

If you prefer n8n over GitHub Actions (e.g. running on your laptop), build these nodes:

```
1. Schedule Trigger
   └─ Cron: 0 6 * * *  (6am daily)

2. HTTP Request — Google Trends
   └─ GET https://trends.google.com/trends/trendingsearches/daily/rss?geo=US
   └─ Parse XML → extract first <title> tag

3. HTTP Request — Gemini API
   └─ POST to Gemini endpoint
   └─ Body: your script prompt with {{topic}} injected
   └─ Parse JSON response

4. HTTP Request — ElevenLabs
   └─ POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}
   └─ Header: xi-api-key: YOUR_KEY
   └─ Body: { "text": "{{script}}", "model_id": "eleven_monolingual_v1" }
   └─ Save MP3 to ./temp/voice.mp3

5. Execute Command — FFmpeg
   └─ Run: bash ./scripts/assemble.sh
   └─ Wait for completion

6. HTTP Request — YouTube Upload
   └─ POST to YouTube Data API v3
   └─ Multipart upload with video + metadata

7. HTTP Request — TikTok Upload
   └─ POST to TikTok Content Posting API

8. HTTP Request — Facebook Upload
   └─ POST to Facebook Graph API
```

---

## Niche Selection

### Best niches for this stack (stock footage works fine)

| Niche | CPM | Growth Speed | Notes |
|-------|-----|-------------|-------|
| Personal finance tips | $8–$20 | Medium | Highest AdSense CPM |
| AI tools / tech news | $6–$15 | Fast | Easy stock footage |
| History facts | $4–$10 | Slow-medium | Evergreen content |
| Productivity / self-improvement | $5–$12 | Medium | High affiliate potential |
| Health tips (not medical) | $6–$14 | Medium | Amazon affiliate friendly |

### Niches to AVOID with stock footage

- Travel / lifestyle → needs real footage
- Food / cooking → needs real footage
- Beauty / fashion → needs real footage
- Gaming → needs screen recordings

### Picking your niche

Run this prompt in Claude Pro once:

> "I want to start a faceless YouTube channel using AI-generated scripts and stock footage. My budget is $11/month. Suggest 5 specific sub-niches within [personal finance / AI tools / history] that have: low competition, high CPM, strong affiliate potential, and work well with stock footage. For each, suggest 10 video title ideas."

---

## Quality Tips

### The 2 things that matter most (takes 10 min/video)

**1. Thumbnail (Canva free — 8 min)**
- Bold text (3–5 words max)
- High contrast colours
- One striking visual
- No clip art or generic stock photos as the main image

**2. Hook review (2 min)**
- Watch the first 7 seconds before it publishes
- Ask: does this make someone stop scrolling?
- The Gemini prompt generates a `hook` field — use it as on-screen text overlay in FFmpeg

### Hook formulas that work

```
"You've been doing [X] wrong your entire life..."
"Nobody talks about this [X] strategy..."
"In 60 seconds: how to [desirable outcome]"
"The #1 reason most people fail at [X]"
"[Shocking fact]. Here's why it matters."
```

### What the YouTube algorithm rewards in 2026

- Watch time (retention curve — aim for 60%+ average)
- Click-through rate (thumbnail + title)
- Consistency (same upload time daily)
- Topical authority (stick to ONE niche)

---

## Revenue Timeline

| Month | Activity | Expected Revenue |
|-------|----------|-----------------|
| Month 1 | Build pipeline, post daily, add affiliate links | $20–$80 (affiliate only) |
| Month 2 | Refine hooks, grow audience | $50–$150 |
| Month 3 | Hit 1k subs + 4k watch hours → YouTube monetisation | $100–$250 |
| Month 4–5 | AdSense + affiliates + TikTok rewards | **$300–$500** |
| Month 6+ | Scale to 2nd channel or add sponsorships | $500–$1,000+ |

### Revenue streams in order of speed

1. **Affiliate links** (fastest — day 1)
   - Amazon Associates: link products mentioned in videos
   - ClickBank / Impact: digital products in your niche
   - Software tools: most SaaS companies have 20–40% recurring commissions

2. **YouTube AdSense** (month 3–4)
   - Requires: 1,000 subscribers + 4,000 watch hours
   - CPM varies: $4–$20 depending on niche

3. **TikTok Creator Rewards** (month 2–3)
   - Requires: 10,000 followers + 100,000 views in last 30 days
   - Earns: $0.02–$0.04 per 1,000 views

4. **Facebook Reels Bonus** (varies)
   - Available in select countries
   - Apply via Facebook Creator Studio

---

## Video Tool Decision Guide

### Should you pay for a video generation tool?

**Right now: No.**

Free tools (FFmpeg + stock footage) are sufficient to validate your niche and build an audience. Paid tools only make sense when:

- You're already earning $100+/month
- Your analytics show retention dropping due to visual quality
- You want to reinvest earnings to scale faster

### If you upgrade later

| Tool | Price | Best for | Verdict |
|------|-------|----------|---------|
| FFmpeg + stock | $0 | Fully automated assembly | Start here |
| AutoShorts.ai | $19/mo | Shorts-only automation | Budget pick |
| Pictory | $23/mo | Script-to-video | Good value |
| Runway Gen-4 | $15/mo | Cinematic AI footage | Quality upgrade |
| InVideo AI | $35/mo | All-in-one automation | Best all-in-one |

**Rule:** Only upgrade when a paid tool directly solves a retention problem shown in your analytics — not before.

---

## Honest Warnings

### Things that can go wrong

**YouTube AI content crackdown**
YouTube is filtering low-effort mass-produced AI content. The fix: add a genuine hook, review thumbnails manually, and stick to a specific niche rather than posting random trending topics.

**ElevenLabs free tier won't work long-term**
The free tier (10k chars/month) covers only ~10 videos. The $11/month Starter tier (30k chars) covers 30 videos/month — enough for daily posting.

**Stock footage feels generic**
Viewers can tell. It works fine in finance/tech/history niches but hurts you in lifestyle niches. Stick to niches where information matters more than visuals.

**Revenue takes 3–5 months**
Month 1 will likely earn under $50 unless you're very lucky with a viral video. The $300–$500 target is realistic at month 4–5, not month 1. Consistency is the only path.

**Platform API changes**
TikTok's API has been unstable. Have a manual backup plan (Buffer free tier) in case the auto-posting breaks.

### Copyright checklist

- ✅ Pexels License — safe for YouTube monetisation
- ✅ Pixabay License — safe for YouTube monetisation
- ✅ CC0 footage — safe everywhere
- ❌ News footage — never use
- ❌ Watermarked previews — never use
- ❌ Music from Spotify/Apple Music — never use
- ❌ Celebrity images — avoid

---

## Quick Start Checklist

- [ ] Create a free GitHub account (github.com)
- [ ] Create a private repo called `video-agent`
- [ ] Get Gemini API key from aistudio.google.com (free, no card)
- [ ] Sign up for ElevenLabs Starter ($11/mo), pick your voice, get voice ID
- [ ] Download 50–100 stock clips into `/stock/` folder in your repo
- [ ] Download 5–10 music tracks into `/music/` folder
- [ ] Add `assemble.sh` and Python scripts to `/scripts/` folder
- [ ] Add all API keys as GitHub Secrets (Settings → Secrets → Actions)
- [ ] Set up YouTube Data API v3, TikTok API, Facebook Graph API
- [ ] Create `.github/workflows/daily_video.yml` with the workflow above
- [ ] Trigger manually once to test (`workflow_dispatch`)
- [ ] Pick your niche (ask Claude Pro for help)
- [ ] Set up Amazon Associates or relevant affiliate program
- [ ] Add affiliate links to YouTube description template in `gemini_script.py`
- [ ] Confirm daily cron is running (Actions tab → check green ticks)

---

*Built with Claude Pro + Gemini 2.5 Flash-Lite (free) + ElevenLabs ($11/mo) + GitHub Actions (free) + FFmpeg (free)*
