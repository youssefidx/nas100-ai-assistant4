import streamlit as st
import pandas as pd
from utils.support_resistance import detect_zones
from utils.trade_signals import generate_trade_signals
from utils.backtest import backtest_strategy
from utils.plots import plot_trades, plot_equity_curve
from utils.download import get_table_download_link
from datetime import time

st.set_page_config(page_title="NAS100 AI Trading Assistant", layout="wide")

st.title("📈 NAS100 AI Trading Assistant")

uploaded_file = st.sidebar.file_uploader("Upload NAS100 Price Data", type=["csv"])
timeframe = st.sidebar.selectbox("Timeframe", ["5min", "15min"])
sl_pct = st.sidebar.slider("Stop Loss %", 1.0, 2.5, 1.5)
tp_pct = st.sidebar.slider("Take Profit %", 3.0, 10.0, 5.0)
use_volume = st.sidebar.checkbox("Use Volume for Confirmation", value=True)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("Data uploaded successfully!")

    zones = detect_zones(df)
    st.subheader("Detected Support & Resistance Zones")
    st.code(str(zones))

    session_start = time(9, 30)
    signals = generate_trade_signals(df, zones, use_volume=use_volume, session_start=session_start)
    signals_df = pd.DataFrame(signals)

    st.subheader("Trade Signals")
    if not signals_df.empty:
        st.write(signals_df.head())
    else:
        st.warning("No trade signals were generated.")

result, equity = backtest_strategy(df, signals_df, sl_pct, tp_pct)

    st.subheader("Trade Visualization")
    st.pyplot(plot_trades(df, signals, zones))

    st.subheader("Equity Curve")
    st.pyplot(plot_equity_curve(equity))

    st.subheader("Performance")
    st.write(f"Total Trades: {result['total']}")
    st.write(f"Wins: {result['wins']} | Losses: {result['losses']}")
    st.write(f"Win Rate: {result['win_rate']}%")
    st.write(get_table_download_link(signals_df), unsafe_allow_html=True)
