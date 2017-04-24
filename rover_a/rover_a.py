#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import logging
import numpy
import threading
import time

import Adafruit_PCA9685
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Map, MapCell, Scan, ScanResult
from scanner import Scanner
from trackcontroller import TrackController
from util import bresenham, pol2cart

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
# logging.basicConfig(level=logging.INFO, format='%(levelname)8s (%(threadName)-10s) %(message)s')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)8s (%(threadName)-10s) %(name)s:%(message)s')
log = logging.getLogger(__name__)


class RoverA:
    def __init__(self):
        log.info("Hello! Starting a-Rex")

        # Parse Config
        Config = ConfigParser.ConfigParser()
        Config.read("config.ini")

        # Init DB
        connection_string = Config.get('database', 'engine')
        engine = create_engine(connection_string, echo=False)

        Base.metadata.create_all(engine)
        self.db_session = sessionmaker(bind=engine)()

        self.pwm = Adafruit_PCA9685.PCA9685(I2C_ADDR_PWM_CONTROLLER)
        self.pwm.set_pwm_freq(60)

        # self.wheels = TrackController(GPIO_PIN_WHEEL_ENCODER_INT, mot_addr=I2C_ADDR_WHEEL_CONTROLLER,
        #                              enc_addr=I2C_ADDR_WHEEL_ENCODERS)

        self.scanner = Scanner(self.pwm, sensor_addr=I2C_ADDR_FORWARD_DISTANCE, pwm_servo_index=PWM_FORWARD_SCANNER,
                               servo_pulse_min=FORWARD_SCANNER_PULSE_MIN, servo_pulse_max=FORWARD_SCANNER_PULSE_MAX,
                               servo_degrees_min=FORWARD_SCANNER_DEGREES_MIN,
                               servo_degrees_max=FORWARD_SCANNER_DEGREES_MAX)

        # Globals
        self.position = (0, 0)
        self.rotation = 90  # polar degree 0 points towards 'east' cartesian (∞,0) rex starts pointed 'north' on map

        # Get Map
        try:
            default_map_name = Config.get('map', 'name')
        except ConfigParser.NoSectionError:
            default_map_name = 'default'

        default_map = self.db_session.query(Map).filter(Map.name == default_map_name).one_or_none()
        if default_map is not None:
            self.map = default_map
        else:
            log.info('Creating new map [{0}]'.format(default_map_name))
            new_map = Map(name=default_map_name, scale=10)
            self.db_session.add(new_map)
            self.db_session.commit()
            self.map = new_map

        log.info('Using map {0}'.format(self.map))

        #Start API
        self.api_thread = threading.Thread(target=self.run_api)


    def run(self):
        val = self.do_scan()

        self.db_session.add(val)
        self.db_session.commit()

        self.update_map(val)

        time.sleep(5)

        exit()

    def do_scan(self, scan_count=1, rescan_tries=5):
        log.info("Starting Scan Quality[{0}]".format(scan_count))

        new_scan = Scan(x=self.position[0], y=self.position[1], rotation=self.rotation, quality=scan_count)
        raw_scan = self.scanner.do_scan(scan_count=scan_count, rescan_tries=rescan_tries)
        results = []

        for deg, measurement in enumerate(raw_scan):
            if measurement is not None:
                results.append(ScanResult(angle=deg, distance=measurement))

        new_scan.scan_results = results

        return new_scan

    def update_map(self, scan):
        hits = []
        misses = []

        for result in scan.scan_results:
            if result.distance is not -1:
                point1 = self.position

                cart = pol2cart(result.distance / self.map.scale, numpy.radians(result.angle + (self.rotation - 90)))
                point2 = (cart[0] + self.position[0], cart[1] + self.position[1])

                line_points = bresenham(point1, point2)
                hit = line_points.path.pop()

                hits.append(hit)
                for line_point in line_points.path:
                    misses.append(line_point)

        misses_dup_len = len(misses)
        misses = set(misses)

        log.info("Found Misses: {0} ({1}) Hits: {2}".format(len(misses), misses_dup_len, len(hits)))

        log.info("Updating Hits")
        for hit in hits:
            hit_cell = MapCell(map=self.map, x=hit[0], y=hit[1], hit=True, scan=scan)
            self.db_session.add(hit_cell)

        log.info("Committing Hits")
        self.db_session.commit()
        log.info("Updating Misses")
        for miss in misses:
            miss_cell = MapCell(map=self.map, x=miss[0], y=miss[1], hit=False, scan=scan)
            self.db_session.add(miss_cell)

        log.info("Committing Misses")
        self.db_session.commit()
        log.info("Map update complete")

