# getting data from Alpha Vantage API
import pandas as pd 
import os
from dotenv import load_dotenv
import requests

load_dotenv()  
alphaKey = os.getenv('alphaKey')

def getData(stock, start = "2022-06-06", end = "2023-01-01"):
    """Fetches stock data from Alpha Vantage API for a given stock symbol and date range.
    Returns a DataFrame with the closing prices for the specified date range."""
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
    # Return only the closing values as a Series
    return df["4. close"]

