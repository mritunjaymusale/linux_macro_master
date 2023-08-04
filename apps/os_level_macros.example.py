from evdev import ecodes,InputDevice
import utils

# ! just for demo purposes only need to find a way to make this work with supportedApps dict
def OSLevelKeybinds(device:InputDevice):
    pressed_keys = device.active_keys()
    macros = {
    frozenset([ecodes.KEY_PAUSE]): lambda: utils.runKeySequence([ecodes.KEY_MICMUTE]),
    }
    conditions = [any(frozenset(pressed_keys) == keys for keys in macros),]
    if  all(conditions):
        macros[frozenset(pressed_keys)]()

