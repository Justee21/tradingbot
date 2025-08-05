import data
import indicator
def runSignalAnalysis(stocks, start, end):
    """
    Runs the indicator analysis on a list of stocks for the given date range.
    Returns a dictionary with stock symbols as keys and their corresponding Buy/Sell/Hold signals as values.
    """
    results = {}
    for stock in stocks:
        signal = indicator.indicator(stock, start, end)
        results[stock] = signal
    print(results)