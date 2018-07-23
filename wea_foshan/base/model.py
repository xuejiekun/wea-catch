# -*- coding:utf-8 -*-
from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy import ForeignKey, UniqueConstraint

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(80), unique=True, nullable=False)
    eng_name = Column(String(120))
    lng = Column(Float)
    lat = Column(Float)
    road = Column(String(10))
    code = Column(String(10))

    dats = relationship('Dat', backref='address', lazy='dynamic')

    def to_json(self):
        dat_dict = {'name': self.name,
                    'eng_name': self.eng_name,
                    'lng': self.lng,
                    'lat': self.lat}
        return dat_dict


class Dat(Base):
    __tablename__ = 'dat'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    temp = Column(Float)
    rainfall = Column(Float)
    wdir = Column(Integer)
    speed = Column(Float)
    logtime = Column(DateTime, nullable=False)
    address_id = Column(Integer, ForeignKey('address.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (
        UniqueConstraint('logtime', 'address_id'),
    )

    def to_json(self):
        dat_dict = {'address_id': self.address_id,
                    'logtime': str(self.logtime),
                    'temp': self.temp,
                    'rainfall': self.rainfall,
                    'wdir': self.wdir,
                    'speed': self.speed}
        return dat_dict
