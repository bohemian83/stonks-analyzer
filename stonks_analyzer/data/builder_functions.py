import yfinance as yf
import numpy as np
from datetime import datetime, timedelta
import logging

logging.getLogger("yfinance").setLevel(logging.CRITICAL)


def calculate_rsi(ticker):
    data = yf.download(
        ticker, period="3mo", interval="1d", progress=False, auto_adjust=True
    )

    delta = data["Close"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    window = 14
    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi.iloc[-1].item()


def calculate_sma(ticker, days):
    number_days = days
    start_date = (datetime.today() - timedelta(days=number_days * 2)).strftime(
        "%Y-%m-%d"
    )
    end_date = datetime.today().strftime("%Y-%m-%d")

    # Grab the stock data
    stock_data = yf.download(
        ticker, start=start_date, end=end_date, progress=False, auto_adjust=True
    )

    # Compute the simple moving average (SMA)
    stock_data["SMA"] = stock_data["Close"].rolling(window=number_days).mean()

    return stock_data["SMA"].iloc[-1].item()


def calculate_30d_volatility(ticker):
    init_date = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = datetime.today().strftime("%Y-%m-%d")
    stock_name = ticker

    stock = yf.download(
        stock_name, init_date, end_date, progress=False, auto_adjust=True
    )
    stock["lag_close"] = stock["Close"].shift(1)
    stock["log_return"] = np.log(stock["Close"].iloc[:, 0] / stock["lag_close"])
    vol = np.std(stock["log_return"])
    vol_annual_log = 252**0.5 * vol
    vol_annual_effective = np.exp(vol_annual_log) - 1

    return vol_annual_effective


def build_meta(stock):
    stock_info = stock.info
    meta = {
        "company_name": stock_info["shortName"],
        "sector": stock_info["sector"],
        "industry": stock_info["industry"],
        "market_cap": stock_info["marketCap"],
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

    return price_history


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
    technical_indicators = {
        "rsi_14": calculate_rsi(ticker),
        "50_day_ma": calculate_sma(ticker, 50),
        "200_day_ma": calculate_sma(ticker, 200),
        "beta": stock_info["beta"],
        "volatility_30d": calculate_30d_volatility(ticker),
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
