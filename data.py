# getting data from Alpha Vantage API
import pandas as pd 
import os
from dotenv import load_dotenv
import requests
import yfinance as yf
import ccxt

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

def getCryptoData(crypto_symbol, start="2022-06-06", end="2023-01-01", exchange="binance"):
    """
    Fetches cryptocurrency data from a crypto exchange (default: Binance) using ccxt.
    Returns a DataFrame with the closing prices for the specified date range.
    
    Args:
        crypto_symbol: Crypto symbol (e.g., 'BTC/USDT', 'ETH/USDT', or 'BTC-USD' for yfinance)
        start: Start date in 'YYYY-MM-DD' format
        end: End date in 'YYYY-MM-DD' format
        exchange: Exchange name (default: 'binance'). Options: 'binance', 'coinbase', 'kraken', etc.
    
    Returns:
        DataFrame with 'close' column and datetime index
    """
    cache_file = f"cache_{crypto_symbol.replace('/', '_')}_{start}_{end}_{exchange}.csv"
    if os.path.exists(cache_file):
        df = pd.read_csv(cache_file, index_col=0, parse_dates=True)
        return df
    
    # Try multiple exchanges as fallback
    exchanges_to_try = [exchange, 'coinbase', 'kraken', 'kucoin']
    if exchange in exchanges_to_try:
        exchanges_to_try = list(dict.fromkeys(exchanges_to_try))  # Remove duplicates while preserving order
    
    for exch in exchanges_to_try:
        try:
            # Initialize the exchange
            exchange_class = getattr(ccxt, exch)
            exchange_instance = exchange_class({
                'enableRateLimit': True,
            })
            
            # Convert dates to timestamps (milliseconds)
            start_ts = int(pd.to_datetime(start).timestamp() * 1000)
            end_ts = int(pd.to_datetime(end).timestamp() * 1000)
            
            # Fetch OHLCV data with pagination
            all_ohlcv = []
            current_ts = start_ts
            limit = 1000  # Most exchanges limit to 1000 candles per request
            
            while current_ts < end_ts:
                ohlcv = exchange_instance.fetch_ohlcv(
                    crypto_symbol,
                    timeframe='1d',
                    since=current_ts,
                    limit=limit
                )
                
                if not ohlcv:
                    break
                    
                all_ohlcv.extend(ohlcv)
                
                # Move to the next batch (last timestamp + 1 day)
                current_ts = ohlcv[-1][0] + (24 * 60 * 60 * 1000)
                
                # Avoid infinite loops
                if len(ohlcv) < limit:
                    break
            
            if not all_ohlcv:
                continue  # Try next exchange
            
            # Convert to DataFrame
            df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            df = df.sort_index()
            
            # Remove duplicates
            df = df[~df.index.duplicated(keep='last')]
            
            # Filter by date range
            df = df[(df.index >= pd.to_datetime(start)) & (df.index <= pd.to_datetime(end))]
            
            # Keep only close column
            df = df[["close"]]
            df.dropna(inplace=True)
            
            if not df.empty:
                # Save to cache
                df.to_csv(cache_file)
                return df
                
        except Exception as e:
            if exch == exchanges_to_try[-1]:  # Last exchange, will try yfinance
                print(f"Error fetching crypto data from {exch}: {e}")
            continue
    
    # Fallback to yfinance (supports crypto like BTC-USD, ETH-USD)
    print("Note: Exchanges (Binance, Coinbase, etc.) are unavailable or blocked in your location.")
    print("Falling back to yfinance for crypto data...")
    try:
        # Convert exchange format to yfinance format (BTC/USDT -> BTC-USD)
        if '/' in crypto_symbol:
            base, quote = crypto_symbol.split('/')
            # yfinance typically uses USD as quote, not USDT
            if quote.upper() == 'USDT':
                yf_symbol = f"{base}-USD"
            else:
                yf_symbol = f"{base}-{quote}"
        else:
            yf_symbol = crypto_symbol
        
        # Update cache file name for yfinance
        cache_file = f"cache_{yf_symbol.replace('-', '_')}_{start}_{end}_yfinance.csv"
        if os.path.exists(cache_file):
            df = pd.read_csv(cache_file, index_col=0, parse_dates=True)
            return df
        
        df = yf.download(yf_symbol, start=start, end=end, progress=False)
        if df.empty:
            raise ValueError(f"Could not fetch data for {crypto_symbol} from any source")
        df = df[["Close"]]
        df.columns = ["close"]
        df.dropna(inplace=True)
        df.to_csv(cache_file)
        return df
    except Exception as e:
        raise ValueError(f"Could not fetch data for {crypto_symbol} from any source. Last error: {e}")
