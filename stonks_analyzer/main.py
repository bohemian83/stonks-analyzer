import sys
from stonks_analyzer.stock_data_builder import get_stock_data

"""
===================================================================================
|  Apple Inc. (AAPL)       Exchange: NASDAQ     Sector: Technology                |
|  Price: $220.70 ▲ +1.3%   Market Cap: $3.4T   P/E: 30.1x   Country: United States  |
===================================================================================

| LEFT COLUMN (Fundamentals KPIs)             | CENTER (30-Day Price Action)      | RIGHT COLUMN (Valuation & Analyst View) |
|---------------------------------------------|----------------------------------|-----------------------------------------|
| 💰 **Revenue (TTM):** $383.0B               | 🕯️ **Candlestick Chart (30 days)**| 📊 **Valuation Ratios**                 |
| 💵 **Net Income (TTM):** $97.0B             |   • OHLC from price_data          |     • P/E: 30.1x                        |
| 💸 **Free Cash Flow (TTM):** $100.0B        |   • 50-day MA: 215.4              |     • P/B: 45.2x                        |
| 📉 **Debt / Equity:** 1.4                   |   • 200-day MA: 190.1             |     • PEG: 2.1x                         |
| 📈 **ROE:** 140%                            |   • Volume bars below chart       |     • EV / EBITDA: 22.0x                |
| 💹 **Dividend Yield:** 0.5%                 |   • RSI(14): 68                   |     • Price / Sales: 7.5x               |
| 📊 **Revenue Growth YoY:** +2%              |                                  |                                         |
| 📉 **Earnings Growth YoY:** –1%             |                                  | 📈 **Analyst Consensus**                |
|---------------------------------------------|                                  |     • Recommendation: BUY               |
|                                             |                                  |     • Rating Avg: 4.2 (1=Sell, 5=Buy)   |
|                                             |                                  |     • Analyst Count: 45                 |
|                                             |                                  |                                         |
|                                             |                                  | 🎯 **Price Targets**                    |
|                                             |                                  |     • Mean: $230                        |
|                                             |                                  |     • High: $250                        |
|                                             |                                  |     • Low: $200                         |
===================================================================================

| BOTTOM PANEL: Technical & Performance Highlights                                                |
|-------------------------------------------------------------------------------------------------|
| ⚙️ 30-Day Volatility: 0.12   |  📈 Beta: 1.3   |  📊 RSI(14): 68 (Slightly overbought)                   |
| 📊 50-Day MA: 215.4  |  📊 200-Day MA: 190.1  → Bullish Trend (Golden Cross)                       |
| 💵 Dividend Yield: 0.5%  |  💹 Revenue Growth YoY: +2%  |  📉 Earnings Growth YoY: –1%                        |
===================================================================================
"""


def analyze(ticker):
    """Analyze a single stock"""

    try:
        stock_data = get_stock_data(ticker)
        print(f"Analyzing stock: {ticker}")
        # Your analysis logic here
    except Exception as e:
        print(f"Error: {e}")


def compare(ticker1, ticker2):
    """Compare two stocks"""
    stock1_data = get_stock_data(ticker1)
    stock2_data = get_stock_data(ticker2)
    print(f"Comparing {ticker1} vs {ticker2}")
    # Your comparison logic here


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\nuv run stonks [options] analyze STOCK\nuv run stonks [options] compare STOCK1 STOCK2"
        )
        sys.exit(1)

    if sys.argv[1] == "analyze":
        if len(sys.argv) < 3:
            print("Usage: uv run stonks [options] analyze STOCK")
            sys.exit(1)

        ticker = sys.argv[2]
        analyze(ticker)

    if sys.argv[1] == "compare":
        if len(sys.argv) < 4:
            print("Usage: uv run stonks [options] analyze STOCK")
            sys.exit(1)

        ticker1 = sys.argv[2]
        ticker2 = sys.argv[3]
        compare(ticker1, ticker2)


if __name__ == "__main__":
    main()
