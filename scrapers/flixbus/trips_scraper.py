"""
Implements flixbus bus trips web scraping.

This module contains a class for scraping and parsing Flixbus trips.
"""
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
    default_days_range: Any
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

    @field_validator("default_days_range")
    def validate_default_days_range(cls, default_days_range):
        if not default_days_range:
            return SCRAP_DAYS
        if not isinstance(default_days_range, int):
            raise ValueError(f"default_days_range must be an int, not {type(default_days_range)}")
        if default_days_range <= 0:
            raise ValueError("default_days_range must be > 0")
        return default_days_range

    @field_validator("start_date")
    def validate_start_date(cls, start_date):
        if start_date > datetime.now(pytz.timezone("Europe/Madrid")):
            raise ValueError("Start date can't be previous than today")
        return start_date

    @field_validator("end_date")
    def validate_end_date(cls, end_date):
        if end_date > datetime.now(pytz.timezone("Europe/Madrid")):
            raise ValueError("End date can't be previous than today")
        return end_date

    def dates_range_generator(self) -> list[str]:
        """
        Returns a list of str for dates with "%d.%m.%Y" format (e.g. "01.08.2023"),
        between start and end dates
        """
        start_date, delta = self.start_date, self.end_date - self.start_date
        dates_range = [start_date + timedelta(days=i) for i in range(delta.days + 1)]
        return [date.strftime("%d.%m.%Y") for date in dates_range]

    def endpoint_uris_generator(self):
        """
        Gen a set of urls for searching trips between the given cities,
        in a range of dates.
        """

        search_trip_uri = "https://global.api.flixbus.com/search/service/v4"
        default_params = "products=%7B%22adult%22%3A1%7D&currency=EUR&search_by=cities"

        departure_dates = self.dates_range_generator()
        departure_city = self.departure_city_uuid
        arrival_city = self.arrival_city_uuid

        for departure_date in departure_dates:
            query_str = (
                f"search?from_city_id={departure_city}&to_city_id={arrival_city}"
                f"&departure_date={departure_date}&adult=1&search_by=cities&currency=USD"
            )
            url = f"{search_trip_uri}/{query_str}&{default_params}"
            yield url

    def __post_init__(self):
        if not self.start_date:
            self.start_date = datetime.now(pytz.timezone("Europe/Madrid")) + timedelta(days=1)
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.default_days_range)
        self.endpoint_uris = list(uri for uri in self.endpoint_uris_generator())
