import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from services import fetch_crypto_prices  # Import from services.py

# Streamlit app configuration
st.set_page_config(page_title="Crypto Price Dashboard", layout="wide")

# Title
st.title("Crypto Price Dashboard")

# Fetch and display crypto prices
crypto_data, timestamp = fetch_crypto_prices()

if crypto_data:
    st.subheader(f"Latest Prices (as of {timestamp} UTC)")

    # Format data for display
    df = pd.DataFrame(crypto_data).T  # Transpose for better display
    df.columns = ['Price (USD)']
    df.index = [crypto.capitalize() for crypto in df.index]  # Capitalize crypto names

    # Display data table with adjusted width and left-aligned text
    st.dataframe(df.style.set_properties(**{'text-align': 'left'}), use_container_width=True)

    # Dropdown to select cryptocurrency
    st.subheader("Price Graph")
    selected_crypto = st.selectbox("Select Cryptocurrency", df.index)

    # Assume historical data is nested inside the fetched data
    if 'history' in crypto_data[selected_crypto.lower()]:
        historical_df = pd.DataFrame(crypto_data[selected_crypto.lower()]['history'])
        historical_df['timestamp'] = pd.to_datetime(historical_df['timestamp'])
    else:
        st.warning(f"No historical data available for {selected_crypto}.")
        historical_df = pd.DataFrame({'timestamp': [timestamp], 'price': [df.loc[selected_crypto, 'Price (USD)']]})

    # Plot graph for the selected cryptocurrency with historical data
    st.write(f"**{selected_crypto}**")
    fig, ax = plt.subplots()
    ax.plot(historical_df['timestamp'], historical_df['price'], marker='o', linestyle='-', color='b')
    ax.set_title(f"{selected_crypto} Price Over Time")
    ax.set_xlabel("Time (UTC)")
    ax.set_ylabel("Price (USD)")
    st.pyplot(fig)
else:
    st.warning("No data available. Please try again later.")
