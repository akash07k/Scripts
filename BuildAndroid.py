import click
import configparser
import glob
import os
import subprocess
from typing import List, Union
from telegram_messenger import TelegramMessenger

rom_choices: List[str] = []
rom_sections: List[str] = []
selected_rom: str = ""
telegram_choices: List[str] = []
telegram_sections: List[str] = []
selected_telegram: str = ""
rom_config = configparser.ConfigParser()
rom_config = configparser.ConfigParser()
telegram_config = configparser.ConfigParser()
CONFIG_DIR = "configs"
ROM_CONFIG_FILE = f"{CONFIG_DIR}/rom.ini"
TELEGRAM_CONFIG_FILE = f"{CONFIG_DIR}/telegram.ini"
rom_config.read(ROM_CONFIG_FILE)
telegram_config.read(TELEGRAM_CONFIG_FILE)
telegram_token: str = ""
telegram_chat_ids: List[str] = []
telegram_user_name: str = ""
bot: TelegramMessenger = None  # type: ignore
repo_sync_command: str = ""
sync_then_build: bool = False
lunch_name: str = ""
device_codename: str = ""
rom_path: str = ""
manifest_url: str = ""
manifest_branch: str = ""
local_manifest_url: str = ""
local_manifest_branch: str = ""
build_variant: str = ""
build_command: str = ""
upload_command: str = ""
download_url: str = ""
sync_choices: List[str] = []
build_choices: List[str] = []


def main():
    click.echo("Welcome to Android builder")
    click.echo("Written by Akash Kakkar")
    choose_rom()
    choose_telegram()
    load_config()
    # Performing the actions based on the selected ROM
    if initialize() and initialize_local_manifests() and prompt_sync_sources() and envsetup_lunch_build():
        click.echo("Building process completed.")
    else:
        click.echo("Building process failed.")


def validate_rom_choice(value: Union[str, int]) -> int:
    try:
        choice = int(value)
        if 1 <= choice <= len(rom_choices):
            return choice
        else:
            raise ValueError()
    except ValueError:
        raise click.BadParameter(
            "Invalid choice. Please choose a valid rom option")


def validate_telegram_choice(value: Union[str, int]) -> int:
    try:
        choice = int(value)
        if 1 <= choice <= len(telegram_choices):
            return choice
        else:
            raise ValueError()
    except ValueError:
        raise click.BadParameter(
            "Invalid choice. Please choose a valid telegram option")


def validate_sync_choice(value: Union[str, int]) -> int:
    try:
        choice = int(value)
        if 1 <= choice <= len(sync_choices):
            return choice
        else:
            raise ValueError()
    except ValueError:
        raise click.BadParameter(
            "Invalid choice. Please choose a valid sync option")


def validate_build_choice(value: Union[str, int]) -> int:
    try:
        choice = int(value)
        if 1 <= choice <= len(build_choices):
            return choice
        else:
            raise ValueError()
    except ValueError:
        raise click.BadParameter(
            "Invalid choice. Please choose a valid build option")


def choose_rom():
    """Prompts the user to choose a rom from the available options."""
    click.echo("Select a rom")
    for section in rom_config.sections():
        rom_name = rom_config.get(section, "rom_name", fallback=None)
        if rom_name is not None:
            global rom_choices
            rom_choices.append(rom_name)
            global rom_sections
            rom_sections.append(section)
            click.echo(f"{len(rom_choices)}. {rom_name}")
    while True:
        try:
            choice: int = click.prompt(
                "Enter the number of your choice", type=int, value_proc=validate_rom_choice)
            global selected_rom
            selected_rom = rom_choices[choice - 1]
            click.echo(f"You have selected {selected_rom}")
            break
        except click.Abort:
            click.echo("Operation aborted. Exiting.")
            break


def choose_telegram():
    """Prompts the user to choose a telegram config from the available options."""
    click.echo("Select a telegram config")
    for section in telegram_config.sections():
        telegram_name = telegram_config.get(section, "name", fallback=None)
        if telegram_name is not None:
            global telegram_choices
            telegram_choices.append(telegram_name)
            global telegram_sections
            telegram_sections.append(section)
            click.echo(f"{len(telegram_choices)}. {telegram_name}")
    while True:
        try:
            choice: int = click.prompt(
                "Enter the number of your choice", type=int, value_proc=validate_telegram_choice)
            global selected_telegram
            selected_telegram = telegram_choices[choice - 1]
            click.echo(f"You have selected {selected_telegram}")
            break
        except click.Abort:
            click.echo("Operation aborted. Exiting.")
            break


