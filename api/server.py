# Copyright (C) 2026 Sugarworm
# This file is part of Zhouyi Divination System.
#
# Zhouyi Divination System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Zhouyi Divination System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import utils
import ziwei
import bazi
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
    focus: Optional[str] = "general" # general, love, wealth, career

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

# API Endpoints

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

@app.post("/api/divine/text")
async def divine_text(req: TextRequest):
    """
    Handles: Company Naming, Name Testing, Phone Number, License Plate, English Name
    Supports focus: general, love, wealth, career
    """
    try:
        result = utils.calculate_hexagram_from_text(req.text, req.focus)
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

@app.post("/api/divine/bazi")
async def divine_bazi(req: BaziRequest):
    """
    Handles: Bazi Analysis (Eight Characters)
    """
    try:
        result = bazi.get_bazi_analysis(req.year, req.month, req.day, req.hour)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/divine/match")
async def divine_match(req: MatchRequest):
    """
    Handles: Bazi Marriage Compatibility
    """
    try:
        male = bazi.get_bazi_analysis(req.male_year, req.male_month, req.male_day, req.male_hour)
        female = bazi.get_bazi_analysis(req.female_year, req.female_month, req.female_day, req.female_hour)
        result = bazi.check_marriage_compatibility(male, female)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Static Files - REMOVED
# We let Vercel handle static files serving directly from the public/ directory
# This avoids "Read-only file system" errors in Serverless environment

if __name__ == "__main__":
    import uvicorn
    # For local development, we can mount static files conditionally
    # But for Vercel deployment, we rely on vercel.json rewrites
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "public")
    if os.path.exists(static_dir):
        app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
