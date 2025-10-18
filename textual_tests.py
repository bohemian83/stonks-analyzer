from textual.app import App, ComposeResult
import yfinance as yf
from textual_plotext import PlotextPlot
import plotext as px


class ScatterApp(App[None]):
    def compose(self) -> ComposeResult:
        yield PlotextPlot()

    def on_mount(self) -> None:
        plt = self.query_one(PlotextPlot).plt

        end = "2025-10-17"
        data = yf.download("aapl", end=end, period="1y", interval="1d")
        data.columns = data.columns.droplevel(1)
        dates = px.datetimes_to_string(data.index)
        plt.candlestick(dates, data)
        plt.title("Stock Price CandleSticks")
        plt.xlabel("Date")
        plt.ylabel("Stock Price $")


if __name__ == "__main__":
    ScatterApp().run()
