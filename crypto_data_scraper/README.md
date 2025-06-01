# Crypto Data Scraper

A real-time cryptocurrency price tracking dashboard built with Streamlit. This application fetches live cryptocurrency data from the CoinGecko API and presents it in an interactive, user-friendly interface.

## Features
- **Live Price Tracking**: Real-time price updates for major cryptocurrencies (Bitcoin, Ethereum, Litecoin, Ripple, Cardano, and Dogecoin)
- **Historical Data**: 30-day price history charts with daily intervals
- **Interactive Visualizations**: Dynamic price charts with hover tooltips and zoom capabilities
- **Price Statistics**: Key metrics including current price, 30-day change, and price highs
- **Responsive Design**: Clean, modern UI that adapts to different screen sizes

## Setup

### Prerequisites
- Python 3.10 or higher
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd data-apps/crypto_data_scraper
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the App
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

### Docker Support
You can also run the app using Docker:

```bash
docker build -t crypto-price-dashboard .
docker run -p 8501:8501 crypto-price-dashboard
```

## Technical Details

### Data Source
- Uses the CoinGecko API for cryptocurrency data
- Implements rate limiting and retry logic for reliable data fetching
- Caches responses to minimize API calls

### Architecture
- `app.py`: Main Streamlit application and UI components
- `services.py`: API interaction and data processing logic
- Rate-limited requests with automatic retries
- Error handling for API failures

## Testing
Run the tests using:
```bash
pytest tests/
```

## Contributing
Feel free to submit issues and enhancement requests!