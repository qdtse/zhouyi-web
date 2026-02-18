from workers import WorkerEntrypoint, Response
import json
import sys
import os

api_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "api")
sys.path.insert(0, api_dir)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

import utils
import ziwei
import bazi

app = FastAPI(
    title="Zhouyi Divination API",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str
    focus: Optional[str] = "general"

class PairRequest(BaseModel):
    num1: int
    num2: int

class ZiweiRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int

class BaziRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int

class MatchRequest(BaseModel):
    male_year: int
    male_month: int
    male_day: int
    male_hour: int
    female_year: int
    female_month: int
    female_day: int
    female_hour: int

@app.get("/health")
@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "modules": {
            "utils": utils is not None,
            "ziwei": ziwei is not None,
            "bazi": bazi is not None
        }
    }

@app.post("/divine/text")
@app.post("/api/divine/text")
async def divine_text(req: TextRequest):
    if utils is None:
        raise HTTPException(status_code=503, detail="Utils module not available")
    try:
        result = utils.calculate_hexagram_from_text(req.text, req.focus)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/divine/zhuge")
@app.post("/api/divine/zhuge")
async def divine_zhuge(req: TextRequest):
    if utils is None:
        raise HTTPException(status_code=503, detail="Utils module not available")
    try:
        result = utils.calculate_zhuge_from_text(req.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/divine/pair")
@app.post("/api/divine/pair")
async def divine_pair(req: PairRequest):
    if utils is None:
        raise HTTPException(status_code=503, detail="Utils module not available")
    try:
        result = utils.calculate_hexagram_from_numbers(req.num1, req.num2)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/divine/random")
@app.get("/api/divine/random")
async def divine_random():
    if utils is None:
        raise HTTPException(status_code=503, detail="Utils module not available")
    try:
        result = utils.get_random_divination()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/divine/current")
@app.get("/api/divine/current")
async def divine_current():
    if utils is None:
        raise HTTPException(status_code=503, detail="Utils module not available")
    try:
        result = utils.get_current_time_divination()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/divine/ziwei")
@app.post("/api/divine/ziwei")
async def divine_ziwei(req: ZiweiRequest):
    if ziwei is None:
        raise HTTPException(status_code=503, detail="Ziwei module not available")
    try:
        chart = ziwei.ZiweiChart(req.year, req.month, req.day, req.hour)
        return chart.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/divine/bazi")
@app.post("/api/divine/bazi")
async def divine_bazi(req: BaziRequest):
    if bazi is None:
        raise HTTPException(status_code=503, detail="Bazi module not available")
    try:
        result = bazi.get_bazi_analysis(req.year, req.month, req.day, req.hour)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/divine/match")
@app.post("/api/divine/match")
async def divine_match(req: MatchRequest):
    if bazi is None:
        raise HTTPException(status_code=503, detail="Bazi module not available")
    try:
        male = bazi.get_bazi_analysis(req.male_year, req.male_month, req.male_day, req.male_hour)
        female = bazi.get_bazi_analysis(req.female_year, req.female_month, req.female_day, req.female_hour)
        result = bazi.check_marriage_compatibility(male, female)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        from workers.asgi import AsgiAdapter
        
        adapter = AsgiAdapter(app)
        return await adapter.fetch(request)
