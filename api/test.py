from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/api/test")
async def test():
    return {"status": "ok", "message": "Basic FastAPI works on Vercel"}

handler = Mangum(app, lifespan="off")
