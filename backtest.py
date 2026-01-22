from data import getData, getCryptoData
from indicator import indicator
import matplotlib.pyplot as plt
import pandas as pd
def backtest(symbol, start, end, initial_investment=10000, asset_type="stock"):
    """
    Backtests a trading strategy on a stock or cryptocurrency.
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL') or crypto symbol (e.g., 'BTC/USDT')
        start: Start date in 'YYYY-MM-DD' format
        end: End date in 'YYYY-MM-DD' format
        initial_investment: Starting capital (default: 10000)
        asset_type: "stock" or "crypto" (default: "stock")
    
    Returns:
        Percentage gain/loss
    """
    total_days = (pd.to_datetime(end) - pd.to_datetime(start)).days
    window_size = max(1, total_days // 5)
    
    # Fetch data based on asset type
    if asset_type == "crypto":
        df = getCryptoData(symbol, start=start, end=end)
    else:
        df = getData(symbol, start=start, end=end)
    if df.empty or len(df) < window_size:
        print("Not enough data to run backtest.")
        return None
    portfolio_value = []
    cash = initial_investment
    shares = 0
    dates = df.index
    signals_generated = {"Buy": 0, "Sell": 0, "Hold": 0}
    trades_executed = {"Buy": 0, "Sell": 0}
    
    # Risk management: track entry prices for stop loss and take profit
    entry_prices = []  # Track entry price for each position
    stop_loss_pct = 0.05  # 5% stop loss
    take_profit_pct = 0.15  # 15% take profit
    
    print(f"Data points: {len(df)}, Window size: {window_size}")
    print(f"First price: ${df.iloc[0]['close']:.2f}, Last price: ${df.iloc[-1]['close']:.2f}")
    print(f"Risk management: Stop loss: {stop_loss_pct*100:.0f}%, Take profit: {take_profit_pct*100:.0f}%")
    
    for i in range(window_size, len(df)):
        current_date = dates[i]
        current_price = df.iloc[i]['close']
        
        # Check stop loss and take profit for existing positions
        if shares > 0 and len(entry_prices) > 0:
            avg_entry_price = sum(entry_prices) / len(entry_prices)
            price_change = (current_price - avg_entry_price) / avg_entry_price
            
            # Stop loss: sell if down more than stop_loss_pct
            if price_change <= -stop_loss_pct:
                cash += shares * current_price
                shares = 0
                entry_prices = []
                trades_executed["Sell"] += 1
            # Take profit: sell if up more than take_profit_pct
            elif price_change >= take_profit_pct:
                # Sell 50% to lock in profits, keep 50% for further gains
                shares_to_sell = shares * 0.5
                cash += shares_to_sell * current_price
                shares -= shares_to_sell
                # Remove half of entry prices
                entry_prices = entry_prices[:len(entry_prices)//2] if len(entry_prices) > 1 else []
                trades_executed["Sell"] += 1
        
        # Get the trading signal (returns tuple: (signal_string, signal_strength))
        signal_result = indicator(df.iloc[:i+1], start=str(dates[i - window_size].date()), end=str(current_date.date()), asset_type=asset_type)
        signal_str, signal_strength = signal_result
        signals_generated[signal_str] = signals_generated.get(signal_str, 0) + 1
        
        if signal_str == "Buy" and cash > 0:
            # Use signal strength to determine position size
            # Signal strength can be 1, 2, or 3 (stronger = invest more)
            # Invest proportionally: +1 = 33%, +2 = 66%, +3 = 100% of available cash
            max_signal_strength = 3  # Maximum possible signal strength
            position_size_pct = min(1.0, abs(signal_strength) / max_signal_strength)
            cash_to_invest = cash * position_size_pct
            
            if asset_type == "crypto":
                # For crypto, support fractional shares - can always buy with any amount of cash
                shares_to_buy = cash_to_invest / current_price
                if shares_to_buy > 0:
                    cash -= cash_to_invest
                    shares += shares_to_buy
                    # Track entry price for risk management
                    entry_prices.extend([current_price] * int(shares_to_buy * 1000))  # Approximate tracking
                    trades_executed["Buy"] += 1
            else:
                # For stocks, buy whole shares only
                # Only buy if we have enough cash for at least one share
                if cash_to_invest >= current_price:
                    shares_to_buy = int(cash_to_invest // current_price)
                    if shares_to_buy > 0:
                        cash_spent = shares_to_buy * current_price
                        cash -= cash_spent
                        shares += shares_to_buy
                        # Track entry price for risk management
                        entry_prices.extend([current_price] * shares_to_buy)
                        trades_executed["Buy"] += 1
        elif signal_str == "Sell" and shares > 0:
            # For selling, use signal strength to determine how much to sell
            # Signal strength can be -1, -2, or -3 (stronger = sell more)
            max_signal_strength = 3
            sell_pct = min(1.0, abs(signal_strength) / max_signal_strength)
            shares_to_sell = shares * sell_pct
            cash += shares_to_sell * current_price
            shares -= shares_to_sell
            # Remove corresponding entry prices
            if len(entry_prices) > 0:
                num_to_remove = int(len(entry_prices) * sell_pct)
                entry_prices = entry_prices[num_to_remove:]
            trades_executed["Sell"] += 1
        
        # Always calculate portfolio value (even if stop loss/take profit triggered)
        portfolio_value.append(cash + shares * current_price)
    
    print(f"Signals generated - Buy: {signals_generated['Buy']}, Sell: {signals_generated['Sell']}, Hold: {signals_generated['Hold']}")
    print(f"Trades executed - Buy: {trades_executed['Buy']}, Sell: {trades_executed['Sell']}")
    print(f"Final cash: ${cash:.2f}")
    if shares > 0:
        print(f"Final position: {shares:.6f} shares worth ${shares * df.iloc[-1]['close']:.2f}")
        
    final_value = portfolio_value[-1]
    gain = ((final_value - initial_investment) / initial_investment) * 100

    print(f"Final Portfolio Value: ${final_value:.2f}")
    print(f"Total Gain: {gain:.2f}%")

    plt.plot(dates[window_size:], portfolio_value)
    asset_label = "Crypto" if asset_type == "crypto" else "Stock"
    plt.title(f"Backtest of {symbol} ({asset_label}) from {start} to {end}")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value ($)")
    plt.tight_layout()
    plt.show()

    return gain