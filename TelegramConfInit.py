from typing import List, Dict
import configparser
import os


def add_telegram_config():
    telegram_configs: List[Dict[str, str]] = []
    add_telegram_config: bool = True
    while add_telegram_config:
        telegram_config: Dict[str, str] = {}
        telegram_config["TELEGRAM_CONFIG_NAME"] = input(
            "Telegram config name: (or press enter for Akash)") or "Akash"
        telegram_config["TELEGRAM_BOT_TOKEN"] = input(
            "Telegram bot Token: ")
        telegram_config["TELEGRAM_CHAT_ID"] = input(
            "Telegram chat ID: ")
        telegram_config["TELEGRAM_USER_NAME"] = input(
            "Telegram user Name: (or press enter for @akashk07)") or "@akashk07"
        telegram_configs.append(telegram_config)
        print("Do you want to add another Telegram config?")
        print("1. Yes")
        print("2. No")
        valid_choices: List[int] = [1, 2]
        choice: int = 0
        while choice not in valid_choices:
            try:
                choice = int(input("Enter your choice: "))
                if choice not in valid_choices:
                    print("Invalid choice. Please enter a valid option.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            if choice != 1:
                add_telegram_config = False
                break
            else:
                add_telegram_config = True
        for i, telegram_config in enumerate(telegram_configs, start=1):
            telegram_section: str = f"TELEGRAM{i}"
            config[telegram_section] = telegram_config


config = configparser.ConfigParser()
print("Welcome to Configuration Initializer")
print("By Akash Kakkar")
print("What do you want to do?")
print("1. Add telegram config")

valid_choices: List[int] = [1,]
choice: int = 0

while choice not in valid_choices:
    try:
        choice = int(input("Enter your choice: "))
        if choice not in valid_choices:
            print("Invalid choice. Please enter a valid option.")
    except ValueError:
        print("Invalid input. Please enter a number.")
if choice == 1:
    add_telegram_config()

# Check if "configs" directory exists, and create it if it doesn't
if not os.path.exists("configs"):
    os.makedirs("configs")

# Write or append the configuration file
with open("configs/telegram.ini", "a") as configfile:
    config.write(configfile)
print("Configuration file created/appended successfully")
