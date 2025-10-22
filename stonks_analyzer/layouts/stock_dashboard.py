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
                    Static("", id="rcl1", classes="rcl"),
                    Static("", id="rcl2", classes="rcl"),
                    Static("", id="rcl3", classes="rcl"),
                    # Static("", id="rcl4", classes="rcl"),
                    # Static("", id="rcl5", classes="rcl"),
                    # Static("", id="rcl6", classes="rcl"),
                    # Static("", id="rcl7", classes="rcl"),
                    # Static("", id="rcl8", classes="rcl"),
                    # Static("", id="rcl9", classes="rcl"),
                    # Static("", id="rcl10", classes="rcl"),
                    # Static("", id="rcl11", classes="rcl"),
                    # Static("", id="rcl12", classes="rcl"),
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
