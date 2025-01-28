from typing import List
import time


class CarController:
    """
    A class to manage car operations such as movement, speed control, and direction handling.
    """
    def __init__(self):
        """Initialize the car's state, speed, and direction."""
        self.control_states = {
            'turn_left': False,
            'turn_right': False,
            'move_forward': False,
            'accelerating': False,
            'decelerating': False
        }
        self.current_speed = 0  # Current speed of the car
        self.current_direction = 90  # Default direction (90 degrees = forward)

        self.MIN_SPEED = 10
        self.MAX_SPEED = 150
        self.ACCELERATION_INCREMENT = 5
        self.ACCELERATION_DELAY = 0.1
        self.DECELERATION_DELAY = 0.1
        self.DECELERATION_INCREMENT = 5

    def _get_state(self, key: str) -> bool:
        """Retrieve the current state of a specific control."""
        return self.control_states.get(key, False)

    def _reset_states(self) -> None:
        """Reset all control states to False."""
        for key in self.control_states:
            self.control_states[key] = False

    def _set_direction(self, direction: int, direction_name: str) -> None:
        """Set the car's direction and update control states."""
        self.control_states['turn_left'] = direction < 90
        self.control_states['turn_right'] = direction > 90
        self.current_direction = direction
        # print(f"Turned {direction_name}")
    
    def _is_halt(self) -> bool:
        """Check if the car is in a halted state."""
        for state in self.control_states.values():
            if state:
                return False
        return True

    def turn_left(self) -> None:
        """Turn the car left."""
        self._set_direction(65, "Left")

    def turn_right(self) -> None:
        """Turn the car right."""
        self._set_direction(115, "Right")

    def turn_forward(self) -> None:
        """Align the car forward."""
        self._set_direction(90, "Forward")

    def move_forward(self) -> None:
        """Move the car forward at the minimum speed."""
        self.control_states['move_forward'] = True
        self.current_speed = self.MIN_SPEED

    def stop(self) -> None:
        """Stop the car and reset all control states."""
        self._reset_states()
        self.current_speed = 0

    def accelerate(self) -> None:
        """Increase the car's speed incrementally until it reaches the maximum speed."""
        self.control_states.update({'move_forward': True, 'accelerating': True, 'decelerating': False})
        print(f"Accelerating at {self.ACCELERATION_INCREMENT} units every {self.ACCELERATION_DELAY} seconds")

        while self.control_states['accelerating'] and self.current_speed < self.MAX_SPEED:
            self.current_speed = min(self.current_speed + self.ACCELERATION_INCREMENT, self.MAX_SPEED)
            print(f"Current Speed: {self.current_speed}")
            time.sleep(self.ACCELERATION_DELAY)

    def decelerate(self) -> None:
        """Decrease the car's speed incrementally until it reaches the minimum speed."""
        self.control_states.update({'move_forward': True, 'accelerating': False, 'decelerating': True})
        print(f"Decelerating at {self.DECELERATION_INCREMENT} units every {self.DECELERATION_DELAY} seconds")

        while self.control_states['decelerating'] and self.current_speed > self.MIN_SPEED:
            self.current_speed = max(self.current_speed - self.DECELERATION_INCREMENT, self.MIN_SPEED)
            print(f"Current Speed: {self.current_speed}")
            time.sleep(self.DECELERATION_DELAY)

    def drift(self) -> None:
        """Enable a drift mode for the car."""
        self._reset_states()
        print("Drifting...")
        time.sleep(1)
        print("Drift Completed")

