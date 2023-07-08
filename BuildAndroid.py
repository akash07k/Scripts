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

selected_rom: str = rom_choices[choice - 1]
selected_section: str = rom_sections[choice - 1]
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


def initialize():
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
        print("ROM directory does not exist. Creating it")
        os.makedirs(rom_path)
        return True


def initialize_local_manifests():
    if os.path.exists(rom_path + "/.repo/local_manifests"):
        print("Local manifest directory exists")
        return True
    else:
        print("Local manifest directory does not exist. Cloning the repo")
        if clone_local_manifest():
            return True
        else:
            return False


def initialize_repo():
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


def clone_local_manifest():
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


def sync_sources():
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


def prompt_sync_sources():
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
        sync_sources()
        return True
    if choice == 2:
        print("Skipping the sync")
        return True
    if choice == 3:
        sync_then_build = True        
        return True


def envsetup_lunch_build():
    os.chdir(rom_path)
    if sync_then_build:
        sync_sources()
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
