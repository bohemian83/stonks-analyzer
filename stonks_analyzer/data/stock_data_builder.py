import yfinance as yf
from stonks_analyzer.data.builder_functions import (
    build_meta,
    build_analyst_summary,
    build_fundamentals,
    build_price_data,
    build_technical_indicators,
    build_valuation_ratios,
)


def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    symbol = stock.info.get("symbol", None)

    if not symbol:
        raise Exception("Ticker not found")

    stock_data = {
        "ticker": ticker.upper(),
        "meta": build_meta(stock),
        "price_data": build_price_data(ticker, "1y"),
        "fundamentals": build_fundamentals(stock),
        "valuation_ratios": build_valuation_ratios(stock),
        "technical_indicators": build_technical_indicators(stock),
        "analyst_summary": build_analyst_summary(stock),
    }

    return stock_data
