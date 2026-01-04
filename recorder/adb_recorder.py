# recorder/adb_recorder.py
# 2Aether Day 2 — FINAL VERSION — FULL PATH ADB
# @realdavejags — NOV 11 2025

import subprocess
import json
import os
from datetime import datetime

ADB_PATH = r"C:\platform-tools\adb.exe"  # ← THIS IS THE FIX

def get_device():
    try:
        output = subprocess.check_output([ADB_PATH, "devices"]).decode()
        for line in output.splitlines():
            if "\tdevice" in line and "List" not in line:
                return line.split("\t")[0]
    except: pass
    return None

def record_screen(duration=15):
    device = get_device()
    if not device:
        print("ERROR: No Android device found. Run 'adb devices' first.")
        return {"error": "No device connected"}

    os.makedirs("recordings", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_path = f"recordings/{timestamp}.mp4"
    json_path = f"recordings/{timestamp}.json"

    print(f"2Aether recording {duration}s on {device}...")

    subprocess.run([
        ADB_PATH, "-s", device, "shell", "screenrecord",
        "--time-limit", str(duration), "/sdcard/2aether.mp4"
    ], check=True)

    subprocess.run([
        ADB_PATH, "-s", device, "pull", "/sdcard/2aether.mp4", video_path
    ], check=True)

    subprocess.run([
        ADB_PATH, "-s", device, "shell", "rm", "/sdcard/2aether.mp4"
    ])

    data = {
        "video": video_path,
        "device": device,
        "duration": duration,
        "recorded_at": datetime.now().isoformat(),
        "builder": "@realdavejags",
        "project": "2Aether",
        "note": "Day 2 — First real phone recording — Cloudless QA Revolution"
    }
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"DONE — Video saved: {video_path}")
    return data

if __name__ == "__main__":
    result = record_screen(duration=15)
    print("DAY 2 COMPLETE — REAL PHONE RECORDING SUCCESS")