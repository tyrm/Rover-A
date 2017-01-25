#!/usr/bin/env python

import logging
import numpy as np
import time

from servo import Servo
from vl53l0x import VL53L0X

SCAN_DISTANCE_MIN = 30
SCAN_DISTANCE_MAX = 2200

logging.getLogger(__name__)


class Scanner():
    def __init__(self, pwm, sensor_addr=0x29, pwm_servo_index=0, servo_pulse_min=150, servo_pulse_max=600,
                 servo_degrees_min=0, servo_degrees_max=180):
        self.sensor = VL53L0X(sensor_addr)
        self.motor = Servo(pwm, pwm_index=pwm_servo_index, pulse_min=servo_pulse_min, pulse_max=servo_pulse_max,
                           degrees_min=servo_degrees_min, degrees_max=servo_degrees_max)

        self.servo_degrees_min = servo_degrees_min
        self.servo_degrees_max = servo_degrees_max

    def do_scan(self, scan_count=1, rescan_tries=5):
        measurement = []

        self.motor.move(self.servo_degrees_min)
        for x in range(0, 181):
            if self.servo_degrees_min > x or x > self.servo_degrees_max:
                measurement.append(None)
            else:
                self.motor.move(x)
                time.sleep(0.01)

                scan = []
                tries = 0

                while tries < rescan_tries:
                    val = self.sensor.measure_distance()

                    if SCAN_DISTANCE_MIN <= val[0] <= SCAN_DISTANCE_MAX:
                        scan.append(val[0])

                        if len(scan) >= scan_count:
                            measurement.append(int(np.mean(scan)))
                            break
                    else:
                        tries += 1

                    time.sleep(0.01)

                if tries >= rescan_tries:
                    if len(scan) > rescan_tries / 2:
                        measurement.append(int(np.mean(scan)))
                    else:
                        measurement.append(-1)

        time.sleep(0.01)
        self.motor.move(90)

        return measurement
