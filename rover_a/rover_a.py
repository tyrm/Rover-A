#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import logging
import numpy
import threading
import time

import Adafruit_PCA9685
import atexit
from flask import Flask
from sqlalchemy import create_engine, case
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

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
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)8s (%(threadName)-10s) %(name)s: %(message)s')
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
        self.DBSession = sessionmaker(bind=engine)

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

        session = self.DBSession()

        default_map = session.query(Map).filter(Map.name == default_map_name).one_or_none()
        if default_map is not None:
            self.map = default_map
        else:
            log.info('Creating new map [{0}]'.format(default_map_name))

            new_map = Map(name=default_map_name, scale=50)
            session.add(new_map)
            session.commit()
            self.map = new_map

        log.info('Using map {0}'.format(self.map))

        # Start API
        self.api_thread = threading.Thread(target=self.run_api)
        self.api_thread.start()

    def run(self):
        session = self.DBSession()
        val = self.do_scan()

        session.add(val)
        session.commit()

        hits, misses = self.make_map_cells(val)

        log.info("Updating Hits")
        session.bulk_save_objects(hits)
        session.commit()
        log.info(hits[0])

        log.info("Updating Misses")
        session.bulk_save_objects(misses)
        session.commit()
        log.info(misses[0])
        log.info("Done")

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

    def make_map_cells(self, scan):
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

        hit_cells = []
        for hit in hits:
            hit_cell = MapCell(map=self.map, x=hit[0], y=hit[1], hit=True, scan=scan)
            hit_cells.append(hit_cell)

        miss_cells = []
        for miss in misses:
            miss_cell = MapCell(map=self.map, x=miss[0], y=miss[1], hit=False, scan=scan)
            miss_cells.append(miss_cell)

        return hit_cells, miss_cells

    def get_map_dimensions(self):
        session = self.DBSession()

        max_x = session.query(MapCell.x.label('x')).order_by(MapCell.x.desc()).first().x
        min_x = session.query(MapCell.x.label('x')).order_by(MapCell.x.asc()).first().x
        max_y = session.query(MapCell.y.label('y')).order_by(MapCell.y.desc()).first().y
        min_y = session.query(MapCell.y.label('y')).order_by(MapCell.y.asc()).first().y

        return (min_x, min_y), (max_x, max_y)

    def get_map(self):
        map_min, map_max = self.get_map_dimensions()

        session = self.DBSession()
        map_query = session.query(MapCell.x.label('x'),
                                  MapCell.y.label('y'),
                                  (func.sum(case({'TRUE': 1.0},
                                                 value=MapCell.hit,
                                                 else_=0.0)) / func.count(MapCell.hit)).label('p')). \
            group_by(MapCell.x, MapCell.y)

        w = map_max[0] - map_min[0]
        h = map_max[1] - map_min[1]

        map_grid = [[None for _ in range(h + 1)] for _ in range(w + 1)]

        for cell in map_query.all():
            map_grid[cell.x - map_min[0]][cell.y - map_min[1]] = cell.p

        return map_grid

    def make_text_map(self, map_grid):

        w = len(map_grid)
        h = len(map_grid[0])

        line = ''
        for y in range(h):
            for x in range(w):
                cell = map_grid[x][h - y - 1]
                if cell is None:
                    line += ' '
                elif cell == 1:
                    line += '*'
                else:
                    line += str(int(cell * 10))
            line += '\n'

        return line

    def run_api(self):
        app = Flask(__name__)

        @app.route("/map")
        def hello():
            map_grid = self.get_map()
            return self.make_text_map(map_grid)

        app.run(host='0.0.0.0')
