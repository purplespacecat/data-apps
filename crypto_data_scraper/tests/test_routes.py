from fastapi.testclient import TestClient
from app.main import app
from app.services.fetcher import crypto_data

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Crypto Price API!"}

def test_get_prices_no_data():
    crypto_data.clear()
    response = client.get("/prices")
    assert response.status_code == 503
    assert response.json() == {"detail": "No data available yet."}

def test_get_prices_with_data():
    crypto_data.update({
        "timestamp": "2025-01-01T00:00:00Z",
        "prices": {"bitcoin": {"usd": 40000}, "ethereum": {"usd": 3000}}
    })
    response = client.get("/prices")
    assert response.status_code == 200
    assert response.json() == crypto_data

def test_get_price_found():
    crypto_data.update({
        "timestamp": "2025-01-01T00:00:00Z",
        "prices": {"bitcoin": {"usd": 40000}}
    })
    response = client.get("/prices/bitcoin")
    assert response.status_code == 200
    assert response.json() == {
        "timestamp": "2025-01-01T00:00:00Z",
        "price": {"usd": 40000}
    }

def test_get_price_not_found():
    crypto_data.update({
        "timestamp": "2025-01-01T00:00:00Z",
        "prices": {"bitcoin": {"usd": 40000}}
    })
    response = client.get("/prices/ethereum")
    assert response.status_code == 404
    assert response.json() == {"detail": "Cryptocurrency not found."}
