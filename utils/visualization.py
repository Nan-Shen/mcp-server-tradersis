import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import base64
from io import BytesIO
import pandas as pd
from utils.retrieve_data import fetch_stock_data
from utils.calculate_metrics import calculate_trading_opportunities

def plot_price_chart(prices: list, chart_type: str = 'line', title: str = 'Price Chart', filename: str = None) -> dict:
    """
    Plots a price chart (line or candlestick) from OHLCV data.
    Args:
        prices: List of dicts with keys 'date', 'open', 'high', 'low', 'close', 'volume'.
        chart_type: 'line' or 'candlestick'.
        title: Chart title.
        filename: Optional filename to save the plot.
    Returns:
        Dict with 'file_path' and 'base64' of the image.
    """
    from matplotlib.ticker import MaxNLocator
    df = pd.DataFrame(prices)
    df['date'] = pd.to_datetime(df['date'])
    fig, ax = plt.subplots(figsize=(10, 5))
    if chart_type == 'line':
        ax.plot(df['date'], df['close'], label='Close Price')
        ax.set_ylabel('Close Price')
    elif chart_type == 'candlestick':
        try:
            from mplfinance.original_flavor import candlestick_ohlc
        except ImportError:
            return {'error': 'mplfinance is required for candlestick charts'}
        df_ohlc = df[['date', 'open', 'high', 'low', 'close']].copy()
        df_ohlc['date'] = mdates.date2num(df_ohlc['date'])
        candlestick_ohlc(ax, df_ohlc.values, width=0.6, colorup='g', colordown='r')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.set_ylabel('Price')
    else:
        return {'error': f'Unknown chart_type: {chart_type}'}
    ax.set_title(title)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(True)
    fig.autofmt_xdate()
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    if not filename:
        filename = f"./data/price_chart_{chart_type}.png"
    with open(filename, 'wb') as f:
        f.write(base64.b64decode(img_base64))
    return {'file_path': filename, 'base64': img_base64}

def plot_financial_metric(dates: list, values: list, metric_name: str = 'Metric', title: str = 'Financial Metric', filename: str = None) -> dict:
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
    fig, ax = plt.subplots(figsize=(10, 5))
    dates = pd.to_datetime(dates)
    ax.plot(dates, values, marker='o', label=metric_name)
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel(metric_name)
    ax.legend()
    ax.grid(True)
    fig.autofmt_xdate()
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    if not filename:
        filename = f"./data/financial_metric_{metric_name}.png"
    with open(filename, 'wb') as f:
        f.write(base64.b64decode(img_base64))
    return {'file_path': filename, 'base64': img_base64}

def plot_comparison_chart(dates: list, series: dict, title: str = 'Comparison Chart', filename: str = None) -> dict:
    """
    Plots a comparison chart for multiple tickers or metrics.
    Args:
        dates: List of date strings.
        series: Dict where keys are labels and values are lists of values for each date.
        title: Chart title.
        filename: Optional filename to save the plot.
    Returns:
        Dict with 'file_path' and 'base64' of the image.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    dates = pd.to_datetime(dates)
    for label, values in series.items():
        ax.plot(dates, values, marker='o', label=label)
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Value')
    ax.legend()
    ax.grid(True)
    fig.autofmt_xdate()
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    if not filename:
        filename = f"./data/comparison_chart.png"
    with open(filename, 'wb') as f:
        f.write(base64.b64decode(img_base64))
    return {'file_path': filename, 'base64': img_base64}

def plot_trading_opportunities(prices: list, short_window: int, long_window: int, title: str = 'Trading Opportunities') -> dict:
    """
    Plots price data with trading signals/opportunities. Create signals based on crossovers:
    - A 'Golden Cross' (bullish signal) occurs when the short-term MA crosses above the long-term MA.
    - A 'Death Cross' (bearish signal) occurs when the short-term MA crosses below the long-term MA.
    Args:
        prices: List of dicts with OHLCV and date.
        short_window: Short window for the short moving average.
        long_window: Long window for the long moving average.
        title: Chart title.
    Returns:
        Dict with 'file_path' and/or 'base64' of the image.
    """
    prices = pd.DataFrame(prices)
    prices = calculate_trading_opportunities(prices, short_window, long_window)
    buy_signals = prices[prices['signal'] == 1]
    sell_signals = prices[prices['signal'] == -1]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(prices['date'], prices['close'], label='Close Price', color='blue', alpha=0.5)
    ax.plot(prices['date'], prices['short_ma'], label=f'Short MA ({short_window})', color='orange')
    ax.plot(prices['date'], prices['long_ma'],  label=f'Long MA ({long_window})', color='magenta')
    if not buy_signals.empty:
        plt.scatter(buy_signals['Date'], buy_signals['Close'], marker='^', color='green', label='Buy Signal', s=100, zorder=5)
    if not sell_signals.empty:
        plt.scatter(sell_signals['Date'], sell_signals['Close'], marker='v', color='red', label='Sell Signal', s=100, zorder=5)
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()
    ax.grid(True)
    fig.autofmt_xdate()
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    if not filename:
        filename = f"./data/trading_opportunities.png"
    with open(filename, 'wb') as f:
        f.write(base64.b64decode(img_base64))
    return {'file_path': filename, 'base64': img_base64}

