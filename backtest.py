from data import getData
from indicator import indicator
import matplotlib.pyplot as plt
import pandas as pd
def backtest(stock, start, end, initial_investment=10000):
    total_days = (pd.to_datetime(end) - pd.to_datetime(start)).days
    window_size = max(1, total_days // 5)
    df = getData(stock, start=start, end=end)
    if df.empty or len(df) < window_size:
        print("Not enough data to run backtest.")
        return None
    portfolio_value = []
    cash = initial_investment
    shares = 0
    dates = df.index
    for i in range(window_size, len(df)):
        current_date = dates[i]
        current_price = df.iloc[i]['close']
        
        # Get the trading signal
        signal = indicator(df.iloc[:i+1], start=str(dates[i - window_size].date()), end=str(current_date.date()))
        
        if signal == "Buy" and cash >= current_price:
            shares += cash // current_price
            cash -= shares * current_price
        elif signal == "Sell" and shares > 0:
            cash += shares * current_price
            shares = 0
            
        # Calculate portfolio value
        portfolio_value.append(cash + shares * current_price)
        
    final_value = portfolio_value[-1]
    gain = ((final_value - initial_investment) / initial_investment) * 100

    print(f"Final Portfolio Value: ${final_value:.2f}")
    print(f"Total Gain: {gain:.2f}%")

    plt.plot(dates[window_size:], portfolio_value)
    plt.title(f"Backtest of {stock} from {start} to {end}")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value ($)")
    plt.tight_layout()
    plt.show()

    return gain