from evdev import ecodes,InputDevice
import utils


def Brave(device:InputDevice,) -> None:
    pressed_keys = device.active_keys()
    macros = {
    frozenset([ecodes.KEY_G]): lambda: openWebsiteInNewTab("https://www.google.com"),
    frozenset([ecodes.KEY_LEFTCTRL, ecodes.KEY_LEFTALT, ecodes.KEY_Y]): lambda: openWebsiteInNewTab("https://www.youtube.com")
    }
    conditions = [any(frozenset(pressed_keys) == keys for keys in macros),
                  utils.getActiveWindowName()=="Brave"]

    def openWebsiteInNewTab(link: str) -> None:
        utils.runKeySequence([ecodes.KEY_LEFTCTRL, ecodes.KEY_T])
        utils.ydotool.type(link)
        utils.runKeySequence([ecodes.KEY_ENTER])

    # if all conditions are true then execute the macro
    if  all(conditions):
        macros[frozenset(pressed_keys)]()