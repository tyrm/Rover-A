#!/usr/bin/env python

import ConfigParser
import logging
import time

import Adafruit_PCA9685
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Scan, ScanResult
from scanner import Scanner
from trackcontroller import TrackController

# Configuration
MY_NAME = 0x0061

GPIO_PIN_WHEEL_ENCODER_INT = 4

I2C_ADDR_FORWARD_DISTANCE = 0x29
I2C_ADDR_PWM_CONTROLLER = 0x4F
I2C_ADDR_WHEEL_CONTROLLER = 0x6F
I2C_ADDR_WHEEL_ENCODERS = 0x27

PWM_FORWARD_SCANNER = 3

# Calibration
FORWARD_SCANNER_DEGREES_MIN = 6
FORWARD_SCANNER_DEGREES_MAX = 174
FORWARD_SCANNER_PULSE_MIN = 150
FORWARD_SCANNER_PULSE_MAX = 599

# Initialization
#logging.basicConfig(level=logging.INFO, format='%(levelname)8s (%(threadName)-10s) %(message)s')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)8s (%(threadName)-10s) %(name)s:%(message)s')

print logging.basicConfig()

logging.info("Hello! Starting a-Rex")


class RoverA:
    def __init__(self):
        # Parse Config
        Config = ConfigParser.ConfigParser()
        Config.read("config.ini")

        # Init DB
        connection_string = Config.get('database', 'engine')
        engine = create_engine(connection_string, echo=False)
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

        self.pwm = Adafruit_PCA9685.PCA9685(I2C_ADDR_PWM_CONTROLLER)
        self.pwm.set_pwm_freq(60)

        #self.wheels = TrackController(GPIO_PIN_WHEEL_ENCODER_INT, mot_addr=I2C_ADDR_WHEEL_CONTROLLER,
        #                              enc_addr=I2C_ADDR_WHEEL_ENCODERS)

        self.scanner = Scanner(self.pwm, sensor_addr=I2C_ADDR_FORWARD_DISTANCE, pwm_servo_index=PWM_FORWARD_SCANNER,
                               servo_pulse_min=FORWARD_SCANNER_PULSE_MIN, servo_pulse_max=FORWARD_SCANNER_PULSE_MAX,
                               servo_degrees_min=FORWARD_SCANNER_DEGREES_MIN,
                               servo_degrees_max=FORWARD_SCANNER_DEGREES_MAX)

        # Globals
        self.position = (0, 0)
        self.rotation = 0


    def run(self):
        val = self.do_scan()

        session = self.Session()
        session.add(val)
        session.commit()

        print(val)

        print(val.scan_results)

        time.sleep(5)

        exit()

    def do_scan(self, scan_count=1, rescan_tries=5):
        logging.info("Starting Scan Quality[{0}]".format(scan_count))

        new_scan = Scan(x=self.position[0], y=self.position[1], rotation=self.rotation, quality=scan_count)
        raw_scan = self.scanner.do_scan(scan_count=scan_count, rescan_tries=rescan_tries)
        results = []

        for deg, measurement in enumerate(raw_scan):
            if measurement is not None:
                results.append(ScanResult(angle=deg, distance=measurement))

        new_scan.scan_results = results

        return new_scan
