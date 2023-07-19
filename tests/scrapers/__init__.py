"""
This module provides factories for generating fake data objects

The factories defined in this module use the 'factory' library
to create instances of scrapers models
The factories make use of the 'Faker' class to generate realistic
fake data for attributes of the models.

Classes:
- BaseScraperFactory: Factory for generating fake BaseScraper instances.
"""

from factory import Factory, Faker

from scrapers import BaseScraper
from scrapers.flixbus.bus_stations_scraper import (
    FlixbusBusStationsParser,
    FlixbusBusStationsScraper,
)
from scrapers.flixbus.trips_scraper import FlixbusTripsScraper


class BaseScraperFactory(Factory):
    class Meta:
        model = BaseScraper

    endpoint_uris = ["http://dummy.url"]


class FlixbusBusStationsScraperFactory(Factory):
    class Meta:
        model = FlixbusBusStationsScraper

    endpoint_uris = ["http://dummy.url"]


class FlixbusTripsScraperFactory(Factory):
    class Meta:
        model = FlixbusTripsScraper

    endpoint_uris = None


class FlixbusBusStationsParserFactory(Factory):
    class Meta:
        model = FlixbusBusStationsParser

    region = "EU"
