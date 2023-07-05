"""
Implements classes for trips web scraping

Classes:
- BaseScraper: Base class for getting data via http requests, include get and parse html data
- BusStationScraper: Special model for bus stations web scraping
- BaseDataPipeline: Model for process and store items results from scrapers
"""
from __future__ import annotations

from pydantic.dataclasses import dataclass
from requests import Session

from scrapers.utils import requests_retry_session


class RequestError(ValueError):
    pass


@dataclass
class BaseScraper:
    """
    Base class for getting data via http requests
    """

    endpoint_url: str
    retries: int = (3,)
    backoff: float = (0.3,)
    status_forcelist: tuple = (500, 502, 503, 504)
    timeout: int = 120
    request_session: Session = None

    def __post_init__(self):
        self.request_session = requests_retry_session(
            retries=self.retries, backoff=self.backoff, status_forcelist=self.status_forcelist
        )

    def get_data(self, query: dict = None):
        """
        Get data via http requests from an endpoint_url to be parsed, proceeded and stored
         using a retry session with custom retries, backoff factor and so on.
        :param query: (dict) for POST method needed to get the data,
        if not given GET will be implemented
        :return: json representation of the data
        """
        session = self.request_session
        url = self.endpoint_url
        timeout = self.timeout
        try:
            if query:
                response = session.post(url=url, json=query, timeout=timeout)
            else:
                response = session.get(url=url, timeout=timeout)
        except Exception as ex:
            # log ex.__class__.__name__
            raise RequestError from ex

        return response.json()

    def parse_data(self):
        """
        Gets the result of get_data() method, parses it to be proceeded and stored
        """


@dataclass
class BusStationScraper(BaseScraper):
    """
    Scraper class for bus stations,
    implements extra methods for special bus station items treatments
    """

    def get_bus_stations(self):
        """
        Method for getting bus stations as items,
        after data of interest is parsed, to be proceeded and stored
        """


@dataclass
class BaseDataPipeline:
    """
    Base class for cleaning, validate and store items from scrapers
    """

    def process_items(self):
        """
        Performs data processing tasks such as cleaning, validation for each item
        """

    def store_items(self):
        """
        Stores items into the correspondant data repository
        """
