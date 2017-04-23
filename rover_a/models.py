#!/usr/bin/env python
import datetime
from sqlalchemy import Column, BigInteger, DateTime, ForeignKey, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Scan(Base):
    __tablename__ = 'scans'
    id = Column(Integer, Sequence('scans_id_seq'), primary_key=True)
    timestamp = Column(DateTime(timezone=True), default=datetime.datetime.now)
    x = Column(BigInteger)
    y = Column(BigInteger)
    quality = Column(Integer)
    rotation = Column(Integer)

    scan_results = relationship("ScanResult")

    def __repr__(self):
        return "<Scan(id='%s', timestamp='%s', x='%s', y='%s', rotation='%s', quality='%s')>" % (
            self.id, self.timestamp, self.x, self.y, self.rotation, self.quality)


class ScanResult(Base):
    __tablename__ = 'scan_results'
    id = Column(Integer, Sequence('scan_results_id_seq'), primary_key=True)
    angle = Column(Integer)
    distance = Column(Integer)
    scan_id = Column(Integer, ForeignKey('scans.id'))
    scan = relationship("Scan", back_populates="scan_results")

    def __repr__(self):
        return "<ScanResult(id='%s', angle='%s', distance='%s' scan_id='%s')>" % (
            self.id, self.angle, self.distance, self.scan_id)
