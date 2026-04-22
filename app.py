# app.
from dotenv import load_dotenv
load_dotenv()
import os
import threading
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from contextlib import asynccontextmanager
import dotenv

import chat_app
from main import run_ingestion

# Global System State
state = {
    "ready": False, 
    "status": "Initializing...",
    "error": None
}

def background_ingestion():
    """Runs ingestion without blocking the main server thread"""
    global state
    try:
        print("[System] Starting background ingestion...")
        success = run_ingestion(force_refresh=False)
        if success:
            state["ready"] = True
            state["status"] = "System Online"
        else:
            state["status"] = "Ingestion Failed (Check Logs)"
    except Exception as e:
        state["error"] = str(e)
        state["status"] = "Critical Error"
        print(f"[System] ❌ Background Task Error: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start ingestion in background
    t = threading.Thread(target=background_ingestion, daemon=True)
    t.start()
    yield

app = FastAPI(lifespan=lifespan)

# Ensure output directory exists
os.makedirs("output_images", exist_ok=True)
app.mount("/images", StaticFiles(directory="output_images"), name="images")

# Setup Templates (Assumes index.html is in /templates)
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
from jinja2 import Environment, FileSystemLoader

from jinja2 import Environment, FileSystemLoader

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
class ChatRequest(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
async def get_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/status")
async def get_status():
    return state

@app.post("/chat")
async def chat_endpoint(request: ChatRequest, req: Request):
    global state
    
    if not state["ready"]:
        return {
            "answer": f"⚠️ **System is warming up.**\nStatus: {state['status']}",
            "images": []
        }

    try:
        # Process Chat
        answer, img_paths = await chat_app.get_response(
            request.query, 
            os.getenv("PINECONE_API_KEY"),
            os.getenv("PINECONE_INDEX_NAME"),
            os.getenv("GEMINI_API_KEY")
        )
        
        # Convert local paths to Web URLs
        web_images = []
        base_url = str(req.base_url).rstrip('/')
        for path in img_paths:
            filename = os.path.basename(path)
            web_images.append(f"{base_url}/images/{filename}")

        return {
            "answer": answer,
            "images": web_images
        }

    except Exception as e:
        print(f"Chat Error: {e}")
        return {"answer": f"**Error:** {str(e)}", "images": []}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)