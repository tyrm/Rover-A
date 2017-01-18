#!/usr/bin/env python3

# from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import logging
import RPi.GPIO as GPIO
from threading import Lock, Thread

from mcp23008 import MCP23008

logging.getLogger(__name__)


class TrackController:
    def __init__(self, interrupt, mot_addr=0x67, enc_addr=0x20):

        # self.controller = Adafruit_MotorHAT(addr=mot_addr)

        self.interrupt = interrupt
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.interrupt, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.encoders = MCP23008(enc_addr)
        self.init_encoders()

        self.odometer = [0, 0, 0, 0]
        self.odometer_lock = Lock()
        self.odometer_thread = Thread(name='Odometer',
                                      target=self.update_odometer)
        self.odometer_thread.start()

    def init_encoders(self):
        self.encoders.set_io_direction([0xff])  # all pins to input
        self.encoders.set_interupt_on_change_pins([0xff])  # enable interrupt on all pins
        self.encoders.set_interupt_control([0x00])  # interrupt on rise and fall
        self.encoders.set_configuration([0x00])  # active-low

    def get_encoders(self):
        val = self.encoders.get_gpio()

        enc_vals = []
        enc_vals.append(self.int2bin((val[0] & 0xC0) >> 6))
        enc_vals.append(self.int2bin(val[0] & 0x03))
        enc_vals.append(self.int2bin((val[0] & 0x0C) >> 2))
        enc_vals.append(self.int2bin((val[0] & 0x30) >> 4))

        return enc_vals

    # Odometer
    def reset_odometer(self):
        with self.odometer_lock:
            self.odometer = [0, 0, 0, 0]

    def inc_odometer(self, index, count=1):
        logging.debug("inc enc[{0}]".format(index))
        with self.odometer_lock:
            self.odometer[index] += count

    def dec_odometer(self, index, count=1):
        logging.debug("dec enc[{0}]".format(index))
        with self.odometer_lock:
            self.odometer[index] -= count

    def update_odometer(self):
        last_value = self.get_encoders()

        while True:
            if GPIO.input(self.interrupt) == 0:
                val = self.get_encoders()


                for index in range(len(val)):
                    if val[index] != last_value[index]:
                        val_int = self.bin2int(self.gray2bin(val[index]))
                        last_int = self.bin2int(self.gray2bin(last_value[index]))

                        if val_int == 0 and last_int == 3:
                            self.inc_odometer(index)
                        elif val_int == 3 and last_int == 0:
                            self.dec_odometer(index)
                        elif val_int == last_int + 1:
                            self.inc_odometer(index)
                        elif val_int == last_int - 1:
                            self.dec_odometer(index)

                last_value = val

    def int2bin(self, n):
        """From positive integer to list of binary bits, msb at index 0

        https://rosettacode.org/wiki/Gray_code#Python
        """
        if n:
            bits = []
            while n:
                n, remainder = divmod(n, 2)
                bits.insert(0, remainder)
            return bits
        else:
            return [0]

    def bin2int(self, bits):
        """From binary bits, msb at index 0 to integer

        https://rosettacode.org/wiki/Gray_code#Python
        """
        i = 0
        for bit in bits:
            i = i * 2 + bit
        return i

    def bin2gray(self, bits):
        """https://rosettacode.org/wiki/Gray_code#Python"""
        return bits[:1] + [i ^ ishift for i, ishift in zip(bits[:-1], bits[1:])]

    def gray2bin(self, bits):
        """https://rosettacode.org/wiki/Gray_code#Python"""
        b = [bits[0]]
        for nextb in bits[1:]: b.append(b[-1] ^ nextb)
        return b
