"""
This module provides factories for generating fake data objects

The factories defined in this module use the 'factory' library
to create instances of scrapers models
The factories make use of the 'Faker' class to generate realistic
fake data for attributes of the models.

"""

from factory import Factory

from pipelines.flixbus.bus_stations_pipeline import (
    FlixbusBusStationsDataLoader,
    FlixbusBusStationsDataProcessor,
)


class FlixbusBusStationsDataProcessorFactory(Factory):
    class Meta:
        model = FlixbusBusStationsDataProcessor


class FlixbusBusStationsDataLoaderFactory(Factory):
    class Meta:
        model = FlixbusBusStationsDataLoader
