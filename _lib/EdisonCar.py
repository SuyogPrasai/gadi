from _lib.car import CarController
from _lib.data_packet import construct_data_packet
import time
import serial

# Constants for serial communication
SERIAL_PORT: str = "COM11"  # Replace with your Arduino's serial port (e.g., "COM3" on Windows, "/dev/ttyUSB0" on Linux)
BAUD_RATE: int = 9600

class EdisonCar(CarController):
    """
    Extends CarController with additional movement styles and functionalities.
    """

    def move_straight(self) -> None:
        """Move the car straight forward."""
        self.turn_forward()
        self.move_forward()

    def move_left(self) -> None:
        """Turn the car left and move forward."""
        self.turn_left()
        self.move_forward()

    def move_right(self) -> None:
        """Turn the car right and move forward."""
        self.turn_right()
        self.move_forward()

    def perform_acceleration(self) -> None:
        """Initiate the car's acceleration."""
        self.accelerate()

    def perform_deceleration(self) -> None:
        """Initiate the car's deceleration."""
        self.decelerate()

    def apply_brakes(self) -> None:
        """Stop the car using brakes."""
        self.stop()

    def perform_drift(self) -> None:
        """Execute a drift maneuver."""
        self.drift()

    def car_status(self) -> str:
        """Retrieve the current status of the car."""
        return f"Speed: {self.current_speed}, Direction: {self.current_direction}"

    def start(self) -> None:
        """
        Monitor the car's direction and speed status and send data packets.
        """
        try:
            with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
                print(f"Serial connection established on {SERIAL_PORT} at {BAUD_RATE} baud.")
                while True:
                    status = self.car_status()
                    print(status)
                    data_packet = construct_data_packet(self.current_direction, self.current_speed)
                    print(f"Data Packet: {data_packet}")
                    ser.write(data_packet.encode())
                    time.sleep(0.1)
        except serial.SerialException as e:
            print(f"Failed to connect to Transmitter at {SERIAL_PORT}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")