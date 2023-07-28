"""
Telegram ticket alerts
"""
import logging
import os
import uuid
from datetime import datetime
from typing import Any

import humanize
import requests
from dotenv import load_dotenv
from pydantic.dataclasses import dataclass

from settings import APP_NAME

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # TODO [improvement] read according to dev or prd

logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.INFO)


@dataclass
class TripsAlertBot:
    """
    Implements a Trips Alert Bot for sending notifications about cheap bus trips.
    It takes a trip and sends it details as alerts via Telegram API.

    Note: Requires the constant `TELEGRAM_BOT_TOKEN`, not defined here.
    """

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

        self.chat_id = TELEGRAM_CHAT_ID

    @property
    def human_departure_date(self):
        """
        Get the humanized departure date of the trip.
        :return: (str) e.g. "4 hours from now"
        """
        departure_date = datetime.strptime(self.trip["departure_date"], "%Y-%m-%dT%H:%M:%S%z")
        return humanize.naturaltime(departure_date)

    @property
    def departure_date(self):
        """
        Get just the date info in '%Y-%m-%d %H:%M' str format
        :return: (str), e.g. "2023-07-27 00:00"
        """
        departure_date = datetime.strptime(self.trip["departure_date"], "%Y-%m-%dT%H:%M:%S%z")
        return f"{departure_date.strftime('%Y-%m-%d %H:%M')}"

    @property
    def ticket_url(self):
        """
        Build the link of shop search flixbus trips
        where the cheap one exists.
        :return:
        """
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
        """
        Builds a friendly message alertinf about a cheap trip
        :return: (str)
        """
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

    async def send_alert_message(self) -> None:
        """
        Send the alert message to the correspondant channel,
        accordinf to https://core.telegram.org/method/messages.sendMessage
        :return: (None)
        """
        trace_uuid = str(uuid.uuid4())

        if "ago" not in self.alert_message:
            # TODO [bug] fix this
            # for some reason tickets from the past are being caught
            message = self.alert_message
            bot_url = self.bot_url
            chat_id = self.chat_id

            logger.info(f"[{trace_uuid}] Trying to send a cheap ticket alert.")

            send_msg_url = f"sendMessage?chat_id=@{chat_id}&text={message}&parse_mode=markdown"
            response = requests.post(f"{bot_url}/{send_msg_url}")

            if response.status_code != 200:
                logger.error(
                    f"[{trace_uuid}] cheap ticket alert not sent! HTTP request to {bot_url} - "
                    f"Error: {response.reason}, Status Code: {response.status_code}"
                )
            else:
                logger.info(
                    f"[{trace_uuid}] cheap ticket alert sent! - Message: {self.alert_message}"
                )
