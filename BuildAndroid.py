import configparser
import os
from typing import List

print("Welcome to Android builder")
print("By Akash Kakkar")

config = configparser.ConfigParser()
config.read('config.ini')

print("Which ROM do you want to build?")
rom_choices: List[str] = []
rom_sections: List[str] = []
for section in config.sections():
    rom_name = config.get(section, "ROM_NAME", fallback=None)
    if rom_name is not None:
        rom_choices.append(rom_name)
        rom_sections.append(section)
        print(f"{len(rom_choices)}. {rom_name}")

choice: int = 0

while choice == 0:
    try:
        choice = int(input("Enter your choice: "))
        if choice < 1 or choice > len(rom_choices):
            print("Invalid choice. Please enter a valid option.")
            choice = 0
    except ValueError:
        print("Invalid input. Please enter a number.")
        choice = 0

selected_rom: str = rom_choices[choice - 1]
selected_section: str = rom_sections[choice - 1]
device_codename: str = config.get(
    selected_section, "DEVICE_CODENAME", fallback="munch")
rom_path: str = config.get(
    selected_section, "ROM_PATH", fallback="/mnt/wsl/rom/cr")
build_variant: str = config.get(
    selected_section, "BUILD_VARIANT", fallback="userdebug")
manifest_url: str = config.get(selected_section, "MANIFEST_URL")
manifest_branch: str = config.get(selected_section, "MANIFEST_BRANCH")
print(
    f"Selected ROM: {selected_rom} for {device_codename} ({selected_section})")

# Performing the actions based on the selected ROM
# Check if the rom directory exists
if os.path.exists(rom_path):
    print("ROM directory exists. Proceeding with the build.")
    os.chdir(rom_path)
else:
    print("ROM directory does not exist. Creating it and initializing the repo")
    os.makedirs(rom_path)
    os.chdir(rom_path)
    exit_status = os.system(
        f"repo init -u {manifest_url} -b {manifest_branch} --git-lfs -g default,-mips,-darwin,-notdefault")
    if exit_status == 0:
        print("Repo initialized successfully")
        print("Syncing the sources")
        sync_sources()
    else:
        print("Error in initializing repo. Please initialize it manually")
        
def sync_sources():
    print("Do you want to sync the sources?")
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
    if choice == 1:
        exit_status = os.system("repo sync -c -j$(nproc --all) --force-sync --no-clone-bundle --no-tags --prune --current-branch --optimized-fetch")
        if exit_status == 0:
            print("Synchronization completed successfully")
        else:
            print("Error in syncing the sources. Please sync the sources manually")

print("Building process completed.")
