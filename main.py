# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn

app = FastAPI(
    title="2Aether",
    description="Cloudless QA Revolution — Built by @realdavejags",
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "2Aether is ALIVE",
        "builder": "@realdavejags",
        "launched": datetime.now().isoformat(),
        "deadline": "2025-12-31T23:59:59-09:00",
        "days_left": 49,
        "repo": "https://github.com/realdavejags/2aether",
        "status": "Day 1 — Server Running"
    }

@app.get("/hello/{name}")
def hello(name: str):
    return {"hello": name, "from": "Aetherion", "time": datetime.now().isoformat()}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"2Aether heard: {data}")
    except WebSocketDisconnect:
        await websocket.close()

if __name__ == "__main__":
    print("2Aether server starting — @realdavejags")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)