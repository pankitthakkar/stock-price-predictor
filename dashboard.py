import base64
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import pandas as pd

def generate_charts(df, symbol):
    charts = {}
    symbol_df = df[df['symbol'] == symbol].copy()
    symbol_df['date'] = pd.to_datetime(symbol_df['date'])
    symbol_df = symbol_df.sort_values('date')
    
    valid_df = symbol_df.dropna(subset=['actual_price']).copy()
    
    if len(valid_df) > 0:
        plt.figure(figsize=(10, 6))
        plt.plot(valid_df['date'], valid_df['actual_price'], label='Actual Price', marker='o')
        plt.plot(valid_df['date'], valid_df['lstm_prediction'], label='LSTM Prediction', marker='x')
        plt.plot(valid_df['date'], valid_df['xgb_prediction'], label='XGBoost Prediction', marker='+')
        plt.title(f'{symbol} - Price Predictions vs Actual')
        plt.xlabel('date')
        plt.ylabel('Price ($)')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        price_img = BytesIO()
        plt.savefig(price_img, format='png')
        price_img.seek(0)
        charts['price_chart'] = base64.b64encode(price_img.read()).decode('utf-8')
        plt.close()
        
        plt.figure(figsize=(10, 6))
        plt.bar(valid_df['date'].astype(str), valid_df['lstm_error'], alpha=0.7, label='LSTM Error')
        plt.bar(valid_df['date'].astype(str), valid_df['xgb_error'], alpha=0.7, label='XGBoost Error')
        plt.title(f'{symbol} - Prediction Errors')
        plt.xlabel('date')
        plt.ylabel('Absolute Error ($)')
        plt.legend()
        plt.grid(True, axis='y')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        error_img = BytesIO()
        plt.savefig(error_img, format='png')
        error_img.seek(0)
        charts['error_chart'] = base64.b64encode(error_img.read()).decode('utf-8')
        plt.close()
        
        mean_lstm_error = valid_df['lstm_error'].mean()
        mean_xgb_error = valid_df['xgb_error'].mean()
        
        lstm_accuracy = 100 * (1 - valid_df['lstm_error'].mean() / valid_df['actual_price'].mean())
        xgb_accuracy = 100 * (1 - valid_df['xgb_error'].mean() / valid_df['actual_price'].mean())
        
        plt.figure(figsize=(8, 6))
        models = ['LSTM', 'XGBoost']
        accuracy = [lstm_accuracy, xgb_accuracy]
        error = [mean_lstm_error, mean_xgb_error]
        
        x = np.arange(len(models))
        width = 0.35
        
        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax2 = ax1.twinx()
        
        bars1 = ax1.bar(x - width/2, accuracy, width, label='Accuracy (%)', color='green', alpha=0.7)
        bars2 = ax2.bar(x + width/2, error, width, label='Avg Error ($)', color='red', alpha=0.7)
        
        ax1.set_xlabel('Models')
        ax1.set_ylabel('Accuracy (%)', color='green')
        ax2.set_ylabel('Average Error ($)', color='red')
        ax1.set_xticks(x)
        ax1.set_xticklabels(models)
        ax1.set_ylim([0, 100])
        
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
        
        plt.title(f'{symbol} - Model Performance')
        plt.tight_layout()
        
        perf_img = BytesIO()
        plt.savefig(perf_img, format='png')
        perf_img.seek(0)
        charts['performance_chart'] = base64.b64encode(perf_img.read()).decode('utf-8')
        plt.close()
    
    latest_row = symbol_df.iloc[-1] if not symbol_df.empty else None
    if latest_row is not None:
        charts['latest_date'] = latest_row['date'].strftime('%Y-%m-%d')
        charts['lstm_prediction'] = latest_row['lstm_prediction']
        charts['xgb_prediction'] = latest_row['xgb_prediction']
    
    return charts