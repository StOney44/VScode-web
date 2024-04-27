import pandas as pd

class Strategy:
    def __init__(self, short_window, long_window):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0

        # Create short simple moving average over the short window
        signals['short_mavg'] = data['Close'].rolling(window=self.short_window, min_periods=1, center=False).mean()

        # Create long simple moving average over the long window
        signals['long_mavg'] = data['Close'].rolling(window=self.long_window, min_periods=1, center=False).mean()

        # Create signals
        signals['signal'][self.short_window:] = \
            (signals['short_mavg'][self.short_window:] > signals['long_mavg'][self.short_window:]) * 1.0

        # Generate trading orders
        signals['positions'] = signals['signal'].diff()

        return signals


class Backtester:
    def __init__(self, strategy, data):
        self.strategy = strategy
        self.data = data

    def run_backtest(self):
        # Generate trading signals
        signals = self.strategy.generate_signals(self.data)

        # Calculate returns
        self.data['returns'] = self.data['Close'].pct_change()

        # Calculate strategy returns
        self.data['strategy_returns'] = signals['positions'].shift(1) * self.data['returns']

        return signals, self.data


# Example usage
if __name__ == "__main__":
    # Load stock data
    # (Assuming data is in the format of pandas DataFrame with columns: 'Date', 'Open', 'High', 'Low', 'Close', 'Volume')
    # Replace this with your actual data loading code
    data = pd.read_csv('stock_data.csv', index_col='Date', parse_dates=True)

    # Define strategy parameters
    short_window = 20
    long_window = 50

    # Initialize strategy
    strategy = Strategy(short_window, long_window)

    # Initialize backtester
    backtester = Backtester(strategy, data)

    # Run backtest
    signals, backtest_results = backtester.run_backtest()

    # Print signals and backtest results
    print("Trading signals:")
    print(signals.head())
    print("\nBacktest results:")
    print(backtest_results.head())