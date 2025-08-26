# TradeBot - Stock Signal Generator

Overall Description:
This project uses various strategies which analyze stocks to generate a Buy, Sell, or Hold signal. This model receives a given stock and a start and end date. From these parameters the model calculates 5 moving averages (of equal length) across the window, the upper and lower Bollinger Bands, and the Relative Strength Index (RSI). This model uses these calculations to return a Buy, Sell, or Hold signal. The calculations required to produce a Buy signal are: all of the moving averages increasing as time progresses, the lower bollinger band being greater than the stock price and the moving averages decreasing as time progresses, the RSI being less than 30 and the moving averages decreasing as time progresses. The calculations required to produce a Sell signal are: all of the moving averages decreasing as time progresses, the upper bollinger band being less than the stock price and the moving averages increasing as time progresses, the RSI being greater than 70 and the moving averages increasing as time progresses. There needs to be greater buy signals than sell signals to return buy and to return sell there needs to be greater sell signals than buy signals, otherwise hold will be returned. Additionally, the bot can be backtested historically to test it's performance in the past on a certain stock.

Tech Stack:
- Python
- Alpha Vantage API
- yfinance 
- `pandas`, `requests`, `dotenv`, `matplotlib`

File Structure:
├── main.py           # Runs analysis
├── indicator.py      # Uses calculations to return signal
├── strategies.py     # Calculates moving averages, Bollinger Bands, RSI
├── data.py           # Downloads and processes Alpha Vantage data
├── backtest.py       # Backtests stock and graphs the bot's performance
├── .env              # Stores API key (not pushed to GitHub)
├── requirements.txt  # Python dependencies
└── README.md         # Project description

Backtest:
Trading bot backtested AAPL from July 20th to August 20th yielding a 6.93% gain over the course of the month, beating the stock's price gain.

Graph of the change in value of the portfolio starting with an initial investment of 10,000:
<img width="638" height="479" alt="Screenshot 2025-08-24 at 6 56 06 PM" src="https://github.com/user-attachments/assets/d1574466-06a1-4ae0-97e6-c35f422ba75c" />

To-Do:
- Add Flask front-end
- Develop machine-learning based strategies
- Allow the bot to work in real-time

