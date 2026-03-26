import streamlit as st
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go

# App Title
st.set_page_config(page_title="Bank Nifty Trend Analyzer", layout="wide")
st.title("📈 Bank Nifty Trend Analyzer")

# Sidebar for inputs
symbol = st.sidebar.text_input("Symbol", "^NSEBANK") # Bank Nifty Yahoo Finance ticker
interval = st.sidebar.selectbox("Interval", ["15m", "60m", "1d"])

# Fetch Data
data = yf.download(symbol, period="1mo", interval=interval)

if not data.empty:
    # Indicators Calculation
    data['RSI'] = ta.rsi(data['Close'], length=14)
    data['MA20'] = ta.sma(data['Close'], length=20)
    
    current_price = data['Close'].iloc[-1]
    last_rsi = data['RSI'].iloc[-1]
    last_ma = data['MA20'].iloc[-1]
    
    # Dashboard Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Price", f"{current_price:.2f}")
    col2.metric("RSI (14)", f"{last_rsi:.2f}")
    col3.metric("SMA (20)", f"{last_ma:.2f}")
    
    # Simple Trend Logic
    st.subheader("Current Trend")
    if current_price > last_ma and last_rsi > 55:
        st.success("🚀 BULLISH (Upward Trend)")
    elif current_price < last_ma and last_rsi < 45:
        st.error("📉 BEARISH (Downward Trend)")
    else:
        st.warning("↔️ NEUTRAL / SIDEWAYS")

    # Interactive Chart
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Price'))
    fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], line=dict(color='orange'), name='MA 20'))
    st.plotly_chart(fig, use_container_view=True)

else:
    st.error("Data nahi mil raha. Please check symbol.")
