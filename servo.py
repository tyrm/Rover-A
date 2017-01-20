#!/usr/bin/env python

import logging
import time

logging.getLogger(__name__)


class Servo:
    def __init__(self, pwm, pwm_index=0, pulse_min=150, pulse_max=600, degrees=180):
        self.pwm = pwm
        self.pwm_index = pwm_index
        self.pulse_min = pulse_min
        self.pulse_max = pulse_max
        self.degrees = degrees

        self.current_position = None
        self.set_position(degrees / 2)

    def move(self, position, sleep=0.010):
        if position > self.current_position:
            for x in range(self.current_position, position):
                self.set_position(x + 1)
                time.sleep(sleep)
        else:
            for x in reversed(range(position, self.current_position)):
                self.set_position(x + 1)
                time.sleep(sleep)

    def set_position(self, position):
        if position < 0:
            position = 0
        elif position > self.degrees:
            position = self.degrees

        big_x = int(self.scale(position, 0, self.degrees, self.pulse_min, self.pulse_max))

        logging.debug("Moving servo {0} to position {1} [{2}]".format(self.pwm_index, position, big_x))
        self.pwm.set_pwm(self.pwm_index, 0, big_x)
        self.current_position = position

    def scale(self, value, input_low, input_high, output_low, output_high):
        return (((float(value) - input_low) / (input_high - input_low)) * (output_high - output_low)) + output_low
