import yfinance as yf
from stonks_analyzer.data.data_builder import (
    build_meta,
    build_analyst_summary,
    build_fundamentals,
    build_price_data,
    build_technical_indicators,
    build_valuation_ratios,
)


def get_yfinance_data(stock_name):
    stock = yf.Ticker(stock_name)
    ticker = stock.info["symbol"]
    stock_data = {
        "ticker": ticker,
        "meta": build_meta(stock),
        "price_data": build_price_data(ticker, "1y"),
        "fundamentals": build_fundamentals(stock),
        "valuation_ratios": build_valuation_ratios(stock),
        "technical_indicators": build_technical_indicators(stock),
        "analyst_summary": build_analyst_summary(stock),
    }

    return stock_data
