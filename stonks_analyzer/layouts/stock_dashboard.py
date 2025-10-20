from textual.widget import Widget
from textual.app import ComposeResult
from textual.containers import Vertical, Grid
from textual.widgets import Placeholder


class StockDashboard(Widget):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Grid(
                Placeholder("This is a custom label for p1.", id="p1"),
                Placeholder("This is a custom label for p1.", id="p2"),
                Placeholder("This is a custom label for p1.", id="p3"),
                id="top",
            ),
            Grid(
                Grid(
                    Placeholder("Left col label 1.", classes="lcl"),
                    Placeholder("Left col label 2.", classes="lcl"),
                    Placeholder("Left col label 3.", classes="lcl"),
                    Placeholder("Left col label 4.", classes="lcl"),
                    Placeholder("Left col label 5.", classes="lcl"),
                    Placeholder("Left col label 6.", classes="lcl"),
                    Placeholder("Left col label 7.", classes="lcl"),
                    Placeholder("Left col label 8.", classes="lcl"),
                    id="left-main-col",
                ),
                Grid(
                    Placeholder("Graph goes here", id="graph"),
                    Grid(
                        Placeholder("under graph 1", id="ug1"),
                        Placeholder("under graph 2", id="ug2"),
                        Placeholder("under graph 3", id="ug3"),
                        id="under-graph",
                    ),
                    id="center-main-col",
                ),
                Grid(
                    Placeholder("Right col label 1.", classes="rcl"),
                    Placeholder("Right col label 2.", classes="rcl"),
                    Placeholder("Right col label 3.", classes="rcl"),
                    Placeholder("Right col label 4.", classes="rcl"),
                    Placeholder("Right col label 5.", classes="rcl"),
                    Placeholder("Right col label 6.", classes="rcl"),
                    Placeholder("Right col label 7.", classes="rcl"),
                    Placeholder("Right col label 8.", classes="rcl"),
                    Placeholder("Right col label 9.", classes="rcl"),
                    Placeholder("Right col label 10.", classes="rcl"),
                    Placeholder("Right col label 11.", classes="rcl"),
                    Placeholder("Right col label 12.", classes="rcl"),
                    id="right-main-col",
                ),
                id="main",
            ),
            Grid(
                Placeholder("This is a custom label for p4.", id="p4"),
                Placeholder("This is a custom label for p5.", id="p5"),
                Placeholder("This is a custom label for p6.", id="p6"),
                id="bottom",
            ),
            id="content",
        )
