import os
import pandas as pd
from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.timeframe import TimeFrame
from dotenv import load_dotenv

# Load environment variables for API keys
load_dotenv()

ALPACA_API_KEY_ID = os.getenv("APCA_API_KEY_ID")
ALPACA_API_SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")

# Initialize client
data_client = StockHistoricalDataClient(ALPACA_API_KEY_ID, ALPACA_API_SECRET_KEY)

def get_latest_data(symbol):
    start_date = "2018-01-02"
    
    daily_request = StockBarsRequest(
        symbol_or_symbols=[symbol], 
        timeframe=TimeFrame.Day, 
        start=pd.Timestamp(start_date),
    )
    
    daily_bars = data_client.get_stock_bars(daily_request).df
    return daily_bars

def get_current_price(symbol):
    today = pd.Timestamp.now().date()
    
    # Get the today's closing price
    daily_request = StockBarsRequest(
        symbol_or_symbols=[symbol], 
        timeframe=TimeFrame.Day, 
        start=today,
    )

    daily_bars = data_client.get_stock_bars(daily_request).df

    if not daily_bars.empty:
        return daily_bars.iloc[-1]['close']
    else:
        request = StockLatestQuoteRequest(symbol_or_symbols=symbol)
        
        latest_quote = data_client.get_stock_latest_quote(request)
    
        # Return the midpoint of bid and ask as an approximation of current price
        quote = latest_quote[symbol]
        return (quote.bid_price + quote.ask_price) / 2