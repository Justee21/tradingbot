import pandas as pd
import data
import strategies
def indicator(stock_or_df, start, end):
    """
    Uses a variety of strategies to generate indicators for a given stock which
    can be used for trading decisions."""
    if isinstance(stock_or_df, pd.DataFrame):
        df = stock_or_df.copy()
    else:
        # If stock_or_df is a string, fetch data using data.getData
        stock = stock_or_df
        try:
            df = data.getData(stock, start = start, end = end)
        except:
            df = data.getData(stock, start = start, end = end, source="yfinance")

    df.index = pd.to_datetime(df.index)

    signal = 0

    # Set up the windows so that there are 5 windows of equal size and the ends of these windows are in
    # window_ends variable
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    total_days = (end - start).days
    window_size = total_days // 5
    window_ends = []
    for i in range(5):
        window_ends.append(start + pd.Timedelta(days=window_size * (i + 1)))
    MAs = []
    for window_end in window_ends:
        MA = strategies.movingAverages(df, end=window_end)
        MAs.append(MA)
    maTrend = "neutral"
    if ((MAs[4]>=MAs[3]) and (MAs[3]>=MAs[2]) and (MAs[2]>=MAs[1]) and (MAs[1]>=MAs[0])):
        maTrend = "up"
        signal+=1
    elif ((MAs[4]<=MAs[3]) and (MAs[3]<=MAs[2]) and (MAs[2]<=MAs[1]) and (MAs[1]<=MAs[0])):
        signal-=1
        maTrend = "down"
    bbSignal = strategies.bollingerBands(df, end = end, window = window_size)
    # Check if the last closing price is above or below the Bollinger Bands
    if (df.iloc[-1]["close"] > bbSignal["upper"].iloc[0] and maTrend == "down"):
        signal-=1
    elif (df.iloc[-1]["close"] < bbSignal["lower"].iloc[0] and maTrend == "up"):
        signal+=1
    rsi = strategies.rsi(df, end = end, window = window_size)
    # Check RSI conditions and compare with moving average trend
    if (rsi > 70 and maTrend == "up"):
        signal-=1
    elif (rsi < 30 and maTrend == "down"):
        signal+=1
    if signal >= 1:
        return "Buy"
    elif signal <= -1:
        return "Sell"
    else:
        return "Hold"
    
    