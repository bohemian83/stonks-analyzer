from textual.app import App, ComposeResult
from textual_plotext import PlotextPlot
import plotext as px
from textual.containers import Container
from stonks_analyzer.layouts.stock_dashboard import StockDashboard
from stonks_analyzer.data.stock_data_builder import get_stock_data


class ScatterApp(App):
    CSS_PATH = "stonks_analyzer/layouts/styles/stock_dashboard_styles.tcss"

    def __init__(self):
        super().__init__()
        self.stock_data = None

    def compose(self) -> ComposeResult:
        with Container(id="app-container"):
            yield StockDashboard()

    def on_mount(self) -> None:
        self.ticker = "AAPL"

        try:
            self.stock_data = get_stock_data(self.ticker)
            self.update_graph()
            self.update_labels()

        except Exception as e:
            print(f"exception {e} caught")

    def update_graph(self) -> None:
        graph_data = self.stock_data["price_data"][2]
        graph_data.columns = graph_data.columns.droplevel(1)
        plt = self.query_one(PlotextPlot).plt

        dates = px.datetimes_to_string(graph_data.index)
        plt.candlestick(dates, graph_data)
        plt.title("Stock Price CandleSticks")
        plt.xlabel("Date")
        plt.ylabel("Stock Price $")


if __name__ == "__main__":
    ScatterApp().run()
