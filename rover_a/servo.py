#!/usr/bin/env python
"""Servo Class for PWM driver"""

import logging
import time

logging.getLogger(__name__)


def scale(value, input_low, input_high, output_low, output_high):
    """Scale a value from one range to another"""
    scaled_input = ((float(value) - input_low) / (input_high - input_low))
    return ((scaled_input) * (output_high - output_low)) + output_low


class Servo:
    """Servo Class for PWM driver

    creates a servo object for a pin on a Adafruit_PCA9685 object"""

    def __init__(self, pwm, pwm_index=0, pulse_min=150, pulse_max=600, degrees_min=0,
                 degrees_max=180):
        self.pwm = pwm
        self.pwm_index = pwm_index
        self.pulse_min = pulse_min
        self.pulse_max = pulse_max
        self.degrees_min = degrees_min
        self.degrees_max = degrees_max

        self.current_position = None
        self.set_position((degrees_max - degrees_min) / 2)

    def move(self, position, sleep=0.010):
        """Move servo to location using a smooth motion"""
        if position > self.current_position:
            for angle in range(self.current_position, position):
                self.set_position(angle + 1)
                time.sleep(sleep)
        else:
            for angle in reversed(range(position, self.current_position)):
                self.set_position(angle)
                time.sleep(sleep)

    def set_position(self, position):
        """Writes position value to Adafruit_PCA9685"""
        if position < self.degrees_min:
            position = self.degrees_min
        elif position > self.degrees_max:
            position = self.degrees_max

        big_x = int(scale(position, self.degrees_min, self.degrees_max, self.pulse_min,
                          self.pulse_max))

        logging.debug("Moving servo %d to position %d [%d]", self.pwm_index, position, big_x)
        self.pwm.set_pwm(self.pwm_index, 0, big_x)
        self.current_position = position
