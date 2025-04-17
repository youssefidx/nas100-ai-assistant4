
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils.support_resistance import detect_zones
from utils.trade_signals import generate_trade_signals
from utils.backtest import backtest_strategy
from utils.plots import plot_trades, plot_equity_curve
from utils.download import get_table_download_link

st.set_page_config(page_title="NAS100 AI Trading Assistant", layout="wide")

st.title("📈 NAS100 AI Trading Assistant")

uploaded_file = st.file_uploader("Upload NAS100 Price CSV", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df.set_index('Datetime', inplace=True)

    st.subheader("Raw Data")
    st.write(df.head())

    # Parameters
    use_volume = st.checkbox("Use Volume for Confirmation", value=True)
    sl_pct = st.slider("Stop Loss (%)", 1.0, 2.5, 1.5)
    tp_pct = st.slider("Take Profit (%)", 3.0, 10.0, 5.0)
    session_start = st.time_input("Start Trading After (EDT)", value=pd.to_datetime("09:30").time())

    # Detect zones
    zones = detect_zones(df)
    st.subheader("Detected Support & Resistance Zones")
    st.write(zones)

    # Generate signals
    signals = generate_trade_signals(df, zones, use_volume=use_volume, session_start=session_start)
    signals_df = pd.DataFrame(signals)

    st.subheader("Trade Signals")
    if signals_df.empty:
        st.warning("No trade signals were generated.")
    else:
        st.write(signals_df.head())
        st.markdown(get_table_download_link(signals_df), unsafe_allow_html=True)

        # Backtest
        result, equity = backtest_strategy(df, signals_df, sl_pct, tp_pct)

        st.subheader("Equity Curve")
        fig1 = plot_equity_curve(equity)
        st.pyplot(fig1)

        st.subheader("Candlestick Chart with Trades")
        fig2 = plot_trades(df, signals_df)
        st.pyplot(fig2)

        st.subheader("Win/Loss Stats")
        st.write(result)
else:
    st.info("Please upload a NAS100 price CSV file to begin.")
