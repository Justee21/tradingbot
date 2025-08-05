#some strategies for trading
# using indicators like moving averages, Bollinger Bands, and RSI
import os
import data
import pandas as pd
def movingAverages(stock, end=None, window=20):
    """
    Calculates Moving Average for the last 'window' periods up to 'end' date (or latest if end is None).
    """
    df = data.getData(stock, end=end) if end else data.getData(stock)
    if end:
        df = df[df.index <= pd.to_datetime(end)]
    df = df.tail(window)
    return df.mean()



def bollingerBands(stock, end=None, window=20, num_std=2):
    """
    Calculates Bollinger Bands for the last 'window' periods up to 'end' date (or latest if end is None).
    """
    df = data.getData(stock, end=end) if end else data.getData(stock)
    if end:
        df = df[df.index <= pd.to_datetime(end)]
    df = df.tail(window)
    rolling_mean = df.mean()
    rolling_std = df.std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return pd.DataFrame({"mean": [rolling_mean], "upper": [upper_band], "lower": [lower_band]}, index=[df.index[-1]])


def rsi(stock, end=None, window=20):
    """
    Calculates the Relative Strength Index (RSI) for the last 'window' periods up to 'end' date (or latest if end is None).
    """
    df = data.getData(stock, end=end) if end else data.getData(stock)
    if end:
        df = df[df.index <= pd.to_datetime(end)]
    df = df.tail(window+1)  # Need window+1 for diff
    delta = df.diff()
    gain = (delta.where(delta > 0, 0)).mean()
    loss = (-delta.where(delta < 0, 0)).mean()
    rs = gain / loss if loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    return rsi