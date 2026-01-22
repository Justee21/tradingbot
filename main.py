import data
import indicator
from backtest import backtest

def runSignalAnalysis(stocks, start, end):
    """
    Runs the indicator analysis on a list of stocks for the given date range.
    Returns a dictionary with stock symbols as keys and their corresponding Buy/Sell/Hold signals as values.
    """
    results = {}
    for stock in stocks:
        signal_result = indicator.indicator(stock, start, end, asset_type="stock")
        signal_str, signal_strength = signal_result
        results[stock] = f"{signal_str} (strength: {signal_strength})"
    print(results)
    return results

def runCryptoSignalAnalysis(cryptos, start, end):
    """
    Runs the indicator analysis on a list of cryptocurrencies for the given date range.
    Returns a dictionary with crypto symbols as keys and their corresponding Buy/Sell/Hold signals as values.
    
    Args:
        cryptos: List of crypto symbols (e.g., ['BTC/USDT', 'ETH/USDT'])
        start: Start date in 'YYYY-MM-DD' format
        end: End date in 'YYYY-MM-DD' format
    """
    results = {}
    for crypto in cryptos:
        signal_result = indicator.indicator(crypto, start, end, asset_type="crypto")
        signal_str, signal_strength = signal_result
        results[crypto] = f"{signal_str} (strength: {signal_strength})"
    print(results)
    return results

# Example usage for stocks
# print(backtest("AAPL", "2025-07-20", "2025-08-20", asset_type="stock"))

# Example usage for crypto
# print(backtest("BTC/USDT", "2025-07-20", "2025-08-20", asset_type="crypto")) 