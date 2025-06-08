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
        Dict mapping ticker to its historical data in columnar format (dict of lists), e.g. {'date': [...], 'open': [...], ...}.
    """
    result = {}
    for ticker in ticker_list:
        data = yf.Ticker(ticker).history(start=start_date, end=end_date, interval=interval)
        if not data.empty:
            data = data.reset_index()
            # Convert all columns to lower case
            data.columns = [str(col).lower() for col in data.columns]
            # Convert 'date' column to string for JSON serialization
            if 'date' in data.columns:
                data['date'] = data['date'].astype(str)
            # Convert to dict of lists (columnar format)
            result[ticker] = {col: data[col].tolist() for col in data.columns}
        else:
            result[ticker] = {}
    return result

def get_dividends(ticker: str) -> str:
    """
    Fetches dividends for the given ticker.
    """
    stock = yf.Ticker(ticker)
    dividends = stock.dividends
    return dividends.to_json()

def get_splits(ticker: str) -> str:
    """
    Fetches splits for the given ticker.
    """
    stock = yf.Ticker(ticker)
    splits = stock.splits
    return splits.to_json()

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
def get_financial_statements(ticker: str, indicator: str) -> str:
    """
    Fetches the annual income statements, balance sheet, and cash flow for the given ticker.
    """
    stock = yf.Ticker(ticker)
    if indicator == "income_statement":
        statements = stock.financials
        return { "income_statement": statements.to_json()}
    elif indicator == "balance_sheet":
        statements = stock.balance_sheet
        return { "balance_sheet": statements.to_json()}
    elif indicator == "cash_flow":
        statements = stock.cashflow
        return { "cash_flow": statements.to_json()}
    else:
        return {"error": f"Invalid indicator: {indicator}"}
