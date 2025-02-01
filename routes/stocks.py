from fastapi import APIRouter
import yfinance as yf

router = APIRouter()

# Fetch Live Stock Market Data
@router.get("/{symbol}")
def get_stock_data(symbol: str):
    stock = yf.Ticker(f"{symbol}.NS")
    stock_info = stock.history(period="1d")
    if not stock_info.empty:
        latest_data = stock_info.iloc[-1]
        return {
            "symbol": symbol,
            "price": latest_data["Close"],
            "change": ((latest_data["Close"] - latest_data["Open"]) / latest_data["Open"]) * 100
        }
    return {"error": "Stock not found"}

# Fetch Historical Stock Data
@router.get("/historical/{symbol}")
def get_historical_stock_data(symbol: str, period: str = "1mo"):
    stock = yf.Ticker(f"{symbol}.NS")
    stock_info = stock.history(period=period)
    if not stock_info.empty:
        historical_data = stock_info.reset_index()[["Date", "Open", "High", "Low", "Close", "Volume"]]
        return historical_data.to_dict(orient="records")
    return {"error": "No historical data found"}
