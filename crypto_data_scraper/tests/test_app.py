import sys
import os
import pytest
from unittest.mock import patch
import requests  # Import requests to use the correct exception type

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services import fetch_crypto_prices  # Import from services.py
import app  # For rendering tests

# Test 1: Check if API fetch function works correctly
def test_fetch_crypto_prices_success():
    mock_response = {
        "bitcoin": {"usd": 40000},
        "ethereum": {"usd": 3000}
    }

    with patch('services.requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status = lambda: None  # Simulate no error

        data, timestamp = fetch_crypto_prices()
        assert "bitcoin" in data
        assert data["bitcoin"]["usd"] == 40000

# Test 2: Check if API fetch handles errors


def test_fetch_crypto_prices_failure():
    with patch('services.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("API request failed")  # Use correct exception

        data, timestamp = fetch_crypto_prices()
        assert data == {}  # Should return empty data on failure
        assert timestamp is None


# Test 3: Check if Streamlit elements are rendered
def test_app_render(monkeypatch):
    from streamlit.testing.v1 import AppTest

    # Mock data to avoid actual API calls
    mock_response = {
        "bitcoin": {"usd": 40000},
        "ethereum": {"usd": 3000}
    }
    monkeypatch.setattr('services.fetch_crypto_prices', lambda: (mock_response, "2025-01-01 00:00:00"))

    at = AppTest.from_file("crypto_data_scraper/app.py")
    at.run()

    # Debugging: Check what elements are being captured
    print(f"Titles found: {at.title}")
    print(f"DataFrames found: {at.dataframe}")

    # Check if title is rendered
    assert len(at.title) > 0, "No titles were rendered in the app!"
    assert "Crypto Price Dashboard" in at.title[0].value

    # Check if DataFrame is rendered
    assert len(at.dataframe) > 0, "No dataframes were rendered in the app!"
    assert at.dataframe[0].value.shape == (2, 1)  # 2 cryptocurrencies, 1 column (Price)
