import requests
from datetime import datetime

# List of cryptocurrencies to fetch
CRYPTO_IDS = ["bitcoin", "ethereum", "litecoin", "ripple", "cardano", "dogecoin"]

# API configuration
API_URL = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(CRYPTO_IDS)}&vs_currencies=usd"

# Function to fetch crypto prices
def fetch_crypto_prices():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        return data, timestamp
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}, None  # Ensure it returns empty data and None for timestamp on failure

