import ta
import pandas as pd

def prepare_features(df):
    df = df.copy()
    
    # Calculate technical indicators
    df["macd"] = ta.trend.MACD(df["close"]).macd()
    df["macd_signal"] = ta.trend.MACD(df["close"]).macd_signal()
    df["macd_diff"] = ta.trend.MACD(df["close"]).macd_diff()
    
    # Bollinger Bands
    bollinger = ta.volatility.BollingerBands(df["close"])
    df["bollinger_h"] = bollinger.bollinger_hband()
    df["bollinger_l"] = bollinger.bollinger_lband()
    df["bollinger_m"] = bollinger.bollinger_mavg()
    df["bb_width"] = (df["bollinger_h"] - df["bollinger_l"]) / df["bollinger_m"]
    
    # Volatility indicators
    df["atr"] = ta.volatility.AverageTrueRange(df["high"], df["low"], df["close"]).average_true_range()
    df["daily_return"] = df["close"].pct_change()
    df["volatility_14"] = df["daily_return"].rolling(window=14).std()
    
    # Volume indicators
    df["obv"] = ta.volume.OnBalanceVolumeIndicator(df["close"], df["volume"]).on_balance_volume()
    df["volume_sma"] = df["volume"].rolling(window=20).mean()
    df["volume_ratio"] = df["volume"] / df["volume_sma"]
    
    # Trend indicators
    df["adx"] = ta.trend.ADXIndicator(df["high"], df["low"], df["close"]).adx()
    df["sma_20"] = ta.trend.SMAIndicator(df["close"], window=20).sma_indicator()
    df["sma_50"] = ta.trend.SMAIndicator(df["close"], window=50).sma_indicator()
    df["ema_20"] = ta.trend.EMAIndicator(df["close"], window=20).ema_indicator()
    
    # VWAP (Volume Weighted Average Price)
    df["vwap"] = (df["close"] * df["volume"]).cumsum() / df["volume"].cumsum()
    
    # RSI
    df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
    
    # Price-based features
    df["price_sma_ratio"] = df["close"] / df["sma_20"]
    df["high_low_ratio"] = df["high"] / df["low"]
    
    df = df.dropna()
    
    # Select features for modeling - exclude OHLCV
    columns_to_drop = []
    for col in ["open", "high", "low", "close", "volume", "symbol", "trade_count"]:
        if col in df.columns:
            columns_to_drop.append(col)
            
    features = df.drop(columns=columns_to_drop)
    
    return df, features