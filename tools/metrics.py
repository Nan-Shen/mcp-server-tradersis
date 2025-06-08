from server import mcp
from utils.calculate_metrics import (
    calculate_growth_rates,
    calculate_technical_indicators,
    calculate_financial_metric
)

@mcp.tool()
def mcp_calculate_growth_rates(series: list) -> dict:
    """
    Calculates growth rates for a time series (e.g., revenue, earnings).
    Args:
        series: List of numbers ordered oldest to newest.
    Returns:
        Dict with annualized growth rate and list of period-over-period growth rates.
    """
    return calculate_growth_rates(series)

@mcp.tool()
def mcp_calculate_technical_indicators(price_data: list, indicator: str, window: int = 14) -> dict:
    """
    Calculates technical indicators (SMA, EMA, RSI, MACD, volatility) on stockprice data.
    Args:
        price_data: List of closing prices ordered oldest to newest.
        indicator: 'sma', 'ema', 'rsi', 'macd', 'volatility'
        window: Window size for the indicator.
    Returns:
        Dict with indicator values.
    """
    return calculate_technical_indicators(price_data, indicator, window)

@mcp.tool()
def mcp_calculate_financial_metrics(financial_data: dict, indicator: str) -> dict:
    """
    Calculates financial metrics from the provided data. The metrics are:
    - gross_margin (need retrieve income_statement)
    - operating_margin (need retrieve income_statement)
    - net_profit_margin (need retrieve income_statement)
    - ebitda (need retrieve income_statement)
    - debt_to_equity (need retrieve balance_sheet)
    - current_ratio (need retrieve balance_sheet)
    - quick_ratio (need retrieve balance_sheet)
    - book_value_per_share (need retrieve balance_sheet)
    - free_cash_flow (need retrieve cash_flow)
    - cash_flow_margin (need retrieve cash_flow)
    - roe (need retrieve income_statement and balance_sheet)
    - roa (need retrieve income_statement and balance_sheet)
    - pe_ratio (need retrieve income_statement and market)
    - pb_ratio (need retrieve income_statement and market)
    - dividend_yield (need retrieve income_statement and market)
    Args:
        financial_data: Dict with financial data.
        indicator: str, one of the supported metric names
        window: int, window size for the indicator
    Returns:
        Dict with financial metrics name as key and value as value. e.g. {'gross_margin': 0.5}
    """
    return calculate_financial_metric(financial_data, indicator)
