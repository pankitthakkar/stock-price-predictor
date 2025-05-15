# modeling.py
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.src.models import Sequential
from keras.src.layers import Input, LSTM, Dense, Dropout
from keras.src.callbacks import EarlyStopping
import xgboost as xgb

def train_models(df, features):
    timesteps = 60
    n_features = features.shape[1]
    
    # Normalize/scale the features
    scaler_features = MinMaxScaler(feature_range=(0, 1))
    scaler_target = MinMaxScaler(feature_range=(0, 1))
    
    scaled_features = scaler_features.fit_transform(features)
    scaled_target = scaler_target.fit_transform(df[["close"]])
    
    X = []
    y = []
    
    for i in range(timesteps, len(df)):
        X.append(scaled_features[i-timesteps:i])
        y.append(scaled_target[i])
    
    X = np.array(X)
    y = np.array(y)
    
    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    
    # Train LSTM Model
    lstm_model = Sequential([
        Input(shape=(timesteps, n_features)),
        LSTM(128, return_sequences=True),
        Dropout(0.2),
        LSTM(64, return_sequences=False),
        Dropout(0.2),
        Dense(1)
    ])
    
    lstm_model.compile(optimizer='adam', loss='mse')
    
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    lstm_model.fit(X_train, y_train, epochs=50, batch_size=64, validation_split=0.1, callbacks=[early_stopping], verbose=0)
    
    # Train XGBoost Model
    X_train_reshaped = X_train.reshape(X_train.shape[0], -1)
    
    xgb_model = xgb.XGBRegressor(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=4,
        reg_lambda=1,
        gamma=0,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )
    
    xgb_model.fit(X_train_reshaped, y_train)
    
    return lstm_model, xgb_model, scaler_features, scaler_target, X_test, y_test, timesteps, n_features

def predict_next_day(model, last_sequence, scaler_target, is_lstm=True):

    sequence = last_sequence.reshape(1, last_sequence.shape[0], last_sequence.shape[1]) if is_lstm else last_sequence.reshape(1, -1)
    
    if is_lstm:
        prediction = model.predict(sequence, verbose=0)
    else:
        prediction = model.predict(sequence)
    
    if len(prediction.shape) == 1:
        prediction = prediction.reshape(-1, 1)
    
    return scaler_target.inverse_transform(prediction)[0][0]
