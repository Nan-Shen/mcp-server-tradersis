from server import mcp
from utils.visualization import (
    plot_price_chart,
    plot_financial_metric,
    plot_comparison_chart,
    plot_trading_opportunities
)

@mcp.tool()
def mcp_plot_price_chart(prices: list, chart_type: str = 'line', title: str = 'Price Chart', filename: str = None) -> dict:
    """
    Generates a price chart (line or candlestick) from OHLCV data. 
    Args:
        prices: List of dicts with keys 'date', 'open', 'high', 'low', 'close', 'volume'.
        chart_type: 'line' or 'candlestick'.
        title: Chart title.
        filename: Optional filename to save the plot.
    Returns:
        Dict with 'file_path' and 'base64' of the image.
    """
    return plot_price_chart(prices, chart_type, title, filename)

@mcp.tool()
def mcp_plot_financial_metric(dates: list, values: list, metric_name: str = 'Metric', title: str = 'Financial Metric', filename: str = None) -> dict:
    """
    Plots a financial metric over time.
    Args:
        dates: List of date strings.
        values: List of metric values.
        metric_name: Name of the metric.
        title: Chart title.
        filename: Optional filename to save the plot.
    Returns:
        Dict with 'file_path' and 'base64' of the image.
    """
    return plot_financial_metric(dates, values, metric_name, title, filename)

@mcp.tool()
def mcp_plot_comparison_chart(dates: list, series: dict, title: str = 'Comparison Chart', filename: str = None) -> dict:
    """
    Plots a comparison chart for multiple tickers or financial metrics over time.
    Args:
        dates: List of date strings.
        series: Dict where keys are labels and values are lists of values for each date.
        title: Chart title.
        filename: Optional filename to save the plot.
    Returns:
        Dict with 'file_path' and 'base64' of the image.
    """
    return plot_comparison_chart(dates, series, title, filename) 

@mcp.tool()
def mcp_plot_trading_opportunities(prices: list, short_window: int=9, long_window: int=21, title: str = 'Trading Opportunities') -> dict:
    """
    Plots price data with trading signals/opportunities.
    Args:
        prices: List of dicts with keys 'date', 'open', 'high', 'low', 'close', 'volume'.
        short_window: Short window for the short moving average. Default is 9.
        long_window: Long window for the long moving average. Default is 21.
        title: Chart title.
    Returns:    
        Dict with 'file_path' and 'base64' of the image.
    """
    return plot_trading_opportunities(prices, short_window, long_window, title)