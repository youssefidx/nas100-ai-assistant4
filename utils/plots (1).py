
import matplotlib.pyplot as plt

def plot_trades(df, signals_df):
    fig, ax = plt.subplots(figsize=(14, 6))
    df['Close'].plot(ax=ax, color='black', label='Close Price')
    
    buys = signals_df[signals_df['Signal'] == 'Buy']
    sells = signals_df[signals_df['Signal'] == 'Sell']
    ax.plot(buys['Datetime'], buys['Price'], '^', color='green', label='Buy Signal', markersize=8)
    ax.plot(sells['Datetime'], sells['Price'], 'v', color='red', label='Sell Signal', markersize=8)
    
    ax.set_title("Trade Entries on NAS100")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.legend()
    return fig

def plot_equity_curve(equity):
    fig, ax = plt.subplots(figsize=(10, 4))
    equity.plot(ax=ax, color='blue')
    ax.set_title("Equity Curve")
    ax.set_ylabel("Balance")
    return fig
