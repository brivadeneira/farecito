"""
Implements classes for trips web scraping,
including getting data via http requests,
parse the scraped data and a special model for bus stations.
"""

from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod
from typing import Any

import requests
from fake_useragent import UserAgent
from pydantic.dataclasses import dataclass
from requests import Session
from requests.adapters import HTTPAdapter, SSLError
from urllib3.util import Retry

from settings import APP_NAME

logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)


@dataclass(kw_only=True)
class BaseScraper:
    """
    Base class for HTTP-based web scrapers.

    This class serves as a foundation for creating web scrapers that retrieve data
    by making HTTP requests to specified endpoint URLs.
    It provides common functionalities such as handling retries,
    custom headers, and user-agent rotation.
    """

    endpoint_uris: Any = None  # TODO fix this, list[str] | Generator = None
    retries: int = 3
    backoff: float = 0.3
    status_forcelist: tuple = (500, 502, 503, 504)
    timeout: int = 120

    def __post_init__(self):
        if self.endpoint_uris is not None:
            if not all(((isinstance(uri, str)) for uri in self.endpoint_uris)):
                raise TypeError("endpoint_uris must be str")
            if not all(
                (
                    uri.startswith("https://") or uri.startswith("http://")
                    for uri in self.endpoint_uris
                )
            ):
                raise TypeError("endpoint_uris must start with a valid schema: https:// or http://")

    @property
    def requests_retry_session(self) -> Session:
        """
        This property creates and configures a new requests Session with a retry mechanism
        for handling HTTP requests.
        According to 'retries', 'backoff', and 'status_forcelist' values.
        It allows 'GET' and 'POST' methods for retries.

        :return: requests.Session object with retry functionality.
        """
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

    def get_data(self, method: str = "GET") -> list[dict]:
        """
        Get data via http requests from an endpoint_url to be parsed, proceeded and stored
        using a retry session with custom retries, backoff factor and so on.
        :param method: 'GET' or 'POST', if not given GET will be implemented
        :return: a list of json representation of the data
        """

        if not any(self.endpoint_uris):
            raise ValueError("at least a valid endpoint URI is mandatory")

        session = self.requests_retry_session
        timeout = self.timeout
        headers = self.build_headers()
        query = self.query

        scraped_data = []

        for url in self.endpoint_uris:
            request_args = {
                "url": url,
                "headers": headers,
                "timeout": timeout,
                "allow_redirects": True,
            }

            if query:
                request_args["json"] = query

            response = None
            try:
                match method:
                    case "GET":
                        response = session.get(**request_args)
                    case "POST":
                        response = session.post(**request_args)
            except requests.exceptions.RetryError as ex:
                logger.error(ex)
                time.sleep(60)
                continue
            except SSLError:
                response = session.get(url, verify=False)

            if response.status_code != 200:
                logger.error(
                    response.raise_for_status()
                )  # TODO [improvement] make this loop resilient
                continue

            scraped_data.append(response.json())
        return scraped_data


@dataclass
class BaseParser(ABC):
    """
    Base class for a parser of scraped data
    """

    scraped_data: list

    @abstractmethod
    def parse_data(self):
        """
        Parse scraped data, to be transformed into items
        :return:
        """
