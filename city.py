"""
city.py
This defines an ORM class that represents a city, its ID and location.
"""

from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship

from base import Base

class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    longtitude = Column(Float)
    latitude = Column(Float)
    forecasts = relationship('Forecast')

    def __init__(self, name: str, longtitude: float, latitude: float):
        self.name = name
        self.longtitude = longtitude
        self.latitude = latitude