[![Daily Stock Price Prediction](https://github.com/pankitthakkar/stock-price-predictor/actions/workflows/main.yml/badge.svg)](https://github.com/pankitthakkar/stock-price-predictor/actions/workflows/main.yml)

Last updated: <!-- LATEST_RUN_DATE -->February 05, 2026 at 20:57 UTC

# 📈 Stock Price Prediction System 🚀
Welcome to the Stock Price Prediction System - where algorithms meet ambition and (hopefully) the market.

## 🧐 What Is This?
This project is an automated stock prediction system that uses [LSTM](https://docs.pytorch.org/docs/stable/generated/torch.nn.LSTM.html) and [XGBoost](https://xgboost.readthedocs.io/en/release_3.0.0/) models to forecast stock prices. Whether you're bullish, bearish, or just curious, this application will help you make data-driven decisions with a touch of flair!

## 💡 Why Predict Stock Prices?
Because the crystal ball broke, and guessing isn't profitable (I know 🥲). Also, it seems fun doesn't it?

## 🛠️ Features
- Daily predictions via LSTM and XGBoost models
- Automatic execution with GitHub Actions
- Real-time stock data fetched via [ALPACA API](https://docs.alpaca.markets/docs/getting-started-with-alpaca-market-data)
- Comparisons of accuracy and error metrics between models

## 📅 How It Works
1. Data from the ALPACA API is fetched daily.
2. The system runs predictions using LSTM and XGBoost models.
3. Results and accuracy comparisons are updated everyday at https://pankitthakkar.github.io/stock-price-predictor/

## 🚀 Getting Started
1. Clone the repo: `git clone https://github.com/pankitthakkar/stock-price-predictor.git`
2. Set up `APCA_API_KEY_ID` & `APCA_API_SECRET_KEY` in the `.env` file.
3. Sit back and watch the market insights roll in!

## 🤔 Why LSTM and XGBoost?
Because sometimes the market is all about memory (LSTM), and sometimes it's about boosting your odds (XGBoost). Either way, I’ve got you covered.

## 💬 Feedback
Found a bug? Have a feature request? Want to share your stock-picking success story? Open an issue or reach out. Just don't blame me if your cat walks across the keyboard and buys 100 shares of something unexpected!

## ⚠️ Disclaimer
This project is for educational purposes only. No stock-picking strategy is guaranteed to succeed, and I recommend consulting a financial advisor before investing.

Buy low, sell high! 🚀
... or Buy high, sell low 📉 — if you're into that.