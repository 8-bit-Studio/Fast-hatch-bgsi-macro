import time
import os
import sys
from datetime import datetime

try:
    import pyautogui
    import pydirectinput
    import keyboard
    import winsound
    import cv2
    import numpy as np
    from PIL import Image
except ImportError as e:
    print(f"\nMissing dependency: {e.name}")
    print("Run: pip install pyautogui pydirectinput keyboard Pillow opencv-python numpy")
    input("\nPress Enter to exit...")
    sys.exit()

# ─── Config ─────────────────────────────────────────────────────────────
VERSION = "V1.1"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_PATH = os.path.join(SCRIPT_DIR, "secret_tag.png")
COOLDOWN_SECONDS = 15

# ─── Detection ──────────────────────────────────────────────────────────
def scan_for_secret_scaled(image_path, scales=(0.95, 1.0, 1.05), threshold=0.85):
    if not os.path.exists(image_path):
        return False

    try:
        screen = pyautogui.screenshot()
        screen_np = np.array(screen.convert("RGB"))
        screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_RGB2GRAY)

        template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            return False

        for scale in scales:
            resized = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
            result = cv2.matchTemplate(screen_gray, resized, cv2.TM_CCOEFF_NORMED)
            if np.max(result) >= threshold:
                return True
    except:
        pass

    return False

# ─── Feedback ───────────────────────────────────────────────────────────
def play_alert():
    try:
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
    except:
        pass

def rainbow_text(text):
    colors = [196, 202, 208, 226, 46, 51, 21, 93, 201]
    output = ""
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        output += f"\033[38;5;{color}m{char}"
    output += "\033[0m"
    print(output)

# ─── Main Loop ──────────────────────────────────────────────────────────
is_running = False
last_key_pressed = None
last_detection_time = 0

print(f"🐣 Auto Egg Hatcher {VERSION}")
print("🎮 Controls: F1 = START | F2 = STOP")
print("=" * 60)

try:
    while True:
        if keyboard.is_pressed('f1') and last_key_pressed != 'f1':
            is_running = True
            last_key_pressed = 'f1'
            print("\n✅ Macro started.")

        elif keyboard.is_pressed('f2') and last_key_pressed != 'f2':
            is_running = False
            last_key_pressed = 'f2'
            print("\n🛑 Macro stopped.")

        if is_running:
            pydirectinput.press('e')

            now = time.time()
            if now - last_detection_time >= COOLDOWN_SECONDS:
                if scan_for_secret_scaled(SECRET_PATH):
                    last_detection_time = now
                    timestamp = datetime.now().strftime("%I:%M %p")
                    rainbow_text(f"Secret hatched at {timestamp}!")
                    play_alert()

        time.sleep(0.05)

except KeyboardInterrupt:
    pass

input("\nPress Enter to exit...")
