
import pandas as pd

def backtest_strategy(df, signals, sl_pct=1.5, tp_pct=5.0):
    balance = 10000
    equity_curve = [balance]
    results = []
    
    for _, signal in signals.iterrows():
        entry_time = signal['Datetime']
        entry_price = signal['Price']
        direction = signal['Signal']

        candle = df.loc[df.index >= entry_time]
        sl_hit = False
        tp_hit = False

        for time, row in candle.iterrows():
            high = row['High']
            low = row['Low']
            if direction == "Buy":
                sl = entry_price * (1 - sl_pct / 100)
                tp = entry_price * (1 + tp_pct / 100)
                if low <= sl:
                    balance -= balance * (sl_pct / 100)
                    sl_hit = True
                    break
                elif high >= tp:
                    balance += balance * (tp_pct / 100)
                    tp_hit = True
                    break
            elif direction == "Sell":
                sl = entry_price * (1 + sl_pct / 100)
                tp = entry_price * (1 - tp_pct / 100)
                if high >= sl:
                    balance -= balance * (sl_pct / 100)
                    sl_hit = True
                    break
                elif low <= tp:
                    balance += balance * (tp_pct / 100)
                    tp_hit = True
                    break

        equity_curve.append(balance)
        results.append({
            "Entry Time": entry_time,
            "Signal": direction,
            "Entry Price": entry_price,
            "Exit Time": time,
            "SL Hit": sl_hit,
            "TP Hit": tp_hit,
            "Balance": balance
        })

    equity_series = pd.Series(equity_curve)
    return pd.DataFrame(results), equity_series
