"""
Telegram ticket alerts
"""
import json
import logging
import os
import time
import uuid
from datetime import datetime
from typing import Any
from urllib.parse import quote_plus

import pytz
import requests
from dotenv import load_dotenv
from pydantic.dataclasses import dataclass

from pipelines.settings import SENT_TRIPS_FILE
from pipelines.utils import city_to_country_code_and_flag
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
        self.trace_uuid = str(uuid.uuid4())

        self.sent_trips_file_path = SENT_TRIPS_FILE

        trip = self.trip
        trip_properties = [
            "uuid",
            "from_city_name",
            "departure_city_uuid",
            "to_city_name",
            "arrival_city_uuid",
            "original_price",
            "actual_price",
            "departure_date",
            "seats_available",
        ]
        try:
            _ = [trip[k] for k in trip_properties]
        except KeyError as exc:
            raise ValueError(f"{', '.join(trip_properties)} trip properties are mandatory") from exc

        if not self.bot_url:
            self.bot_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

        self.chat_id = TELEGRAM_CHAT_ID
        self.sent_alerts_path = "sent_trips.json"

    def read_sent_trips_from_json(self):
        file_path = self.sent_trips_file_path

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {}
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file)

        return data

    def write_sent_trip_data_to_json(self):
        file_path = self.sent_trips_file_path
        trip_to_save = {self.trip["uuid"]: self.trip}

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {}

        data.update(trip_to_save)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def trip_already_sent(self, trip_uuid: str) -> bool:
        data = self.read_sent_trips_from_json()
        return trip_uuid in data

    @property
    def departure_date_time(self):
        return datetime.strptime(self.trip["departure_date"], "%Y-%m-%dT%H:%M:%S%z")

    @property
    def departure_date(self):
        """
        Get only the departure date as .
        :return: (str) e.g. "4 hours from now"
        """
        return self.departure_date_time.strftime("%Y-%m-%d")

    @property
    def human_departure_date_time(self) -> str:
        """
        Format the datetime info in a friendly one, '%A, %B %d, %Y, %I:%M %p' str format
        :return: (str), e.g. "2023-07-31T19:00" will be "Sunday, July 31, 2023, 07:00 PM"
        """
        return f"{self.departure_date_time.strftime('%A, #%B %d, %Y, %I:%M %p')}"

    @property
    def custom_date_trip_message(self) -> str:
        """
        Gen a custom emoji + word according to the distance
        from now to the cheap trip datetime as follows:
        0-3: "coming"
        4-7: "just ahead"
        7 - end of the same month: "soon"
        next months: month's name
        :return:
        """
        departure_date_time = self.departure_date_time
        delta = departure_date_time - datetime.now(pytz.timezone("Europe/Madrid"))
        current_month = departure_date_time.month

        match delta.days:
            case 0 | 1 | 2 | 3:
                return "🔥 Coming!"
            case 4 | 5 | 6 | 7:
                return "🔔 Just ahead!"
            case _ if current_month == datetime.today().month:
                return "🔜 Soon"
            case _:
                return f"🎒 In {departure_date_time.strftime('#%B')}"

    @property
    def route_country_code_and_flag(self) -> str:
        """
        Gen a custom emoji of the country's flag according to the src/dst
        """
        from_city_name, to_city_name = self.trip["from_city_name"], self.trip["to_city_name"]
        src_cc_flag, dst_cc_flag = city_to_country_code_and_flag(
            from_city_name
        ), city_to_country_code_and_flag(to_city_name)

        if src_cc_flag == dst_cc_flag:
            cc_flag = src_cc_flag
            return f"from #{from_city_name} to #{to_city_name} #{cc_flag}\n"

        return f"from #{from_city_name} #{src_cc_flag} to #{to_city_name} #{dst_cc_flag}\n"

    def custom_discount_trip_message(self, discount):
        """
        Gen a custom emoji + word according to the % of discount
        from now to the cheap trip as follows:
        50: #up50%
        50-70: #+50%
        +70: #+70%
        next months: month's name
        :return:
        """

        match discount:
            case _ if discount <= 50:
                return "#UPto50% OFF🎫"
            case _ if discount <= 70:
                return "#UPto70% OFF🔻"
            case _:
                return "#over70% OFF🔥"

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
        departure_date = self.departure_date
        return (
            f"https://shop.flixbus.com/search?departureCity={departure_city_uuid}&"
            f"arrivalCity={arrival_city_uuid}&rideDate={departure_date}"
        )

    @property
    def alert_message(self):
        """
        Builds a friendly message alert about a cheap trip
        :return: (str)
        """
        seats_available = self.trip["seats_available"]

        original_price, actual_price = self.trip["original_price"], self.trip["actual_price"]
        discount = ((original_price - actual_price) / original_price) * 100

        human_departure_date_time, ticket_url = self.human_departure_date_time, self.ticket_url
        custom_date_message = self.custom_date_trip_message
        route_country_code_and_flag = self.route_country_code_and_flag
        custom_discount_message = self.custom_discount_trip_message(discount)

        return (
            f"{custom_date_message} a cheap ticket for you!\n"
            f"🚌 {route_country_code_and_flag}\n"
            f"💰 for just **{actual_price} EUROS**! ({custom_discount_message})\n"
            f"📆 Schedule your next trip for {human_departure_date_time} GMT+2 time zone \n"
            f"🏃 Hurry up! just **{seats_available} remaining seats**\n"
            f"👉 {ticket_url}"
        )

    async def send_alert_message(self) -> None:
        """
        Send the alert message to the correspondant channel,
        accordinf to https://core.telegram.org/method/messages.sendMessage
        :return: (None)
        """

        trip_uuid = self.trip["uuid"]
        from_city, to_city = self.trip["from_city_name"], self.trip["to_city_name"]
        date, price = self.trip["departure_date"], self.trip["actual_price"]

        if self.trip_already_sent(trip_uuid):
            logger.info(
                f"[{self.trace_uuid}] Trip with uuid {trip_uuid}: "
                f"{from_city}->{to_city} at {date} for {price} already sent."
            )
            return

        if self.departure_date_time <= datetime.now(pytz.timezone("Europe/Madrid")):
            logger.error(
                f"[{self.trace_uuid}] Trip with uuid {trip_uuid}: "
                f"{from_city}->{to_city} at {date} for {price} is in the past."
            )
            return
            # TODO [bug] fix this
            # for some reason tickets from the past are being caught

        message = quote_plus(self.alert_message)
        bot_url = self.bot_url
        chat_id = self.chat_id

        logger.info(f"[{self.trace_uuid}] Trying to send a cheap ticket alert.")

        send_msg_url = f"sendMessage?chat_id=@{chat_id}&text={message}&parse_mode=markdown"
        response = requests.post(f"{bot_url}/{send_msg_url}")

        if response.status_code != 200:
            logger.error(
                f"[{self.trace_uuid}] Error: {response.reason}, Status Code: {response.status_code}"
            )
            logger.error(
                f"[{self.trace_uuid}] Trip with uuid {trip_uuid}: "
                f"{from_city}->{to_city} at {date} for {price} "
                f"can not be alerted: {response.reason}."
            )
        else:
            try:
                self.write_sent_trip_data_to_json()
                logger.info(
                    f"[{self.trace_uuid}] Trip with uuid {trip_uuid}: "
                    f"{from_city}->{to_city} at {date} for {price} saved."
                )
            except Exception as exc:
                logger.error(
                    f"[{self.trace_uuid}] Trip with uuid {trip_uuid}: "
                    f"{from_city}->{to_city} at {date} for {price} can not be saved: {exc}."
                )
            # TODO [improvement] path for not sending a lot of alerts at once
            time.sleep(15)
