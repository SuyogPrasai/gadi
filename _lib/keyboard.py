from pynput import keyboard
from threading import Lock
from _lib.data_parser import process_data_packets

# State dictionary to track each key's state
key_states = {
    'w': False,
    'a': False,
    'd': False,
    'ctrl_l': False,
    'ctrl_r': False,
    # Add more keys as needed
}

# Thread-safe lock for managing key_states
state_lock = Lock()

def display_keys_pressed():
    """Display all keys currently pressed."""
    with state_lock:
        pressed_keys = [key for key, pressed in key_states.items() if pressed]
    if pressed_keys:

        process_data_packets(pressed_keys)
    else:
        print("No keys pressed.")

def on_press(key):
    """Handle key press events."""
    try:
        with state_lock:
            # Handle alphanumeric keys and combinations
            if hasattr(key, 'char') and key.char:
                char = key.char.lower()  # Normalize to lowercase
                if char in key_states:
                    key_states[char] = True
                # Special cases for Ctrl combinations
                if char == '\x17':  # Ctrl+W
                    key_states['w'] = True
                    key_states['ctrl_l'] = True
                elif char == '\x04':  # Ctrl+D
                    key_states['d'] = True
                    key_states['ctrl_l'] = True
                elif char == '\x01':  # Ctrl+A
                    key_states['a'] = True
                    key_states['ctrl_l'] = True
            # Handle special keys
            elif key == keyboard.Key.ctrl_l:
                key_states['ctrl_l'] = True
            elif key == keyboard.Key.ctrl_r:
                key_states['ctrl_r'] = True

        display_keys_pressed()
    except Exception as e:
        print(f"Error handling key press: {e}")

def on_release(key):
    """Handle key release events."""
    try:
        with state_lock:
            # Handle alphanumeric keys and combinations
            if hasattr(key, 'char') and key.char:
                char = key.char.lower()  # Normalize to lowercase
                if char in key_states:
                    key_states[char] = False
                # Special cases for Ctrl combinations
                if char == '\x17':  # Ctrl+W
                    key_states['w'] = False
                    key_states['ctrl_l'] = False
                elif char == '\x04':  # Ctrl+D
                    key_states['d'] = False
                    key_states['ctrl_l'] = False
                elif char == '\x01':  # Ctrl+A
                    key_states['a'] = False
                    key_states['ctrl_l'] = False
            # Handle special keys
            elif key == keyboard.Key.ctrl_l:
                key_states['ctrl_l'] = False
            elif key == keyboard.Key.ctrl_r:
                key_states['ctrl_r'] = False

        display_keys_pressed()
    except Exception as e:
        print(f"Error handling key relb   ease: {e}")

    return True  # Continue listening