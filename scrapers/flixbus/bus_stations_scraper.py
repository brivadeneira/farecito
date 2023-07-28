"""
Implements flixbus bus trips web scraping.

This module contains classes for scraping bus station data from the Flixbus website.
It includes scraping and parsing classes
"""
import logging
from typing import Any

from pydantic import validator
from pydantic.dataclasses import dataclass

from scrapers import BaseParser, BaseScraper
from settings import APP_NAME

logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)


@dataclass
class FlixbusBusStationsScraper(BaseScraper):
    """
    A class for scraping bus station data from the Flixbus
    website. It extends the `BaseScraper` class and provides a custom query for fetching
    cities that can be reached by bus from a given region.
    """

    region: str = "EU"
    query_size: int = 3000  # cities to get (all EU cities count around 2800)

    def __post_init__(self):
        self.endpoint_uris = ["https://d1ioiftasz4l3w.cloudfront.net/cities_v2/_search"]

    @validator("region")
    def validate_region(cls, region):
        """
        Validate region value according to region ISO code
        """
        valid_iso_regions = {"EU", "US", "BRA"}
        region = region.upper()
        if region not in valid_iso_regions:
            raise ValueError(f"Region must be one of the following: {', '.join(valid_iso_regions)}")
        return region

    @property
    def region_coordinates(self):
        """
        Cities can be obtained according to one of the regions
        of https://www.flixbus.com/bus-routes,
        coordinates for each one were got manually.
        :return: a dict with bottom_right and top_left latitude and longitude values
        """
        match self.region:
            case "EU":
                return {
                    "bottom_right": {"lat": 16.636191878397664, "lon": 97.11914062500001},
                    "top_left": {"lat": 63.509375401175134, "lon": -71.63085937500001},
                }
            case "US":
                return {
                    "bottom_right": {"lat": 6.664607562172573, "lon": -10.019531250000002},
                    "top_left": {"lat": 54.97761367069628, "lon": -178.76953125},
                }
            case "BRA":
                return {
                    "bottom_right": {"lat": -38.2036553180715, "lon": -2.4609375000000004},
                    "top_left": {"lat": -11.60919340793894, "lon": -86.83593750000001},
                }

    @property
    def query(self):
        """
        Build the query for request all cities of a given region flixbus routes,
        that can be reached by bus, making a POST against its search API.
        Notice that search_volume indicates the popularity of the city.
        :return: (dict) a query ready to get the region cities
        """

        return {
            "_source": ["name", "location", "id", "search_volume", "uuid", "reachable"],
            # _source keys available: ['_language', 'name', 'location', 'id',
            # 'search_volume', 'field_site', 'uuid', 'reachable', 'slug', 'transportation_category']
            "from": 0,
            "query": {
                "bool": {
                    "filter": [
                        {"geo_bounding_box": {"location": self.region_coordinates}},
                        {"terms": {"transportation_category": ["bus"]}},
                    ],  # 'flixtrain', 'train'
                    "must": [
                        {"term": {"field_site.keyword": {"value": "flixbus"}}},
                        {"term": {"_language.keyword": {"value": "en-us"}}},
                    ],
                }
            },
            "size": self.query_size,
            "sort": [{"search_volume": {"order": "desc"}}],
        }


@dataclass
class FlixbusBusStationsParser(BaseParser):
    """
    A class for parsing the scraped data obtained by the
    `FlixbusBusStationsScraper`. It extends the `BaseParser` class and implements the
    abstract method `parse_data` to transform the data into a list of dictionaries
    representing bus stations.
    """

    region: str = "EU"

    def parse_data(self) -> list[Any]:
        """
        Gets the result of get_data() method, parses it to be proceeded and stored
        """
        [scraped_data] = self.scraped_data

        city_items = []

        for hit in scraped_data["hits"]["hits"]:
            try:
                source = hit["_source"]
            except KeyError:
                logging.error("Malformed hit %s", hit)
                continue

            item_data = [
                (k, source.get(k))
                for k in ["id", "name", "uuid", "location", "search_volume", "reachable"]
            ]
            item_data.append(("region", self.region))
            item = dict(item_data)

            city_items.append(item)

        return city_items
