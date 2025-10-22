from textual.widget import Widget
from textual.app import ComposeResult
from textual.containers import Vertical, Grid
from textual.widgets import Static, Placeholder


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
