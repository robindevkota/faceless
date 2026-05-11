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
import http.server
import threading

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
REDIRECT_URI  = "http://localhost:8080"
SCOPE         = "https://www.googleapis.com/auth/youtube.upload"

auth_code = None

class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if "code" in params:
            auth_code = params["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<h2>Authorization successful! You can close this tab.</h2>")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"<h2>Error: no code received.</h2>")
    def log_message(self, format, *args):
        pass  # suppress server logs

def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("ERROR: YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET must be set in .env")
        return

    params = urllib.parse.urlencode({
        "client_id":     CLIENT_ID,
        "redirect_uri":  REDIRECT_URI,
        "scope":         SCOPE,
        "response_type": "code",
        "access_type":   "offline",
        "prompt":        "select_account",
    })
    auth_url = f"https://accounts.google.com/o/oauth2/auth?{params}"

    # start local server to catch the redirect
    server = http.server.HTTPServer(("localhost", 8080), CallbackHandler)
    thread = threading.Thread(target=server.handle_request)
    thread.daemon = True
    thread.start()

    print("\nOpening browser for YouTube authorization...")
    print("If browser doesn't open, visit this URL manually:")
    print(f"\n{auth_url}\n")
    webbrowser.open(auth_url)

    print("Waiting for authorization (complete in browser)...")
    thread.join(timeout=120)

    if not auth_code:
        print("ERROR: No authorization code received. Try again.")
        return

    body = urllib.parse.urlencode({
        "code":          auth_code,
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

    print("\nSUCCESS! Add this to your .env file:")
    print(f"\nYOUTUBE_REFRESH_TOKEN={data['refresh_token']}\n")

if __name__ == "__main__":
    main()
