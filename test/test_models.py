#!/usr/bin/env python
import datetime
import types
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from rover_a.models import Base, Scan, ScanResult


class TestScanModel(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=engine)
        self.session = Session()

        Base.metadata.create_all(engine)

        test_scan = Scan(x=12, y=67, rotation=187)
        self.session.add(test_scan)

    def test_scan_model_return_value(self):
        test_result = self.session.query(Scan).first()
        self.assertEqual(test_result.x, 12)
        self.assertEqual(test_result.y, 67)
        self.assertEqual(test_result.rotation, 187)

    def test_scan_model_return_instance(self):
        test_result = self.session.query(Scan).first()
        self.assertIsInstance(test_result.x, types.IntType)
        self.assertIsInstance(test_result.y, types.IntType)
        self.assertIsInstance(test_result.rotation, types.IntType)
        self.assertIsInstance(test_result.timestamp, datetime.datetime)


class TestScanResultModel(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=engine)
        self.session = Session()

        Base.metadata.create_all(engine)

        test_scan = Scan(x=12, y=67, rotation=187)
        test_scan.scan_results = [ScanResult(angle=0, distance=1234, scans=10)]
        self.session.add(test_scan)
        self.session.flush()

    def test_scan_model_return_value(self):
        test_result = self.session.query(ScanResult).first()
        self.assertEqual(test_result.angle, 0)
        self.assertEqual(test_result.distance, 1234)
        self.assertEqual(test_result.scans, 10)

    def test_scan_model_return_instance(self):
        test_result = self.session.query(ScanResult).first()
        self.assertIsInstance(test_result.angle, types.IntType)
        self.assertIsInstance(test_result.distance, types.IntType)
        self.assertIsInstance(test_result.scans, types.IntType)


if __name__ == '__main__':
    unittest.main()
