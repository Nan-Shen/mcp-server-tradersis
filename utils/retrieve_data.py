import yfinance as yf
import pandas as pd
from datetime import datetime
# market data tools
def get_current_price(ticker: str) -> dict:
    """
    Fetches the latest price for the given ticker.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    if not data.empty:
        price = data['Close'].iloc[-1]
        timestamp = data.index[-1].to_pydatetime().isoformat()
        return {
            "ticker": ticker,
            "price": float(price),
            "currency": stock.info.get("currency", "USD"),
            "timestamp": timestamp
        }
    else:
        return {"error": f"No data found for ticker {ticker}"}
    
def fetch_stock_data(ticker_list, start_date, end_date, interval="1d"):
    """
    Fetches historical stock data for one ticker or a list of tickers from start date to end date using yfinance.
    Args:
        ticker_list: List of ticker symbols (e.g., ['AAPL', 'MSFT', 'GOOGL'])
        start_date: Start date of the data (e.g., '2024-01-01')
        end_date: End date of the data (e.g., '2024-12-31')
        interval: Data interval (e.g., '1d', '1h', '5m', etc.)
    Returns:
        Dict mapping ticker to its historical data (as a list of dicts).
    """
    result = {}
    for ticker in ticker_list:
        data = yf.Ticker(ticker).history(start=start_date, end=end_date, interval=interval)
        if not data.empty:
            result[ticker] = data.to_dict(orient="records")
            # Convert Timestamp to string for JSON serialization
            for rec in result[ticker]:
                if "Date" in rec:
                    rec["Date"] = str(rec["Date"]) 
        else:
            result[ticker] = []
    return result

def get_dividends(ticker: str) -> dict:
    """
    Fetches dividends for the given ticker.
    """
    stock = yf.Ticker(ticker)
    dividends = stock.dividends
    return dividends.to_dict()

def get_splits(ticker: str) -> dict:
    """
    Fetches splits for the given ticker.
    """
    stock = yf.Ticker(ticker)
    splits = stock.splits
    return splits.to_dict()

def get_ticker_info(ticker: str) -> dict:
    """
    Fetches basic info about the ticker (name, sector, etc.)
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "ticker": ticker,
        "name": info.get("shortName", ""),
        "exchange": info.get("exchange", ""),
        "sector": info.get("sector", ""),
        "industry": info.get("industry", ""),
        "currency": info.get("currency", "USD")
    }

# financial statements extraction tools
def get_financial_statements(ticker: str) -> dict:
    """
    Fetches the annual financial statements, balance sheet, and cash flow for the given ticker.
    """
    stock = yf.Ticker(ticker)
    statements = stock.financials
    bs = stock.balance_sheet
    cf = stock.cashflow
    return {
        "financial_statements": statements.to_dict(),
        "balance_sheet": bs.to_dict(),
        "cash_flow": cf.to_dict()
    }

