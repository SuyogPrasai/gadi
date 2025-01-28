from typing import List

# Constants for packet communication
PACKET_START_BYTE: int = 0x02  # Identifies the start of the data packet
sequence_number: int = 0       # Packet sequence number (increments with each packet)
speed: int = 0                # Current speed value
direction: int = 0            # Current direction value
ACCELERATION_STEP: int = 5    # Increment step for speed
DECELERATION_STEP: int = 5    # Decrement step for speed


def calculate_checksum(data: List[int]) -> int:
    """
    Calculate the checksum for a given data packet.

    Args:
        data (List[int]): The list of data bytes.

    Returns:
        int: The checksum value (sum of all bytes modulo 256).
    """
    try:
        return sum(data) & 0xFF
    except Exception as e:
        print(f"Error calculating checksum: {e}")
        return 0


def construct_data_packet(current_direction: int, current_speed: int) -> bytes:
    """
    Construct a data packet using the given direction and speed.

    Args:
        current_direction (int): The direction value (e.g., 0 = stationary, 1 = left, 2 = right).
        current_speed (int): The speed value (0-255).

    Returns:
        bytes: The constructed data packet as a bytes object.
    """
    global sequence_number
    try:
        # Increment sequence number
        sequence_number += 1
        
        # Construct the data packet
        data = [
            PACKET_START_BYTE,
            current_direction,
            current_speed,
            sequence_number % 256
        ]
        
        # Add checksum to the packet
        checksum = calculate_checksum(data)
        data.append(checksum)
        
        return bytes(data)
    except Exception as e:
        print(f"Error constructing data packet: {e}")
        return bytes()


def process_key_inputs(active_keys: List[str]) -> None:
    """
    Process the list of active keys and update the global speed and direction values.

    Args:
        active_keys (List[str]): List of keys currently pressed (e.g., ['w', 'ctrl_l']).
    """
    global speed, direction

    try:
        # Handle forward movement ('w')
        if 'w' in active_keys:
            if 'ctrl_l' in active_keys:
                speed = min(speed + ACCELERATION_STEP, 255)  # Accelerate, cap at 255
            else:
                speed = max(speed - DECELERATION_STEP, 1)    # Decelerate, prevent negative speed
        else:
            speed = 0  # Reset speed if 'w' is not pressed

        # Handle direction changes ('a' = left, 'd' = right)
        if 'a' in active_keys:
            direction = 1  # Left
        elif 'd' in active_keys:
            direction = 2  # Right
        else:
            direction = 0  # Stationary/default
        return (speed, direction)
    except Exception as e:
        print(f"Error processing key inputs: {e}")
        return (0, 0)


def process_data_packets(active_keys: List[str]) -> None:
    """
    Process the list of active keys and send data packets to the robot.

    Args:
        active_keys (List[str]): List of keys currently pressed (e.g., ['w', 'ctrl_l']).
    """
    try:
        # Process key inputs to update speed and direction
        speed , direction = process_key_inputs(active_keys)
        
        # Construct a data packet using the current speed and direction
        data_packet = construct_data_packet(direction, speed)
        
        # Send the data packet to the robot
        # send_data_packet(data_packet)
        print(' '.join(f'{byte:02x}' for byte in data_packet))  # Print the data packet in hexadecimal format
    except Exception as e:
        print(f"Error processing data packets: {e}")
