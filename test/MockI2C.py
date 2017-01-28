from Adafruit_GPIO import I2C


def get_i2c_device(address, busnum=None, i2c_interface=None, **kwargs):
    return MockDevice(address, busnum, i2c_interface)


class MockDevice(I2C.Device):
    def __init__(self, address, busnum, i2c_interface=None):
        self.address = address
        self.register = {}

    def write8(self, register, value):
        self.register[register] = value

    def readU8(self, register):
        if register not in self.register:
            raise RuntimeError('No mock Register data to read for register {0}'.format(register))
        return self.register[register]
