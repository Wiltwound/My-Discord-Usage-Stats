import time
import pyperclip
import json
from datetime import datetime
import os

DATA_FILE = "data/usage.json"

def ensure_data_file():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def track_clipboard():
    print("🟢 Tracking Discord messages... Copy a message to log it.")
    last_clipboard = ""
    while True:
        try:
            text = pyperclip.paste()
            if text != last_clipboard and len(text.strip()) > 0:
                now = datetime.now().isoformat()
                print(f"📥 {now[:19]} | {text[:50]}{'...' if len(text) > 50 else ''}")

                data = load_data()
                data.append({
                    "message": text,
                    "timestamp": now,
                    "server": "Unknown"
                })
                save_data(data)
                last_clipboard = text
        except Exception as e:
            print("⚠️ Error:", e)

        time.sleep(1)

if __name__ == "__main__":
    ensure_data_file()
    track_clipboard()
