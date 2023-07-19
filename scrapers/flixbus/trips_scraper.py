"""
Implements flixbus bus trips web scraping
"""
import itertools
from datetime import datetime, timedelta
from typing import Any

from pydantic import validator
from pydantic.dataclasses import dataclass

from alerts_telegram_bot.eu_tickets_telegram_alerts import send_alert_to_telegram_channel
from scrapers import BaseParser, BaseScraper


@dataclass
class FlixbusTripsScraper(BaseScraper):
    """
    Look for trips from and to given cities
    and during a range of dates.
    """

    departure_city_uuid: str
    arrival_city_uuids: list[str]
    start_date: datetime = None
    end_date: datetime = None

    @validator("start_date")
    def validate_start_date(cls, start_date):
        if start_date > datetime.now():
            raise ValueError("Start date can't be previous than today")
        return start_date

    @validator("end_date")
    def validate_end_date(cls, end_date):
        if end_date > datetime.now():
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
        arrival_cities = self.arrival_city_uuids

        for arrival_city, departure_date in itertools.product(arrival_cities, departure_dates):
            query_str = (
                f"search?from_city_id={departure_city}&to_city_id={arrival_city}"
                f"&departure_date={departure_date}&adult=1&search_by=cities&currency=USD"
            )
            url = f"{search_trip_uri}/{query_str}&{default_params}"
            yield url

    def __post_init__(self):
        if not self.start_date:
            self.start_date = datetime.now()
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=90)
        self.endpoint_uris = list(uri for uri in self.endpoint_uris_generator())


@dataclass
class FlixbusTripsParser(BaseParser):
    region: str = "EU"

    def alert_cheap_tickets(self, trip: dict[str, Any]):
        from_city_name, to_city_name = trip["from_city_name"], trip["to_city_name"]
        price, seats_available = trip["price_total"], trip["seats_available"]
        departure_date = trip["departure_date"]

        send_alert_to_telegram_channel(
            from_city_name=from_city_name,
            departure_city_uuid=trip["departure_city_id"],
            to_city_name=to_city_name,
            arrival_city_uuid=trip["arrival_city_id"],
            price=price,
            departure_date=departure_date,
            seats_available=seats_available,
        )

    def parse_data(self) -> list[Any]:
        """
        Gets the result of get_data() method, parses it to be proceeded and stored
        """
        # TODO refactor this!
        for response in self.scraped_data:
            for trip in response["trips"]:
                for result_key, result_value in trip["results"].items():
                    if result_value["available"]["seats"]:
                        departure_city_uuid = trip["departure_city_id"]
                        arrival_city_uuid = trip["arrival_city_id"]
                        parsed_trip = {
                            "from_city_name": response["cities"][departure_city_uuid],
                            "to_city_name": response["cities"][arrival_city_uuid],
                            "departure_city_uuid": departure_city_uuid,
                            "arrival_city_uuid": arrival_city_uuid,
                            "date": trip["date"],
                            "uid": result_key,
                            "status": result_value["status"],
                            "provider": result_value["provider"],
                            "duration_hours": result_value["duration"]["hours"],
                            "duration_minutes": result_value["duration"]["minutes"],
                            "price_total": result_value["price"]["total"],
                            "seats_available": result_value["available"]["seats"],
                        }  # this should be part of processing, but...
                        if result_value["price"]["total"] < 10:  # TODO improve this
                            self.alert_cheap_tickets(parsed_trip)
