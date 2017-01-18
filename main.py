#!/usr/bin/env python

import logging
import time

from trackcontroller import TrackController

#Configuration
MY_NAME = 0x0061

GPIO_PIN_WHEEL_ENCODER_INT = 4

I2C_ADDR_FORWARD_DISTANCE = 0x29
I2C_ADDR_PWM_CONTROLLER = 0x4F
I2C_ADDR_WHEEL_CONTROLLER = 0x6F
I2C_ADDR_WHEEL_ENCODERS = 0x27

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)8s (%(threadName)-10s) %(message)s',
                    )

logging.info("starting")

wheels = TrackController(GPIO_PIN_WHEEL_ENCODER_INT, mot_addr=I2C_ADDR_WHEEL_CONTROLLER,
                         enc_addr=I2C_ADDR_WHEEL_ENCODERS)

wheels.set_motor_speed(0)
wheels.set_track_direction(1,1)
wheels.set_track_direction(-1,2)

for i in range(255):
    wheels.set_motor_speed(i)
    time.sleep(0.01)

for i in reversed(range(255)):
    wheels.set_motor_speed(i)
    time.sleep(0.01)

wheels.set_motor_direction(0)

time.sleep(5)

exit()
