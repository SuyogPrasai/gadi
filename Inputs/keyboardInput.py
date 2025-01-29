from _lib.EdisonCar import EdisonCar
from pynput import keyboard
from threading import Lock
import os
import time
import threading

def on_press(key):
    """Handle key press events."""
    try:
        with state_lock:
            if hasattr(key, 'char') and key.char:
                char = key.char.lower()
                if char == '\x03':  # Ctrl+C to exit
                    print("Exiting...")
                    os._exit(0)
                if char in key_states:
                    key_states[char] = True
                if char == '\x04':
                    key_states['d'] = True
                    key_states['ctrl_l'] = True
                if char == '\x01':
                    key_states['a'] = True
                    key_states['ctrl_l'] = True
                if char == '\x17':
                    key_states['w'] = True
                    key_states['ctrl_l'] = True
                
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
            if hasattr(key, 'char') and key.char:
                char = key.char.lower()
                if char in key_states:
                    key_states[char] = False
                if char == '\x04':
                    key_states['d'] = False
                    key_states['ctrl_l'] = False
                if char == '\x01':
                    key_states['a'] = False
                    key_states['ctrl_l'] = False
                if char == '\x17':
                    key_states['w'] = False
                    key_states['ctrl_l'] = False
            elif key == keyboard.Key.ctrl_l:
                key_states['ctrl_l'] = False
            elif key == keyboard.Key.ctrl_r:
                key_states['ctrl_r'] = False
    except Exception as e:
        print(f"Error handling key release: {e}")
    return True

if __name__ == "__main__":
    car = EdisonCar()

    # Run car.start() in a separate thread
    car_thread = threading.Thread(target=car.start, daemon=True)
    car_thread.start()

    # Initialize key states before starting the listener
    key_states = {
        'w': False,
        'a': False,
        'd': False,
        'ctrl_l': False,
        'ctrl_r': False,
    }
    state_lock = Lock()

    # Start the keyboard listener
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        if car._is_halt():  # Ensure _is_halt() is properly called
            print(car.car_status())  # Ensure car_status() is called

        while True:
            speed, direction = car.car_status()  # Ensure car_status() returns (speed, direction)
            print(f"{car.control_states} | [ speed = {speed}, direction = {direction} ]")
            
            if key_states['w']:
                if key_states['ctrl_l'] and car.current_speed < car.MAX_SPEED:
                    car.control_states['decelerating'] = False
                    car.control_states['accelerating'] = True
                    car.current_speed += car.ACCELERATION_INCREMENT
                elif car.current_speed > car.MIN_SPEED and (not key_states['ctrl_l']):
                    car.control_states['decelerating'] = True
                    car.control_states['accelerating'] = False
                    car.current_speed -= car.DECELERATION_INCREMENT
                else:
                    car.control_states['decelerating'] = False
                    car.move_forward()
            else:
                car.apply_brakes()

            if key_states['a'] and key_states['d']:
                car.turn_forward()
            elif not key_states['a'] and not key_states['d']:
                car.turn_forward()
            elif key_states['a']:
                car.turn_left()
            elif key_states['d']:
                car.turn_right()

            time.sleep(0.2)


        # # Start the listener in a separate process
        # mp_2 = multiprocessing.Process(target=Listener)
        # mp_2.start()

        # mp_1.join()
        # mp_2.join()
