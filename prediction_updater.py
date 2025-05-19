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
    
    actual_price = get_current_price(symbol)
    
    # Find the most recent prediction for this symbol that hasn't been updated with actual price
    unupdated_predictions = df[
        (df['symbol'] == symbol) & 
        (df['actual_price'].isna()) & 
        (df['date'] < today)
    ]
    
    if not unupdated_predictions.empty:
        # Sort by date in descending order to get the most recent prediction
        most_recent = unupdated_predictions.sort_values('date', ascending=False).iloc[0]
        idx = most_recent.name
        
        # Update the most recent unupdated prediction with actual price and calculate errors
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
