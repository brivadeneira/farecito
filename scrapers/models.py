"""
Implements classes for trips web scraping

Classes:
- BaseScraper: Base class for getting data via http requests
- BaseParser: Base class for parse scraped data
- BusStationScraper: Special model for bus stations web scraping
"""

from __future__ import annotations

from typing import Any

from fake_useragent import UserAgent
from pydantic.dataclasses import dataclass
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


class RequestError(ValueError):
    pass


@dataclass
class BaseScraper:
    """
    Base class for getting data via http requests
    """

    endpoint_uri: str = None
    retries: int = 3
    backoff: float = 0.3
    status_forcelist: tuple = (500, 502, 503, 504)
    timeout: int = 120

    def __post_init__(self):
        # TODO, fix this! For some reason pydantic is not validating this
        if self.endpoint_uri:
            if not isinstance(self.endpoint_uri, str):
                raise TypeError(f"endpoint_uri must be a str {type(self.endpoint_uri)}")

    @property
    def requests_retry_session(self):
        session = Session()
        retries = Retry(
            total=self.retries,
            backoff_factor=self.backoff,
            status_forcelist=self.status_forcelist,
            allowed_methods={"GET", "POST"},
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))
        return session

    def build_headers(self) -> dict:
        """
        Build an HTTP GET/POST header with a random user agent.
        :return: (dict) with the headers ready to use
        """
        random_user_agent = UserAgent().random

        accept = (
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
        )
        return {
            "User-Agent": random_user_agent,
            "Accept": accept,
            "Connection": "keep-alive",
        }

    @property
    def query(self) -> dict:
        """
        Builds a custom query to be used getting data
        :return: (dict) with a custom query
        """
        return {}

    def get_data(self, method: str = "GET"):
        """
        Get data via http requests from an endpoint_url to be parsed, proceeded and stored
        using a retry session with custom retries, backoff factor and so on.
        :param method: 'GET' or 'POST', if not given GET will be implemented
        :return: json representation of the data
        """

        if not self.endpoint_uri:
            raise ValueError("a valid endpoint URI is mandatory")

        session = self.requests_retry_session
        url = self.endpoint_uri
        timeout = self.timeout
        headers = self.build_headers()
        query = self.query

        request_args = {
            "url": url,
            "headers": headers,
            "json": query,
            "timeout": timeout,
            "allow_redirects": True,
        }

        try:
            match method:
                case "GET":
                    response = session.get(**request_args)
                case "POST":
                    response = session.post(**request_args)
        except Exception as ex:
            raise RequestError(ex) from ex

        response.raise_for_status()

        scraped_data = response.json()

        return self.parse_items(scraped_data)


@dataclass
class BaseParser:
    """
    Base class for a parser of scraped data
    """

    scraped_data: Any

    def parse_data(self):
        """
        Parse scraped data, to be transformed into items
        :return:
        """
