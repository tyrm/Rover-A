#!/usr/bin/env python

import Adafruit_PCA9685
import logging
import time

from scanner import Scanner
from trackcontroller import TrackController

# Configuration
MY_NAME = 0x0061

GPIO_PIN_WHEEL_ENCODER_INT = 4

I2C_ADDR_FORWARD_DISTANCE = 0x29
I2C_ADDR_PWM_CONTROLLER = 0x4F
I2C_ADDR_WHEEL_CONTROLLER = 0x6F
I2C_ADDR_WHEEL_ENCODERS = 0x27

PULSE_FORWARD_SCANNER_MIN = 150
PULSE_FORWARD_SCANNER_MAX = 599

PWM_FORWARD_SCANNER = 3

# Initialization
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)8s (%(threadName)-10s) %(message)s',
                    )

logging.info("starting")

pwm = Adafruit_PCA9685.PCA9685(I2C_ADDR_PWM_CONTROLLER)
pwm.set_pwm_freq(60)

wheels = TrackController(GPIO_PIN_WHEEL_ENCODER_INT, mot_addr=I2C_ADDR_WHEEL_CONTROLLER,
                         enc_addr=I2C_ADDR_WHEEL_ENCODERS)

scanner = Scanner(pwm, sensor_addr=I2C_ADDR_FORWARD_DISTANCE, pwm_servo_index=PWM_FORWARD_SCANNER,
                  servo_pulse_min=PULSE_FORWARD_SCANNER_MIN, servo_pulse_max=PULSE_FORWARD_SCANNER_MAX)


def main():
    val = scanner.do_scan()

    print(val)

    time.sleep(5)

    exit()


if __name__ == "__main__":
    main()