def load_config():
    """Loads the config from the selected rom and telegram config."""
    global telegram_token
    telegram_token = telegram_config.get(
        selected_telegram, "token")
    global telegram_chat_ids
    telegram_chat_ids = [telegram_config.get(
        selected_telegram, "chat_ids")]
    global telegram_user_name
    telegram_user_name = telegram_config.get(
        selected_telegram, "username")  # type: ignore
    global bot
    bot = TelegramMessenger(token=telegram_token, chat_ids=telegram_chat_ids)
    global repo_sync_command
    repo_sync_command = rom_config.get(selected_rom, "repo_sync_command")
    global lunch_name
    lunch_name = rom_config.get(selected_rom, "lunch_name")
    global device_codename
    device_codename = rom_config.get(selected_rom, "device_codename")
    global rom_path
    rom_path = rom_config.get(selected_rom, "rom_path")
    global manifest_url
    manifest_url = rom_config.get(selected_rom, "manifest_url")
    global manifest_branch
    manifest_branch = rom_config.get(selected_rom, "manifest_branch")
    global local_manifest_url
    local_manifest_url = rom_config.get(selected_rom, "local_manifest_url")
    global local_manifest_branch
    local_manifest_branch = rom_config.get(
        selected_rom, "local_manifest_branch")
    global build_variant
    build_variant = rom_config.get(selected_rom, "build_variant")
    global build_command
    build_command = rom_config.get(selected_rom, "build_command")
    global upload_command
    upload_command = rom_config.get(selected_rom, "upload_command")
    global download_url
    download_url = rom_config.get(selected_rom, "download_url")


def initialize() -> bool:
    bot.send_message(
        f"👷‍♂️🏗️ @{telegram_user_name} is preparing to build: {selected_rom} for {device_codename}")
    if os.path.exists(rom_path):
        click.echo("ROM directory exists")
        os.chdir(rom_path)
        if os.path.exists(rom_path + "/.repo"):
            click.echo("Repo directory exists")
            return True
        else:
            click.echo("Repo directory does not exist. Initializing it")
            if initialize_repo():
                return True
            else:
                return False
    else:
        click.echo("ROM directory does not exist. Creating it")
        os.makedirs(rom_path)
        return True


def initialize_local_manifests() -> bool:
    message = "Initializing the local manifests"
    click.echo(message)
    bot.send_message(f"{message} 〰️")
    if os.path.exists(rom_path + "/.repo/local_manifests"):
        click.echo("Local manifest directory exists")
        return True
    else:
        click.echo("Local manifest directory does not exist. Cloning the repo")
        if clone_local_manifest():
            message = "Local manifests cloned successfully"
            click.echo(message)
            bot.send_message(f"{message} 〰️🏛️")
            return True
        else:
            return False


def initialize_repo() -> bool:
    message = "Initializing the repo"
    click.echo(message)
    bot.send_message(f"{message} 🚔🏎️")
    os.chdir(rom_path)
    try:
        repo_init_command = f"repo init -u {manifest_url} -b {manifest_branch} --git-lfs -g default,-mips,-darwin,-notdefault"
        result = subprocess.run(
            f"bash -c '{repo_init_command}'", check=True, text=True, shell=True)
        click.echo(result.stdout)
        message = f"Repo initialized successfully"
        click.echo(message)
        bot.send_message(f"{message} 😂🥂🥂")
        return True
    except Exception as e:
        click.echo(
            f"Error in initializing the repo. Please initialize it manually: {e}")
        bot.send_message("Error in initializing the repo 💥💥🤯")
        return False


def clone_local_manifest() -> bool:
    os.chdir(rom_path)
    try:
        clone_local_manifest_command = f"git clone {local_manifest_url} -b {local_manifest_branch} {rom_path}/.repo/local_manifests"
        result = subprocess.run(
            f"bash -c '{clone_local_manifest_command}'", check=True, text=True, shell=True)
        click.echo(result.stdout)
        click.echo(f"Local manifest cloned successfully")
        return True
    except Exception as e:
        click.echo(
            f"Error in cloning the local manifest. Please clone it manually: {e}")
        bot.send_message("Error in cloning the local manifest 💥💥🤯🤯")
        return False


def sync_sources() -> bool:
    message = "Synchronizing the sources"
    click.echo(message)
    bot.send_message(f"{message} 🙋🚄🚅🚅")
    os.chdir(rom_path)
    try:
        result = subprocess.run(
            f"bash -c '{repo_sync_command}'", check=True, text=True, shell=True)
        click.echo(result.stdout)
        message = f"Synchronization completed successfully"
        click.echo(message)
        bot.send_message(f"{message} 🥂🥂🍸")
        return True
    except Exception as e:
        click.echo(
            f"Error in syncing the sources. Please sync the sources manually: {e}")
        return False


