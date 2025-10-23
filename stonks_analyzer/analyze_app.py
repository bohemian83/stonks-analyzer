import plotext as px
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Footer, Header
from stonks_analyzer.layouts.stock_dashboard import StockDashboard
from stonks_analyzer.layouts.ticker_input_screen import TickerInputScreen
from stonks_analyzer.data.stock_data_builder import get_stock_data


class AnalyseApp(App):
    CSS_PATH = "layouts/styles/stock_dashboard_styles.tcss"

    BINDINGS = [
        ("ctrl+t", "change_ticker", "Change Ticker"),
        ("[", "previous_theme", "Previous theme"),
        ("]", "next_theme", "Next theme"),
    ]

    def __init__(self):
        super().__init__()
        self.title = "Stonks Analyzer"
        self.stock_data = None
        self.theme = "gruvbox"
        self.theme_names = [
            theme for theme in self.available_themes if theme != "textual-ansi"
        ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="app-container"):
            yield StockDashboard()
        yield Footer()

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
            self.query_one(StockDashboard).update_all(self.stock_data)

        except Exception as e:
            self.push_screen(
                TickerInputScreen(error_message=str(e)), self.handle_ticker_input
            )

    def action_next_theme(self) -> None:
        themes = self.theme_names
        index = themes.index(self.current_theme.name)
        self.theme = themes[(index + 1) % len(themes)]
        self.notify_new_theme(self.current_theme.name)

    def action_previous_theme(self) -> None:
        themes = self.theme_names
        index = themes.index(self.current_theme.name)
        self.theme = themes[(index - 1) % len(themes)]
        self.notify_new_theme(self.current_theme.name)

    def notify_new_theme(self, theme_name: str) -> None:
        self.clear_notifications()
        self.notify(
            title="Theme updated",
            message=f"Theme is {theme_name}.",
        )
