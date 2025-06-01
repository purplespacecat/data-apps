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
    prices_data = {crypto: data['usd'] for crypto, data in crypto_data.items()}
    df = pd.DataFrame(prices_data.items(), columns=['Cryptocurrency', 'Price (USD)'])
    df['Cryptocurrency'] = df['Cryptocurrency'].apply(str.capitalize)  # Capitalize crypto names

    # Create a styled dataframe with centered text
    styled_df = df.style.set_table_styles([
        {'selector': 'th', 'props': [('text-align', 'center !important')]},
        {'selector': 'td', 'props': [('text-align', 'center !important')]},
        # Add padding and vertical alignment
        {'selector': '', 'props': [('padding', '8px !important'), ('vertical-align', 'middle')]},
    ]).format({
        'Price (USD)': '${:.2f}'
    })

    # Display the styled dataframe
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )

    # Dropdown to select cryptocurrency
    st.subheader("Price Graph")
    selected_crypto = st.selectbox("Select Cryptocurrency", df['Cryptocurrency'])

    # Get historical data for the selected cryptocurrency
    selected_crypto_lower = selected_crypto.lower()
    if selected_crypto_lower in crypto_data and 'history' in crypto_data[selected_crypto_lower]:
        historical_df = pd.DataFrame(crypto_data[selected_crypto_lower]['history'])
        historical_df['timestamp'] = pd.to_datetime(historical_df['timestamp'])

        # Create the price trend visualization
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        # Plot the line
        ax.plot(historical_df['timestamp'], historical_df['price'],
                linestyle='-', linewidth=2, color='#1f77b4')

        # Add points
        ax.scatter(historical_df['timestamp'], historical_df['price'],
                  color='#1f77b4', s=50, alpha=0.6)

        # Customize the plot
        ax.set_title(f"{selected_crypto} Price Trend - Last 30 Days",
                    fontsize=14, pad=20)
        ax.set_xlabel("Date (UTC)", fontsize=12)
        ax.set_ylabel("Price (USD)", fontsize=12)

        # Format y-axis to show dollar amounts
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.2f}'))

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)

        # Add grid
        ax.grid(True, linestyle='--', alpha=0.7)

        # Adjust layout to prevent label cutoff
        plt.tight_layout()

        # Show the plot
        st.pyplot(fig)

        # Display some key statistics
        st.subheader("Price Statistics")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Current Price",
                f"${crypto_data[selected_crypto_lower]['usd']:,.2f}"
            )

        with col2:
            price_change = (historical_df['price'].iloc[-1] - historical_df['price'].iloc[0])
            price_change_pct = (price_change / historical_df['price'].iloc[0]) * 100
            st.metric(
                "30-Day Change",
                f"${price_change:,.2f}",
                f"{price_change_pct:,.1f}%"
            )

        with col3:
            st.metric(
                "30-Day High",
                f"${historical_df['price'].max():,.2f}"
            )
    else:
        st.warning(f"No historical data available for {selected_crypto}.")
else:
    st.warning("No data available. Please try again later.")
