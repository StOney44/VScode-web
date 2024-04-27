import yfinance as yf
import pandas as pd
import requests

class DonchianChannelStrategy:
    def __init__(self, symbol, channel_id, bot_token):
        self.symbol = symbol
        self.channel_id = channel_id
        self.bot_token = bot_token

    def fetch_data(self, start_date, end_date):
        stock = yf.Ticker(self.symbol)
        data = stock.history(start=start_date, end=end_date)
        return data

    def generate_signals(self, data):
        # 전략을 적용하는 코드
        pass

    def send_slack_message(self, message):
        # Slack 메시지 전송 코드
        pass

    def run_strategy(self, start_date, end_date):
        df = self.fetch_data(start_date, end_date)
        signals = self.generate_signals(df)
        buy_signals = signals[signals['positions'] == 1]

        for index, row in buy_signals.iterrows():
            message = f"Buy signal detected for {self.symbol} at {index.strftime('%Y-%m-%d')} (Price: ${row['Close']})"
            self.send_slack_message(message)


class Interface:
    def __init__(self):
        self.strategies = ['Donchian Channel', 'Moving Average', 'RSI']
        self.selected_strategy = None

    def select_strategy(self):
        print("Select a strategy:")
        for idx, strategy in enumerate(self.strategies):
            print(f"{idx + 1}. {strategy}")
        
        selection = int(input("Enter the number of the strategy: "))
        self.selected_strategy = self.strategies[selection - 1]

    def input_stock_ticker(self):
        return input("Enter the stock ticker: ")

    def input_date_range(self):
        start_date = input("Enter the start date (YYYY-MM-DD): ")
        end_date = input("Enter the end date (YYYY-MM-DD): ")
        return start_date, end_date

    def run_interface(self):
        self.select_strategy()
        symbol = self.input_stock_ticker()
        start_date, end_date = self.input_date_range()

        if self.selected_strategy == 'Donchian Channel':
            channel_id = "YOUR_SLACK_CHANNEL_ID"
            bot_token = "YOUR_SLACK_BOT_TOKEN"
            strategy = DonchianChannelStrategy(symbol, channel_id, bot_token)
            strategy.run_strategy(start_date, end_date)
        elif self.selected_strategy == 'Moving Average':
            # Moving Average 전략 실행 코드
            pass
        elif self.selected_strategy == 'RSI':
            # RSI 전략 실행 코드
            pass


if __name__ == "__main__":
    interface = Interface()
    interface.run_interface()