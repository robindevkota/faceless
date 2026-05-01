#!/usr/bin/env python3
"""
get_youtube_token.py — one-time script to get a new YouTube refresh token
Run this once, copy the refresh token into your .env file
"""

import urllib.request
import urllib.parse
import json
import os
import webbrowser

# load .env file manually
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

CLIENT_ID     = os.environ.get("YOUTUBE_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("YOUTUBE_CLIENT_SECRET", "")
REDIRECT_URI  = "urn:ietf:wg:oauth:2.0:oob"
SCOPE         = "https://www.googleapis.com/auth/youtube.upload"

def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("ERROR: YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET must be set in .env")
        return

    auth_url = (
        "https://accounts.google.com/o/oauth2/auth"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPE}"
        "&response_type=code"
        "&access_type=offline"
        "&prompt=consent"
    )

    print("\nOpening browser for YouTube authorization...")
    print("If browser doesn't open, visit this URL manually:")
    print(f"\n{auth_url}\n")
    webbrowser.open(auth_url)

    code = input("Paste the authorization code here: ").strip()

    body = urllib.parse.urlencode({
        "code":          code,
        "client_id":     CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri":  REDIRECT_URI,
        "grant_type":    "authorization_code"
    }).encode()

    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token",
        data=body, method="POST"
    )

    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())

    if "refresh_token" not in data:
        print(f"Error: {data}")
        return

    print("\n✅ SUCCESS! Add this to your .env file:")
    print(f"\nYOUTUBE_REFRESH_TOKEN={data['refresh_token']}\n")

if __name__ == "__main__":
    main()
