from pynput import keyboard
import serial
from threading import Lock
import os
from typing import List

# Constants for packet communication
PACKET_START_BYTE: int = 0x02  # Identifies the start of the data packet
sequence_number: int = 0       # Packet sequence number (increments with each packet)
speed: int = 0                # Current speed value
direction: int = 0            # Current direction value
ACCELERATION_STEP: int = 5    # Increment step for speed
DECELERATION_STEP: int = 5    # Decrement step for speed

# Initialize serial communication
SERIAL_PORT: str = "COM11"  # Replace with your Arduino's serial port (e.g., "COM3" on Windows, "/dev/ttyUSB0" on Linux)
BAUD_RATE: int = 9600

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Serial connection established on {SERIAL_PORT} at {BAUD_RATE} baud.")
except Exception as e:
    print(f"Failed to connect to {SERIAL_PORT}: {e}")
    ser = None

# State dictionary to track each key's state
key_states = {
    'w': False,
    'a': False,
    'd': False,
    'ctrl_l': False,
    'ctrl_r': False,
}

# Thread-safe lock for managing key_states
state_lock = Lock()

# Callback functions for keyboard events
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
        print(f"Error handling key release: {e}")
    
    return True  # Continue listening

def calculate_checksum(data: List[int]) -> int:
    """Calculate the checksum for a given data packet."""
    try:
        return sum(data) & 0xFF
    except Exception as e:
        print(f"Error calculating checksum: {e}")
        return 0

def construct_data_packet(current_direction: int, current_speed: int) -> bytes:
    """Construct a data packet using the given direction and speed."""
    global sequence_number
    try:
        sequence_number += 1
        data = [
            PACKET_START_BYTE,
            current_direction,
            current_speed,
            sequence_number % 256
        ]
        checksum = calculate_checksum(data)
        data.append(checksum)
        return bytes(data)
    except Exception as e:
        print(f"Error constructing data packet: {e}")
        return bytes()

def process_key_inputs(active_keys: List[str]) -> None:
    """Process the list of active keys and update the global speed and direction values."""
    global speed, direction

    try:
        if 'w' in active_keys:
            if 'ctrl_l' in active_keys:
                speed = min(speed + ACCELERATION_STEP, 255)  # Accelerate
            else:
                speed = max(speed - DECELERATION_STEP, 1)  # Decelerate
        else:
            speed = 0  # Reset speed if 'w' is not pressed

        if 'a' in active_keys:
            direction = 1  # Left
        elif 'd' in active_keys:
            direction = 2  # Right
        else:
            direction = 0  # Stationary
    except Exception as e:
        print(f"Error processing key inputs: {e}")

def process_data_packets(active_keys: List[str]) -> None:
    """Process the list of active keys and send data packets to the robot."""
    try:
        # Process key inputs to update speed and direction
        process_key_inputs(active_keys)
        
        # Construct a data packet using the current speed and direction
        data_packet = construct_data_packet(direction, speed)
        
        # Send the data packet to the robot
        if ser:
            ser.write(data_packet)  # Send data packet directly as bytes
        print(' '.join(f'{byte:02x}' for byte in data_packet))  # Print in hex
    except Exception as e:
        print(f"Error processing data packets: {e}")

# Start the keyboard listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
w