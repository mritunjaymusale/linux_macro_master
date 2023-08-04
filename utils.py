import subprocess
from termcolor import cprint
import argparse
from ydotool import YdoTool
from evdev import ecodes
ydotool = YdoTool()

def runShellCommand(command:str):
    try:
    # Run the shell command
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
    # Handle the error
        cprint(f"Error: {e.returncode}",'red',attrs=['bold'])
        cprint(f"\nOutput: {e.output.decode()}",'yellow',attrs=['bold'])
    else:
    # Process the output as string
        return output.decode('utf-8')


def getCLIArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--device',
        help='the name of device based on /dev/input/by-id/',
        default=None)
    parser.add_argument(
        '--debug',
        help='shows current keypresses on selected keyboard in the terminal',
        action='store_true'
        )
    args = parser.parse_args()
    return args

def getActiveWindowName():
    # ! works only in gnome check readme file
    raw_string = runShellCommand("gdbus call --session --dest org.gnome.Shell --object-path /org/gnome/Shell/Extensions/WindowsExt --method org.gnome.Shell.Extensions.WindowsExt.FocusTitle")
    
    # Extract text after "-" and before "',)"
    only_window_name = raw_string.split("- ")[-1].split("',)")[0]

    return only_window_name

def runKeySequence(ev_keyList:list):
    '''
    simulates a key press and release; 1 means key press, 0 means key release
    '''
    ydotoolKeySequence = []

    # iterate in forward direction
    for key in ev_keyList:
        ydotoolKeySequence.append(f"{key}:1")

    # iterate in reverse direction
    for key in reversed(ev_keyList):
        ydotoolKeySequence.append(f"{key}:0")

    
    ydotool.key(*ydotoolKeySequence)
    ydotool.exec()
    ydotool.reset()

def printCurrentlyPressedKeys(device):
    pressed_keys = device.active_keys()
    cprint(f"Current window in focus: "+getActiveWindowName(),color='magenta',attrs=['bold'],)
    cprint(f"Device: {device}",color='green',attrs=['bold'],)
    cprint(f"Pressed key : "+''.join(
            map(str, list(map(ecodes.keys.get, pressed_keys)))), color='yellow', attrs=['bold'])
