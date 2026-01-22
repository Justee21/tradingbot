#some strategies for trading
# using indicators like moving averages, Bollinger Bands, and RSI
import os
import data
import pandas as pd
def movingAverages(df, end=None, window=20):
    """
    Calculates Moving Average for the last 'window' periods up to 'end' date (or latest if end is None).
    """
    df = df.copy()
    if end is not None:
        # Filter to data up to end date
        df = df[df.index <= pd.to_datetime(end)]
    # Take the last 'window' periods
    df = df.tail(window)
    if len(df) == 0:
        return 0
    return df["close"].mean()



def bollingerBands(df, end=None, window=20, num_std=2):
    """
    Calculates Bollinger Bands for the last 'window' periods up to 'end' date (or latest if end is None).
    """
    df = df.copy()
    if end is not None:
        # Filter to data up to end date
        df = df[df.index <= pd.to_datetime(end)]
    # Take the last 'window' periods
    df = df.tail(window)
    if len(df) == 0:
        # Return default values if no data
        return pd.DataFrame({"mean": [0], "upper": [0], "lower": [0]}, index=[pd.Timestamp.now()])
    rolling_mean = df["close"].mean()
    rolling_std = df["close"].std()
    if pd.isna(rolling_std) or rolling_std == 0:
        rolling_std = 0.01  # Small default to avoid division issues
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return pd.DataFrame({"mean": [rolling_mean], "upper": [upper_band], "lower": [lower_band]}, index=[df.index[-1]])


def rsi(df, end=None, window=20):
    """
    Calculates the Relative Strength Index (RSI) for the last 'window' periods up to 'end' date (or latest if end is None).
    """
    df = df.copy()
    if end is not None:
        # Filter to data up to end date
        df = df[df.index <= pd.to_datetime(end)]
    # Need window+1 for diff calculation
    df = df.tail(window+1)
    if len(df) < 2:
        return 50  # Neutral RSI if not enough data
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).mean()
    loss = (-delta.where(delta < 0, 0)).mean()
    rs = gain / loss if loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    return rsi