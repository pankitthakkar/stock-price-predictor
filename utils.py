import pandas as pd
import datetime

def is_data_current(daily_bars):
    """
    Check if the data is current (contains today's or yesterday's data)
    Returns True if data is current, False otherwise
    """
    if daily_bars.empty:
        return False
        
    # Get the latest date from the data
    latest_data_index = daily_bars.index[-1]
    
    if isinstance(latest_data_index, tuple):
        latest_data_date = latest_data_index[1]
    else:
        latest_data_date = latest_data_index
    
    if isinstance(latest_data_date, str):
        latest_data_date = pd.to_datetime(latest_data_date)
    
    # Extract the date
    latest_data_date = latest_data_date.date()

    # Get today's date
    today = datetime.date.today()

    is_current = latest_data_date == today
    
    return is_current
