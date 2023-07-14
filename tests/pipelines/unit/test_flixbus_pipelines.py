"""
Implements tests for Scrapers models.
"""
import unittest

import pytest

from pipelines.flixbus.bus_pipeline import FlixbusBusStationsDataPipeline
from tests.pipelines import FlixbusBusStationsDataPipelineFactory


class TestFlixbusBusStationsDataPipeline(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, flixbus_busstations_parsed_data_mock):
        self.parsed_data = flixbus_busstations_parsed_data_mock

    def test_flixbus_bustations_pipeline(self):
        flixbus_pipeline = FlixbusBusStationsDataPipelineFactory(parsed_data=self.parsed_data)
        self.assertIsInstance(flixbus_pipeline, FlixbusBusStationsDataPipeline)
        self.assertIsInstance(flixbus_pipeline.chunk_size, int)
        self.assertIsInstance(flixbus_pipeline.chunk_size, int)
        processed_items = flixbus_pipeline.process_items()
        self.assertIsInstance(processed_items, list)
        all(self.assertIsInstance(item, dict) for item in processed_items)

        # TODO improve test


if __name__ == "__main__":
    unittest.main()
