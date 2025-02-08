from fastapi import APIRouter, HTTPException
from app.services.fetcher import get_all_prices, get_price_by_id

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Welcome to the Crypto Price API!"}

@router.get("/prices")
async def get_prices():
    try:
        return get_all_prices()
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.get("/prices/{crypto_id}")
async def get_price(crypto_id: str):
    try:
        return get_price_by_id(crypto_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
