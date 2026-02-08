from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import utils
import ziwei
import os

app = FastAPI(title="Zhouyi Divination API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class TextRequest(BaseModel):
    text: str

class PairRequest(BaseModel):
    num1: int
    num2: int

class SplitRequest(BaseModel):
    number: int

class ZiweiRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int

# API Endpoints

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

@app.post("/api/divine/text")
async def divine_text(req: TextRequest):
    """
    Handles: Company Naming, Name Testing, Phone Number, License Plate, English Name
    """
    try:
        result = utils.calculate_hexagram_from_text(req.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/divine/zhuge")
async def divine_zhuge(req: TextRequest):
    """
    Handles: Zhuge Shenshu Divination
    """
    try:
        result = utils.calculate_zhuge_from_text(req.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/divine/pair")
async def divine_pair(req: PairRequest):
    """
    Handles explicit number pairs
    """
    try:
        result = utils.calculate_hexagram_from_numbers(req.num1, req.num2)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/divine/random")
async def divine_random():
    """
    Handles Random Divination
    """
    try:
        result = utils.get_random_divination()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/divine/current")
async def divine_current():
    """
    Handles Current Time Divination
    """
    try:
        result = utils.get_current_time_divination()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/divine/ziwei")
async def divine_ziwei(req: ZiweiRequest):
    """
    Handles: Ziwei Doushu Chart
    """
    try:
        chart = ziwei.ZiweiChart(req.year, req.month, req.day, req.hour)
        return chart.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Static Files
# Create static directory if not exists
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
