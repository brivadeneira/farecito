"""
This module provides factories for generating fake data objects

The factories defined in this module use the 'factory' library
to create instances of scrapers models
The factories make use of the 'Faker' class to generate realistic
fake data for attributes of the models.

Classes:
- FlixbusBusStationsDataPipelineFactory: Factory for generating fake Pipeline instances.
"""

from factory import Factory

from pipelines.flixbus.bus_pipeline import FlixbusBusStationsDataPipeline


class FlixbusBusStationsDataPipelineFactory(Factory):
    class Meta:
        model = FlixbusBusStationsDataPipeline
