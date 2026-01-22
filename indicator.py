import pandas as pd
import data
import strategies
def indicator(stock_or_df, start, end, asset_type="stock"):
    """
    Uses a variety of strategies to generate indicators for a given stock or crypto which
    can be used for trading decisions.
    
    Args:
        stock_or_df: Stock symbol, crypto symbol, or DataFrame
        start: Start date
        end: End date
        asset_type: "stock" or "crypto" (default: "stock")
    """
    if isinstance(stock_or_df, pd.DataFrame):
        df = stock_or_df.copy()
    else:
        # If stock_or_df is a string, fetch data
        symbol = stock_or_df
        if asset_type == "crypto":
            try:
                df = data.getCryptoData(symbol, start=start, end=end)
            except:
                # Fallback: try yfinance format (e.g., BTC-USD)
                df = data.getData(symbol, start=start, end=end, source="yfinance")
        else:
            # Default to stock
            try:
                df = data.getData(symbol, start=start, end=end)
            except:
                df = data.getData(symbol, start=start, end=end, source="yfinance")

    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    signal = 0

    # Set up the windows so that there are 5 windows of equal size and the ends of these windows are in
    # window_ends variable
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    total_days = (end - start).days
    
    # Filter dataframe to the date range
    df_filtered = df[(df.index >= start) & (df.index <= end)]
    
    # Calculate window size based on available data
    # We need at least 5 windows, so window_size should be total_days // 5
    # But we also want at least 5 data points per window for meaningful analysis
    window_size = max(5, total_days // 5)
    
    # If we don't have enough data points, reduce window size
    if len(df_filtered) < window_size * 5:
        # Adjust window size to fit available data
        window_size = max(3, len(df_filtered) // 5)
        if window_size < 3 or len(df_filtered) < 10:
            return "Hold"  # Not enough data for analysis
    
    window_ends = []
    for i in range(5):
        window_ends.append(start + pd.Timedelta(days=window_size * (i + 1)))
    
    MAs = []
    for window_end in window_ends:
        # Filter data up to window_end
        df_window = df_filtered[df_filtered.index <= window_end]
        if len(df_window) < window_size:
            # Use all available data if not enough
            MA = strategies.movingAverages(df_window, end=window_end, window=min(window_size, len(df_window)))
        else:
            MA = strategies.movingAverages(df_window, end=window_end, window=window_size)
        MAs.append(MA)
    maTrend = "neutral"
    # Improved trend detection: stronger weight for recent trends
    recent_trend = (MAs[4] - MAs[0]) / MAs[0] if MAs[0] > 0 else 0  # Percentage change
    
    if ((MAs[4]>=MAs[3]) and (MAs[3]>=MAs[2]) and (MAs[2]>=MAs[1]) and (MAs[1]>=MAs[0])):
        maTrend = "up"
        signal += 1
        # Stronger signal if trend is accelerating
        if MAs[4] > MAs[3] * 1.02:  # Recent acceleration
            signal += 1
    elif ((MAs[4]<=MAs[3]) and (MAs[3]<=MAs[2]) and (MAs[2]<=MAs[1]) and (MAs[1]<=MAs[0])):
        maTrend = "down"
        signal -= 1
        # Stronger signal if downtrend is accelerating
        if MAs[4] < MAs[3] * 0.98:  # Recent acceleration
            signal -= 1
    
    bbSignal = strategies.bollingerBands(df_filtered, end = end, window = window_size)
    current_price = df_filtered.iloc[-1]["close"] if len(df_filtered) > 0 else 0
    
    # Improved Bollinger Bands logic: buy when oversold in uptrend, sell when overbought in downtrend
    if len(df_filtered) > 0 and len(bbSignal) > 0:
        bb_upper = bbSignal["upper"].iloc[0]
        bb_lower = bbSignal["lower"].iloc[0]
        bb_middle = bbSignal["mean"].iloc[0]
        
        # Buy signal: price below lower band in uptrend (oversold bounce opportunity)
        if current_price < bb_lower and maTrend == "up":
            signal += 1
        # Strong buy: price well below lower band
        if current_price < bb_lower * 0.98:
            signal += 1
            
        # Sell signal: price above upper band in downtrend (overbought in weak market)
        if current_price > bb_upper and maTrend == "down":
            signal -= 1
        # Strong sell: price well above upper band
        if current_price > bb_upper * 1.02:
            signal -= 1
    
    rsi = strategies.rsi(df_filtered, end = end, window = window_size)
    
    # Improved RSI logic: more nuanced signals
    # Buy when RSI is oversold (<30) especially in uptrend (dip buying)
    if rsi < 30:
        if maTrend == "up":
            signal += 2  # Strong buy: oversold in uptrend
        elif maTrend == "neutral":
            signal += 1  # Moderate buy: oversold
    # Strong oversold
    elif rsi < 20:
        signal += 1  # Extreme oversold
    
    # Sell when RSI is overbought (>70) especially in downtrend
    if rsi > 70:
        if maTrend == "down":
            signal -= 2  # Strong sell: overbought in downtrend
        elif maTrend == "neutral":
            signal -= 1  # Moderate sell: overbought
    # Strong overbought
    elif rsi > 80:
        signal -= 1  # Extreme overbought
    
    # RSI divergence: if price is making new lows but RSI is rising (bullish)
    if len(df_filtered) >= 10:
        recent_low = df_filtered["close"].tail(10).min()
        recent_high = df_filtered["close"].tail(10).max()
        price_change = (current_price - recent_low) / recent_low if recent_low > 0 else 0
        if price_change > 0.05 and rsi < 50 and maTrend == "up":  # Price recovering, RSI not overbought
            signal += 1
    # Return both the signal string and the numeric signal strength
    if signal >= 1:
        return ("Buy", signal)
    elif signal <= -1:
        return ("Sell", signal)
    else:
        return ("Hold", 0)
    
    