"""
Telegram ticket alerts
"""
import logging
import os
from datetime import datetime
from typing import Any

import humanize
import requests
from dotenv import load_dotenv
from pydantic.dataclasses import dataclass

from settings import APP_NAME

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)


@dataclass
class TripsAlertBot:
    trip: dict[str, Any]
    bot_url: str = None

    def __post_init__(self):
        trip = self.trip
        trip_properties = [
            "from_city_name",
            "departure_city_uuid",
            "to_city_name",
            "arrival_city_uuid",
            "price",
            "departure_date",
            "seats_available",
        ]
        if not any(trip.get(k) for k in trip_properties):
            raise ValueError(f"{', '.join(trip_properties)} trip properties are mandatory.")

        if not self.bot_url:
            self.bot_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

    @property
    def human_departure_date(self):
        departure_date = datetime.strptime(self.trip["departure_date"], "%Y-%m-%dT%H:%M:%S%z")
        return humanize.naturaltime(departure_date)

    @property
    def departure_date(self):
        departure_date = datetime.strptime(self.trip["departure_date"], "%Y-%m-%dT%H:%M:%S%z")
        return f"{departure_date.strftime('%Y-%m-%d %H:%M')}"

    @property
    def ticket_url(self):
        departure_city_uuid, arrival_city_uuid = (
            self.trip["departure_city_uuid"],
            self.trip["arrival_city_uuid"],
        )
        departure_date = self.departure_date.split(" ")[0]
        url = (
            f"https://shop.flixbus.com/search?departureCity={departure_city_uuid}&"
            f"arrivalCity={arrival_city_uuid}&rideDate={departure_date}"
        )
        return url.replace("&", "%26")

    @property
    def alert_message(self):
        from_city_name, to_city_name = self.trip["from_city_name"], self.trip["to_city_name"]
        seats_available, price = self.trip["seats_available"], self.trip["price_total"]
        human_departure_date, ticket_url = self.human_departure_date, self.ticket_url
        departure_date = self.departure_date

        return (
            f"🎟 A cheap ticket for you!\n"
            f"🚌 from {from_city_name} to {to_city_name}\n"
            f"💰 for just **{price} EUROS**!\n"
            f"📆 Schedule your next trip for {departure_date} "
            f"({human_departure_date}) GMT+2 time zone \n"
            f"🏃 Hurry up! just **{seats_available} remaining seats**\n"
            f"➡️ {ticket_url}"
        )

    async def send_alert_message(self):
        if "ago" not in self.alert_message:
            # TODO fix this
            # for some reason tickets from the past are being catched
            message = self.alert_message
            bot_url = self.bot_url

            send_msg_url = f"sendMessage?chat_id=@farecito_eu&text={message}&parse_mode=markdown"
            response = requests.post(f"{bot_url}/{send_msg_url}")

            if response.status_code != 200:
                logging.error("%s", response)
            else:
                logging.info("Cheap ticket sent!")