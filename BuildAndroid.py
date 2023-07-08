import configparser
import os
import subprocess
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

print("Which telegram config you want to use for sending the notifications?")
telegram_choices: List[str] = []
telegram_sections: List[str] = []
for section in config.sections():
    telegram_name: str = config.get(section, "telegram_name", fallback="Akash")
    if telegram_name is not None:  # type : ignore # type: ignore
        telegram_choices.append(telegram_name)
        telegram_sections.append(section)
        print(f"{len(telegram_choices)}. {telegram_name}")
choice: int = 0
while choice == 0:
    try:
        choice = int(input("Enter your choice: "))
        if choice < 1 or choice > len(telegram_choices):
            print("Invalid choice. Please enter a valid option.")
            choice = 0
    except ValueError:
        print("Invalid input. Please enter a number.")
        choice = 0


selected_rom: str = rom_choices[choice - 1]
selected_section: str = rom_sections[choice - 1]
selected_telegram: str = telegram_choices[choice - 1]
selected_telegram_section: str = telegram_sections[choice - 1]
telegram_token: str = config.get(selected_telegram_section, "TELEGRAM_TOKEN")
telegram_chat_id: str = config.get(
    selected_telegram_section, "TELEGRAM_CHAT_ID")
telegram_user_name: str = config.get(
    selected_telegram_section, "TELEGRAM_USER_NAME")
repo_sync_command: str = config.get(selected_section, "REPO_SYNC_COMMAND",
                                    fallback="repo sync -c -j$(nproc --all) --force-sync --no-clone-bundle --no-tags --prune --current-branch --optimized-fetch")
sync_then_build: bool = False
lunch_name: str = config.get(
    selected_section, "LUNCH_NAME", fallback="lineage")
device_codename: str = config.get(
    selected_section, "DEVICE_CODENAME", fallback="munch")
rom_path: str = config.get(
    selected_section, "ROM_PATH", fallback="/mnt/wsl/rom/cr")
build_variant: str = config.get(
    selected_section, "BUILD_VARIANT", fallback="userdebug")
build_command: str = config.get(
    selected_section, "BUILD_COMMAND", fallback="m bacon -j$(nproc --all)")
manifest_url: str = config.get(selected_section, "MANIFEST_URL")
manifest_branch: str = config.get(selected_section, "MANIFEST_BRANCH")
local_manifest_url: str = config.get(selected_section, "LOCAL_MANIFEST_URL")
local_manifest_branch: str = config.get(
    selected_section, "LOCAL_MANIFEST_BRANCH")


print(
    f"Selected ROM: {selected_rom} for {device_codename} ({selected_section})")


def initialize() -> bool:
    if os.path.exists(rom_path):
        print("ROM directory exists")
        os.chdir(rom_path)
        if os.path.exists(rom_path + "/.repo"):
            print("Repo directory exists")
            return True
        else:
            print("Repo directory does not exist. Initializing it")
            if initialize_repo():
                return True
            else:
                return False
    else:
        print("ROM directory does not exist. Creating it")
        os.makedirs(rom_path)
        return True


def initialize_local_manifests() -> bool:
    if os.path.exists(rom_path + "/.repo/local_manifests"):
        print("Local manifest directory exists")
        return True
    else:
        print("Local manifest directory does not exist. Cloning the repo")
        if clone_local_manifest():
            return True
        else:
            return False


def initialize_repo() -> bool:
    os.chdir(rom_path)
    try:
        result = subprocess.run(["bash", "-c",
                                 f"repo init -u {manifest_url} -b {manifest_branch} --git-lfs -g default,-mips,-darwin,-notdefault"], check=True, text=True)
        print(result.stdout)
        print(f"Repo initialized successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(
            f"Error in initializing the repo. Please initialize it manually: {e.output}")
        return False


def clone_local_manifest() -> bool:
    os.chdir(rom_path)
    try:
        result = subprocess.run(["bash", "-c",
                                 f"git clone {local_manifest_url} -b {local_manifest_branch} {rom_path}/.repo/local_manifests"], check=True, text=True)
        print(result.stdout)
        print(f"Local manifest cloned successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(
            f"Error in cloning the local manifest. Please clone it manually: {e.output}")
        return False


def sync_sources() -> bool:
    os.chdir(rom_path)
    try:
        result = subprocess.run(["bash", "-c",
                                 repo_sync_command], check=True, text=True)
        print(result.stdout)
        print(f"Synchronization completed successfully")
        return True
    except subprocess.CalledProcessError as error:
        print(
            f"Error in syncing the sources. Please sync the sources manually: {error.output}")
        return False


def prompt_sync_sources() -> bool:
    print("Do you want to sync the sources?")
    print("1. Yes")
    print("2. No")
    print("3. Sync then build")
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
        result = sync_sources()
        if not result:
            return False
        return result
    if choice == 2:
        print("Skipping the sync")
        return True
    if choice == 3:
        global sync_then_build
        print("Sources will be synced right before the build")
        sync_then_build = True
        return sync_then_build
    else:
        return False


def envsetup_lunch_build() -> bool:
    os.chdir(rom_path)
    envsetup_command: str = ". build/envsetup.sh"
    lunch_command: str = f"lunch {lunch_name}_{device_codename}-{build_variant}"
    consolidated_command: str = f"{envsetup_command} && {lunch_command} && {build_command}"
    print("Do you want a clean build?")
    print("1. No")
    print("2. Yes")
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
        consolidated_command: str = f"{envsetup_command} && {lunch_command} && {build_command}"
    if choice == 2:
        clean_command: str = "m clean -j$(nproc --all)"
        consolidated_command: str = f"{envsetup_command} && {clean_command} && {lunch_command} && {build_command}"

    try:
        if sync_then_build:
            result = sync_sources()
            if not result:
                return False
        result = subprocess.run(
            ["bash", "-c", consolidated_command], check=True, text=True)
        print("Build completed successfully")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("Error in building the rom, please build it manually:", e)
        print("Output:")
        print(e.output)
        return False


# Performing the actions based on the selected ROM
if initialize() and initialize_local_manifests() and prompt_sync_sources() and envsetup_lunch_build():
    print("Building process completed.")
else:
    print("Building process failed.")
