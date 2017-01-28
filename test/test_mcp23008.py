#!/usr/bin/env python
import datetime
import types
import unittest

import MockI2C
from rover_a.mcp23008 import MCP23008

MCP23008_REG_IODIR = 0x0000
MCP23008_REG_IPOL = 0x0001
MCP23008_REG_GPINTEN = 0x0002
MCP23008_REG_DEFVAL = 0x0003
MCP23008_REG_INTCON = 0x0004
MCP23008_REG_IOCON = 0x0005
MCP23008_REG_GPPU = 0x0006
MCP23008_REG_INTF = 0x0007
MCP23008_REG_INTCAP = 0x0008
MCP23008_REG_GPIO = 0x0009
MCP23008_REG_OLAT = 0x000A


class TestMCP23008(unittest.TestCase):
    def setUp(self):
        self.device = MCP23008(0x29, i2c=MockI2C)

        self.device.set_io_direction(0x11)
        self.device.set_input_polarity(0x22)
        self.device.set_interupt_on_change_pins(0x33)
        self.device.set_default_value(0x44)
        self.device.set_interupt_control(0x55)
        self.device.set_configuration(0x66)
        self.device.set_pull_up_resistor(0x77)
        self.device.set_gpio(0x88)
        self.device.set_output_latch(0x99)

        self.device.device.register[MCP23008_REG_INTF] = 0xAA
        self.device.device.register[MCP23008_REG_INTCAP] = 0xBB

    def test_i2c_register_values(self):
        self.assertEqual(self.device.device.register[MCP23008_REG_IODIR], 0x11)
        self.assertEqual(self.device.device.register[MCP23008_REG_IPOL], 0x22)
        self.assertEqual(self.device.device.register[MCP23008_REG_GPINTEN], 0x33)
        self.assertEqual(self.device.device.register[MCP23008_REG_DEFVAL], 0x44)
        self.assertEqual(self.device.device.register[MCP23008_REG_INTCON], 0x55)
        self.assertEqual(self.device.device.register[MCP23008_REG_IOCON], 0x66)
        self.assertEqual(self.device.device.register[MCP23008_REG_GPPU], 0x77)
        self.assertEqual(self.device.device.register[MCP23008_REG_GPIO], 0x88)
        self.assertEqual(self.device.device.register[MCP23008_REG_OLAT], 0x99)

    def test_device_get_values(self):
        self.assertEqual(self.device.get_io_direction(), 0x11)
        self.assertEqual(self.device.get_input_polarity(), 0x22)
        self.assertEqual(self.device.get_interupt_on_change_pins(), 0x33)
        self.assertEqual(self.device.get_default_value(), 0x44)
        self.assertEqual(self.device.get_interupt_control(), 0x55)
        self.assertEqual(self.device.get_configuration(), 0x66)
        self.assertEqual(self.device.get_pull_up_resistor(), 0x77)
        self.assertEqual(self.device.get_gpio(), 0x88)
        self.assertEqual(self.device.get_output_latch(), 0x99)
        self.assertEqual(self.device.get_interupt_flag(), 0xAA)
        self.assertEqual(self.device.get_interupt_capture(), 0xBB)