#!/usr/bin/env python

import unittest

from MockPCA9685 import MockPCA9685
from rover_a.servo import Servo, scale

class TestServoClass(unittest.TestCase):
    def test_scale_math(self):
        pwm = MockPCA9685()
        servo = Servo(pwm)
        self.assertEqual(scale(0, 0, 10, 0, 100), 0.0)
        self.assertEqual(scale(2, 0, 10, 0, 100), 20.0)
        self.assertEqual(scale(10, 0, 10, 0, 100), 100.0)
        self.assertEqual(scale(1, 0, 2, 0, 1), 0.50)

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

    def test_pwm_index(self):
        pwm = MockPCA9685()
        servo = Servo(pwm)
        servo.set_position(0)
        self.assertTupleEqual(pwm.get_pwm(0), (0,150))
        servo = Servo(pwm, pwm_index=1)
        servo.set_position(0)
        self.assertTupleEqual(pwm.get_pwm(1), (0,150))
        servo = Servo(pwm, pwm_index=2)
        servo.set_position(0)
        self.assertTupleEqual(pwm.get_pwm(2), (0,150))
        servo = Servo(pwm, pwm_index=3)
        servo.set_position(0)
        self.assertTupleEqual(pwm.get_pwm(3), (0,150))
        servo = Servo(pwm, pwm_index=4)
        servo.set_position(0)
        self.assertTupleEqual(pwm.get_pwm(4), (0,150))
        servo = Servo(pwm, pwm_index=5)
        servo.set_position(0)
        self.assertTupleEqual(pwm.get_pwm(5), (0,150))
        servo = Servo(pwm, pwm_index=6)
        servo.set_position(0)
        self.assertTupleEqual(pwm.get_pwm(6), (0,150))
        servo = Servo(pwm, pwm_index=7)
        servo.set_position(0)
        self.assertTupleEqual(pwm.get_pwm(7), (0,150))

if __name__ == '__main__':
    unittest.main()
