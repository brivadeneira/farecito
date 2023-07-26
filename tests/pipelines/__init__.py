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
from pipelines.flixbus.bus_trips_pipeline import FlixbusTripsTracker
from pipelines.trip_alerts import TripsAlertBot


class FlixbusBusStationsDataProcessorFactory(Factory):
    class Meta:
        model = FlixbusBusStationsDataProcessor


class FlixbusBusStationsDataLoaderFactory(Factory):
    class Meta:
        model = FlixbusBusStationsDataLoader


class FlixbusTripsTrackerFactory(Factory):
    class Meta:
        model = FlixbusTripsTracker


class TripsAlertBotFactory(Factory):
    class Meta:
        model = TripsAlertBot
