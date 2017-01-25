#!/usr/bin/env python

import unittest

from MockPCA9685 import MockPCA9685
from rover_a.servo import Servo

class TestServoClass(unittest.TestCase):
    def test_scale_math(self):
        pwm = MockPCA9685()
        servo = Servo(pwm)
        self.assertEqual(servo.scale(0, 0, 10, 0, 100), 0.0)
        self.assertEqual(servo.scale(2, 0, 10, 0, 100), 20.0)
        self.assertEqual(servo.scale(10, 0, 10, 0, 100), 100.0)
        self.assertEqual(servo.scale(1, 0, 2, 0, 1), 0.50)

    def test_set_position(self):
        pwm = MockPCA9685()
        servo = Servo(pwm)
        servo.set_position(0)
        self.assertEqual(pwm.get_pwm(0), (0,150))
        servo.set_position(90)
        self.assertEqual(pwm.get_pwm(0), (0,375))
        servo.set_position(180)
        self.assertEqual(pwm.get_pwm(0), (0,600))

    def test_move(self):
        pwm = MockPCA9685()
        servo = Servo(pwm)
        servo.move(0, 0)
        self.assertEqual(pwm.get_pwm(0), (0,150))
        servo.move(90, 0)
        self.assertEqual(pwm.get_pwm(0), (0,375))
        servo.move(180, 0)
        self.assertEqual(pwm.get_pwm(0), (0,600))
        servo.move(90, 0)
        self.assertEqual(pwm.get_pwm(0), (0,375))
        servo.move(0, 0)
        self.assertEqual(pwm.get_pwm(0), (0,150))

if __name__ == '__main__':
    unittest.main()