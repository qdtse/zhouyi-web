from workers import WorkerEntrypoint, Response
import json
import sys
import os

src_dir = os.path.dirname(os.path.abspath(__file__))
api_dir = os.path.join(os.path.dirname(src_dir), "api")
sys.path.insert(0, src_dir)
sys.path.insert(0, api_dir)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# 延迟加载模块，避免启动时 CPU 超限
utils = None
ziwei = None
bazi = None

def load_modules():
    global utils, ziwei, bazi
    if utils is None:
        import utils as _utils
        utils = _utils
    if ziwei is None:
        import ziwei as _ziwei
        ziwei = _ziwei
    if bazi is None:
        import bazi as _bazi
        bazi = _bazi

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
        "modules_loaded": utils is not None
    }

@app.post("/divine/text")
@app.post("/api/divine/text")
async def divine_text(req: TextRequest):
    try:
        load_modules()
        result = utils.calculate_hexagram_from_text(req.text, req.focus)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/divine/zhuge")
@app.post("/api/divine/zhuge")
async def divine_zhuge(req: TextRequest):
    try:
        load_modules()
        result = utils.calculate_zhuge_from_text(req.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/divine/pair")
@app.post("/api/divine/pair")
async def divine_pair(req: PairRequest):
    try:
        load_modules()
        result = utils.calculate_hexagram_from_numbers(req.num1, req.num2)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/divine/random")
@app.get("/api/divine/random")
async def divine_random():
    try:
        load_modules()
        result = utils.get_random_divination()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/divine/current")
@app.get("/api/divine/current")
async def divine_current():
    try:
        load_modules()
        result = utils.get_current_time_divination()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/divine/ziwei")
@app.post("/api/divine/ziwei")
async def divine_ziwei(req: ZiweiRequest):
    try:
        load_modules()
        chart = ziwei.ZiweiChart(req.year, req.month, req.day, req.hour)
        return chart.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/divine/bazi")
@app.post("/api/divine/bazi")
async def divine_bazi(req: BaziRequest):
    try:
        load_modules()
        result = bazi.get_bazi_analysis(req.year, req.month, req.day, req.hour)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/divine/match")
@app.post("/api/divine/match")
async def divine_match(req: MatchRequest):
    try:
        load_modules()
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
