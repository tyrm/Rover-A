#!/usr/bin/env python


import Adafruit_PCA9685

class MockPCA9685(Adafruit_PCA9685.PCA9685):
    def __init__(self, address=0x40, i2c=None, **kwargs):
        self.pwm = {}

    def set_pwm(self, channel, on, off):
        self.pwm[channel] = (on, off)

    def get_pwm(self, channel):
        if channel not in self.pwm:
            raise RuntimeError('No mock PWM data to read for channel {0}'.format(channel))
        return self.pwm[channel]

