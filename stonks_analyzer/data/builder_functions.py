import yfinance as yf
import numpy as np
from datetime import datetime, timedelta
import logging

logging.getLogger("yfinance").setLevel(logging.CRITICAL)


def format_number(n):
    suffixes = ["", "K", "M", "B", "T"]
    index = 0
    while abs(n) >= 1000 and index < len(suffixes) - 1:
        n /= 1000.0
        index += 1
    if n.is_integer():
        return f"{int(n)}{suffixes[index]}"
    else:
        return f"{n:.1f}{suffixes[index]}"


def calculate_rsi(data_rsi):
    data = data_rsi

    delta = data["Close"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    window = 14
    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    rsi14 = round(rsi.iloc[-1].item(), 0)

    assessment = ""
    if 0 < rsi14 < 20:
        assessment = "Deeply oversold"
    elif 20 <= rsi14 < 40:
        assessment = "Bearish zone"
    elif 40 <= rsi14 < 60:
        assessment = "Neutral zone"
    elif 60 <= rsi14 < 80:
        assessment = "Bullish zone"
    else:
        assessment = "Extremely overbought"

    return rsi14, assessment


def calculate_sma(data_sma, days):
    data = data_sma
    number_days = days
    data["SMA"] = data["Close"].rolling(window=number_days).mean()

    return data["SMA"].iloc[-1].item()


def calculate_30d_volatility(data_vol):
    data = data_vol
    data["lag_close"] = data["Close"].shift(1)
    data["log_return"] = np.log(data["Close"].iloc[:, 0] / data["lag_close"])
    vol = np.std(data["log_return"])
    vol_annual_log = 252**0.5 * vol
    vol_annual_effective = np.exp(vol_annual_log) - 1

    return round(vol_annual_effective.item(), 2)


def build_meta(stock):
    stock_info = stock.info
    meta = {
        "company_name": stock_info["shortName"],
        "sector": stock_info["sector"],
        "industry": stock_info["industry"],
        "market_cap": format_number(stock_info["marketCap"]),
        "exchange": stock_info["fullExchangeName"],
        "currency": stock_info["currency"],
        "country": stock_info["country"],
    }

    return meta


def build_price_data(ticker, period):
    end = datetime.today().strftime("%Y-%m-%d")
    historical_data = yf.download(
        ticker, end=end, period=period, interval="1d", progress=False, auto_adjust=True
    )
    historical_data = historical_data.reset_index()

    price_history = []
    for index, row in historical_data.iterrows():
        price_history.append(
            {
                "date": row["Date"].item().strftime("%Y-%m-%d"),
                "open": row["Open"].item(),
                "high": row["High"].item(),
                "low": row["Low"].item(),
                "close": row["Close"].item(),
                "volume": row["Volume"].item(),
            }
        )

    pct_change = (
        price_history[-1]["close"] - price_history[-2]["close"]
    ) / price_history[-2]["close"]

    if pct_change > 0:
        change = "▲"
    elif pct_change < 0:
        change = "▼"
    else:
        change = "➖"

    pct_change = abs(pct_change)

    return price_history, f"{change} {pct_change:.1%}"


def build_fundamentals(stock):
    stock_ttm_income = stock.ttm_income_stmt
    stock_balance = stock.balance_sheet
    stock_info = stock.info
    stock_cashflow = stock.cashflow

    fundamentals = {
        "revenue_ttm": stock_ttm_income.loc["Total Revenue"].iloc[0].item(),
        "net_income_ttm": stock_ttm_income.loc["Net Income"].iloc[0].item(),
        "free_cash_flow_ttm": stock_cashflow.loc["Free Cash Flow"].iloc[0].item(),
        "total_assets": stock_balance.loc["Total Assets"].iloc[0].item(),
        "total_liabilities": stock_balance.loc[
            "Total Liabilities Net Minority Interest"
        ]
        .iloc[0]
        .item(),
        "shareholders_equity": stock_balance.loc["Stockholders Equity"].iloc[0].item(),
        "debt_to_equity": stock_balance.loc["Total Debt"].iloc[0].item()
        / stock_balance.loc["Stockholders Equity"].iloc[0].item(),
        "roe": stock_ttm_income.loc["Net Income"].iloc[0].item()
        / stock_balance.loc["Stockholders Equity"].iloc[0].item(),
        "dividend_yield": stock_info["trailingAnnualDividendYield"],
        "revenue_growth_yoy": stock_info["revenueGrowth"],
        "earnings_growth_yoy": stock_info["earningsGrowth"],
    }

    return fundamentals


def build_valuation_ratios(stock):
    stock_info = stock.info
    valuation_ratios = {
        "pe_ratio": stock_info["forwardPE"],
        "pb_ratio": stock_info["priceToBook"],
        "peg_ratio": stock_info["trailingPegRatio"],
        "ev_to_ebitda": stock_info["enterpriseToEbitda"],
        "price_to_sales": stock_info["priceToSalesTrailing12Months"],
    }
    return valuation_ratios


def build_technical_indicators(stock):
    stock_info = stock.info
    ticker = stock_info["symbol"]

    data = yf.download(
        ticker, period="1y", interval="1d", progress=False, auto_adjust=True
    )
    data = data.reset_index()

    data_len = data["Date"].size
    data_rsi = data[-90:data_len].copy()
    data_50d = data[-100:data_len].copy()
    data_200d = data[-200:data_len].copy()
    data_30d = data[-30:data_len].copy()

    sma_50d = round(calculate_sma(data_50d, 50), 2)
    sma_200d = round(calculate_sma(data_200d, 200), 2)

    technical_indicators = {
        "rsi_14": calculate_rsi(data_rsi),
        "50_day_ma": sma_50d,
        "200_day_ma": sma_200d,
        "cross": "Bullish Trend -> Golden Cross"
        if sma_50d > sma_200d
        else "Bearish Trend -> Death Cross",
        "beta": stock_info["beta"],
        "volatility_30d": calculate_30d_volatility(data_30d),
    }

    return technical_indicators


def build_analyst_summary(stock):
    stock_info = stock.info
    analyst_summary = {
        "rating_average": stock_info["recommendationMean"],
        "rating_scale": "1=Sell, 5=Buy",
        "analyst_count": stock_info["numberOfAnalystOpinions"],
        "target_price_mean": stock_info["targetMeanPrice"],
        "target_price_high": stock_info["targetHighPrice"],
        "target_price_low": stock_info["targetLowPrice"],
        "consensus_recommendation": stock_info["recommendationKey"],
    }

    return analyst_summary


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
