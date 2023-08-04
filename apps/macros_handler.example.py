from .brave import Brave
from .os_level_macros import OSLevelKeybinds
import utils
from evdev import ecodes

def rootMacrosHandler(device,cli_args):
    # TODO: need to find a way to make OSLevelKeybinds work with supportedApps dict so that the same logic 
    # TODO: can be reused instead of making a special condition for it

    supportedApps = {
        # do not put OSLevelKeybinds in supportedApps,since this uses  getWindowsName() which is not supported at OS level
        "Brave": Brave,
        
    }
    
    pressed_keys = device.active_keys()
    if cli_args.debug:
        utils.printCurrentlyPressedKeys(device)

    # Temp hack to make OSLevelKeybinds work by bypassing supportedApps dict
    elif pressed_keys.__contains__(ecodes.KEY_PAUSE) and pressed_keys.__len__() == 1:
        OSLevelKeybinds(device)
    else:
        supportedApps[utils.getActiveWindowName()](device)