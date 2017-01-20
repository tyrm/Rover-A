#!/usr/bin/env python

import logging

from servo import Servo
from vl53l0x import VL53L0X

logging.getLogger(__name__)


class Scanner():
    def __init__(self, pwm, sensor_addr=0x29, pwm_servo_index=0, servo_pulse_min=150, servo_pulse_max=600):
        self.sensor = VL53L0X(sensor_addr)
        self.motor = Servo(pwm, pwm_index=pwm_servo_index, pulse_min=servo_pulse_min, pulse_max=servo_pulse_max)
