import streamlit as st
import pandas as pd
from services import fetch_crypto_prices  # Import from services.py

# Streamlit app configuration
st.set_page_config(page_title="Crypto Price Dashboard", layout="centered")

# Title
st.title("📈 Crypto Price Dashboard")

# Fetch and display crypto prices
crypto_data, timestamp = fetch_crypto_prices()

if crypto_data:
    st.subheader(f"Latest Prices (as of {timestamp} UTC)")

    # Format data for display
    df = pd.DataFrame(crypto_data).T  # Transpose for better display
    df.columns = ['Price (USD)']
    df.index = [crypto.capitalize() for crypto in df.index]  # Capitalize crypto names

    st.dataframe(df)  # Use st.dataframe for better detection in tests
else:
    st.warning("No data available. Please try again later.")
