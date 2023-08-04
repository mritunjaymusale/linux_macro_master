# linux_macro_master
# Macros

## Get permission for the needed device 
-  Give yourself permission of read+write of that device `sudo chmod a+r+w /dev/input/by-id/[my-device-name]`
- Add yourself to the `input` group `sudo usermod -a -G input [my-username]` 
- Based on [this](https://github.com/robinuniverse/Keebie/tree/1b5806a111b56e124aa36889a7133d5a285bee1f#keebie) guide

## Install OS level dependencies

`sudo dnf install python3-tkinter python3-devel python3-opencv xdotool speech-dispatcher-utils gnome-screenshot`

## Install python level dependencies

`pip3 install -r requirements.txt`

## Getting started
There are examples in the apps folder remove the examples word from the file name to use them.

## For wayland issue try these

- Screenshot work around for wayland through [Gnome screenshot](https://gitlab.com/irsn/snitch-ci#xwayland)

- This is optional but if needed it needs to be run after login  
`xhost +local:$USER`

- Install [ydotool](https://github.com/ReimuNotMoe/ydotool)

    - This one handles typing keyboard keys as a virtual input device
    - Incase you get `TypeError: 'function' object is not iterable` try my [merge request](https://gitlab.com/jdsieci/pyydotool/-/merge_requests/1)
    - Make it executable by current user as root
    `sudo chmod u+s /usr/bin/yodotool /bin/ydotoold`

- Install window calls extended extension for gnome
    - [Link](https://extensions.gnome.org/extension/4974/window-calls-extended/)
    - ```gdbus call --session --dest org.gnome.Shell --object-path /org/gnome/Shell/Extensions/WindowsExt --method org.gnome.Shell.Extensions.WindowsExt.FocusTitle```  
    - [Source](https://github.com/hseliger/window-calls-extended)
    - This extension is needed to get the name of the window that is currently in focus


## Why another tool for macros ?
Other tools usually do key to key or key to sequence or can only do automation using gui only. Most of these are stuck on XOrg which will be soon deprecated. 

Currently, this can do key-to-key and key-to-seq or seq-to-seq, the long term goal with this one is to do all the above and use something like pyautogui to do gui automation as well. Additionally, this can also be used to send completely custom commands based on the window in focus or just direct commands using shell or whatever is possible through python.
