# Rover-A [![Build Status](https://travis-ci.org/tyrm/Rover-A.svg?branch=master)](https://travis-ci.org/tyrm/Rover-A)
First Rover Prototype.

## Required Libraries
* [Adafruit_GPIO](https://github.com/adafruit/Adafruit_Python_GPIO)
* [Adafruit_MotorHAT](https://github.com/adafruit/Adafruit-Motor-HAT-Python-Library)
* [Adafruit_PCA9685](https://github.com/adafruit/Adafruit_Python_PCA9685)

## Hardware
* Raspbery Pi Model A+
* [8-Channel PWM or Servo FeatherWing](https://www.adafruit.com/product/2928)
  * 12-bit resolution for each output
* [Adafruit VL53L0X Time of Flight Distance Sensor](https://www.adafruit.com/products/3317)
  * ~30 to 1000mm range
* [DC Motor + Stepper FeatherWing](https://www.adafruit.com/product/2927)
  * 4 full H-Bridges
* [MCP23008 - i2c 8 input/output port](https://www.adafruit.com/products/593)
  * 8 general purpose pins
  * interrupt via an external pin
* [Rover 5 Chssis](https://www.sparkfun.com/products/10336)
  * 4 independent DC motors
  * 4 independent hall-effect encoders

## i²c Addresses
| Address | Purpose | Device |
| --- | --- | --- |
| ~~0x19~~ | Triple-axis Accelerometer/Magnetometer  | Adafruit 10-DOF IMU Breakout (Planned) |
| ~~0x1E~~ | Triple-axis Accelerometer/Magnetometer  | Adafruit 10-DOF IMU Breakout (Planned) |
| 0x27 | Wheel Encoders | MCP23008 - i2c 8 input/output port expander |
| 0x29 | Forward Distance | Adafruit VL53L0X Time of Flight Distance Sensor |
| ~~0x45~~ | Battery Use monitor | INA219 High Side DC Current Sensor  (Planned) |
| ~~0x47~~ | Battery Temp Monitor | Contact-less Infrared Thermopile (Planned) |
| 0x4F | Servo Controller | 8-Channel PWM or Servo FeatherWing |
| ~~0x68~~ | RTC | Adafruit DS3231 Precision RTC Breakout (Planned) |
| ~~0x6B~~ | L3GD20H Triple-Axis Gyro | Adafruit 10-DOF IMU Breakout (Planned) |
| 0x6F | Wheel Motor Controller | DC Motor + Stepper FeatherWing |
| 0x70 |  | *PCA9685 Call All* |
| ~~0x73~~ | i²c Multiplexer (for addl. ToF) | TCA9548A I2C Multiplexer (Planned) |
| ~~0x77~~ | Barometric Pressure/Temperature/Altitude Sensor | Adafruit 10-DOF IMU Breakout (Planned) |
