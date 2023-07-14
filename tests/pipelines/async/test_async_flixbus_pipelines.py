"""
Implements tests for Scrapers models.
"""

from unittest.async_case import IsolatedAsyncioTestCase

import pytest


class TestFlixbusBusStationsDataPipeline(IsolatedAsyncioTestCase):
    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, mocker, flixbus_busstations_proccesed_data_mock):
        self.mocker = mocker
        self.parsed_data = flixbus_busstations_proccesed_data_mock
        self.processed_items = flixbus_busstations_proccesed_data_mock

    @pytest.mark.asyncio
    async def test_flixbus_bustations_pipeline(self):
        pipeline_mock = self.mocker.patch(
            "pipelines.flixbus.bus_pipeline.FlixbusBusStationsDataPipeline", autospec=True
        )
        pipeline_mock.store_items(self.processed_items)
