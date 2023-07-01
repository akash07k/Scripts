import ctypes
import sys

print("---Android build environment launcher---")

def elevate():
    print("Checking if running with administrator priveleges...");
    if ctypes.windll.shell32.IsUserAnAdmin():
        # Already running with administrator privileges
        print("Already running with administrator priveleges...")
        return

    print("Not running with administrator priveleges...")
    # Re-launch cmd.exe with administrator privileges and pass the arguments
    print("Re-launching the command prompt with administrator priveleges and passing the arguments to it...")
    terminal_args = "new-tab --title \"AndroidBuildEnv\" cmd /k "
    command_args = 'wsl --shutdown && wsl --mount \\\\.\\PHYSICALDRIVE3 --partition 2 --name rom && wsl'
    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        "wt.exe",
         terminal_args + command_args,
        None,
        1
    )

# Call the elevate function to launch cmd.exe as elevated with arguments
elevate()
