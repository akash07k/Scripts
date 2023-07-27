import click
import configparser
import os


def main():
    click.echo("Welcome to android rom configuration initializer")
    click.echo("Written by Akash Kakkar")
    add_config()


config = configparser.ConfigParser()
CONFIG_DIR = "configs"
CONFIG_FILE = f"{CONFIG_DIR}/rom.ini"


def write_configuration() -> bool:
    # Check if "configs" directory exists, and create it if it doesn't
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    # Write the entire configuration to the file
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)
    click.echo("Configuration written to the file successfully")
    return True


def is_section_duplicate(section_name: str) -> bool:
    """Check if the section already exists in the configuration file."""
    config.read(CONFIG_FILE)
    return section_name in config.sections()


@click.command()
@click.option("--rom-name", prompt="Enter the name of the rom",
              help="Name of the rom", default="crDroid")
@click.option("--repo-sync-command", prompt="Enter the command to sync the repo",
              help="Command to sync the repo", default="repo sync -c -j$(nproc --all) --force-sync --no-clone-bundle --no-tags --prune --current-branch --optimized-fetch")
@click.option("--lunch-name", prompt="Enter the lunch name",
              help="Lunch name", default="lineage")
@click.option("--rom-path", prompt="Enter the path of the rom",
              help="Path of the rom", default="/mnt/wsl/rom/cr")
@click.option("--device-codename", prompt="Enter the codename of the device",
              help="Codename of the device", default="munch")
@click.option("--build-variant", prompt="Enter the build variant",
              help="Build variant", default="userdebug")
@click.option("--build-command", prompt="Enter the build command",
              help="Build command", default="m bacon")
@click.option("--manifest-url", prompt="Enter the manifest url",
              help="Manifest url", default="https://github.com/crdroidandroid/android.git")
@click.option("--manifest-branch", prompt="Enter the manifest branch",
              help="Manifest branch", default="13.0")
@click.option("--local-manifest-url", prompt="Enter the local manifest url",
              help="Local manifest url", default="https://github.com/akash07k/local_manifests.git")
@click.option("--local-manifest-branch", prompt="Enter the local manifest branch",
              help="Local manifest branch", default="lineage")
@click.option("--upload-command", prompt="Enter the upload command",
              help="Upload command", default="curl --ssl -k -T {uploadfile} ftp://uploadme.example.com/files/munch/9.x/ --user username:password")
@click.option("--download-url", prompt="Enter the download URL",
              help="Download URL", default="https://sourceforge.net/projects/crdroid/files/munch/9.x/{filename}/download")
def add_config(rom_name: str, repo_sync_command: str, lunch_name: str, rom_path: str, device_codename: str, build_variant: str, build_command: str, manifest_url: str, manifest_branch: str, local_manifest_url: str, local_manifest_branch: str, upload_command: str, download_url: str) -> bool:
    """Add a configuration to the configuration file."""
    if is_section_duplicate(f"{rom_name}_Rom"):
        click.echo(
            f"Configuration section '{name}_Rom' already exists. Please choose a different name.")
        return False

    # Read the existing configurations
    config.read(CONFIG_FILE)

    # Add the new configuration
    config[f"{rom_name}_Rom"] = {
        "rom_name": rom_name,
        "repo_sync_command": repo_sync_command,
        "lunch_name": lunch_name,
        "rom_path": rom_path,
        "device_codename": device_codename,
        "build_variant": build_variant,
        "build_command": build_command,
        "manifest_url": manifest_url,
        "manifest_branch": manifest_branch,
        "local_manifest_url": local_manifest_url,
        "local_manifest_branch": local_manifest_branch,
        "upload_command": upload_command,
        "download_url": download_url,
    }

    # Write the updated configuration to the file
    write_configuration()
    add_another = click.confirm(
        "Do you want to add another config?", default=False)
    if add_another:
        add_config()
    else:
        click.echo("Bye bye!")
    return True


if __name__ == "__main__":
    main()
