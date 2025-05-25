import pandas as pd
import datetime
from pathlib import Path
from data_collection import get_current_price

def get_next_market_day(start_date=None):
    if start_date is None:
        start_date = datetime.datetime.now().date()
    next_day = start_date + datetime.timedelta(days=1)
    while next_day.weekday() >= 5:
        next_day += datetime.timedelta(days=1)
    return next_day

def update_prediction_file(symbol, lstm_prediction, xgb_prediction):
    today = datetime.datetime.now().date()
    prediction_date = get_next_market_day(today)
    prediction_date_str = prediction_date.strftime('%Y-%m-%d')
    
    file_path = Path('prediction_results.csv')
    
    if not file_path.exists():
        df = pd.DataFrame(columns=[
            'date', 'symbol', 'lstm_prediction', 'xgb_prediction', 
            'actual_price', 'lstm_error', 'xgb_error'
        ])
        df.to_csv(file_path, index=False)
    
    df = pd.read_csv(file_path)
    
    actual_price = get_current_price(symbol)
    
    # Update actual price for the most recent prediction before today
    unupdated_predictions = df[
        (df['symbol'] == symbol) & 
        (df['actual_price'].isna()) & 
        (pd.to_datetime(df['date']).dt.date < today)
    ]
    
    if not unupdated_predictions.empty:
        most_recent = unupdated_predictions.sort_values('date', ascending=False).iloc[0]
        idx = most_recent.name
        
        df.at[idx, 'actual_price'] = actual_price
        df.at[idx, 'lstm_error'] = abs(actual_price - df.at[idx, 'lstm_prediction'])
        df.at[idx, 'xgb_error'] = abs(actual_price - df.at[idx, 'xgb_prediction'])
    
    new_row = {
        'date': prediction_date_str,
        'symbol': symbol,
        'lstm_prediction': lstm_prediction,
        'xgb_prediction': xgb_prediction,
        'actual_price': None,
        'lstm_error': None,
        'xgb_error': None
    }
    
    new_df = pd.DataFrame([new_row])
    df = pd.concat([new_df, df], ignore_index=True)
    df.to_csv(file_path, index=False)
    
    return df
