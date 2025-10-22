import plotext as px
from textual.app import App, ComposeResult
from textual_plotext import PlotextPlot
from textual.containers import Container
from stonks_analyzer.layouts.stock_dashboard import StockDashboard
from stonks_analyzer.layouts.ticker_input_screen import TickerInputScreen
from stonks_analyzer.data.stock_data_builder import get_stock_data

# Constants at the top of your file


class AnalyseApp(App):
    CSS_PATH = "layouts/styles/stock_dashboard_styles.tcss"

    BINDINGS = [
        ("ctrl+t", "change_ticker", "Change Ticker"),
    ]

    def __init__(self):
        super().__init__()
        self.stock_data = None

    def compose(self) -> ComposeResult:
        with Container(id="app-container"):
            yield StockDashboard()

    def on_mount(self) -> None:
        self.push_screen(TickerInputScreen(), self.handle_ticker_input)

    def action_change_ticker(self) -> None:
        self.push_screen(TickerInputScreen(), self.handle_ticker_input)

    def handle_ticker_input(self, ticker: str | None) -> None:
        if not ticker:
            self.exit()
            return

        self.ticker = ticker

        try:
            self.stock_data = get_stock_data(self.ticker)
            self.update_graph()
            self.update_labels()

        except Exception as e:
            print(f"exception {e} caught")
            self.push_screen(
                TickerInputScreen(error_message=str(e)), self.handle_ticker_input
            )

    def update_graph(self) -> None:
        # plt = self.query_one("#graph", PlotextPlot).plt
        # dates = px.datetimes_to_string(self.stock_data.index)
        # plt.candlestick(
        #     dates,
        #     [
        #         self.stock_data["Open"].tolist(),
        #         self.stock_data["High"].tolist(),
        #         self.stock_data["Low"].tolist(),
        #         self.stock_data["Close"].tolist(),
        #     ],
        # )
        # plt.title(f"{self.ticker} Stock Price")
        pass

    def update_top(self) -> None:
        self.query_one("#top1").update(
            f"{self.stock_data['meta']['company_name']} ({self.stock_data['ticker']})"
        )
        self.query_one("#top2").update(
            f"Exchange: {self.stock_data['meta']['exchange']}"
        )
        self.query_one("#top3").update(f"Sector: {self.stock_data['meta']['sector']}")
        self.query_one("#top4").update(
            f"Price: ${round(self.stock_data['price_data'][0][-1]['close'], 2)} {self.stock_data['price_data'][1]} "
        )
        self.query_one("#top5").update(
            f"Market Cap: {self.stock_data['meta']['market_cap']}"
        )
        self.query_one("#top6").update(
            f"P/E: {self.stock_data['valuation_ratios']['pe_ratio']}"
        )

    def update_bottom(self) -> None:
        self.query_one("#btm1").update(
            f"30d Volatility: {self.stock_data['technical_indicators']['volatility_30d']}"
        )
        self.query_one("#btm2").update(
            f"Beta: {self.stock_data['technical_indicators']['beta']}"
        )
        self.query_one("#btm3").update(
            f"RSI(14): {self.stock_data['technical_indicators']['rsi_14'][0]} {self.stock_data['technical_indicators']['rsi_14'][1]} "
        )
        self.query_one("#btm4").update(
            f"50d MA: ${self.stock_data['technical_indicators']['50_day_ma']}"
        )
        self.query_one("#btm5").update(
            f"200d MA: ${self.stock_data['technical_indicators']['200_day_ma']}"
        )
        self.query_one("#btm6").update(
            f"{self.stock_data['technical_indicators']['cross']}"
        )

    def update_labels(self) -> None:
        self.update_top()
        self.update_bottom()
