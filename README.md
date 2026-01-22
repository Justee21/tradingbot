# TradeBot - Stock & Crypto Signal Generator

Overall Description:
TradeBot analyzes stocks and cryptocurrencies and returns a Buy, Sell, or Hold signal for a given symbol and date range. It builds a composite signal using five moving averages, Bollinger Bands, and RSI, then scores the market conditions. Uptrend momentum and oversold signals contribute to Buy scores, while downtrend momentum and overbought signals contribute to Sell scores. The final decision is based on which side has the stronger signal, with Hold returned when the signals are balanced. The same strategy can also be backtested to evaluate historical performance on stocks or crypto.

Tech Stack:
- Python
- Alpha Vantage API (for stocks)
- ccxt (for cryptocurrencies)
- yfinance (fallback for both stocks and crypto)
- `pandas`, `requests`, `dotenv`, `matplotlib`

File Structure:
├── main.py           # Runs analysis for stocks and crypto
├── indicator.py      # Uses calculations to return signal
├── strategies.py     # Calculates moving averages, Bollinger Bands, RSI
├── data.py           # Downloads and processes stock/crypto data
├── backtest.py       # Backtests stocks/crypto and graphs performance
├── crypto_example.py # Examples for using crypto functionality
├── .env              # Stores API key (not pushed to GitHub)
├── requirements.txt  # Python dependencies
└── README.md         # Project description

Usage Examples:

**Stocks:**
```python
from backtest import backtest
from indicator import indicator

# Get signal for a stock
signal = indicator("AAPL", "2025-07-20", "2025-08-20", asset_type="stock")

# Backtest a stock
gain = backtest("AAPL", "2025-07-20", "2025-08-20", asset_type="stock")
```

**Cryptocurrencies:**
```python
from backtest import backtest
from indicator import indicator
import data

# Get signal for a cryptocurrency
signal = indicator("BTC/USDT", "2024-01-01", "2024-12-31", asset_type="crypto")

# Backtest a cryptocurrency
gain = backtest("BTC/USDT", "2024-01-01", "2024-12-31", asset_type="crypto")

# Fetch crypto data directly
df = data.getCryptoData("BTC/USDT", start="2024-01-01", end="2024-12-31", exchange="binance")
```

**Supported Crypto Exchanges:**
- Binance (default)
- Coinbase
- Kraken
- And many more via ccxt library

**Crypto Symbol Format:**
- Use exchange format: `BTC/USDT`, `ETH/USDT`, `BNB/USDT`
- Or yfinance format: `BTC-USD`, `ETH-USD` (will use yfinance as fallback)

Backtest:
Trading bot backtested AAPL from July 20th to August 20th yielding a 6.93% gain over the course of the month, beating the stock's price gain.

**Crypto Examples:**
Crypto backtest example showing BTC-USD performance over the course of 2025:
<img width="624" height="472" alt="btc2025" src="https://github.com/user-attachments/assets/19eb8681-3ec9-447e-90ea-10af7e63db51" />

Crypto backtest example showing ETH-USD performance over the course of 2025:
<img width="631" height="476" alt="Screenshot 2026-01-22 at 5 50 50 PM" src="https://github.com/user-attachments/assets/4031b8bf-8482-4751-b8d7-282758c90c1e" />

Crypto backtest example showing BNB-USD performance over the course of 2025:
<img width="632" height="472" alt="Screenshot 2026-01-22 at 5 51 08 PM" src="https://github.com/user-attachments/assets/9d9f1909-551f-4042-be22-c91c877f619e" />


To-Do:
- Add Flask front-end
- Develop machine-learning based strategies
- Allow the bot to work in real-time

