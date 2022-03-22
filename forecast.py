from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey

from base import Base


class Forecast(Base):
    __tablename__ = 'forecasts'

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.id'))
    datetime = Column(DateTime)
    humidity = Column(Float)
    temperature = Column(Float)
    feels_like = Column(Float)

    def __init__(self, datetime, humidity, temperature, feels_like):
        self.datetime = datetime
        self.humidity = humidity
        self.temperature = temperature
        self.feels_like = feels_like
