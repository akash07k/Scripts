from typing import List, Dict
import configparser
import os


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
        rom["UPLOAD_COMMAND"] = input(
            "Upload command (or press enter to use curl --ssl -k -T {uploadfile} ftp://uploadme.example.com/files/munch/9.x/ --user username:password): ") or "curl --ssl -k -T {uploadfile} ftp://uploadme.example.com/files/munch/9.x/ --user username:password"
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


config = configparser.ConfigParser()
print("Welcome to Configuration Initializer")
print("By Akash Kakkar")
print("What do you want to do?")
print("1. Add a new ROM and device to configuration")
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
    add_rom_config()


# Check if "configs" directory exists, and create it if it doesn't
if not os.path.exists("configs"):
    os.makedirs("configs")

# Write or append the configuration file
with open("configs/telegram.ini", "a") as configfile:
    config.write(configfile)
print("Configuration file created/appended successfully")
