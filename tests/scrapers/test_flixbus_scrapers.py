"""
Implements tests for Scrapers models.
"""
import unittest

import pytest

from scrapers.flixbus.bus_stations_scraper import (
    FlixbusBusStationsParser,
    FlixbusBusStationsScraper,
)
from tests.scrapers import FlixbusBusStationsParserFactory, FlixbusBusStationsScraperFactory


class TestFlixbusBusStationsScraper(unittest.TestCase):
    """
    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, mocker, dummy_uri):
        self.mocker = mocker
        self.dummy_url = dummy_uri
    """

    def test_flixbus_bustations_scraper(self):
        flixbus_scraper = FlixbusBusStationsScraperFactory()
        self.assertIsInstance(flixbus_scraper, FlixbusBusStationsScraper)
        self.assertIsInstance(flixbus_scraper.query_size, int)
        self.assertIsInstance(flixbus_scraper.query, dict)

        flixbus_scraper = FlixbusBusStationsScraperFactory(region="eu")
        self.assertEqual(flixbus_scraper.region, "EU")
        eu_expected_coordinates = {
            "bottom_right": {"lat": 16.636191878397664, "lon": 97.11914062500001},
            "top_left": {"lat": 63.509375401175134, "lon": -71.63085937500001},
        }
        self.assertEqual(eu_expected_coordinates, flixbus_scraper.region_coordinates)
        # TODO test requests


class TestrFlixbusBusStationsParser(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, flixbus_busstations_response_data_mock):
        self.data_to_parse = flixbus_busstations_response_data_mock

    def test_flixbus_bustations_scraper(self):
        flixbus_parser = FlixbusBusStationsParserFactory(scraped_data=[self.data_to_parse])
        self.assertIsInstance(flixbus_parser, FlixbusBusStationsParser)
        parsed_data = flixbus_parser.parse_data()

        self.assertIsInstance(parsed_data, list)
        expected_keys = {"location", "search_volume", "reachable", "name", "id", "uuid", "region"}
        self.assertTrue(set(item.keys) == expected_keys for item in parsed_data)
        # TODO improve test


if __name__ == "__main__":
    unittest.main()
