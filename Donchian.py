import requests
import pandas as pd
from datetime import datetime, timedelta

class DonchianChannelStrategy:
    def __init__(self, symbol, api_key, channel_id, bot_token):
        self.symbol = symbol
        self.api_key = api_key
        self.channel_id = channel_id
        self.bot_token = bot_token

    def fetch_data(self):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self.symbol}&apikey={self.api_key}"
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data['Time Series (Daily)']).T
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)
        return df

    def generate_signals(self, data):
        data['20_days_high'] = data['2. high'].rolling(window=20).max()
        data['10_days_low'] = data['3. low'].rolling(window=10).min()
        data['signal'] = 0
        data['signal'] = data['signal'].where(data['20_days_high'] <= data['4. close'].shift(1), 1)
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
            message = f"Buy signal detected for {self.symbol} at {index.strftime('%Y-%m-%d')} (Price: ${row['4. close']})"
            self.send_slack_message(message)


if __name__ == "__main__":
    symbol = "MSFT"  # Microsoft 주식
    api_key = "YOUR_ALPHA_VANTAGE_API_KEY"
    channel_id = "YOUR_SLACK_CHANNEL_ID"
    bot_token = "YOUR_SLACK_BOT_TOKEN"

    strategy = DonchianChannelStrategy(symbol, api_key, channel_id, bot_token)
    strategy.run_strategy()