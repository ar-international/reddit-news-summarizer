from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import json
import os
import sys
from main import lambda_handler

app = FastAPI()

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

NEWS_FILE = "news_summary.json"

@app.get("/api/news")
async def get_news():
    if not os.path.exists(NEWS_FILE):
        return []
    try:
        with open(NEWS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/refresh")
async def refresh_news():
    try:
        # Simulate Lambda context
        result = lambda_handler(None, None)
        if result.get("statusCode") == 200:
            # Re-read the file to return the latest data
            with open(NEWS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {"message": "Refresh successful", "data": data}
        else:
            raise HTTPException(status_code=500, detail=result.get("body"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
