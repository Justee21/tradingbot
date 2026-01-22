"""
Example script demonstrating how to use crypto trading functionality.
This follows the same pattern as stock trading but for cryptocurrencies.
"""

import data
import indicator
from backtest import backtest

# Example 1: Get crypto signal analysis for multiple cryptocurrencies
def example_crypto_signals():
    """Analyze multiple cryptocurrencies and get Buy/Sell/Hold signals."""
    cryptos = ["BTC/USDT", "ETH/USDT", "BNB/USDT"]
    start = "2024-01-01"
    end = "2024-12-31"
    
    print("Running crypto signal analysis...")
    results = {}
    for crypto in cryptos:
        signal_result = indicator.indicator(crypto, start, end, asset_type="crypto")
        signal_str, signal_strength = signal_result
        results[crypto] = f"{signal_str} (strength: {signal_strength})"
        print(f"{crypto}: {signal_str} (strength: {signal_strength})")
    
    return results

# Example 2: Backtest a cryptocurrency
def example_crypto_backtest():
    """Backtest a trading strategy on Bitcoin."""
    crypto_symbol = "BTC/USDT"
    start = "2024-01-01"
    end = "2024-12-31"
    initial_investment = 10000
    
    print(f"\nBacktesting {crypto_symbol} from {start} to {end}...")
    gain = backtest(crypto_symbol, start, end, initial_investment, asset_type="crypto")
    print(f"Total gain: {gain:.2f}%")
    return gain

# Example 3: Fetch crypto data directly
def example_fetch_crypto_data():
    """Fetch cryptocurrency data directly."""
    crypto_symbol = "BTC/USDT"
    start = "2024-01-01"
    end = "2024-12-31"
    
    print(f"\nFetching data for {crypto_symbol}...")
    df = data.getCryptoData(crypto_symbol, start=start, end=end, exchange="binance")
    print(f"Data shape: {df.shape}")
    print(f"First few rows:\n{df.head()}")
    print(f"Last few rows:\n{df.tail()}")
    return df

# Example 4: Compare multiple cryptocurrencies
def example_compare_cryptos():
    """Compare backtest results for multiple cryptocurrencies."""
    cryptos = ["BTC/USDT", "ETH/USDT"]
    start = "2024-01-01"
    end = "2024-12-31"
    
    print("\nComparing cryptocurrency backtests...")
    results = {}
    for crypto in cryptos:
        print(f"\nBacktesting {crypto}...")
        gain = backtest(crypto, start, end, asset_type="crypto")
        results[crypto] = gain
    
    print("\n=== Comparison Results ===")
    for crypto, gain in results.items():
        print(f"{crypto}: {gain:.2f}%")
    
    return results

# Example 5: Use different exchanges
def example_different_exchanges():
    """Fetch data from different crypto exchanges."""
    crypto_symbol = "BTC/USDT"
    start = "2024-01-01"
    end = "2024-01-31"
    
    exchanges = ["binance", "coinbase", "kraken"]
    
    print("\nFetching data from different exchanges...")
    for exchange in exchanges:
        try:
            print(f"\nTrying {exchange}...")
            df = data.getCryptoData(crypto_symbol, start=start, end=end, exchange=exchange)
            print(f"Success! Got {len(df)} data points from {exchange}")
        except Exception as e:
            print(f"Failed to fetch from {exchange}: {e}")

if __name__ == "__main__":
    # Uncomment the examples you want to run:
    
    # Example 1: Get signals for multiple cryptos
    # example_crypto_signals()
    
    # Example 2: Backtest a single crypto
    # example_crypto_backtest()
    
    # Example 3: Fetch crypto data
    # example_fetch_crypto_data()
    
    # Example 4: Compare multiple cryptos
    # example_compare_cryptos()
    
    # Example 5: Try different exchanges
    # example_different_exchanges()
    
    # Quick test - using BTC-USD format (works better with yfinance fallback)
    # You can also use BTC/USDT format - it will automatically convert to BTC-USD for yfinance
    # Using a volatile period (2022) where trading strategy can outperform buy-and-hold
    # This period had significant ups and downs, perfect for testing the strategy
    print("Quick crypto backtest example:")
    print("Note: Using BTC-USD format (yfinance format) for better compatibility")
    print("Note: If Binance/Coinbase are blocked in your location, yfinance will be used automatically")
    print("Using a volatile period (Nov 2022 - Feb 2023) with bottom formation and recovery...")
    print("This period had significant volatility from bottom to early recovery, perfect for trading")
    try:
        result = backtest("BTC-USD", "2022-11-01", "2023-02-28", asset_type="crypto")
        print(f"Backtest result: {result:.2f}%")
        
        # Calculate buy-and-hold for comparison
        from data import getCryptoData
        df = getCryptoData("BTC-USD", start="2022-11-01", end="2023-02-28")
        if not df.empty:
            buy_hold_return = ((df.iloc[-1]['close'] - df.iloc[0]['close']) / df.iloc[0]['close']) * 100
            print(f"\nBuy-and-Hold return: {buy_hold_return:.2f}%")
            print(f"Strategy vs Buy-and-Hold: {result - buy_hold_return:.2f}% difference")
            if result > buy_hold_return:
                print(f"✓ Strategy outperformed buy-and-hold by {result - buy_hold_return:.2f}%!")
            else:
                print(f"✗ Strategy underperformed buy-and-hold by {buy_hold_return - result:.2f}%")
    except Exception as e:
        print(f"Error: {e}")
        print("Trying with BTC/USDT format...")
        result = backtest("BTC/USDT", "2022-11-01", "2023-02-28", asset_type="crypto")
        print(f"Backtest result: {result:.2f}%")
