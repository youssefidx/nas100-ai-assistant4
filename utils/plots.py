import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def plot_trades(df, signals, zones):
    fig, ax = plt.subplots(figsize=(12, 6))

    df_plot = df.copy()
    df_plot['Datetime'] = df_plot['Datetime'] if 'Datetime' in df_plot.columns else df_plot.index
    df_plot['Datetime'] = pd.to_datetime(df_plot['Datetime'])

    ax.plot(df_plot['Datetime'], df_plot['Close'], label='Close Price', linewidth=1)

    for zone in zones:
        if isinstance(zone, dict):
            if 'support' in zone:
                ax.axhline(zone['support'], color='green', linestyle='--', alpha=0.5)
            if 'resistance' in zone:
                ax.axhline(zone['resistance'], color='red', linestyle='--', alpha=0.5)

    for signal in signals:
        dt = pd.to_datetime(signal['Datetime'])
        if signal['Signal'] == 'breakout_long':
            ax.scatter(dt, signal['Price'], color='blue', marker='^', label='Long Entry')
        elif signal['Signal'] == 'breakout_short':
            ax.scatter(dt, signal['Price'], color='orange', marker='v', label='Short Entry')

    ax.set_title("Trade Signals on Price Chart")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    fig.autofmt_xdate()
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())
    return fig

def plot_equity_curve(equity):
    fig, ax = plt.subplots(figsize=(10, 4))
    equity['Datetime'] = pd.to_datetime(equity['Datetime'])
    ax.plot(equity['Datetime'], equity['Equity'], label='Equity Curve', color='blue')
    ax.set_title("Equity Curve")
    ax.set_xlabel("Time")
    ax.set_ylabel("Equity")
    ax.legend()
    return fig
