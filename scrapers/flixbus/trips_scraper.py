"""
Implements flixbus bus trips web scraping.

This module contains a class for scraping and parsing Flixbus trips.
"""
import random
from datetime import datetime, timedelta
from typing import Any

import pytz
from pydantic.dataclasses import dataclass
from pydantic.functional_validators import field_validator

from pipelines.settings import SCRAP_DAYS
from scrapers import BaseScraper


@dataclass
class FlixbusTripsScraper(BaseScraper):
    """
    A class for scraping Flixbus trips between specified departure
    and arrival cities and within a given date range.

    It extends the `BaseScraper` class and provides methods
    for generating the URLs for searching trips in a set of dates.
    """

    # TODO [bug] fix this: dataclass not fully defined
    departure_city_uuid: Any
    arrival_city_uuid: Any
    start_date: Any = None
    end_date: Any = None

    @field_validator("departure_city_uuid")
    def validate_departure_city_uuid(cls, departure_city_uuid):
        if not isinstance(departure_city_uuid, str):
            raise ValueError(f"departure_city_uuid must be a str, not {type(departure_city_uuid)}")
        return departure_city_uuid

    @field_validator("arrival_city_uuid")
    def validate_arrival_city_uuid(cls, arrival_city_uuid):
        if not isinstance(arrival_city_uuid, str):
            raise ValueError(f"arrival_city_uuid must be a str, not {type(arrival_city_uuid)}")
        return arrival_city_uuid

    def dates_range_generator(self) -> list[str]:
        """
        Returns a list of str for dates with "%d.%m.%Y" format (e.g. "01.08.2023"),
        between start and end dates
        """
        start_date = self.start_date
        delta = self.end_date - self.start_date
        dates_range = [start_date + timedelta(days=i) for i in range(delta.days + 1)]
        return [date.strftime("%d.%m.%Y") for date in dates_range]

    def endpoint_uris_generator(self):
        """
        Gen a set of urls for searching trips between the given cities,
        in a range of dates.
        """

        search_trip_uri = "https://global.api.flixbus.com/search/service/v4"
        default_params = (
            "&products=%7B%22adult%22%3A1%7D&currency=EUR"
            "&search_by=cities&include_after_midnight_rides=1"
        )

        departure_dates = self.dates_range_generator()
        random.shuffle(departure_dates)
        departure_city = self.departure_city_uuid
        arrival_city = self.arrival_city_uuid

        for departure_date in departure_dates:
            query_str = (
                f"search?from_city_id={departure_city}&to_city_id={arrival_city}"
                f"&departure_date={departure_date}"
            )
            url = f"{search_trip_uri}/{query_str}&{default_params}"
            yield url

    def __post_init__(self):
        if not self.start_date:
            self.start_date = datetime.now(pytz.timezone("Europe/Madrid"))
        if not self.end_date:
            days = int(SCRAP_DAYS)
            self.end_date = self.start_date + timedelta(days)

        self.endpoint_uris = list(uri for uri in self.endpoint_uris_generator())
