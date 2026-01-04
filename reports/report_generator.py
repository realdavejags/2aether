# reports/report_generator.py
# 2Aether Day 4 — One-Click HTML + Video Report (Cloudless)
# Built by @realdavejags — Ships Nov 11 2025

import json
import base64
from pathlib import Path
from datetime import datetime
from jinja2 import Template
import os
import cv2

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2Aether Report — {{ timestamp }}</title>
    <style>
        body { font-family: 'Courier New', monospace; background: #0d0d0d; color: #00ff41; margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: auto; background: #1a1a1a; border: 2px solid #00ff41; border-radius: 15px; padding: 30px; box-shadow: 0 0 30px #00ff41; }
        .header { text-align: center; margin-bottom: 40px; }
        h1 { font-size: 4em; margin: 0; text-shadow: 0 0 20px #00ff41; }
        .builder { color: #00ff41; font-weight: bold; font-size: 1.5em; }
        .video { text-align: center; margin: 40px 0; }
        video { width: 100%; max-width: 900px; border: 3px solid #00ff41; border-radius: 12px; box-shadow: 0 0 25px #00ff41; }
        .bugs { background: rgba(0, 255, 65, 0.1); padding: 25px; border-radius: 12px; margin: 30px 0; }
        .bug { background: rgba(255, 0, 0, 0.3); padding: 18px; margin: 15px 0; border-left: 6px solid #ff0040; border-radius: 10px; }
        .footer { text-align: center; margin-top: 60px; font-size: 1.1em; opacity: 0.8; }
        .note { font-style: italic; color: #00ff41; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>2AETHER</h1>
            <p class="builder">Built by @realdavejags</p>
            <p>Report generated: {{ now }}</p>
        </div>

        <div class="video">
            <video controls poster="data:image/png;base64,{{ thumbnail }}">
                <source src="data:video/mp4;base64,{{ video_b64 }}" type="video/mp4">
                Your browser does not support video.
            </video>
        </div>

        <div class="bugs">
            <h2>Bugs Detected ({{ bug_count }})</h2>
            {% if bugs %}
                {% for bug in bugs %}
                <div class="bug">
                    <strong>{{ bug.type|upper }}</strong> at {{ "%.2f"|format(bug.timestamp) }}s
                    {% if bug.confidence %}
                    <br><small>Confidence: {{ "%.2f"|format(bug.confidence) }} | Severity: {{ bug.severity }}</small>
                    {% else %}
                    <br><small>Severity: {{ bug.severity }}</small>
                    {% endif %}
                </div>
                {% endfor %}
            {% else %}
                <p>No bugs detected — Clean run.</p>
            {% endif %}
        </div>

        <div class="footer">
            <p class="note">2Aether — No cloud. No login. No limits.</p>
            <p>https://github.com/realdavejags/2aether</p>
            <p>Dec 31 2025 or we die trying.</p>
        </div>
    </div>
</body>
</html>
"""

def generate_report(video_path, ai_report_path):
    video = Path(video_path)
    ai_report = Path(ai_report_path)

    if not video.exists() or not ai_report.exists():
        return {"error": "Video or AI report not found"}

    # Encode video
    with open(video, "rb") as f:
        video_b64 = base64.b64encode(f.read()).decode()

    # Read AI report
    with open(ai_report) as f:
        ai_data = json.load(f)

    # Generate thumbnail
    cap = cv2.VideoCapture(str(video))
    ret, frame = cap.read()
    thumbnail = ""
    if ret:
        _, buffer = cv2.imencode(".png", frame)
        thumbnail = base64.b64encode(buffer).decode()
    cap.release()

    # Render HTML
    template = Template(HTML_TEMPLATE)
    html = template.render(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        now=datetime.now().isoformat(),
        video_b64=video_b64,
        thumbnail=thumbnail,
        bug_count=len(ai_data.get("bugs", [])),
        bugs=ai_data.get("bugs", []),
        builder="@realdavejags"
    )

    report_path = video.with_suffix(".2aether.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"REPORT LIVE: {report_path}")
    print(f"OPEN: file://{report_path.absolute()}")
    return {"report": str(report_path)}

if __name__ == "__main__":
    recordings = Path("recordings")
    latest_video = max(recordings.glob("*.mp4"), key=os.path.getctime, default=None)
    latest_ai = max(recordings.glob("*.ai_report.json"), key=os.path.getctime, default=None)

    if latest_video and latest_ai:
        result = generate_report(latest_video, latest_ai)
        print("DAY 4 COMPLETE — HTML + VIDEO REPORT LIVE")
    else:
        print("Run ADB recorder + AI detector first.")