def prompt_sync_sources() -> bool:
    global sync_choices
    sync_choices.append("1. Yes")
    sync_choices.append("2. No")
    sync_choices.append("3. Sync then build")
    click.echo("Do you want to sync the sources?")
    for sync_choice in sync_choices:
        click.echo(f"{sync_choice}")
    while True:
        try:
            choice: int = click.prompt(
                "Enter the number of your choice", type=int, value_proc=validate_sync_choice)
            click.echo(f"You have selected {sync_choices[choice - 1 ]}")
            if choice == 1:
                result = sync_sources()
                if not result:
                    return False
                return result
            elif choice == 2:
                click.echo("Skipping the sync")
                return True
            elif choice == 3:
                global sync_then_build
                click.echo("Sources will be synced right before the build")
                sync_then_build = True
                return sync_then_build
            else:
                return False
        except click.Abort:
            click.echo("Operation aborted. Exiting.")
            return False
            break


def envsetup_lunch_build() -> bool:
    global build_choices
    build_choices.append("1. No")
    build_choices.append("2. Yes")
    message = "Proceeding with the build"
    click.echo(message)
    os.chdir(rom_path)
    envsetup_command: str = ". build/envsetup.sh"
    lunch_command: str = f"lunch {lunch_name}_{device_codename}-{build_variant}"
    consolidated_command: str = f"{envsetup_command} && {lunch_command} && {build_command}"
    click.echo("Do you want a clean build?")
    for build_choice in build_choices:
        click.echo(f"{build_choice}")
    while True:
        try:
            choice: int = click.prompt(
                "Enter the number of your choice", type=int, value_proc=validate_build_choice)
            click.echo(f"You have selected {build_choices[choice - 1]}")
            if choice == 1:
                consolidated_command: str = f"{envsetup_command} && {lunch_command} && {build_command}"
                message = "Proceeding with a dirty build"
                bot.send_message(f"{message} 🚄🪁💸")
            elif choice == 2:
                clean_command: str = "m clean -j$(nproc --all)"
                consolidated_command: str = f"{envsetup_command} && {clean_command} && {lunch_command} && {build_command}"
                message = "Proceeding with a clean build"
                bot.send_message(f"{message} 🪁💸🚄🚅🚅")
            try:
                if sync_then_build:
                    result = sync_sources()
                    if not result:
                        return False
                message = "Building the rom "
                click.echo(message)
                bot.send_message(f"{message} 🪁🛩️✈️🛫")
                result = subprocess.run(
                    f"bash -c '{consolidated_command}'", check=True, text=True, shell=True)
                message = "Build completed successfully"
                click.echo(message)
                bot.send_message(f"{message} 🏗️🏢🏦🏨✈️🛬🛬🛬")
                click.echo(result.stdout)
                upload_build()
                return True
            except Exception as e:
                click.echo(
                    f"Error in building the rom, please build it manually: {e}")
                bot.send_message(f"Error in building the rom {e} 🤯💥💥💣🤯")
                click.echo("Output:")
                click.echo(e)
                return False
        except click.Abort:
            click.echo("Operation aborted. Exiting.")
            return False
            break


def get_latest_file(extension: str = ".zip", directory: str = f"out/target/product/{device_codename}") -> str:
    # Create a list of all .zip files in the directory
    file_list = glob.glob(os.path.join(directory, f'*{extension}'))
    # Sort the list of files by modification time
    sorted_files = sorted(file_list, key=os.path.getmtime)
    if sorted_files:
        # Get the latest file
        latest_file = sorted_files[-1]
        click.echo(f"Latest {extension} file: {latest_file}")
        return latest_file
    else:
        click.echo(f"No {extension} files found in the directory.")
        return "None"


def upload_build():
    os.chdir(rom_path)
    global upload_command
    latest_build = get_latest_file(
        extension=".zip", directory=f"out/target/product/{device_codename}")
    if latest_build != "None":
        click.echo("Uploading the build")
        bot.send_message("Uploading the build 🏦")
        if "{uploadfile}" in upload_command:
            upload_command = upload_command.replace(
                "{uploadfile}", f"{latest_build}")
        try:
            result = subprocess.run(
                f"bash -c '{upload_command}'", check=True, text=True, shell=True)
            click.echo(result.stdout)
            global download_url
            if "{filename}" in download_url:
                download_url = download_url.replace(
                    "{filename}", f"{latest_build}")
            message = f"Build uploaded successfully! Download it from [Here]({download_url})"
            click.echo(message)
            bot.send_message(f"{message} 🍷🍷🥂🥂🍾🍾")
        except Exception as e:
            click.echo(
                f"Error in uploading the build, please upload it manually: {e}")
            bot.send_message(f"Error in uploading the build {e}")
            click.echo("Output:")
            click.echo(e)


if __name__ == "__main__":
    main()
