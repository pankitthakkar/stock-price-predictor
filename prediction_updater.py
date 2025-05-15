import pandas as pd
import datetime
from pathlib import Path
from data_collection import get_current_price

def update_prediction_file(symbol, lstm_prediction, xgb_prediction):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    file_path = Path('prediction_results.csv')
    
    if not file_path.exists():
        df = pd.DataFrame(columns=[
            'date', 'symbol', 'lstm_prediction', 'xgb_prediction', 
            'actual_price', 'lstm_error', 'xgb_error'
        ])
        df.to_csv(file_path, index=False)
    
    df = pd.read_csv(file_path)
    
    # Checks yesterday's prediction & updates it with the actual price
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    
    actual_price = get_current_price(symbol)
        
    # Updates yesterday's row with actual price and calculate error
    yesterday_row = df[(df['date'] == yesterday) & (df['symbol'] == symbol)]
    if not yesterday_row.empty:
        idx = yesterday_row.index[0]
        df.at[idx, 'actual_price'] = actual_price
        df.at[idx, 'lstm_error'] = abs(actual_price - df.at[idx, 'lstm_prediction'])
        df.at[idx, 'xgb_error'] = abs(actual_price - df.at[idx, 'xgb_prediction'])
    
    # Add today's prediction
    new_row = {
        'date': today,
        'symbol': symbol,
        'lstm_prediction': lstm_prediction,
        'xgb_prediction': xgb_prediction,
        'actual_price': None,
        'lstm_error': None,
        'xgb_error': None
    }
    
    # Create a new DataFrame with today's prediction first
    new_df = pd.DataFrame([new_row])
    
    # Then concatenate the existing data
    df = pd.concat([new_df, df], ignore_index=True)
    
    # Save the updated file
    df.to_csv(file_path, index=False)
    
    return df
