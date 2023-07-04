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
build_command: str = config.get(
    selected_section, "BUILD_COMMAND", fallback="m bacon -j$(nproc --all)")
manifest_url: str = config.get(selected_section, "MANIFEST_URL")
manifest_branch: str = config.get(selected_section, "MANIFEST_BRANCH")
local_manifest_url: str = config.get(selected_section, "LOCAL_MANIFEST_URL")
local_manifest_branch: str = config.get(
    selected_section, "LOCAL_MANIFEST_BRANCH")

print(
    f"Selected ROM: {selected_rom} for {device_codename} ({selected_section})")


def check_rom_repo_dirs():
    if os.path.exists(rom_path):
        print("ROM directory exists")
        os.chdir(rom_path)
        if os.path.exists(rom_path + "/.repo"):
            print("Repo directory exists")
            print("Syncing the sources")
            sync_sources()
        else:
            print("Repo directory does not exist. Initializing it")
            initialize_repo()
            check_local_manifest_dir()
            sync_sources()
    else:
        print("ROM directory does not exist. Creating it")
        os.makedirs(rom_path)
        os.chdir(rom_path)


def check_local_manifest_dir():
    if os.path.exists(rom_path + "/.repo/local_manifests"):
        print("Local manifest directory exists. Updating the repo")
        os.chdir(rom_path + "/.repo/local_manifests")
        exit_status = os.system("git pull --rebase")
        if exit_status == 0:
            print("Local manifest updated successfully")
            os.chdir(rom_path)
        else:
            print("Error in updating local manifest. Please update it manually")
    else:
        print("Local manifest directory does not exist. Cloning the repo")
        clone_local_manifest()


def initialize_repo():
    exit_status = os.system(
        f"repo init -u {manifest_url} -b {manifest_branch} --git-lfs -g default,-mips,-darwin,-notdefault")
    if exit_status == 0:
        print("Repo initialized successfully")
        print("Syncing the sources")
        sync_sources()
    else:
        print("Error in initializing repo. Please initialize it manually")


def clone_local_manifest():
    exit_status = os.system(
        f"git clone {local_manifest_url} -b {local_manifest_branch} {rom_path}/.repo/local_manifests")
    if exit_status == 0:
        print("Local manifest cloned successfully")
    else:
        print("Error in cloning the local manifest. Please clone it manually")


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
        exit_status = os.system(
            "repo sync -c -j$(nproc --all) --force-sync --no-clone-bundle --no-tags --prune --current-branch --optimized-fetch")
        if exit_status == 0:
            print("Synchronization completed successfully")
        else:
            print("Error in syncing the sources. Please sync the sources manually")


# Performing the actions based on the selected ROM
check_rom_repo_dirs()


print("Building process completed.")
