#!/usr/bin/env python
import datetime
from sqlalchemy import Column, BigInteger, Boolean, DateTime, ForeignKey, Integer, String, Sequence
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

    map_cells = relationship("MapCell")
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

class Map(Base):
    __tablename__ = 'maps'
    id = Column(Integer, Sequence('maps_id_seq'), primary_key=True)
    name = Column(String, unique=True)
    scale = Column(Integer) # mm per grid square

    map_cells = relationship("MapCell")

    def __repr__(self):
        return "<Map(id='%s', name='%s', scale='%s')>" % (
            self.id, self.name, self.scale)

class MapCell(Base):
    __tablename__ = 'map_cells'
    id = Column(Integer, Sequence('map_cells_id_seq'), primary_key=True)
    map_id = Column(Integer, ForeignKey('maps.id'))
    map = relationship("Map", back_populates="map_cells")
    x = Column(BigInteger)
    y = Column(BigInteger)
    hit = Column(Boolean)
    scan_id = Column(Integer, ForeignKey('scans.id'))
    scan = relationship("Scan", back_populates="map_cells")



