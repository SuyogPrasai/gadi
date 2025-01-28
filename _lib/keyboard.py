from pynput import keyboard

# State variables
keys_pressed = set()  # Set to track pressed keys
modifiers_pressed = set()  # Separate set to track modifier keys

def display_keys_pressed():
    """Display all keys currently pressed."""
    if keys_pressed or modifiers_pressed:  # Check if any keys are pressed
        pressed_keys = [str(key) if not isinstance(key, str) else key for key in keys_pressed]
        pressed_modifiers = [str(mod) for mod in modifiers_pressed]
        all_keys = pressed_modifiers + pressed_keys  # Combine normal and modifier keys
        print(f"Keys pressed: {', '.join(all_keys)}")

def on_press(key: keyboard.Key) -> None:
    """Handle key press events."""
    try:
        # Normal keys (e.g., 'w', 'a', 'd')
        if hasattr(key, 'char') and key.char in {'w', 'a', 'd'}:
            keys_pressed.add(key.char)
        # Modifier keys (e.g., Ctrl)
        elif key in {keyboard.Key.ctrl_l, keyboard.Key.ctrl_r}:
            modifiers_pressed.add(key)
        display_keys_pressed()  # Show currently pressed keys
    except Exception as e:
        print(f"Error handling key press: {e}")

def on_release(key: keyboard.Key) -> bool:
    """Handle key release events."""
    try:
        # Remove released keys
        if hasattr(key, 'char') and key.char in {'w', 'a', 'd'}:
            keys_pressed.discard(key.char)
        elif key in {keyboard.Key.ctrl_l, keyboard.Key.ctrl_r}:
            modifiers_pressed.discard(key)
        display_keys_pressed()  # Update currently pressed keys
    except Exception as e:
        print(f"Error handling key release: {e}")
    return True  # Continue listening