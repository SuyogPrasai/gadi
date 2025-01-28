from pynput import keyboard

# State dictionary to track each key's state
key_states = {
    'w': False,
    'a': False,
    'd': False,
    'ctrl_l': False,
    'ctrl_r': False,
    # Add more keys as needed
}

def display_keys_pressed():
    """Display all keys currently pressed."""
    pressed_keys = [key for key, pressed in key_states.items() if pressed]
    if pressed_keys:
        print(f"Keys pressed: {', '.join(pressed_keys)}")

def on_press(key):
    """Handle key press events."""
    try:
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

        display_keys_pressed()  # Show currently pressed keys
    except Exception as e:
        print(f"Error handling key press: {e}")

def on_release(key):
    """Handle key release events."""
    try:
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

        display_keys_pressed()  # Update currently pressed keys
    except Exception as e:
        print(f"Error handling key release: {e}")

    return True  # Continue listening

def main():
    """Start the keyboard listener."""
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()