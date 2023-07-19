"""
Implements tests for Scrapers models.
"""
import unittest

import pytest
from pydantic import ValidationError

from pipelines.flixbus.bus_stations_pipeline import (
    FlixbusBusStationsDataLoader,
    FlixbusBusStationsDataProcessor,
)
from tests.pipelines import (
    FlixbusBusStationsDataLoaderFactory,
    FlixbusBusStationsDataProcessorFactory,
)


class TestFlixbusBusStationsDataProcessor(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def __inject_fixtures(
        self, flixbus_busstations_parsed_data_mock, flixbus_busstations_processed_data_mock
    ):
        self.parsed_data = flixbus_busstations_parsed_data_mock
        self.processed_data = flixbus_busstations_processed_data_mock

    def test_flixbus_bustations_data_processor(self):
        flixbus_data_processor = FlixbusBusStationsDataProcessorFactory(
            parsed_data=self.parsed_data
        )
        self.assertIsInstance(flixbus_data_processor, FlixbusBusStationsDataProcessor)
        self.assertIsInstance(flixbus_data_processor.chunk_size, int)
        self.assertIsInstance(flixbus_data_processor.chunk_size, int)
        processed_items = flixbus_data_processor.process_items()
        self.assertIsInstance(processed_items, list)
        all(self.assertIsInstance(item, dict) for item in processed_items)

        # TODO improve test

    def test_invalid_parsed_data_value(self):
        with self.assertRaises(ValidationError):
            FlixbusBusStationsDataProcessorFactory(parsed_data=-3.1416)

    def test_flixbus_bustations_data_loader(self):
        flixbus_data_loader = FlixbusBusStationsDataLoaderFactory(
            processed_data=self.processed_data
        )
        self.assertIsInstance(flixbus_data_loader, FlixbusBusStationsDataLoader)

    def test_invalid_processed_data_value(self):
        with self.assertRaises(ValidationError):
            FlixbusBusStationsDataLoaderFactory(processed_data=-3.1416)


if __name__ == "__main__":
    unittest.main()
