"""
Test loader
"""
import asyncio
from unittest.async_case import IsolatedAsyncioTestCase

import pytest

from tests.pipelines import FlixbusBusStationsDataLoaderFactory


class TestFlixbusBusStationsDataLoader(IsolatedAsyncioTestCase):
    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, mocker, flixbus_busstations_processed_data_mock):
        self.mocker = mocker
        self.processed_data = flixbus_busstations_processed_data_mock

    @pytest.mark.asyncio
    async def test_flixbus_load_busstations(self):
        # TODO fix this test
        _ = FlixbusBusStationsDataLoaderFactory(processed_data=self.processed_data)
        _ = self.mocker.patch("neo4j.AsyncGraphDatabase.driver", autospec=True)

        # queries = flixbus_loader.build_cypher_queries()
        # _ = await flixbus_loader.load_items()

        # self.assertEqual(flixbus_loader.build_cypher_queries.mock_call_me.call_count == 2)
        # conn_driver_mock.__aenter__().run.assert_called_with(queries)

        # driver_mock = conn_driver_mock.return_value  # driver()
        # session_mock = driver_mock.session()
        # session_mock.__aenter__.assert_awaited_once()
        # session_mock.__aexit__.assert_awaited_once()


if __name__ == "__main__":
    asyncio.run(pytest.main(["-v"]))
