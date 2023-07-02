from typing import List, Dict
import configparser

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
    roms: List[Dict[str, str]] = []
    add_rom: bool = True

    while add_rom:
        rom: Dict[str, str] = {}
        rom["ROM_NAME"] = input(
            "ROM name (or press enter to use crDroid): ") or "crDroid"
        rom["ROM_PATH"] = input(
            "ROM path (or press enter to use /mnt/wsl/rom/cr): ") or "/mnt/wsl/rom/cr"
        rom["DEVICE_CODENAME"] = input(
            "Device code name (or press enter to use munch): ") or "munch"
        rom["BUILD_VARIANT"] = input(
            "Build variant (or press enter to use userdebug): ") or "userdebug"
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

with open('config.ini', 'a') as configfile:  # Use 'a' mode to append
    config.write(configfile)

print("Configuration file created/appended successfully")
