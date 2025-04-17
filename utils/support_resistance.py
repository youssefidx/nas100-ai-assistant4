
import pandas as pd

def detect_zones(data: pd.DataFrame, window: int = 50, threshold: float = 0.02):
    """
    Detect support and resistance zones based on price clustering and wicks.
    
    :param data: A pandas DataFrame with at least the 'High', 'Low', 'Close' columns
    :param window: The window size for calculating local highs/lows
    :param threshold: The price movement threshold to consider for support/resistance
    :return: A tuple of support and resistance levels (support, resistance)
    """

    # Ensure 'Close', 'High', and 'Low' columns are in the data
    if not all(col in data.columns for col in ['Close', 'High', 'Low']):
        raise ValueError("Data must contain 'Close', 'High', and 'Low' columns.")

    # Find local peaks and valleys (support and resistance levels)
    data['rolling_max'] = data['High'].rolling(window=window).max()
    data['rolling_min'] = data['Low'].rolling(window=window).min()

    # Define support (local minimum) and resistance (local maximum)
    support = data[data['Low'] == data['rolling_min']]['Low']
    resistance = data[data['High'] == data['rolling_max']]['High']

    # Filter support and resistance by threshold
    support = support[support.pct_change() > threshold]
    resistance = resistance[resistance.pct_change() > threshold]

    return support, resistance
