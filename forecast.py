"""
forecast.py
This defines an ORM class that represents forecasts for a city. Has a foreign key relation with the cities table.
"""

import datetime

from sqlalchemy import Column, Integer, Float, Date, Time, ForeignKey, CheckConstraint
from base import Base


class Forecast(Base):
    __tablename__ = 'forecasts'

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.id'))
    date = Column(Date)
    time = Column(Time)
    humidity = Column(Float, CheckConstraint('humidity >= 0'))
    temperature = Column(Float)
    feels_like = Column(Float)

    def __init__(self, date: datetime.date, time: datetime.time, humidity: float, temperature: float,
                 feels_like: float):
        self.date = date
        self.time = time
        self.humidity = humidity
        self.temperature = temperature
        self.feels_like = feels_like
