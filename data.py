# getting data from Alpha Vantage API
import pandas as pd 
import os
from dotenv import load_dotenv
import requests
import yfinance as yf

load_dotenv()  
alphaKey = os.getenv('alphaKey')

def getData(stock, start = "2022-06-06", end = "2023-01-01", source="alphavantage"):
    """Fetches stock data from Alpha Vantage API or yfinance for a given stock symbol and date range.
    Returns a DataFrame with the closing prices for the specified date range."""
    cache_file = f"cache_{stock}_{start}_{end}_{source}.csv"
    if os.path.exists(cache_file):
        df = pd.read_csv(cache_file, index_col=0, parse_dates=True)
        return df
    if source == "alphavantage":
        url = 'https://www.alphavantage.co/query'
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": stock,
            "outputsize": "compact",
            "apikey": alphaKey
        }
        r = requests.get(url, params)
        data = r.json()
        # Extract time series data
        ts_key = "Time Series (Daily)"
        if ts_key not in data:
            print("API response:", data)
            raise KeyError(f"'{ts_key}' not found in API response.")   
        ts_data = data[ts_key]
        df = pd.DataFrame.from_dict(ts_data, orient="index")
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        # Filter by date range
        df = df[(df.index >= pd.to_datetime(start)) & (df.index <= pd.to_datetime(end))]
        df = df.apply(pd.to_numeric)
        df = df.apply(pd.to_numeric)
        df = df.rename(columns={"4. close": "close"}) 
        df = df[["close"]]  # Keep only close column
        df.to_csv(cache_file)
        return df
    elif source == "yfinance":
        df = yf.download(stock, start=start, end=end)
        df = df[["Close"]]
        df.columns = ["close"]
        df.dropna(inplace=True)
        df.to_csv(cache_file)
        return df

