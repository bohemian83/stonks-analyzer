# Stonks Analyzer

A terminal-based stock analysis application that provides financial data visualization and analysis for stocks.

## Features

- **Terminal UI**: Rich terminal interface built with Textual framework
- **Stock Data**: Stock information powered by Yahoo Finance API
- **Comprehensive Analysis**:
    - Company fundamentals (revenue, income, cash flow, ratios)
    - Technical indicators (RSI, moving averages, volatility)
    - Valuation metrics (P/E, P/B, PEG ratios)
    - Analyst recommendations and price targets
- **Visual Charts**: Candlestick price charts with 50-day and 200-day moving averages
- **Theme Support**: Multiple UI themes with keyboard shortcuts for easy switching

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management. Make sure you have uv installed, then install the project dependencies:

```bash
uv sync
```

## Usage

To run the stock analyzer:

```bash
uv run stonks analyze
```

This will launch the interactive terminal interface where you can:

1. Enter a stock ticker symbol (e.g., AAPL, MSFT, GOOGL)
2. View comprehensive stock analysis including price charts, fundamentals, and technical indicators
3. Switch between different UI themes using `[` and `]` keys
4. Change to a different stock using `Ctrl+T`

## Key Bindings

- `Ctrl+T`: Change ticker symbol
- `[`: Previous theme
- `]`: Next theme
- `Ctrl+C`: Exit application

## Dependencies

- **Python 3.14+**
- **Textual**: Terminal UI framework
- **yfinance**: Yahoo Finance API wrapper
- **pandas & numpy**: Data processing
- **plotext**: Terminal-based plotting
- **textual-plotext**: Plotext integration for Textual

## Project Structure

```
stonks_analyzer/
├── data/                    # Data fetching and processing
├── layouts/                 # UI components and styling
├── analyze_app.py          # Main Textual application
├── main.py                 # Entry point
└── cli.py                  # Command-line interface
```

## License

This project is open source and available under the MIT License.
