from typing import List

PACKET_START_BYTE = 0x02

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
