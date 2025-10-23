import sys
from stonks_analyzer.analyze_app import AnalyseApp


def main():
    if len(sys.argv) < 2:
        print("Usage:\nuv run stonks analyze")
        sys.exit(1)

    try:
        app = AnalyseApp()
        app.run()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
