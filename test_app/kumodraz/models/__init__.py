from .weather import Weather
from kumodraz.utils import db

weather = Weather(db)

__all__ = [
    weather
]