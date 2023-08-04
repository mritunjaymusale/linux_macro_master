from keyboard import KeyboardSelector,KeyboardListener
import utils
from apps.macros_handler import rootMacrosHandler

cli_args = utils.getCLIArgs()

selected_keyboard = KeyboardSelector().selectKeyboard(cli_args.device)

KeyboardListener.getCompleteControl(selected_keyboard)
KeyboardListener.startKeyEventListenerLoop(selected_keyboard, rootMacrosHandler,cli_args)