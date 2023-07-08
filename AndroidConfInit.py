from typing import List, Dict
import configparser


def add_rom_config():
    roms: List[Dict[str, str]] = []
    add_rom: bool = True

    while add_rom:
        rom: Dict[str, str] = {}
        rom["ROM_NAME"] = input(
            "ROM name (or press enter to use crDroid): ") or "crDroid"
        rom["REPO_SYNC_COMMAND"] = input(
            "Repo sync command (or press enter for repo sync -c -j$(nproc --all) --force-sync --no-clone-bundle --no-tags --prune --current-branch --optimized-fetch") or "repo sync -c -j$(nproc --all) --force-sync --no-clone-bundle --no-tags --prune --current-branch --optimized-fetch"
        rom["lunch_name"] = input(
            "Rom lunch name (or press enter to use lineage): ") or "lineage"
        rom["ROM_PATH"] = input(
            "ROM path (or press enter to use /mnt/wsl/rom/cr): ") or "/mnt/wsl/rom/cr"
        rom["DEVICE_CODENAME"] = input(
            "Device code name (or press enter to use munch): ") or "munch"
        rom["BUILD_VARIANT"] = input(
            "Build variant (or press enter to use userdebug): ") or "userdebug"
        rom["BUILD_COMMAND"] = input(
            "Build command (or press enter to use m bacon): ") or "m bacon"
        rom["MANIFEST_URL"] = input(
            "Manifest URL: (or press enter to use https://github.com/crdroidandroid/android.git)") or "https://github.com/crdroidandroid/android.git"
        rom["MANIFEST_BRANCH"] = input(
            "Manifest branch: (or press enter to use 13.0)") or "13.0"
        rom["LOCAL_MANIFEST_URL"] = input(
            "Local manifest URL: (or press enter to use https://github.com/akash07k/local_manifests)") or "https://github.com/akash07k/local_manifests.git"
        rom["LOCAL_MANIFEST_BRANCH"] = input(
            "Local manifest branch: (or press enter to use lineage)") or "lineage"
        roms.append(rom)
        print("Do you want to add another ROM?")
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
            add_rom = False

    for i, rom in enumerate(roms, start=1):
        rom_section: str = f"ROM{i}"
        config[rom_section] = rom


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
print("1. Add a new ROM and device to configuration")
print("2. Add telegram config")

valid_choices: List[int] = [1, 2, 3]
choice: int = 0

while choice not in valid_choices:
    try:
        choice = int(input("Enter your choice: "))
        if choice not in valid_choices:
            print("Invalid choice. Please enter a valid option.")
    except ValueError:
        print("Invalid input. Please enter a number.")

if choice == 1:
    add_rom_config()
elif choice == 2:
    add_telegram_config()


with open('config.ini', 'a') as configfile:  # Use 'a' mode to append
    config.write(configfile)

print("Configuration file created/appended successfully")
