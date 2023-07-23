import click
import configparser
import os


def main():
    click.echo("Welcome to telegram configuration initializer")
    click.echo("Written by Akash Kakkar")
    add_config()


config = configparser.ConfigParser()
CONFIG_DIR = "configs"
CONFIG_FILE = f"{CONFIG_DIR}/telegram.ini"


def write_configuration() -> bool:
    # Check if "configs" directory exists, and create it if it doesn't
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    # Write or append the configuration file
    with open(CONFIG_FILE, "a") as configfile:
        config.write(configfile)
    click.echo("Configuration file created/appended successfully")
    return True


def is_section_duplicate(section_name: str) -> bool:
    """Check if the section already exists in the configuration file."""
    config.read(CONFIG_FILE)
    return section_name in config.sections()


@click.command()
@click.option("--name", prompt="Enter your Telegram config name",
              help="Enter your Telegram config name", default="default")
@click.option("--token", prompt="Enter your Telegram bot token",
              help="Enter your Telegram bot token", default="123456789:abcdefghijklmnopqrstuvwxyz")
@click.option("--chatid", prompt="Enter your Telegram chat ID",
              help="Enter your Telegram chat ID", default="123456789")
@click.option("--username", prompt="Enter your Telegram username",
              help="Enter your Telegram username", default="akashk07")
def add_config(name: str, token: str, chatid: str, username: str) -> bool:
    """Add a new configuration to the configuration file"""
    if is_section_duplicate(f"{name}_Telegram"):
        click.echo(
            f"Configuration section '{name}_Telegram' already exists. Please choose a different name.")
        return False

    config[f"{name}_Telegram"] = {
        "name": name,
        "token": token,
        "chatid": chatid,
        "username": username
    }
    write_configuration()
    return True


if __name__ == "__main__":
    main()
