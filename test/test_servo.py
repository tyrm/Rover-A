#!/usr/bin/env python

import unittest

from MockPCA9685 import MockPCA9685
from rover_a.servo import Servo

class TestServoClass(unittest.TestCase):
    def test_scale_math(self):
        pwm = MockPCA9685()
        servo = Servo(pwm)
        self.assertEqual(servo.scale(2, 0, 10, 0, 100), 20)

if __name__ == '__main__':
    unittest.main()