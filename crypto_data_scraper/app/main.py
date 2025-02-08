from fastapi import FastAPI
from app.api.routes import router
from app.services.fetcher import fetch_crypto_prices
import asyncio

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(fetch_crypto_prices())

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
