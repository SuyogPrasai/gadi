from _lib.EdisonCar import EdisonCar
from pynput import keyboard
from threading import Lock
import os
import time

car = EdisonCar()

car.start()

key_states = {
    'w': False,
    'a': False,
    'd': False,
    'ctrl_l': False,
    'ctrl_r': False,
}

state_lock = Lock()

def on_press(key):
    """Handle key press events."""
    try:
        with state_lock:
            # Handle alphanumeric keys and combinations
            if hasattr(key, 'char') and key.char:
                char = key.char.lower()  # Normalize to lowercase
                if char == '\x03':
                    print("Exiting...")
                    os._exit(0)
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

    except Exception as e:
        print(f"Error handling key release: {e}")
    
    return True  # Continue listening

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    while True:

        if not car._is_halt():
            print(key_states)

        if key_states['w']:
            if key_states['ctrl_l']:
                car.control_states['decelerating'] = False
                car.control_states['accelerating'] = True
                car.current_speed += car.ACCELERATION_INCREMENT
                print(car.current_speed)
            if (not key_states['ctrl_l']) and car.current_speed > car.MIN_SPEED:
                
                car.control_states['decelerating'] = True
                car.control_states['accelerating'] = False
             
                car.current_speed -= car.DECELERATION_INCREMENT
                print(car.current_speed)
            if not key_states['ctrl_l'] and car.control_states['accelerating'] is False and car.control_states['decelerating'] is False:    
                car.move_straight()
        if not key_states['w']:
            car.apply_brakes()
        if key_states['a'] and key_states['d']:
            car.move_forward()
        if key_states['a']:
            car.turn_left()
        if key_states['d']:
            car.turn_right()
        time.sleep(0.2)
        
        