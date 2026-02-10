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

import os
import sys

# Ensure current directory is in path for local imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# Conditional imports for utils/ziwei/bazi
try:
    import utils
    import ziwei
    import bazi
except ImportError:
    try:
        from . import utils
        from . import ziwei
        from . import bazi
    except ImportError as e:
        # Last resort: try adding parent dir
        sys.path.append(os.path.dirname(current_dir))
        import api.utils as utils
        import api.ziwei as ziwei
        import api.bazi as bazi

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Zhouyi Divination API",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Note: Static files are handled by Vercel's outputDirectory config
# Do NOT mount static files here in serverless environment
# This prevents conflicts with Vercel's routing

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return {"detail": "Internal server error", "error": str(exc)}

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
    """
    Handles: Company Naming, Name Testing, Phone Number, License Plate, English Name
    Supports focus: general, love, wealth, career
    """
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
    """
    Handles: Zhuge Shenshu Divination
    """
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
    """
    Handles explicit number pairs
    """
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
    """
    Handles Random Divination
    """
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
    """
    Handles Current Time Divination
    """
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
    """
    Handles: Ziwei Doushu Chart
    """
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
    """
    Handles: Bazi Analysis (Eight Characters)
    """
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
    """
    Handles: Bazi Marriage Compatibility
    """
    if bazi is None:
        raise HTTPException(status_code=503, detail="Bazi module not available")
    try:
        male = bazi.get_bazi_analysis(req.male_year, req.male_month, req.male_day, req.male_hour)
        female = bazi.get_bazi_analysis(req.female_year, req.female_month, req.female_day, req.female_hour)
        result = bazi.check_marriage_compatibility(male, female)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files for local development
# In production (Vercel), this is handled by Vercel configuration
public_path = os.path.join(os.path.dirname(current_dir), "public")
if os.path.exists(public_path):
    app.mount("/", StaticFiles(directory=public_path, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    # For local development only
    # Vercel handles static files via vercel.json routes
    uvicorn.run(app, host="0.0.0.0", port=8000)
