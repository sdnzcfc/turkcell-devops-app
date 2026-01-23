from fastapi import FastAPI, Request
from datetime import datetime
import os

app = FastAPI()

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

os.makedirs(LOG_DIR, exist_ok=True)

@app.post("/log")
async def log_message(data: dict, request: Request):
    message = data.get("message", "")
    ip = request.client.host
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} | {ip} | {message}\n")
    return {"status": "ok"}
