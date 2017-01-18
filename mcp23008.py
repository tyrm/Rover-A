#!/usr/bin/env python3
from Adafruit_GPIO import I2C

# Register Addresses
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


class MCP23008:
    def __init__(self, address, i2c=None):
        if i2c is None:
            i2c = I2C

        self.device = i2c.get_i2c_device(address)

    def set_io_direction(self, val):
        self.device.writeList(MCP23008_REG_IODIR, val)

    def get_io_direction(self):
        return self.device.readList(MCP23008_REG_IODIR, 1)

    def set_input_polarity(self, val):
        self.device.writeList(MCP23008_REG_IPOL, val)

    def get_input_polarity(self):
        return self.device.readList(MCP23008_REG_IPOL, 1)

    def set_interupt_on_change_pins(self, val):
        self.device.writeList(MCP23008_REG_GPINTEN, val)

    def get_interupt_on_change_pins(self):
        return self.device.readList(MCP23008_REG_GPINTEN, 1)

    def set_default_value(self, val):
        self.device.writeList(MCP23008_REG_DEFVAL, val)

    def get_default_value(self):
        return self.device.readList(MCP23008_REG_DEFVAL, 1)

    def set_interupt_control(self, val):
        self.device.writeList(MCP23008_REG_INTCON, val)

    def get_interupt_control(self):
        return self.device.readList(MCP23008_REG_INTCON, 1)

    def set_configuration(self, val):
        self.device.writeList(MCP23008_REG_IOCON, val)

    def get_configuration(self):
        return self.device.readList(MCP23008_REG_IOCON, 1)

    def set_pull_up_resistor(self, val):
        self.device.writeList(MCP23008_REG_GPPU, val)

    def get_pull_up_resistor(self):
        return self.device.readList(MCP23008_REG_GPPU, 1)

    def get_interupt_flag(self):
        return self.device.readList(MCP23008_REG_INTF, 1)

    def get_interupt_capture(self):
        return self.device.readList(MCP23008_REG_INTCAP, 1)

    def set_gpio(self, val):
        self.device.writeList(MCP23008_REG_GPIO, val)

    def get_gpio(self):
        return self.device.readList(MCP23008_REG_GPIO, 1)

    def set_output_latch(self, val):
        self.device.writeList(MCP23008_REG_OLAT, val)

    def get_output_latch(self):
        return self.device.readList(MCP23008_REG_OLAT, 1)
