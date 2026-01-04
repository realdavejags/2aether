# ai/bug_detector.py — FINAL WORKING VERSION
# Input: UINT8 (0-255) — matches your model

import tensorflow as tf
import cv2
import numpy as np
import json
from pathlib import Path
from datetime import datetime
import os

interpreter = tf.lite.Interpreter(model_path="ai/models/bug_model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def preprocess_frame(frame):
    img = cv2.resize(frame, (224, 224))
    img = img.astype(np.uint8)  # ← UINT8 FIX
    img = np.expand_dims(img, axis=0)
    return img

def analyze_video(video_path):
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return {"error": "Could not open video"}

    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    bugs = []
    prev_frame = None
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret: break

        # Freeze detection
        if prev_frame is not None:
            diff = cv2.absdiff(frame, prev_frame)
            if np.mean(diff) < 10:
                bugs.append({
                    "type": "freeze",
                    "timestamp": round(frame_count / fps, 2),
                    "severity": "HIGH"
                })

        # AI inference every 30 frames
        if frame_count % 30 == 0:
            input_data = preprocess_frame(frame)
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()
            output = interpreter.get_tensor(output_details[0]['index'])[0]
            confidence = float(np.max(output))
            pred_class = int(np.argmax(output))

            if confidence > 0.85:
                bugs.append({
                    "type": "ui_anomaly",
                    "timestamp": round(frame_count / fps, 2),
                    "confidence": confidence,
                    "severity": "CRITICAL" if confidence > 0.95 else "HIGH"
                })

        prev_frame = frame.copy()
        frame_count += 1

    cap.release()

    report = {
        "video": str(video_path),
        "analyzed_at": datetime.now().isoformat(),
        "bugs_found": len(bugs),
        "bugs": bugs,
        "builder": "@realdavejags",
        "note": "Day 3 — AI brain live — UINT8 model fixed"
    }

    report_path = Path(video_path).with_suffix(".ai_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"AI COMPLETE — {len(bugs)} anomalies found")
    print(f"Report: {report_path}")
    return report

if __name__ == "__main__":
    latest = max(Path("recordings").glob("*.mp4"), key=os.path.getctime, default=None)
    if latest:
        result = analyze_video(latest)
        print("DAY 3 COMPLETE — AI BRAIN LIVE")
    else:
        print("No video found. Run ADB recorder first.")