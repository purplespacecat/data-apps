import requests
import asyncio
from datetime import datetime
from app.config import API_URL, POLL_INTERVAL

crypto_data = {}

async def fetch_crypto_prices():
    global crypto_data
    while True:
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            data = response.json()
            crypto_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "prices": data
            }
            print(f"Data fetched at {crypto_data['timestamp']}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
        await asyncio.sleep(POLL_INTERVAL)

def get_all_prices():
    if not crypto_data:
        raise ValueError("No data available yet.")
    return crypto_data

def get_price_by_id(crypto_id: str):
    if not crypto_data or crypto_id not in crypto_data['prices']:
        raise ValueError("Cryptocurrency not found.")
    return {
        "timestamp": crypto_data["timestamp"],
        "price": crypto_data["prices"][crypto_id]
    }
