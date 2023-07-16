import os
import logging
import requests
from typing import List


class TelegramMessenger:
    def __init__(self, token: str, chat_ids: List[str]) -> None:
        self.token: str = token
        self.chat_ids: List[str] = chat_ids
        self.base_url: str = f"https://api.telegram.org/bot{self.token}"

    def send_message(self, message: str, parse_mode: str = "Markdown") -> None:
        url = f"{self.base_url}/sendMessage"
        params = {
            "text": message,
            "parse_mode": parse_mode or "Markdown"
        }
        for chat_id in self.chat_ids:
            params["chat_id"] = chat_id
            response = requests.get(url, params=params)
            if response.status_code == 200:
                print(
                    f"Telegram message sent successfully to chat ID {chat_id}: {message}")
            else:
                print(f"Failed to send message to chat ID {chat_id}")


def main():
    # Set up logging to see any errors
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Retrieve bot token and chat IDs from environment variables
    token = os.environ.get("BOT_TOKEN", "")
    chat_ids_str = os.environ.get("CHAT_IDS", "")
    chat_ids = chat_ids_str.split(",") if chat_ids_str else []

    # Create an instance of the TelegramMessenger class with bot token and chat IDs
    bot = TelegramMessenger(token=token, chat_ids=chat_ids)

    # Send a message with markdown formatting
    message = "Hello, *world*! [google](https://google.com)"
    bot.send_message(message, parse_mode="Markdown")


if __name__ == "__main__":
    main()
