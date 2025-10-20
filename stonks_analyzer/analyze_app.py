import plotext as px
from textual.app import App, ComposeResult
from textual_plotext import PlotextPlot
from stonks_analyzer.layouts.stock_dashboard import StockDashboard
from stonks_analyzer.data.stock_data_builder import get_stock_data


class AnalyseApp(App):
    CSS_PATH = "layouts/styles/stock_dashboard_styles.tcss"

    def __init__(self, ticker: str):
        super().__init__()
        self.ticker = ticker
        self.stock_data = None

    def compose(self) -> ComposeResult:
        yield StockDashboard()

    def on_mount(self) -> None:
        self.stock_data = get_stock_data(self.ticker)
        self.update_graph()
        self.update_labels()

    def update_graph(self) -> None:
        plt = self.query_one("#graph", PlotextPlot).plt
        dates = px.datetimes_to_string(self.stock_data.index)
        plt.candlestick(
            dates,
            [
                self.stock_data["Open"].tolist(),
                self.stock_data["High"].tolist(),
                self.stock_data["Low"].tolist(),
                self.stock_data["Close"].tolist(),
            ],
        )
        plt.title(f"{self.ticker} Stock Price")

    def update_labels(self) -> None:
        # Update placeholders with actual data
        self.query_one("#p1").update(f"Ticker: {self.ticker}")
        # ... update other labels with stock_data values
