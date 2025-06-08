from server import mcp
from utils.retrieve_data import (
    get_current_price,
    fetch_stock_data,
    get_dividends,
    get_splits,
    get_ticker_info,
    get_financial_statements
)

@mcp.tool()
def retrieve_current_price(ticker: str) -> dict:
    """
    Retrieves the current price for the given ticker.
    Args:
        ticker: The ticker symbol of the stock to retrieve the current price for.
    Returns:
        A JSON-serializable dict with the current price and related info.
    """
    return get_current_price(ticker)

@mcp.tool()
def retrieve_stock_data(ticker_list: list, start_date: str, end_date: str, interval: str = "1d") -> dict:
    """
    Retrieves stock data for a list of tickers using yfinance.
    Args:
        ticker_list: List of ticker symbols (e.g., ['AAPL', 'MSFT', 'GOOGL'])
        start_date: Start date of the data (e.g., '2024-01-01')
        end_date: End date of the data (e.g., '2024-12-31')
        interval: Data interval (e.g., '1d', '1h', '5m', etc.)
    Returns:
        Dict mapping ticker to its historical data (as a list of dicts).
    """
    return fetch_stock_data(ticker_list, start_date, end_date, interval)

@mcp.tool()
def retrieve_dividends(ticker: str) -> dict:
    """
    Retrieves dividends for the given ticker.
    """
    return get_dividends(ticker)

@mcp.tool()
def retrieve_splits(ticker: str) -> dict:
    """
    Retrieves splits for the given ticker.
    """
    return get_splits(ticker)

@mcp.tool()
def retrieve_ticker_info(ticker: str) -> dict:
    """
    Retrieves information about the given ticker.
    Args:
        ticker: The ticker symbol of the stock to retrieve the information for.
    Returns:
        A JSON-serializable dict with information about the given ticker.
    """
    return get_ticker_info(ticker)

@mcp.tool()
def retrieve_financial_statements(ticker: str, indicator: str) -> dict:
    """
    Retrieves the annual income statements, balance sheet, or cash flow for the given ticker. 
    Args:
        ticker: The ticker symbol of the stock to retrieve the statements for.
        indicator: The type of financial statement to retrieve. e.g. "income_statement", "balance_sheet", "cash_flow"
    Returns:
        A JSON-serializable dict with income statements, balance sheet, or cash flow.
    """
    return get_financial_statements(ticker, indicator)