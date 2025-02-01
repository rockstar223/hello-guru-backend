from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import HistoricalStock
import pandas as pd
import numpy as np
import yfinance as yf
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from ta.trend import MACD

router = APIRouter()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to compute technical indicators
def compute_indicators(df):
    df["EMA_20"] = EMAIndicator(close=df["Close"], window=20).ema_indicator()
    df["RSI_14"] = RSIIndicator(close=df["Close"], window=14).rsi()
    macd = MACD(close=df["Close"])
    df["MACD"] = macd.macd()
    df["MACD_Signal"] = macd.macd_signal()
    return df

# Function to generate Buy/Sell signals
def generate_signals(df):
    signals = []
    for i in range(len(df)):
        if df["MACD"][i] > df["MACD_Signal"][i] and df["RSI_14"][i] < 30:
            signals.append("BUY")
        elif df["MACD"][i] < df["MACD_Signal"][i] and df["RSI_14"][i] > 70:
            signals.append("SELL")
        else:
            signals.append("HOLD")
    df["Signal"] = signals
    return df

# API to analyze stock and generate Buy/Sell signals
@router.get("/{symbol}/analyze")
def analyze_stock(symbol: str):
    stock = yf.Ticker(f"{symbol}.NS")
    stock_data = stock.history(period="3mo")

    if stock_data.empty:
        return {"error": "Stock data not available"}

    stock_data = stock_data.reset_index()
    stock_data = compute_indicators(stock_data)
    stock_data = generate_signals(stock_data)

    return stock_data[["Date", "Close", "EMA_20", "RSI_14", "MACD", "MACD_Signal", "Signal"]].to_dict(orient="records")
