from termcolor import cprint
from evdev import InputDevice
from evdev import ecodes
import evdev
import time
import questionary
from typing import List,Callable

class KeyboardSelector:
    
    
    @staticmethod
    def selectKeyboard(device):
        if device is None:
            selected_keyboard = KeyboardSelector.selectKeyboardUsingUI()
        else:
            selected_keyboard = InputDevice('/dev/input/by-id/' + device)
            cprint("Selected keyboard: " + device, color='green', attrs=['bold'])             
        return selected_keyboard

    @staticmethod
    def selectKeyboardUsingUI():
        cprint("Searching for input devices...", color='yellow', attrs=['bold'])
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        choices = [{'name': device.name, 'value': device} for device in devices]
        result = questionary.select('Select your secondary keyboard (currently only supports one keyboard per instance of the script):', choices=choices).ask()
        return result


class ModifierKeyIdentifier(object):
    """
    Base class for handling keyboards
    """
    @staticmethod
    def isMetaKey(pressed_keys):
        return (pressed_keys.__contains__(ecodes.KEY_LEFTMETA)
                or pressed_keys.__contains__(ecodes.KEY_RIGHTMETA))

    @staticmethod
    def isControlKey(pressed_keys):
        return (pressed_keys.__contains__(ecodes.KEY_LEFTCTRL)
                or pressed_keys.__contains__(ecodes.KEY_RIGHTCTRL))

    @staticmethod
    def isAltKey(pressed_keys):
        return (pressed_keys.__contains__(ecodes.KEY_LEFTALT)
                or pressed_keys.__contains__(ecodes.KEY_RIGHTALT))

    @staticmethod
    def isShiftKey(pressed_keys):
        return (pressed_keys.__contains__(ecodes.KEY_LEFTSHIFT)
                or pressed_keys.__contains__(ecodes.KEY_RIGHTSHIFT))




class KeyboardListener(object):
    """
    Makes the ev-dev handler for keyboard, much simpler
    """     
    
    @staticmethod
    def getCompleteControl(device):
        # gains complete control of keyboard, all keys are locked to this script
        device.grab()

    @staticmethod
    def startKeyEventListenerLoop(device: evdev.InputDevice, user_callback: Callable[[List[int], evdev.InputDevice], None], *args, **kwargs) -> None:
        """
        Uses evdev's readloop to get keyboard events.

        Args:
            device (evdev.InputDevice): The input device to listen to.
            user_callback (Callable): The function to call when a key event is detected.
                The function should accept device as the first argument,
                followed by any additional arguments passed to this function.
            *args: Additional positional arguments to pass to the user_callback function.
            **kwargs: Additional keyword arguments to pass to the user_callback function.

        Returns:
            None

        Raises:
            None

        Example:
            def my_callback(device: evdev.InputDevice) -> None:
                pressed_keys = device.active_keys()
                print(pressed_keys)

            device = evdev.InputDevice('/dev/input/event0')
            startKeyEventListenerLoop(device, my_callback)

        """
        # blink the leds twice to indicate that the listener loop is running
        KeyboardLeds.serially_blink_keyboard_leds(device)
        KeyboardLeds.serially_blink_keyboard_leds(device)

        for event in device.read_loop():
            if event.type == ecodes.EV_KEY:
                if device.active_keys() != []:
                    user_callback( device, *args, **kwargs)




class KeyboardLeds(object):
    """
    Manages all led functions of the keyboard
    """    

    @staticmethod
    def blink_all_keyboard_leds( device):
        KeyboardLeds.setKeyboardLEDPattern(device, 0, 0, 0)
        time.sleep(0.01)
        KeyboardLeds.setKeyboardLEDPattern(device, 1, 1, 1)
        time.sleep(0.01)
        KeyboardLeds.setKeyboardLEDPattern(device, 0, 0, 0)

    @staticmethod
    def serially_blink_keyboard_leds(device):
        KeyboardLeds.setKeyboardLEDPattern(device, 0, 0, 0)
        time.sleep(0.07)
        KeyboardLeds.setKeyboardLEDPattern(device, 1, 0, 0)
        time.sleep(0.07)
        KeyboardLeds.setKeyboardLEDPattern(device, 0, 1, 0)
        time.sleep(0.07)
        KeyboardLeds.setKeyboardLEDPattern(device, 0, 0, 1)
        time.sleep(0.07)
        KeyboardLeds.setKeyboardLEDPattern(device, 0, 0, 0)

    @staticmethod
    def setKeyboardLEDPattern(device, num_led, caps_led, scroll_led):
        device.set_led(ecodes.LED_NUML, num_led)
        device.set_led(ecodes.LED_CAPSL, caps_led)
        device.set_led(ecodes.LED_SCROLLL, scroll_led)