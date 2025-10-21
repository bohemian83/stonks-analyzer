from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Input, Button, Label, Static
from textual.containers import Container, Horizontal


class TickerInputScreen(ModalScreen[str]):
    CSS_PATH = "styles/ticker_input_styles.tcss"

    def __init__(self, error_message: str = ""):
        self.error_message = error_message
        super().__init__()

    def compose(self) -> ComposeResult:
        with Container(id="ticker-dialog"):
            yield Label("Enter Stock Ticker:", id="question")
            yield Input(placeholder="e.g., AAPL", id="ticker-input")
            yield Static(self.error_message, id="ticker-error")
            with Horizontal(id="buttons"):
                yield Button("OK", variant="primary", id="ok")
                yield Button("Cancel", variant="default", id="cancel")

    def on_mount(self) -> None:
        self.query_one(Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ok":
            ticker = self.query_one(Input).value.strip().upper()
            if not ticker:
                self.query_one("#ticker-error", Static).update("Please enter a ticker")
                return

            if not ticker.isalpha() or len(ticker) > 5:
                self.query_one("#ticker-error", Static).update("Invalid ticker format")
                return

            self.dismiss(ticker)
        else:
            self.dismiss(None)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        ticker = event.value.strip().upper()
        if ticker and ticker.isalpha() and len(ticker) <= 5:
            self.dismiss(ticker)
        else:
            self.query_one("#ticker-error", Static).update("Invalid ticker format")
