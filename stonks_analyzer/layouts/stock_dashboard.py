from textual.widget import Widget
from textual.app import ComposeResult
from textual.containers import Vertical, Grid
from textual.widgets import Static, Placeholder
from textual_plotext import PlotextPlot
import plotext as px


class StockDashboard(Widget):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Grid(
                Static("", id="top1"),
                Static("", id="top2"),
                Static("", id="top3"),
                Static("", id="top4"),
                Static("", id="top5"),
                Static("", id="top6"),
                id="top",
            ),
            Grid(
                Grid(
                    Static("", id="lcl1", classes="lcl"),
                    Static("", id="lcl2", classes="lcl"),
                    Static("", id="lcl3", classes="lcl"),
                    Static("", id="lcl4", classes="lcl"),
                    Static("", id="lcl5", classes="lcl"),
                    Static("", id="lcl6", classes="lcl"),
                    Static("", id="lcl7", classes="lcl"),
                    Static("", id="lcl8", classes="lcl"),
                    id="left-main-col",
                ),
                Grid(
                    PlotextPlot(id="graph"),
                    id="center-main-col",
                ),
                Grid(
                    Static("", id="rcl1", classes="rcl"),
                    Static("", id="rcl2", classes="rcl"),
                    Static("", id="rcl3", classes="rcl"),
                    id="right-main-col",
                ),
                id="main",
            ),
            Grid(
                Static("", id="btm1"),
                Static("", id="btm2"),
                Static("", id="btm3"),
                Static("", id="btm4"),
                Static("", id="btm5"),
                Static("", id="btm6"),
                id="bottom",
            ),
            id="content",
        )

    def update_all(self, stock_data: dict) -> None:
        self.update_graph(stock_data)
        self.update_top(stock_data)
        self.update_bottom(stock_data)
        self.update_left(stock_data)
        self.update_right(stock_data)

    def update_graph(self, stock_data: dict) -> None:
        graph_data = stock_data["price_data"][2]
        graph_data.columns = graph_data.columns.droplevel(1)
        dates = px.datetimes_to_string(graph_data.index)

        plt = self.query_one("#graph").plt

        sma50 = stock_data["technical_indicators"]["50_day_ma"][0]
        sma200 = stock_data["technical_indicators"]["200_day_ma"][0]

        sma50d_dates = px.datetimes_to_string(sma50.index)
        sma200d_dates = px.datetimes_to_string(sma200.index)

        plt.grid(True, True)
        plt.candlestick(dates, graph_data)

        plt.plot(
            sma50d_dates, sma50.tolist(), label="50-day Moving Avg", marker="braille"
        )
        plt.plot(
            sma200d_dates, sma200.tolist(), label="200-day Moving Avg", marker="braille"
        )

        plt.title(f"{stock_data['ticker']} Price Candlesticks (1y)")
        plt.xlabel("Date")
        plt.ylabel("Stock Price $")

    def update_left(self, stock_data: dict) -> None:
        self.query_one("#lcl1").update(
            f"Revenue (TTM): ${stock_data['fundamentals']['revenue_ttm']}"
        )
        self.query_one("#lcl2").update(
            f"Net Income(TTM): ${stock_data['fundamentals']['net_income_ttm']}"
        )
        self.query_one("#lcl3").update(
            f"Free Cash Flow (TTM): ${stock_data['fundamentals']['free_cash_flow_ttm']}"
        )
        self.query_one("#lcl4").update(
            f"Debt / Equity: {stock_data['fundamentals']['debt_to_equity']}"
        )
        self.query_one("#lcl5").update(f"ROE: {stock_data['fundamentals']['roe']}")
        self.query_one("#lcl6").update(
            f"Dividend Yield: {stock_data['fundamentals']['dividend_yield']}"
        )
        self.query_one("#lcl7").update(
            f"Revenue Growth YoY: {stock_data['fundamentals']['revenue_growth_yoy']}"
        )
        self.query_one("#lcl8").update(
            f"Earnings Growth YoY: {stock_data['fundamentals']['earnings_growth_yoy']}"
        )

    def update_right(self, stock_data: dict) -> None:
        self.query_one("#rcl1").update(
            f"**Valuation Ratios\n\n • P/E: {stock_data['valuation_ratios']['pe_ratio']}\n • P/B: {stock_data['valuation_ratios']['pb_ratio']}\n • PEG: {stock_data['valuation_ratios']['peg_ratio']}\n • EV / EBITDA: {stock_data['valuation_ratios']['ev_to_ebitda']}\n • Price / Sales: {stock_data['valuation_ratios']['price_to_sales']}"
        )
        self.query_one("#rcl2").update(
            f"**Analyst Consensus\n\n • Recommendation: {stock_data['analyst_summary']['consensus_recommendation']}\n • Rating Avg: {stock_data['analyst_summary']['rating_average']} (1=Sell, 5=Buy)\n • Analyst Count: {stock_data['analyst_summary']['analyst_count']}"
        )
        self.query_one("#rcl3").update(
            f"**Price Targets\n\n • Mean: ${stock_data['analyst_summary']['target_price_mean']}\n • High: ${stock_data['analyst_summary']['target_price_high']}\n • Low: ${stock_data['analyst_summary']['target_price_low']}"
        )

    def update_top(self, stock_data: dict) -> None:
        price_with_color = (
            f"[green]{stock_data['price_data'][1]}[/]"
            if "▲" in {stock_data["price_data"][1]}
            else f"[red]{stock_data['price_data'][1]}[/]"
        )
        self.query_one("#top1").update(
            f"{stock_data['meta']['company_name']} ({stock_data['ticker']})"
        )
        self.query_one("#top2").update(f"Exchange: {stock_data['meta']['exchange']}")
        self.query_one("#top3").update(f"Sector: {stock_data['meta']['sector']}")
        self.query_one("#top4").update(
            f"Price: ${round(stock_data['price_data'][0][-1]['close'], 2)} {price_with_color}"
        )
        self.query_one("#top5").update(
            f"Market Cap: {stock_data['meta']['market_cap']}"
        )
        self.query_one("#top6").update(f"Country: {stock_data['meta']['country']}")

    def update_bottom(self, stock_data: dict) -> None:
        self.query_one("#btm1").update(
            f"30-Day Volatility: {stock_data['technical_indicators']['volatility_30d']}"
        )
        self.query_one("#btm2").update(
            f"Beta: {stock_data['technical_indicators']['beta']}"
        )
        self.query_one("#btm3").update(
            f"RSI(14): {stock_data['technical_indicators']['rsi_14'][0]} {stock_data['technical_indicators']['rsi_14'][1]} "
        )
        self.query_one("#btm4").update(
            f"50-Day Moving Avg: ${stock_data['technical_indicators']['50_day_ma'][1]}"
        )
        self.query_one("#btm5").update(
            f"200-Day Moving Avg: ${stock_data['technical_indicators']['200_day_ma'][1]}"
        )
        self.query_one("#btm6").update(f"{stock_data['technical_indicators']['cross']}")
