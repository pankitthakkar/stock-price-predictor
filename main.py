import pandas as pd
import datetime
from data_collection import get_latest_data
from feature_engineering import prepare_features
from modeling import train_models, predict_next_day
from prediction_updater import update_prediction_file
from dashboard_generator import generate_dashboard
from utils import is_data_current

def main():
    print(f"Starting prediction job at {datetime.datetime.now()}")

    symbols = ["AAPL"]

    for symbol in symbols:
        print(f"Processing {symbol}...")
        
        # Gets the latest data
        daily_bars = get_latest_data(symbol)
        
        # Check if data is current
        if not is_data_current(daily_bars):
            print(f"Data for {symbol} is not current. Skipping prediction for this symbol.")
            continue
        
        # Prepares the features
        df, features = prepare_features(daily_bars)
        
        # Train models
        lstm_model, xgb_model, scaler_features, scaler_target, X_test, y_test, timesteps, n_features = train_models(df, features)
        
        # Get the last sequence for prediction
        last_sequence = X_test[-1]
        
        # Predicts next day prices
        next_day_lstm = predict_next_day(lstm_model, last_sequence, scaler_target, is_lstm=True)
        next_day_xgb = predict_next_day(xgb_model, last_sequence, scaler_target, is_lstm=False)
        
        print(f"{symbol} LSTM Next Day Prediction: ${next_day_lstm:.2f}")
        print(f"{symbol} XGBoost Next Day Prediction: ${next_day_xgb:.2f}")
        
        # Updates the prediction file
        updated_df = update_prediction_file(symbol, next_day_lstm, next_day_xgb)
        
        # Prints the last few rows of the updated file
        print("\nUpdated prediction results:")
        print(updated_df.tail())
    
    # After processing all symbols, generate the dashboard
    try:
        dashboard_path = generate_dashboard(pd.read_csv('prediction_results.csv'))
        print(f"\nDashboard generated: {dashboard_path}")
    except Exception as e:
        print(f"Error generating dashboard: {str(e)}")

if __name__ == "__main__":
    main()
