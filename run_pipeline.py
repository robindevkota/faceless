#!/usr/bin/env python3
"""
run_pipeline.py — runs the full pipeline in one command
Usage: python run_pipeline.py [--facebook] [--youtube] [--all]
"""

import subprocess
import sys
import os

def run(script: str):
    print(f"\n{'='*50}")
    print(f"Running: {script}")
    print('='*50)
    result = subprocess.run([sys.executable, f"scripts/{script}"])
    if result.returncode != 0:
        print(f"\nERROR: {script} failed. Stopping pipeline.")
        sys.exit(1)

def main():
    args = sys.argv[1:]
    post_facebook = "--facebook" in args or "--all" in args
    post_youtube  = "--youtube"  in args or "--all" in args

    # step 1: pick script
    run("gemini_script.py")

    # step 2: generate voice
    run("edge_tts_voice.py")

    # step 3: assemble video
    run("assemble_video.py")

    # step 4: upload
    if post_youtube:
        run("upload_youtube.py")

    if post_facebook:
        run("upload_facebook.py")

    if not post_facebook and not post_youtube:
        print("\nVideo ready at ./temp/output.mp4")
        print("To post, run with --facebook or --youtube or --all")

    print("\nPipeline complete!")

if __name__ == "__main__":
    main()
