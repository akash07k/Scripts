import configparser
from typing import List

print("Welcome to Android builder")
print("By Akash Kakkar")

config = configparser.ConfigParser()
config.read('config.ini')

print("Which ROM do you want to build?")
rom_choices: List[str] = []

for section in config.sections():
    rom_name = config.get(section, "ROM_NAME", fallback=None)
    if rom_name is not None:
        rom_choices.append(rom_name)
        print(f"{len(rom_choices)}. {rom_name}")

choice: int = 0

while choice is 0:
    try:
        choice = int(input("Enter your choice: "))
        if not 1 <= choice <= len(rom_choices):
            print("Invalid choice. Please enter a valid option.")
            choice = 0
    except ValueError:
        print("Invalid input. Please enter a number.")
        choice = 0

selected_rom: str = rom_choices[choice - 1]
print(f"Selected ROM: {selected_rom}")

# Perform the actions based on the selected ROM
# Add your logic here to build the selected ROM

print("Building process completed.")
