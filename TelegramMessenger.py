import logging
import requests


class TelegramMessenger:
    def __init__(self, token: str, chat_id: str) -> None:
        self.token: str = token
        self.chat_id: str = chat_id
        self.base_url: str = f"https://api.telegram.org/bot{self.token}"

    def send_message(self, message: str, parse_mode: str = None) -> None:  # type: ignore
        url = f"{self.base_url}/sendMessage"
        params = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": parse_mode or "Markdown"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print(f"Telegram message sent successfully: {message}")
        if response.status_code != 200:
            print(f"Fail to send message")

def main():
    # Set up logging to see any errors
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Create an instance of the TelegramMessenger class with your bot token and chat ID
    bot = TelegramMessenger(
        token="YOUR_BOT_TOKEN", chat_id="YOUR_CHAT_ID")

    # Send a message with markdown formatting
    message = "Hello, *world*! [google](https://google.com)"
    bot.send_message(message, parse_mode="Markdown")


if __name__ == "__main__":
    main()
