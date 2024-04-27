import yfinance as yf
import pandas as pd
import requests

class DonchianChannelStrategy:
    def __init__(self, symbol, channel_id, bot_token):
        self.symbol = symbol
        self.channel_id = channel_id
        self.bot_token = bot_token

    def fetch_data(self):
        stock = yf.Ticker(self.symbol)
        data = stock.history(period="max")
        return data

    def generate_signals(self, data):
        data['20_days_high'] = data['High'].rolling(window=20).max()
        data['10_days_low'] = data['Low'].rolling(window=10).min()
        data['signal'] = 0
        data.loc[data['Close'] > data['20_days_high'].shift(1), 'signal'] = 1
        data['positions'] = data['signal'].diff()

        return data

    def send_slack_message(self, message):
        url = f"https://slack.com/api/chat.postMessage"
        headers = {
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "channel": self.channel_id,
            "text": message
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            print("Failed to send message to Slack.")
        else:
            print("Message sent to Slack successfully.")

    def run_strategy(self):
        df = self.fetch_data()
        signals = self.generate_signals(df)
        buy_signals = signals[signals['positions'] == 1]

        for index, row in buy_signals.iterrows():
            message = f"Buy signal detected for {self.symbol} at {index.strftime('%Y-%m-%d')} (Price: ${row['Close']})"
            self.send_slack_message(message)


if __name__ == "__main__":
    symbol = "MSFT"  # Microsoft 주식
    channel_id = "YOUR_SLACK_CHANNEL_ID"
    bot_token = "YOUR_SLACK_BOT_TOKEN"

    strategy = DonchianChannelStrategy(symbol, channel_id, bot_token)
    strategy.run_strategy()