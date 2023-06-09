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
from scrapers.flixbus.bus_scraper import FlixbusBusStationsParser, FlixbusBusStationsScraper


class BaseScraperFactory(Factory):
    class Meta:
        model = BaseScraper

    endpoint_uri = Faker("url")


class FlixbusBusStationsScraperFactory(Factory):
    class Meta:
        model = FlixbusBusStationsScraper


class FlixbusBusStationsParserFactory(Factory):
    class Meta:
        model = FlixbusBusStationsParser

    region = "EU"
