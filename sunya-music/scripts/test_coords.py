"""
Test script - just pastes song 1 lyrics and stops. No style, no Create click.
Run this, switch to Suno, and check if lyrics got pasted correctly.
"""
import pyautogui
import pyperclip
import time

STARTUP_DELAY = 5
LYRICS_FIELD  = (370, 320)

TEST_LYRICS = """Om Namah Shivaya Om Namah Shivaya
Har Har Mahadev Har Har Shankar
Test lyrics - Song 1"""

print(f"Switch to Suno Chrome NOW - starting in {STARTUP_DELAY}s...")
for i in range(STARTUP_DELAY, 0, -1):
    print(f"  {i}...", end="\r", flush=True)
    time.sleep(1)
print("Clicking lyrics field...")

pyautogui.click(*LYRICS_FIELD, clicks=3, interval=0.1)
time.sleep(0.5)
pyautogui.hotkey("ctrl", "a")
time.sleep(0.2)
pyautogui.press("backspace")
time.sleep(0.3)
pyperclip.copy(TEST_LYRICS)
pyautogui.hotkey("ctrl", "v")
time.sleep(0.5)

print("Done! Check if lyrics appeared in Suno.")
print(f"Mouse is currently at: {pyautogui.position()}")
