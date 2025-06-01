import requests
from datetime import datetime, timedelta
import time

# List of cryptocurrencies to fetch
CRYPTO_IDS = ["bitcoin", "ethereum", "litecoin", "ripple", "cardano", "dogecoin"]

# API configuration
BASE_URL = "https://api.coingecko.com/api/v3"
CURRENT_PRICE_URL = f"{BASE_URL}/simple/price?ids={','.join(CRYPTO_IDS)}&vs_currencies=usd"

def handle_rate_limit(response):
    """Handle rate limiting by waiting if necessary"""
    if response.status_code == 429:
        # If rate limited, wait for a bit before retrying
        time.sleep(60)  # Wait for 60 seconds
        return True
    return False

def make_request(url, params=None, max_retries=3):
    """Make a request with retry logic and rate limit handling"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params)
            if handle_rate_limit(response):
                continue  # Retry after waiting
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:  # Last attempt
                raise e
            time.sleep(5)  # Wait before retrying
    return None

def fetch_historical_data(crypto_id):
    """Fetch 30 days of historical data for a cryptocurrency"""
    try:
        history_url = f"{BASE_URL}/coins/{crypto_id}/market_chart"
        params = {
            'vs_currency': 'usd',
            'days': '30',
            'interval': 'daily'
        }

        data = make_request(history_url, params=params)
        if not data:
            return []

        # Convert the price data to the format we need
        historical_data = []
        for timestamp_ms, price in data['prices']:
            timestamp = datetime.fromtimestamp(timestamp_ms / 1000)  # Convert from milliseconds
            historical_data.append({
                'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'price': price
            })

        return historical_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching historical data for {crypto_id}: {e}")
        return []

def fetch_crypto_prices():
    """Fetch current and historical prices for cryptocurrencies"""
    try:
        # Fetch current prices with retry logic
        current_data = make_request(CURRENT_PRICE_URL)
        if not current_data:
            return {}, None

        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        # Add historical data for each cryptocurrency
        result_data = {}
        for crypto_id in CRYPTO_IDS:
            if crypto_id in current_data:
                result_data[crypto_id] = {
                    'usd': current_data[crypto_id]['usd'],
                    'history': fetch_historical_data(crypto_id)
                }

        return result_data, timestamp
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}, None

